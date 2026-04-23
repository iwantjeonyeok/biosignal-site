#!/usr/bin/env python3
"""
Split ECG/EEG/EMG overview index.md files into a 3-level page hierarchy.

  # N. Title          -> skey/N-title/index.md  (if has children)
                      -> skey/N-title.md         (if leaf)
  ## N.M Title        -> skey/N-title/NM-title/index.md  (if has children)
                      -> skey/N-title/NM-title.md         (if leaf)
  ### N.M.K Title     -> skey/N-title/NM-title/NMK-title.md  (always leaf)

Section-5 (datasets) gets the individual dataset pages as nav children.
"""

import re
from pathlib import Path

DOCS_ROOT = Path(r"C:\Users\jangg\biosignal-site\docs")
SITE_ROOT = Path(r"C:\Users\jangg\biosignal-site")

# ── Utilities ─────────────────────────────────────────────────────────────────

def slugify(text: str, maxlen: int = 35) -> str:
    s = re.sub(r"\*+", "", text).lower().strip()
    s = re.sub(r"[^\w\s\-]", "", s, flags=re.UNICODE)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:maxlen].rstrip("-")


def parse_heading(line: str):
    """Return (hashes, parts, title) or None."""
    m = re.match(r"^(#+)\s+(.+)$", line)
    if not m:
        return None
    hashes = len(m.group(1))
    raw = re.sub(r"\*+", "", m.group(2)).strip()
    nm = re.match(r"^(\d+(?:\.\d+)*)\.*\s+(.+)$", raw)
    if nm:
        parts = [int(x) for x in nm.group(1).split(".")]
        title = nm.group(2).strip()
    else:
        parts = []
        title = raw
    return hashes, parts, title


def is_page_section(hashes: int, parts: list) -> bool:
    if not parts:
        return False
    return (
        (hashes == 1 and len(parts) == 1)
        or (hashes == 2 and len(parts) == 2)
        or (hashes == 3 and len(parts) == 3)
    )


def sec_slug(parts: list, title: str) -> str:
    num = "-".join(str(p) for p in parts)
    t = slugify(title)
    return f"{num}-{t}" if t else num


def adjust_paths(lines: list, up: int) -> list:
    """Prepend ../ * up to relative image/link hrefs."""
    if up == 0:
        return lines
    prefix = "../" * up

    def fix(m):
        bracket, path = m.group(1), m.group(2)
        if re.match(r"https?://", path) or path.startswith(("#", "/")):
            return m.group(0)
        return f"{bracket}({prefix}{path})"

    return [re.sub(r"(!?\[[^\]]*\])\(([^)]+)\)", fix, ln) for ln in lines]


# ── Section parsing ───────────────────────────────────────────────────────────

def collect_sections(lines: list) -> list:
    """
    Return a list of dicts for every page-level heading in lines.
    Each dict: pos, hashes, parts, title, own_start, own_end, full_end, has_children
    """
    raw = []
    for i, line in enumerate(lines):
        h = parse_heading(line)
        if h and is_page_section(h[0], h[1]):
            raw.append({"pos": i, "hashes": h[0], "parts": h[1], "title": h[2]})

    parts_set = {tuple(s["parts"]) for s in raw}

    def has_ch(parts):
        d = len(parts)
        t = tuple(parts)
        return any(len(op) == d + 1 and op[:d] == t for op in parts_set)

    for j, sec in enumerate(raw):
        # full_end: before next same-or-shallower section
        full_end = len(lines)
        for k in range(j + 1, len(raw)):
            if len(raw[k]["parts"]) <= len(sec["parts"]):
                full_end = raw[k]["pos"]
                break
        sec["full_end"] = full_end

        # own_end: before first direct child
        own_end = full_end
        for k in range(j + 1, len(raw)):
            if raw[k]["pos"] >= full_end:
                break
            np = raw[k]["parts"]
            if len(np) == len(sec["parts"]) + 1 and np[: len(sec["parts"])] == sec["parts"]:
                own_end = raw[k]["pos"]
                break
        sec["own_start"] = sec["pos"] + 1
        sec["own_end"] = own_end
        sec["has_children"] = has_ch(sec["parts"])

    return raw


# ── File path & depth ─────────────────────────────────────────────────────────

