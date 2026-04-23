#!/usr/bin/env python3
"""
Convert Notion export to MkDocs Material docs/ directory.

Key features:
- Bracket-depth tracking parser (handles parentheses in paths and links in alt text)
- <aside> → admonition (directory trees get code-fenced, plain text does not)
- Image captions deduplication
- Citation [N] → footnote [^N] conversion
"""

import re
import shutil
import sys
from pathlib import Path
from urllib.parse import unquote

# ─── Paths ────────────────────────────────────────────────────────────────────

EXPORT_ROOT = Path(
    r"C:\Users\jangg\OneDrive\Desktop\biosignal dataset export 파일"
    r"\ExportBlock-0b59b7b2-1ace-4cbc-9088-ac94d3ee3184-Part-1"
)
SRC_BASE = EXPORT_ROOT / "Biosignal Dataset"
SITE_ROOT = Path(r"C:\Users\jangg\biosignal-site")
DOCS_ROOT = SITE_ROOT / "docs"

# ─── Helpers ─────────────────────────────────────────────────────────────────

UUID_RE = re.compile(r"\s[0-9a-f]{32}$", re.IGNORECASE)


def strip_uuid(stem: str) -> str:
    return UUID_RE.sub("", stem).strip()


def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[^\w\s\-]", "", s, flags=re.UNICODE)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def sanitize_image_name(name: str) -> str:
    return name.replace(" ", "-")


# ─── Build source → dest file map ─────────────────────────────────────────────

def build_md_map() -> dict[Path, Path]:
    md_map: dict[Path, Path] = {}

    # Root index
    root_md = EXPORT_ROOT / "Biosignal Dataset 0227749b6b8f825399448104ee57be3e.md"
    md_map[root_md.resolve()] = DOCS_ROOT / "index.md"

    # Section index pages
    section_indices = {
        "ECG Dataset 3d27749b6b8f82f4991681cdc005fad1.md": DOCS_ROOT / "ecg" / "index.md",
        "EEG Dataset 7867749b6b8f82c89bce01631fbce920.md": DOCS_ROOT / "eeg" / "index.md",
        "EEG Dataset (1) 0ac7749b6b8f83599ba7015d58c4e249.md": DOCS_ROOT / "eeg" / "eeg-dataset-2.md",
        "EMG dataset 49e7749b6b8f828e863301c7fb2055ea.md": DOCS_ROOT / "emg" / "index.md",
    }
    for fname, dest in section_indices.items():
        src = (SRC_BASE / fname).resolve()
        md_map[src] = dest

    # Subpage directories
    subpage_dirs = {
        SRC_BASE / "ECG Dataset": "ecg",
        SRC_BASE / "EEG Dataset": "eeg",
        SRC_BASE / "EEG Dataset (1)": "eeg",  # duplicates → same slug OK
        SRC_BASE / "EMG dataset": "emg",
    }
    for src_dir, section in subpage_dirs.items():
        if not src_dir.exists():
            print(f"WARNING: directory not found: {src_dir}", file=sys.stderr)
            continue
        for src_file in src_dir.glob("*.md"):
            stem = strip_uuid(src_file.stem)
            slug = slugify(stem)
            dest = DOCS_ROOT / section / f"{slug}.md"
            md_map[src_file.resolve()] = dest

    return md_map


# ─── Image destination directory ──────────────────────────────────────────────

def image_dest_dir(dest_md: Path) -> Path:
    rel = dest_md.relative_to(DOCS_ROOT)
    parts = rel.parts

    if len(parts) == 1:                   # docs/index.md
        return DOCS_ROOT / "images"
    section, fname = parts[0], parts[1]
    stem = Path(fname).stem
    if fname == "index.md":               # docs/{sec}/index.md
        return DOCS_ROOT / section / "images"
    if fname == "eeg-dataset-2.md":       # EEG Dataset (1) page shares images
        return DOCS_ROOT / section / "images"
    return DOCS_ROOT / section / stem     # docs/{sec}/{slug}.md → docs/{sec}/{slug}/


# ─── Bracket-depth image/link parser ─────────────────────────────────────────

