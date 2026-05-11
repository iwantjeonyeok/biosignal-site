# CBraMod — Criss-Cross Brain Foundation Model

> **CBraMod: A Criss-Cross Brain Foundation Model for EEG Decoding**
> Jiquan Wang, Sha Zhao, Zhiling Luo, Yangxuan Zhou, Haiteng Jiang, Shijian Li, Tao Li, Gang Pan. **ICLR 2025.**

- Paper (OpenReview): https://openreview.net/forum?id=NPNUHgHF2w
- Official code: https://github.com/wjq-learning/CBraMod
- Preprocessing scripts folder: https://github.com/wjq-learning/CBraMod/tree/main/preprocessing

## Pre-training Data Summary

Unlike LaBraM (which aggregates ~20 datasets), CBraMod is pre-trained on a **single but very large** corpus:

- **Dataset:** Temple University Hospital EEG Corpus (TUEG), v2.0.0
- **Raw scale:** 69,652 clinical EEG recordings • 14,987 subjects • 26,846 sessions • ~27,062 hours (≥40 distinct channel configurations, mostly sampled at 256 Hz)
- **After preprocessing:** **1,109,545 EEG samples (>9,000 hours)**, significantly larger than LaBraM's pre-training pool.

### Preprocessing pipeline (paper §3.1 + `preprocessing_tueg_for_pretraining.py`)

1. Discard recordings shorter than 5 min; drop the first and last minute of each recording.
2. Keep only the 19 common 10–20 channels: `Fp1, Fp2, F7, F3, Fz, F4, F8, T3, C3, Cz, C4, T4, T5, P3, Pz, P4, T6, O1, O2`.
3. Band-pass filter **0.3–75 Hz**, notch filter **60 Hz**.
4. Resample to **200 Hz** and segment into non-overlapping **30-second** windows.
5. Reject windows with any amplitude exceeding 100 µV, then unit-normalize to 100 µV so values ≈ [-1, 1].

The exact script used by the authors lives at [`preprocessing/preprocessing_tueg_for_pretraining.py`](https://github.com/wjq-learning/CBraMod/blob/main/preprocessing/preprocessing_tueg_for_pretraining.py).

## Pre-training Dataset

| Dataset | Subjects | Sessions | Raw hours | #Samples after cleaning | Rate (Hz) | Access |
|---------|----------|----------|-----------|-------------------------|-----------|--------|
| TUEG (Temple Univ. Hospital EEG Corpus) | 14,987 | 26,846 | ~27,062 | 1,109,545 (>9,000 h) | 256 (mixed) | Free registration → https://isip.piconepress.com/projects/nedc/html/tuh_eeg/ |

## Downstream datasets (informational — not used for pre-training)

CBraMod evaluates on 12 public datasets spanning 10 BCI tasks: FACED, SEED-V, PhysioNet-MI, SHU-MI, ISRUC, CHB-MIT, BCIC2020-3, Mumtaz2016, SEED-VIG, MentalArithmetic, TUEV, TUAB. Individual preprocessing scripts for each are in the same [`preprocessing/`](https://github.com/wjq-learning/CBraMod/tree/main/preprocessing) folder.

## How to reproduce the pre-training preprocessing

```bash
# 1) Request TUEG access and download the corpus (free)
#    https://isip.piconepress.com/projects/nedc/html/tuh_eeg/
# 2) Clone CBraMod
git clone https://github.com/wjq-learning/CBraMod
cd CBraMod && pip install -r requirements.txt
# 3) Run the TUEG pre-training preprocessor (adjust paths inside the script)
python preprocessing/preprocessing_tueg_for_pretraining.py
# 4) Launch pre-training
python pretrain_main.py
```

## Citation

```bibtex
@inproceedings{wang2025cbramod,
  title={CBraMod: A Criss-Cross Brain Foundation Model for EEG Decoding},
  author={Wang, Jiquan and Zhao, Sha and Luo, Zhiling and Zhou, Yangxuan and Jiang, Haiteng and Li, Shijian and Li, Tao and Pan, Gang},
  booktitle={The Thirteenth International Conference on Learning Representations (ICLR)},
  year={2025}
}
```
