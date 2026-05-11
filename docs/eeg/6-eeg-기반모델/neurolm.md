# NeuroLM — Multi-task EEG Foundation Model with an LLM backbone

> **NeuroLM: A Universal Multi-task Foundation Model for Bridging the Gap between Language and EEG Signals**
> Wei-Bang Jiang, Yansen Wang, Bao-Liang Lu, Dongsheng Li. **ICLR 2025.**

- Paper (OpenReview): https://openreview.net/forum?id=Io9yFt7XH7
- Official code: https://github.com/935963004/NeuroLM
- Preprocessing scripts folder: https://github.com/935963004/NeuroLM/tree/main/dataset_maker

## Pre-training Data Summary

NeuroLM reuses the LaBraM data-collection philosophy but **scales up by ~10×**: the authors additionally use the full TUEG corpus (≈24,000 hours) alongside the previously curated public corpora. The total after cleaning is **~25,000 hours**, making it (at the time of publication) the largest public-EEG pre-training pool reported.

### Preprocessing (paper §3.2 "Data Preprocessing")
- Band-pass filter 0.1–75 Hz
- Notch filter 50 Hz or 60 Hz depending on the data source's geographic region
- Resample to **200 Hz**
- Normalize by dividing by 100 (values in µV → roughly [-1, 1])

NeuroLM's pre-training data conversion script is [`dataset_maker/prepare_TUH_pretrain.py`](https://github.com/935963004/NeuroLM/blob/main/dataset_maker/prepare_TUH_pretrain.py); downstream dataset scripts (`prepare_TUAB.py`, `prepare_TUEV.py`, `prepare_SEED.py`, `prepare_HMC.py`, `prepare_TUSL.py`, `prepare_workload.py`) live alongside it.

## Pre-training Datasets (Table 6 of the paper)

| # | Dataset | Hours | #Ch | Rate (Hz) | Notes | Download |
|---|---------|-------|-----|-----------|-------|----------|
| 1 | **TUEG** (Temple Univ. Hospital EEG Corpus, full) | ~24,000 | 17–23 | 250–1024 | 26,846 clinical recordings. The single biggest contributor. | https://isip.piconepress.com/projects/nedc/html/tuh_eeg/ |
| 2 | SEED Series (SEED-IV / SEED-V / SEED-GER / SEED-FRA) | 170.54 | 62 | 1000 | Emotion videos | https://bcmi.sjtu.edu.cn/home/seed/ |
| 3 | BCI Competition IV-1 | 8.21 | 59 | 1000 | Motor imagery | https://www.bbci.de/competition/iv/#dataset1 |
| 4 | Emobrain | 4.94 | 64 | 1024 | IAPS-elicited emotion, 16 subjects | https://www.eecs.qmul.ac.uk/mmv/datasets/emobrain/ |
| 5 | Grasp and Lift | 11.72 | 32 | 500 | 12 subjects, GAL | https://www.kaggle.com/c/grasp-and-lift-eeg-detection |
| 6 | Inria BCI Challenge | 29.98 | 56 | 600 | 26 subjects, P300 | https://www.kaggle.com/c/inria-bci-challenge |
| 7 | PhysioNet Motor Movement/Imagery | 47.3 | 64 | 160 | 109 volunteers | https://physionet.org/content/eegmmidb/1.0.0/ |
| 8 | Raw EEG Data (Trujillo 2020) | 34.35 | 64 | 256 | Categorization tasks | https://openneuro.org/datasets/ds003490 |
| 9 | Resting State EEG Data (Trujillo 2017) | 3.04 | 64 | 256 | 22 subjects | https://openneuro.org/datasets/ds003478 |
| 10 | Siena Scalp EEG Database | 30.47 | 31 | 512 | 14 epilepsy patients | https://physionet.org/content/siena-scalp-eeg/1.0.0/ |
| 11 | SPIS Resting State Dataset | 0.83 | 64 | 2048 | 10 subjects, attention task | https://github.com/mastaneht/SPIS-Resting-State-Dataset |
| 12 | Target Versus Non-Target | 16 | 32 | 512 | 50 subjects, Brain Invaders P300 | https://zenodo.org/record/2649069 |
| 13 | Self-collected EEG corpus (SJTU) | 342.23 | 62 | 1000 | 140+ subjects | Not publicly released |

**Total (after cleaning): ≈25,000 hours.**

> **Note on overlap with LaBraM.** NeuroLM drops LaBraM's TUH sub-corpus splits (TUAR/TUEP/TUSZ/TUSL) in favour of the **full TUEG corpus**, and omits MoBI/SEED-V from the pre-training pool since these are used as downstream evaluation sets.

## How to reproduce the pre-training preprocessing

```bash
# 1) Download each dataset above; request TUEG access (free).
git clone https://github.com/935963004/NeuroLM
cd NeuroLM && pip install -r requirements.txt
# 2) Convert TUEG to pickle files
python dataset_maker/prepare_TUH_pretrain.py  --input_dir /path/to/tueg --output_dir /path/to/pkl
# 3) (Optional) also prepare text corpus
python text_dataset_maker/prepare.py
# 4) Train neural tokenizer → causal pre-training → instruction tuning
python train_vq.py && python train_pretrain.py && python train_instruction.py
```

## Citation

```bibtex
@inproceedings{jiang2025neurolm,
  title={{NeuroLM}: A Universal Multi-task Foundation Model for Bridging the Gap between Language and {EEG} Signals},
  author={Jiang, Wei-Bang and Wang, Yansen and Lu, Bao-Liang and Li, Dongsheng},
  booktitle={The Thirteenth International Conference on Learning Representations (ICLR)},
  year={2025}
}
```