def build_maps(sections: list, skey: str):
    """Build slug_map and file_path_map from parsed sections."""
    slug_map = {tuple(s["parts"]): sec_slug(s["parts"], s["title"]) for s in sections}

    def fp(s):
        parts = s["parts"]
        d = len(parts)
        base = DOCS_ROOT / skey
        if d == 1:
            sl = slug_map[tuple(parts)]
            return base / sl / "index.md" if s["has_children"] else base / f"{sl}.md"
        elif d == 2:
            p1 = slug_map[tuple(parts[:1])]
            sl = slug_map[tuple(parts)]
            parent_hc = next(
                (x["has_children"] for x in sections if x["parts"] == parts[:1]), False
            )
            if s["has_children"]:
                return base / p1 / sl / "index.md"
            else:
                return base / p1 / f"{sl}.md"
        elif d == 3:
            p1 = slug_map[tuple(parts[:1])]
            p2 = slug_map[tuple(parts[:2])]
            sl = slug_map[tuple(parts)]
            return base / p1 / p2 / f"{sl}.md"

    file_map = {tuple(s["parts"]): fp(s) for s in sections}
    return slug_map, file_map


def up_levels(sec: dict) -> int:
    d = len(sec["parts"])
    if d == 1:
        return 1 if sec["has_children"] else 0
    elif d == 2:
        return 2 if sec["has_children"] else 1
    elif d == 3:
        return 2
    return 0


def is_dataset_section(s: dict) -> bool:
    return len(s["parts"]) == 1 and s["parts"][0] == 5 and "데이터셋" in s.get("title", "")


# ── Dataset page discovery ────────────────────────────────────────────────────

def get_dataset_pages(skey: str) -> list:
    """
    Return list of {title, rel_path} for individual dataset pages.
    Scans docs/skey/*.md directly, skipping index.md and section files
    (files whose names start with a digit, which we create in this script).
    Title is read from the first H1 heading in each file.
    """
    sec_dir = DOCS_ROOT / skey
    datasets = []
    for p in sorted(sec_dir.glob("*.md")):
        if p.name == "index.md":
            continue
        if re.match(r"^\d{1,2}-", p.name):
            continue
        # Read first H1 for the title
        title = p.stem.replace("-", " ").title()
        try:
            for line in p.read_text(encoding="utf-8").splitlines():
                m = re.match(r"^#\s+(.+)$", line)
                if m:
                    title = m.group(1).strip()
                    break
        except Exception:
            pass
        datasets.append({"title": title, "rel": f"{skey}/{p.name}"})
    return datasets


# ── Write section files ───────────────────────────────────────────────────────

def write_section_files(skey: str, lines: list, sections: list, file_map: dict):
    by_parts = {tuple(s["parts"]): s for s in sections}

    for s in sections:
        key = tuple(s["parts"])
        fp = file_map[key]
        up = up_levels(s)

        own = lines[s["own_start"] : s["own_end"]]
        own = adjust_paths(own, up)

        num_str = ".".join(str(p) for p in s["parts"])
        content = f"# {num_str}. {s['title']}\n\n" + "\n".join(own)

        # Fix 2: add clickable child links to parent pages
        if s["has_children"]:
            child_keys = sorted(
                [p for p in by_parts if len(p) == len(key) + 1 and p[: len(key)] == key]
            )
            child_links = []
            for ck in child_keys:
                cs = by_parts[ck]
                child_fp = file_map[ck]
                rel = child_fp.relative_to(fp.parent)
                if rel.name == "index.md":
                    link = str(rel.parent).replace("\\", "/") + "/"
                else:
                    link = str(rel).replace("\\", "/")
                child_num = ".".join(str(p) for p in cs["parts"])
                child_links.append(f"[{child_num}. {cs['title']}]({link})")
            if child_links:
                content = content.rstrip() + "\n\n" + "\n\n".join(child_links) + "\n"

        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content, encoding="utf-8")
        print(f"    {fp.relative_to(DOCS_ROOT)}")


# ── Nav building ──────────────────────────────────────────────────────────────

def build_nav(sections: list, skey: str, file_map: dict, dataset_pages: list) -> list:
    by_parts = {tuple(s["parts"]): s for s in sections}

    def rp(fp: Path) -> str:
        return str(fp.relative_to(DOCS_ROOT)).replace("\\", "/")

    def nav_title(s):
        num = ".".join(str(p) for p in s["parts"])
        return f"{num}. {s['title']}"

    def build_entry(parts_tup):
        s = by_parts[parts_tup]
        title = nav_title(s)
        fp = file_map[parts_tup]
        children_keys = sorted(
            [p for p in by_parts if len(p) == len(parts_tup) + 1 and p[: len(parts_tup)] == parts_tup]
        )

        is_ds = is_dataset_section(s)

        if not s["has_children"] and not is_ds:
            return {title: rp(fp)}

        if is_ds:
            # Fix 4/5: path-only entry (navigation.indexes) = no "개요" label
            sub = [rp(fp)]
            sub.extend({d["title"]: d["rel"]} for d in dataset_pages)
        else:
            sub = [{"개요": rp(fp)}]
            for cp in children_keys:
                sub.append(build_entry(cp))

        return {title: sub}

    level1 = sorted(p for p in by_parts if len(p) == 1)

    # Fix 3: swap sections 6 and 7 for ECG and EEG (기반모델 before 결론)
    if skey in ("ecg", "eeg"):
        l = list(level1)
        idx6 = next((i for i, p in enumerate(l) if p == (6,)), -1)
        idx7 = next((i for i, p in enumerate(l) if p == (7,)), -1)
        if idx6 >= 0 and idx7 >= 0:
            l[idx6], l[idx7] = l[idx7], l[idx6]
        level1 = l

    return [build_entry(t) for t in level1]


