# REVE — Representation for EEG with Versatile Embeddings

> **REVE: A Foundation Model for EEG Adapting to Any Setup with Large-Scale Pre-training on 25,000 Subjects**
> Yassine El Ouahidi, Jonathan Lys, Philipp Thölke, Nicolas Farrugia, Bastien Pasdeloup, Vincent Gripon, Karim Jerbi, Giulia Lioi. **NeurIPS 2025.**

- Project page: https://brain-bzh.github.io/reve/
- Official code: https://github.com/elouayas/reve_eeg
- Preprocessing folder: https://github.com/elouayas/reve_eeg/tree/main/preprocessing

## Pre-training Data Summary

REVE assembles — by a wide margin — the **largest and most diverse public EEG pre-training corpus to date**:

- **92 datasets • 24,274 subjects • 150,833 unique sessions • 61,415 hours**
- **19 TB** of raw data → **6 TB** after standard preprocessing
- Spans clinical, cognitive, BCI, and research domains, 396 unique electrode names, 3-10-5 system recordings in BrainVision / BioSemi / EDF / GDF / EEGLAB formats.

### Composition (Appendix Table 7)

| Axis | Group | #Subjects | Hours | #Datasets |
|------|-------|-----------|-------|-----------|
| Category | BCI | 791 | 457 | 28 |
| Category | Cognition | 4,193 | 10,376 | 56 |
| Category | Clinic | 19,290 | 50,581 | 8 |
| Platform | TUH (TUEG) | 14,987 | 26,847 | 1 |
| Platform | Physionet | 607 | 22,707 | 2 |
| Platform | OpenNeuro | 4,153 | 10,194 | 56 |
| Platform | MOABB | 711 | 384 | 27 |
| Platform | Other | 3,802 | 1,250 | 6 |
| Channels | [3, 30) | 19,871 | 50,870 | 31 |
| Channels | [30, 80) | 1,781 | 1,516 | 48 |
| Channels | [80, 129] | 2,622 | 9,027 | 13 |
| **Total** | | **24,274** | **61,415** | **92** |

### Preprocessing pipeline (paper §3.1.1)
1. Drop recordings shorter than 10 s and any recording used in downstream tasks.
2. Resample to **200 Hz**, band-pass filter **0.5–99.5 Hz**, convert to float32.
3. Z-score normalize using statistics computed across each recording session.
4. Clip values exceeding 15 standard deviations (unlike CBraMod, REVE *keeps* signals above 100 µV, contributing to the 60,000 h total vs 9,000 h in CBraMod and 2,534 h in LaBraM).
5. Collect or infer 3-D electrode coordinates (10-5 system); recordings without identifiable positions are excluded.

> The REVE repository includes per-dataset conversion scripts in [`preprocessing/`](https://github.com/elouayas/reve_eeg/tree/main/preprocessing) (e.g. `preprocessing_bciciv2a.py`, `preprocessing_physio.py`, `preprocessing_hmc.py`, `preprocessing_faced.py`, `preprocessing_mumtaz.py`, `preprocessing_speech.py`, `preprocessing_stress.py`, `ISRUC/prepare_ISRUC.py`) with a dedicated [`preprocessing/README.md`](https://github.com/elouayas/reve_eeg/blob/main/preprocessing/README.md).

## Platform-level download entry points

Rather than listing all 92 datasets individually, REVE pulls them from four main hubs plus a handful of "other" sources:

| Platform | Entry point | Notes |
|----------|-------------|-------|
| **TUH (TUEG)** | https://isip.piconepress.com/projects/nedc/html/tuh_eeg/ | Free with registration. 26,847 h. |
| **PhysioNet** | https://physionet.org/ | REVE uses Siena Scalp EEG (CC-BY 4.0) and ICARE (CC-BY-NC-SA 4.0). |
| **OpenNeuro** | https://openneuro.org/ | 56 datasets. All under CC0. See dataset IDs list below. |
| **MOABB** | https://github.com/NeuroTechX/moabb | 27 BCI datasets under BSD 3-Clause. The MOABB Python package handles download + loading programmatically. |
| **Other** | | NMT (CC-BY), HMS (CC-BY-NC 4.0), SparrKULee (CC-BY-NC 4.0), Inria Large (Zenodo, CC-BY 4.0), THINGS2 (CC-BY 4.0), TDBRAIN (GPL-3.0 on Brainclinics), Healthy Brain Network EEG Releases 4 & 5 (NKI). |

### OpenNeuro dataset IDs used by REVE (56 datasets)

```
ds004706, ds004582, ds004356, ds005189, ds003887, ds003885, ds004043, ds004357,
ds003825, ds004816, ds004840, ds005262, ds004477, ds005273, ds004561, ds004951,
ds004324, ds005095, ds005509, ds005506, ds005507, ds005510, ds005511, ds005512,
ds005514, ds001787, ds003690, ds004603, ds003969, ds004147, ds003004, ds002711,
ds004152, ds005089, ds004264, ds004315, ds004408, ds005121, ds003775, ds004572,
ds002778, ds003846, ds002279, ds002680, ds004148, ds004902, ds002680, ds004284,
ds004395, ds005508, ds005697, ds005620, ds005594, ds005586
```

Each OpenNeuro ID resolves to `https://openneuro.org/datasets/<id>` (e.g. https://openneuro.org/datasets/ds004706).

### MOABB datasets used by REVE (27 datasets)

AlexMI, BNCI2014004, BNCI2015001, BNCI2015004, Cho2017, Lee2019_MI, Liu2024, Ofner2017, Shin2017A, Weibo2014, Zhou2016, Schirrmeister2017, Kalunga2016, Lee2019_SSVEP, Nakanishi2015, BI2014a, BI2014b, Korczowski2019, BNCI2014008, BNCI2014009, Riccio2013, Aricò2014, BNCI2015003, EPFLP300, BI2015a, Sosulski2019, Lee2019_ERP.

All of these are loadable in one line via the [MOABB](https://moabb.neurotechx.com/) package, e.g.:

```python
from moabb.datasets import BNCI2014_001
data = BNCI2014_001().get_data()
```

## How to reproduce the pre-training preprocessing

```bash
# 1) Install REVE
git clone https://github.com/elouayas/reve_eeg
cd reve_eeg && pip install -e .

# 2) Download the constituent datasets
#    - TUEG: request access on the TUH EEG portal
#    - OpenNeuro: openneuro-py download --dataset ds004706 --target-dir ...
#    - MOABB: handled automatically by the moabb package
#    - Physionet/NMT/HMS/etc: follow preprocessing/README.md

# 3) Convert each corpus to REVE's expected format
python preprocessing/preprocessing_physio.py --input ... --output ...
# (repeat for each dataset; see preprocessing/README.md)

# 4) Launch pretraining
python src/train.py +experiment=pretrain_base
```

## Citation

```bibtex
@inproceedings{elouahidi2025reve,
  title={{REVE}: A Foundation Model for {EEG} Adapting to Any Setup with Large-Scale Pre-training on 25{,}000 Subjects},
  author={El Ouahidi, Yassine and Lys, Jonathan and Th{\"o}lke, Philipp and Farrugia, Nicolas and Pasdeloup, Bastien and Gripon, Vincent and Jerbi, Karim and Lioi, Giulia},
  booktitle={Advances in Neural Information Processing Systems (NeurIPS)},
  year={2025}
}
```