def _parse_bracket_content(text: str, start: int) -> tuple[int, str] | None:
    """
    Starting at text[start] which should be '[', find the matching ']'.
    Returns (end_pos, content) where end_pos is position AFTER ']', or None.
    """
    assert text[start] == "["
    depth = 0
    i = start + 1
    while i < len(text):
        c = text[i]
        if c == "\n":
            return None  # images/links don't span lines
        if c == "[":
            depth += 1
        elif c == "]":
            if depth == 0:
                return i + 1, text[start + 1 : i]
            depth -= 1
        i += 1
    return None


def _parse_paren_content(text: str, start: int) -> tuple[int, str] | None:
    """
    Starting at text[start] which should be '(', find the matching ')'.
    Returns (end_pos, content) or None.
    """
    assert text[start] == "("
    depth = 0
    i = start + 1
    while i < len(text):
        c = text[i]
        if c == "\n":
            return None
        if c == "(":
            depth += 1
        elif c == ")":
            if depth == 0:
                return i + 1, text[start + 1 : i]
            depth -= 1
        i += 1
    return None


def iter_images_and_links(text: str):
    """
    Yield (start, end, kind, inner, href) for every ![alt](src) and [text](href).
    kind = 'image' | 'link'
    Uses bracket-depth tracking so paths/alts with () or [] are handled correctly.
    """
    i = 0
    n = len(text)
    while i < n:
        # Image: ![
        if text[i] == "!" and i + 1 < n and text[i + 1] == "[":
            bracket_start = i + 1
            r = _parse_bracket_content(text, bracket_start)
            if r:
                after_bracket, alt = r
                if after_bracket < n and text[after_bracket] == "(":
                    r2 = _parse_paren_content(text, after_bracket)
                    if r2:
                        after_paren, src = r2
                        yield i, after_paren, "image", alt, src
                        i = after_paren
                        continue
        # Link: [ not preceded by !
        elif text[i] == "[" and (i == 0 or text[i - 1] != "!"):
            r = _parse_bracket_content(text, i)
            if r:
                after_bracket, link_text = r
                if after_bracket < n and text[after_bracket] == "(":
                    r2 = _parse_paren_content(text, after_bracket)
                    if r2:
                        after_paren, href = r2
                        yield i, after_paren, "link", link_text, href
                        i = after_paren
                        continue
        i += 1


# ─── Image resolution ─────────────────────────────────────────────────────────

def resolve_and_copy_image(src_file: Path, dest_md: Path, img_src: str) -> str:
    """Decode img_src, copy the file, return relative path from dest_md."""
    decoded = unquote(img_src)
    abs_img = (src_file.parent / decoded).resolve()

    if not abs_img.exists():
        print(f"  WARNING: image not found: {abs_img}", file=sys.stderr)
        return img_src  # keep original if missing

    dest_dir = image_dest_dir(dest_md)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_name = sanitize_image_name(abs_img.name)
    dest_img = dest_dir / dest_name

    try:
        shutil.copy2(abs_img, dest_img)
    except Exception as e:
        print(f"  WARNING: copy failed {abs_img} → {dest_img}: {e}", file=sys.stderr)
        return img_src

    rel = dest_img.relative_to(dest_md.parent)
    return str(rel).replace("\\", "/")


# ─── Link resolution ──────────────────────────────────────────────────────────

def resolve_internal_link(
    src_file: Path, dest_md: Path, href: str, md_map: dict[Path, Path]
) -> str:
    decoded = unquote(href)
    if not decoded.endswith(".md"):
        return href

    abs_src = (src_file.parent / decoded).resolve()
    target_dest = md_map.get(abs_src)
    if target_dest is None:
        print(f"  WARNING: no mapping for: {abs_src}", file=sys.stderr)
        return href

    try:
        rel = target_dest.relative_to(dest_md.parent)
        rel_str = str(rel).replace("\\", "/")
    except ValueError:
        from os.path import relpath
        rel_str = relpath(str(target_dest), str(dest_md.parent)).replace("\\", "/")

    if rel_str == "index.md" or rel_str.endswith("/index.md"):
        rel_str = rel_str[: -len("index.md")] or "./"
    else:
        rel_str = rel_str[:-3] + "/"

    return rel_str


# ─── Combined image + link processor ──────────────────────────────────────────