# ── Update index.md ───────────────────────────────────────────────────────────

def update_index(skey: str, lines: list, sections: list, file_map: dict):
    """Replace index.md with title + section link list."""
    title_line = lines[0] if lines else f"# {skey.upper()} Dataset"

    links = []
    for s in sections:
        if len(s["parts"]) != 1:
            continue
        fp = file_map[tuple(s["parts"])]
        rel = fp.relative_to(DOCS_ROOT / skey)
        num = ".".join(str(p) for p in s["parts"])
        if rel.name == "index.md":
            link = str(rel.parent).replace("\\", "/") + "/"
        else:
            link = str(rel).replace("\\", "/")
        links.append(f"[{num}. {s['title']}]({link})")

    new_text = title_line.rstrip() + "\n\n" + "\n\n".join(links) + "\n"
    (DOCS_ROOT / skey / "index.md").write_text(new_text, encoding="utf-8")


# ── mkdocs.yml rewrite ────────────────────────────────────────────────────────

def yaml_key(k: str) -> str:
    """Quote a YAML key if it contains characters that need quoting."""
    if ":" in k or "#" in k or "[" in k or "]" in k or "{" in k or "}" in k:
        escaped = k.replace('"', '\\"')
        return f'"{escaped}"'
    return k


def nav_to_yaml(items, indent=1):
    prefix = "  " * indent
    lines = []
    for item in items:
        if isinstance(item, str):
            # path-only entry for navigation.indexes section index
            lines.append(f"{prefix}- {item}")
        else:
            for k, v in item.items():
                yk = yaml_key(k)
                if isinstance(v, list):
                    lines.append(f"{prefix}- {yk}:")
                    lines.append(nav_to_yaml(v, indent + 1))
                else:
                    lines.append(f"{prefix}- {yk}: {v}")
    return "\n".join(lines)


def rewrite_mkdocs_yml(ecg_nav, eeg_nav, emg_nav):
    yml_path = SITE_ROOT / "mkdocs.yml"
    text = yml_path.read_text(encoding="utf-8")

    # Extract everything before 'nav:'
    nav_start = text.index("\nnav:")
    header = text[: nav_start + 1]

    nav_body = nav_to_yaml([
        {"Home": "index.md"},
        {"ECG": [{"ECG Overview": "ecg/index.md"}] + ecg_nav},
        {"EEG": [{"EEG Overview": "eeg/index.md"}, {"EEG Dataset (상세)": "eeg/eeg-dataset-2.md"}] + eeg_nav},
        {"EMG": [{"EMG Overview": "emg/index.md"}] + emg_nav},
    ])

    yml_path.write_text(header + "nav:\n" + nav_body + "\n", encoding="utf-8")
    print(f"  Updated {yml_path}")


# ── Main ──────────────────────────────────────────────────────────────────────

def process(skey: str):
    print(f"\n[{skey.upper()}]")
    idx = DOCS_ROOT / skey / "index.md"
    lines = idx.read_text(encoding="utf-8").split("\n")

    sections = collect_sections(lines)
    print(f"  {len(sections)} page-level sections found")

    slug_map, file_map = build_maps(sections, skey)
    dataset_pages = get_dataset_pages(skey)
    print(f"  {len(dataset_pages)} dataset pages")

    write_section_files(skey, lines, sections, file_map)
    update_index(skey, lines, sections, file_map)

    return build_nav(sections, skey, file_map, dataset_pages)


def main():
    ecg_nav = process("ecg")
    eeg_nav = process("eeg")
    emg_nav = process("emg")
    rewrite_mkdocs_yml(ecg_nav, eeg_nav, emg_nav)
    print("\nDone. Run: py -m mkdocs build")


if __name__ == "__main__":
    main()
