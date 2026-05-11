# LaBraM — Large Brain Model

> **Large Brain Model for Learning Generic Representations with Tremendous EEG Data in BCI**
> Wei-Bang Jiang, Li-Ming Zhao, Bao-Liang Lu. **ICLR 2024 (Spotlight).**

- Paper (OpenReview): https://openreview.net/forum?id=QzTpTRVtrP
- Official code: https://github.com/935963004/LaBraM
- Preprocessing scripts folder: https://github.com/935963004/LaBraM/tree/main/dataset_maker

## Pre-training Data Summary

LaBraM is pre-trained on **~2,534.78 hours** of EEG collected from **about 20 public + self-collected datasets** (used for both the vector-quantized neural tokenizer and the masked-EEG modeling stage). The four downstream datasets (TUAB, TUEV, SEED-V, MoBI) are explicitly excluded from the pre-training pool.

### Uniform preprocessing
1. Band-pass filter 0.1–75 Hz
2. Notch filter at 50 Hz
3. Resample to **200 Hz**
4. Scale to µV and clip values to approximately [-1, 1] (unit = 100 µV)

The pre-training preprocessing pipeline lives at [`dataset_maker/make_h5dataset_for_pretrain.py`](https://github.com/935963004/LaBraM/blob/main/dataset_maker/make_h5dataset_for_pretrain.py). Downstream-specific scripts (`make_TUAB.py`, `make_TUEV.py`) also live in the same folder.

## Pre-training Datasets

| # | Dataset | Hours | #Ch | Rate (Hz) | Short description | Download |
|---|---------|-------|-----|-----------|-------------------|----------|
| 1 | BCI Competition IV-1 | 8.21 | 59 | 1000 | Motor imagery, 7 subjects, 2 classes (+idle) | https://www.bbci.de/competition/iv/#dataset1 |
| 2 | Emobrain | 4.94 | 64 | 1024 | IAPS-elicited emotion, 16 subjects (EEG+fNIRS) | https://www.eecs.qmul.ac.uk/mmv/datasets/emobrain/ |
| 3 | Grasp and Lift EEG Challenge | 11.72 | 32 | 500 | GAL trials, 12 subjects | https://www.kaggle.com/c/grasp-and-lift-eeg-detection |
| 4 | Inria BCI Challenge | 29.98 | 56 | 600 | P300 speller, 26 subjects | https://www.kaggle.com/c/inria-bci-challenge |
| 5 | EEG Motor Movement/Imagery Dataset | 47.3 | 64 | 160 | PhysioNet MMI, 109 subjects | https://physionet.org/content/eegmmidb/1.0.0/ |
| 6 | Raw EEG Data (Trujillo 2020) | 34.35 | 64 | 256 | Information-Integration & Rule-Based categorization | https://openneuro.org/datasets/ds003490 |
| 7 | Resting State EEG Data (Trujillo 2017) | 3.04 | 64 | 256 | 22 subjects, 8 min eyes-closed / eyes-open | https://openneuro.org/datasets/ds003478 |
| 8 | SEED Series (SEED / SEED-IV / SEED-V / SEED-GER / SEED-FRA) | 166.75 | 62 | 1000 | Emotion recognition, videos | https://bcmi.sjtu.edu.cn/home/seed/ |
| 9 | Siena Scalp EEG Database | 30.47 | 31 | 512 | 14 epilepsy patients | https://physionet.org/content/siena-scalp-eeg/1.0.0/ |
| 10 | SPIS Resting State Dataset | 0.83 | 64 | 2048 | 10 subjects, eyes-open/closed + attention task | https://github.com/mastaneht/SPIS-Resting-State-Dataset |
| 11 | Target Versus Non-Target | 16 | 32 | 512 | 50 subjects, Brain Invaders P300 | https://zenodo.org/record/2649069 |
| 12 | TUAR (TUH Artifact) | 92.22 | 23 | 256 | TUEG subset, 5 artifact types | https://isip.piconepress.com/projects/tuh_eeg/html/downloads.shtml |
| 13 | TUEP (TUH Epilepsy) | 591.22 | 19–23 | 256 | 100 epilepsy + 100 non-epilepsy subjects | https://isip.piconepress.com/projects/tuh_eeg/html/downloads.shtml |
| 14 | TUSZ (TUH Seizure) | 1138.53 | 19–23 | 256 | Manually annotated seizure events | https://isip.piconepress.com/projects/tuh_eeg/html/downloads.shtml |
| 15 | TUSL (TUH Slowing) | 20.59 | 23 | 256 | TUEG subset, slowing events | https://isip.piconepress.com/projects/tuh_eeg/html/downloads.shtml |
| 16 | Self-collected EEG (SJTU/Jiang et al.) | 342.23 | 62 | 1000 | 140+ subjects, ESI NeuroScan, various conditions | Not publicly released |

**Total: ~2,534.78 hours.** Access to all TUH sub-corpora (TUAR/TUEP/TUSZ/TUSL) requires free registration with the [Temple University Hospital EEG Corpus](https://isip.piconepress.com/projects/nedc/html/tuh_eeg/).

## How to reproduce the pre-training preprocessing

1. Download each dataset from the links above (and request TUH access for TUAR/TUEP/TUSZ/TUSL).
2. Clone LaBraM and install `requirements.txt`.
3. Convert raw `.cnt`/`.edf`/`.bdf` to HDF5 patches via:
   ```bash
   python dataset_maker/make_h5dataset_for_pretrain.py \
       --input_dir /path/to/raw \
       --output_dir /path/to/h5
   ```
4. Launch pre-training with `run_vqnsp_training.py` then `run_labram_pretraining.py`.

## Citation

```bibtex
@inproceedings{jiang2024labram,
  title={Large Brain Model for Learning Generic Representations with Tremendous EEG Data in BCI},
  author={Jiang, Wei-Bang and Zhao, Li-Ming and Lu, Bao-Liang},
  booktitle={The Twelfth International Conference on Learning Representations (ICLR)},
  year={2024}
}
```