def process_links_and_images(
    text: str, src_file: Path, dest_md: Path, md_map: dict[Path, Path]
) -> str:
    parts: list[str] = []
    last = 0

    for start, end, kind, inner, href in iter_images_and_links(text):
        parts.append(text[last:start])

        if kind == "image":
            if href.startswith("http://") or href.startswith("https://"):
                parts.append(text[start:end])  # external image, keep as-is
            else:
                new_src = resolve_and_copy_image(src_file, dest_md, href)
                parts.append(f"![{inner}]({new_src})")

        else:  # link
            if (
                href.startswith("http://")
                or href.startswith("https://")
                or href.startswith("#")
            ):
                parts.append(text[start:end])
            elif href.endswith(".md") or unquote(href).endswith(".md"):
                new_href = resolve_internal_link(src_file, dest_md, href, md_map)
                parts.append(f"[{inner}]({new_href})")
            else:
                parts.append(text[start:end])

        last = end

    parts.append(text[last:])
    return "".join(parts)


# ─── <aside> conversion ───────────────────────────────────────────────────────

_TREE_CHARS = frozenset("├└─│")


def convert_aside(text: str) -> str:
    """
    <aside>...</aside> → MkDocs !!! note admonition.

    Directory trees (lines with ├ └ ─ │) → wrapped in a code block.
    Regular text (callout notes, lists, etc.) → plain indented content
    so that Markdown inside (bold, links, lists) still renders.
    """

    def replace_aside(m: re.Match) -> str:
        inner = m.group(1)
        lines = inner.split("\n")
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()

        is_tree = any(set(line) & _TREE_CHARS for line in lines)

        result = ["", '!!! note ""']
        if is_tree:
            result.append("    ```")
            for line in lines:
                result.append(f"    {line}")
            result.append("    ```")
        else:
            for line in lines:
                result.append(f"    {line}")
        result.append("")
        return "\n".join(result)

    return re.sub(
        r"<aside>\s*\n(.*?)\n\s*</aside>",
        replace_aside,
        text,
        flags=re.DOTALL,
    )


# ─── Image caption deduplication ─────────────────────────────────────────────

def deduplicate_image_captions(text: str) -> str:
    """
    Remove duplicate caption paragraphs that follow image tags.

    Uses the bracket-depth parser so alt text with nested [link](url) is handled.
    Pattern A: next non-blank line == alt text (normalised) → remove dup
    Pattern B: alt is generic '*.png' or empty, next non-blank line starts with * → absorb
    """
    lines = text.split("\n")
    result: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Use depth-tracking parser: detect a line that is solely one image token
        found = list(iter_images_and_links(stripped))
        is_sole_image = (
            len(found) == 1
            and found[0][2] == "image"
            and found[0][0] == 0
            and found[0][1] == len(stripped)
        )

        if is_sole_image:
            _, _, _, alt, _ = found[0]
            result.append(line)

            # Collect blank lines ahead
            j = i + 1
            blank_buf: list[str] = []
            while j < len(lines) and not lines[j].strip():
                blank_buf.append(lines[j])
                j += 1

            if j < len(lines):
                next_line = lines[j]
                norm_alt  = re.sub(r"\*+", "", alt).strip()
                norm_next = re.sub(r"\*+", "", next_line).strip()

                # Pattern A: exact text duplicate
                if norm_alt and norm_alt == norm_next:
                    i = j + 1  # skip blank_buf and dup line
                    continue

                # Pattern B: generic alt, next line is a real caption (*bold*)
                if alt.strip().lower().endswith(".png") or alt.strip() == "":
                    next_stripped = next_line.strip()
                    if next_stripped.startswith("**") or next_stripped.startswith("*"):
                        # Rebuild image tag with real caption as alt text
                        # (safe: alt was a plain filename, no nested brackets)
                        new_img = stripped.replace(f"![{alt}]", f"![{next_stripped}]", 1)
                        indent = line[: len(line) - len(line.lstrip())]
                        result[-1] = indent + new_img
                        i = j + 1  # skip dup line
                        continue

                result.extend(blank_buf)
            else:
                result.extend(blank_buf)
            i = j
        else:
            result.append(line)
            i += 1

    return "\n".join(result)


# ─── Citation → footnote conversion ──────────────────────────────────────────

