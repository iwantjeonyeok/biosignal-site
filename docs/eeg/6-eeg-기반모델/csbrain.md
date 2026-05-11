# CSBrain — Cross-scale Spatiotemporal Brain Foundation Model

> **CSBrain: A Cross-scale Spatiotemporal Brain Foundation Model for EEG Decoding**
> Yuchen Zhou, Jiamin Wu, Zichen Ren, Zhouheng Yao, Weiheng Lu, Kunyu Peng, Qihao Zheng, Chunfeng Song, Wanli Ouyang, Chao Gou. **NeurIPS 2025.**

- Paper (arXiv): https://arxiv.org/abs/2506.23075
- Official code: https://github.com/yuchen2199/CSBrain
- Downstream preprocessing folder: https://github.com/yuchen2199/CSBrain/tree/main/preprocessing

## Pre-training Data Summary

CSBrain adopts the **same pre-training corpus and the same preprocessing pipeline as CBraMod**:

- **Dataset:** Temple University Hospital EEG Corpus (TUEG)
- **After cleaning:** **1,109,545 EEG segments (>9,000 hours)** — identical pool to CBraMod.
- Pre-training objective: masked autoencoding, 50 % masking, 40 epochs on 4× A100.

### Preprocessing (paper §3.1)
1. Band-pass **0.3–75 Hz**, notch filter at **60 Hz**.
2. Resample to **200 Hz**; segment into **30 s** non-overlapping windows.
3. Clip amplitude to 100 µV so the range falls in [-1, 1].

The CSBrain README explicitly instructs users to **"follow CBraMod"** for the TUEG pre-training preprocessing, so see: https://github.com/wjq-learning/CBraMod/blob/main/preprocessing/preprocessing_tueg_for_pretraining.py

The CSBrain repository's own [`preprocessing/`](https://github.com/yuchen2199/CSBrain/tree/main/preprocessing) folder only contains scripts for three **downstream** datasets that were not covered by CBraMod: **HMC**, **Siena**, and **TUSL**.

## Pre-training Dataset

| Dataset | Segments | Hours | Rate (Hz) | Access |
|---------|----------|-------|-----------|--------|
| TUEG (Temple Univ. Hospital EEG Corpus) | 1,109,545 | >9,000 | 200 (after resampling) | Free registration → https://isip.piconepress.com/projects/nedc/html/tuh_eeg/ |

## Downstream datasets (16 datasets / 11 tasks — not used for pre-training)

BCIC-IV-2a, PhysioNet-MI, SHU-MI, FACED, SEED-V, CHB-MIT, Siena, ISRUC, HMC, BCIC2020-3, SEED-VIG, MentalArithmetic, Mumtaz2016, TUEV, TUAB, TUSL. See `preprocessing/` in CSBrain for HMC/Siena/TUSL and the [CBraMod preprocessing folder](https://github.com/wjq-learning/CBraMod/tree/main/preprocessing) for the rest.

## How to reproduce the pre-training preprocessing

```bash
# 1) Obtain TUEG from TUH (free, with registration).
# 2) Clone CBraMod and run its TUEG preprocessor:
git clone https://github.com/wjq-learning/CBraMod
python CBraMod/preprocessing/preprocessing_tueg_for_pretraining.py
# 3) Clone CSBrain and launch pre-training:
git clone https://github.com/yuchen2199/CSBrain
cd CSBrain && bash sh/pretrain_CSBrain.sh
```

## Citation

```bibtex
@inproceedings{zhou2025csbrain,
  title={{CSBrain}: A Cross-scale Spatiotemporal Brain Foundation Model for {EEG} Decoding},
  author={Zhou, Yuchen and Wu, Jiamin and Ren, Zichen and Yao, Zhouheng and Lu, Weiheng and Peng, Kunyu and Zheng, Qihao and Song, Chunfeng and Ouyang, Wanli and Gou, Chao},
  booktitle={Advances in Neural Information Processing Systems (NeurIPS)},
  year={2025}
}
```