def convert_citations(text: str) -> str:
    lines = text.split("\n")

    # Detect reference section heading
    ref_heading_re = re.compile(
        r"^#{1,6}\s+(?:\d+\.\s+)?(?:References?|참고문헌)\s*$",
        re.IGNORECASE,
    )
    ref_start = next(
        (i for i, l in enumerate(lines) if ref_heading_re.match(l)), None
    )
    body_end = ref_start if ref_start is not None else len(lines)

    # ── Inline citation expansion ──────────────────────────────────────────────
    INLINE_RE = re.compile(r"(?<![!\[])\[(\d[\d,\s\-–]*)\](?![\(\[])")

    def expand(m: re.Match) -> str:
        inner = m.group(1)
        parts: list[str] = []
        # Range: 1-3
        rng = re.match(r"^(\d+)\s*[-–]\s*(\d+)$", inner.strip())
        if rng:
            for n in range(int(rng.group(1)), int(rng.group(2)) + 1):
                parts.append(f"[^{n}]")
            return "".join(parts)
        # Comma-separated
        for part in inner.split(","):
            part = part.strip()
            if re.match(r"^\d+$", part):
                parts.append(f"[^{part}]")
            else:
                return m.group(0)
        return "".join(parts)

    body_lines = [INLINE_RE.sub(expand, l) for l in lines[:body_end]]

    if ref_start is None:
        return "\n".join(body_lines)

    # ── Reference section conversion ───────────────────────────────────────────
    ref_lines = lines[ref_start:]
    converted: list[str] = []
    in_refs = False  # True once we've passed the heading

    for line in ref_lines:
        if ref_heading_re.match(line):
            converted.append(line)
            in_refs = True
            continue

        # Format 1: [N] Text
        m1 = re.match(r"^\[(\d+)\]\s+(.+)$", line)
        # Format 2: N. Text  (only inside ref section)
        m2 = re.match(r"^(\d+)\.\s+(.+)$", line) if in_refs else None

        if m1:
            converted.append(f"[^{m1.group(1)}]: {m1.group(2)}")
            in_refs = True
        elif m2:
            converted.append(f"[^{m2.group(1)}]: {m2.group(2)}")
        else:
            converted.append(line)

    return "\n".join(body_lines) + "\n" + "\n".join(converted)


# ─── Main file processor ──────────────────────────────────────────────────────

def process_file(src_file: Path, dest_md: Path, md_map: dict[Path, Path]) -> None:
    print(f"  {src_file.name} → {dest_md.relative_to(SITE_ROOT)}")
    dest_md.parent.mkdir(parents=True, exist_ok=True)

    text = src_file.read_text(encoding="utf-8")

    text = convert_aside(text)
    text = process_links_and_images(text, src_file, dest_md, md_map)
    text = deduplicate_image_captions(text)
    text = convert_citations(text)

    dest_md.write_text(text, encoding="utf-8")


# ─── Nav generation ───────────────────────────────────────────────────────────

def build_nav(md_map: dict[Path, Path]) -> list:
    # Build dest → original Notion title (UUID stripped); prefer EEG Dataset over EEG Dataset (1)
    dest_to_title: dict[Path, str] = {}
    for src, dest in md_map.items():
        original = strip_uuid(src.stem)
        # Only set if not already set (EEG Dataset pages come before EEG Dataset (1) in dict order)
        if dest not in dest_to_title:
            dest_to_title[dest] = original

    ecg: list[tuple[str, str]] = []
    eeg: list[tuple[str, str]] = []
    emg: list[tuple[str, str]] = []

    for dest in set(md_map.values()):
        rel = dest.relative_to(DOCS_ROOT)
        parts = rel.parts
        if len(parts) == 1:
            continue  # root

        section, fname = parts[0], parts[1]
        rel_str = str(rel).replace("\\", "/")

        if fname == "index.md":
            title = {"ecg": "ECG Overview", "eeg": "EEG Overview", "emg": "EMG Overview"}.get(section, "Overview")
        elif fname == "eeg-dataset-2.md":
            title = "EEG Dataset (상세)"
        else:
            # Use original Notion page name (preserves acronyms and special chars)
            title = dest_to_title.get(dest, Path(fname).stem.replace("-", " ").title())

        bucket = {"ecg": ecg, "eeg": eeg, "emg": emg}.get(section)
        if bucket is not None:
            bucket.append((title, rel_str))

    def sort_pages(pages: list[tuple[str, str]]) -> list[dict]:
        idx = [(t, p) for t, p in pages if Path(p).name == "index.md"]
        detail = [(t, p) for t, p in pages if Path(p).name == "eeg-dataset-2.md"]
        rest = sorted(
            [(t, p) for t, p in pages if Path(p).name not in ("index.md", "eeg-dataset-2.md")],
            key=lambda x: x[0].lower(),
        )
        return [{t: p} for t, p in idx + detail + rest]

    return [
        {"Home": "index.md"},
        {"ECG": sort_pages(ecg)},
        {"EEG": sort_pages(eeg)},
        {"EMG": sort_pages(emg)},
    ]


# ─── mkdocs.yml writer ────────────────────────────────────────────────────────

def nav_to_yaml(nav_list: list, indent: int = 1) -> str:
    prefix = "  " * indent
    lines: list[str] = []
    for item in nav_list:
        for title, value in item.items():
            if isinstance(value, list):
                lines.append(f"{prefix}- {title}:")
                lines.append(nav_to_yaml(value, indent + 1))
            else:
                lines.append(f"{prefix}- {title}: {value}")
    return "\n".join(lines)


def write_mkdocs_yml(nav: list) -> None:
    nav_yaml = nav_to_yaml(nav)
    content = f"""\
site_name: "Biosignal Dataset"
site_url: "https://USERNAME.github.io/biosignal-site/"
repo_url: "https://github.com/USERNAME/biosignal-site"
repo_name: "biosignal-site"

theme:
  name: material
  language: ko
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: 다크 모드
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: 라이트 모드
  font:
    text: Noto Sans KR
    code: Roboto Mono
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - navigation.indexes
    - search.highlight
    - search.suggest
    - content.code.copy

plugins:
  - search:
      lang: ko

markdown_extensions:
  - admonition
  - footnotes
  - tables
  - attr_list
  - md_in_html
  - toc:
      permalink: true
  - pymdownx.superfences
  - pymdownx.details
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite

extra_javascript:
  - https://polyfill.io/v3/polyfill.min.js?features=es6
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js

extra_css:
  - stylesheets/extra.css

nav:
{nav_yaml}
"""
    out = SITE_ROOT / "mkdocs.yml"
    out.write_text(content, encoding="utf-8")
    print(f"Wrote {out}")


# ─── Extra CSS for Korean typography ─────────────────────────────────────────

def write_extra_css() -> None:
    css_dir = DOCS_ROOT / "stylesheets"
    css_dir.mkdir(parents=True, exist_ok=True)
    (css_dir / "extra.css").write_text(
        """\
/* Korean typography */
body {
  word-break: keep-all;
  overflow-wrap: break-word;
}

/* Admonition content: allow markdown rendering */
.admonition p,
.admonition li {
  line-height: 1.7;
}

/* Image captions */
img + em,
img + p > em {
  display: block;
  text-align: center;
  font-size: 0.85em;
  color: var(--md-default-fg-color--lighter);
  margin-top: 0.25em;
}
""",
        encoding="utf-8",
    )


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    print("Building file map...")
    md_map = build_md_map()
    print(f"  {len(md_map)} source files mapped.")

    if DOCS_ROOT.exists():
        print(f"Cleaning {DOCS_ROOT} ...")
        shutil.rmtree(DOCS_ROOT)
    DOCS_ROOT.mkdir(parents=True)

    print("Processing files...")
    for src, dest in md_map.items():
        if not src.exists():
            print(f"  WARNING: source not found: {src}", file=sys.stderr)
            continue
        process_file(src, dest, md_map)

    write_extra_css()

    print("Building nav & mkdocs.yml ...")
    nav = build_nav(md_map)
    write_mkdocs_yml(nav)

    total_md  = sum(1 for f in DOCS_ROOT.rglob("*.md"))
    total_img = sum(1 for f in DOCS_ROOT.rglob("*.png"))
    print(f"\nDone - {total_md} MD files, {total_img} images.")


if __name__ == "__main__":
    main()
