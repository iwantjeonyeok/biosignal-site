# NERVE — Noise-Variability-Robust EEG Foundation Model

> **NERVE: Noise-Variability-Robust EEG Foundation Model with Electrode-Brain Interactions**
> Anonymous authors. **ICML 2026 (under review).**

- Official code (anonymous repo referenced in paper): https://github.com/NERVE-2026/NERVE

## Pre-training Data Summary

NERVE curates a deliberately task-diverse pre-training corpus designed to expose the model to 10 distinct use cases (seizure detection, gait recognition, emotion recognition, motor imagery, sleep staging, event-type classification, vigilance, workload, mental-disorder diagnosis, grasp-and-lift):

- **27 publicly available EEG datasets • 16,595 raw hours**
- **After preprocessing: 213,784 EEG samples • 10,956 hours** — substantially larger than LaBraM (2,534.78 h) and CBraMod (9,000 h), and in the same ballpark as their 9,000–25,000 h range.
- Unified **128-channel** configuration (most electrodes available across datasets are retained; missing channels are filled with zeros so the model can treat them as an explicit "missing-channel mask").

### Preprocessing pipeline (paper §3.1, Appendix C.3)
1. **Channel selection** — keep as many electrodes as possible (up to 128), filling missing ones with zeros to act as a missing-channel mask.
2. **Band-pass filter** 0.3–75 Hz (slow-drift removal + high-frequency muscle/equipment-noise suppression).
3. **Notch filter** at 50 Hz (power-line interference).
4. **Resample to 200 Hz.**
5. **Z-score normalization** to mitigate inter- and intra-subject variability.
6. Patch length **P = 200 (1 s)**; stride **1 s** for the noise-robust neural tokenizer and **4 s** for the NERVE foundation model. Total patches per sample capped at 256.

### Architecture (paper §3.2, Appendix B.1)
- **Backbone:** 12-layer **EPA (Electrode-Position-Aware) Transformer**, 200 hidden dim, 800 FFN, 10 attention heads, **6 cortical-region position-router groups**.
- **Noise-robust neural tokenizer:** 3-layer 1D-CNN patch encoder + 9-layer EPA encoder / 3-layer EPA decoder, 8192×64 codebook, trained with **denoising temporal-spectral prediction** (Gaussian noise augmentation σ=0.05, reconstructing both time-domain signal and DFT-based normalized spectral representation).
- **Pre-training loss:** masked EEG modeling (50 % mask ratio) + **KoLeo regularization** for variability-robust learning: `L = L_MEM + α · L_KoLeo`, α = 0.1.
- Pre-trained sequentially (tokenizer → model) on **4× NVIDIA A100-80G for ~5 days**.

## Pre-training Datasets (Table 7 of the paper)

Hours are the raw totals listed in Table 7; channel counts are the **used** channel counts reported in Appendix B.2.

| # | Dataset | Task | #Ch (used) | Rate (Hz) | Hours | Download |
|---|---------|------|:---:|:---:|---:|---|
| 1 | Resting State EEG Data (Trujillo 2017) | Raw / resting | 64 | 256 | 3 | https://openneuro.org/datasets/ds003478 |
| 2 | Neonate (Stevenson 2019) | Seizure detection | 19 | 256 | 57 | https://zenodo.org/record/4940267 |
| 3 | Siena Scalp EEG (Detti 2020) | Seizure detection | 28 | 512 | 141 | https://physionet.org/content/siena-scalp-eeg/1.0.0/ |
| 4 | TUSZ (TUH Seizure) | Seizure detection | 20 | 256 | 1,474 | https://isip.piconepress.com/projects/nedc/html/tuh_eeg/ |
| 5 | 2018 PhysioNet Challenge (You Snooze You Win) | Sleep staging | 6 | 200 | 14,611 | https://physionet.org/content/challenge-2018/1.0.0/ |
| 6 | SEED | Emotion | 62 | 1000 | 42 | https://bcmi.sjtu.edu.cn/home/seed/ |
| 7 | SEED-IV | Emotion | 62 | 200 | 42 | https://bcmi.sjtu.edu.cn/home/seed/ |
| 8 | DREAMER | Emotion | 14 | 128 | 24 | https://zenodo.org/record/546113 |
| 9 | Emobrain | Emotion | 64 | 1024 | 3 | https://www.eecs.qmul.ac.uk/mmv/datasets/emobrain/ |
| 10 | BCI Competition IV-2a | Motor imagery | 22 | 250 | 13 | https://www.bbci.de/competition/iv/#dataset2a |
| 11 | BCI Competition IV-2b | Motor imagery | 3 | 250 | 26 | https://www.bbci.de/competition/iv/#dataset2b |
| 12 | BCI Competition IV-1 | Motor imagery | 59 | 1000 | 14 | https://www.bbci.de/competition/iv/#dataset1 |
| 13 | SHU-MI | Motor imagery | 32 | 250 | 799 | https://doi.org/10.6084/m9.figshare.19228725.v3 |
| 14 | Inria BCI Challenge | Event type (P300) | 56 | 600 | 14 | https://www.kaggle.com/c/inria-bci-challenge |
| 15 | Target vs Non-Target (Brain Invaders) | Event type (P300) | 32 | 512 | 4 | https://zenodo.org/record/2649069 |
| 16 | MoBI | Event type (gait) | 60 | 100 | 9 | https://www.nature.com/articles/sdata201874 (figshare) |
| 17 | BCIC2020-3 | Event type (imagined speech) | 64 | 256 | 272 | https://osf.io/pq7vb/ |
| 18 | SPIS Resting State | Vigilance | 64 | 256 | 1 | https://github.com/mastaneht/SPIS-Resting-State-Dataset |
| 19 | FatigueSet | Vigilance / fatigue | 4 | 256 | 11 | https://fatigueset.github.io/ |
| 20 | Stew | Workload | 14 | 128 | 4 | https://ieee-dataport.org/open-access/stew-simultaneous-task-eeg-workload-dataset |
| 21 | Raw EEG Data (Trujillo 2021) | Workload / categorization | 64 | 256 | 34 | https://doi.org/10.18738/T8/HAYF5H |
| 22 | Mental Arithmetic (Zyma 2019) | Workload | 19 | 500 | 2 | https://physionet.org/content/eegmat/1.0.0/ |
| 23 | Berlin_dsr (Shin 2018) | Workload (discrimination) | 28 | 200 | 5 | http://doc.ml.tu-berlin.de/simultaneous_EEG_NIRS/ |
| 24 | Berlin_nback (Shin 2018) | Workload (n-back) | 28 | 200 | 8 | http://doc.ml.tu-berlin.de/simultaneous_EEG_NIRS/ |
| 25 | Berlin_wg (Shin 2018) | Workload (word-generation) | 28 | 200 | 13 | http://doc.ml.tu-berlin.de/simultaneous_EEG_NIRS/ |
| 26 | Mumtaz2016 (MDD vs HC) | Mental disorder | 19 | 256 | 10 | https://figshare.com/articles/dataset/EEG_Data_New/4244171 |
| 27 | Grasp and Lift EEG Challenge | Grasp-and-lift recognition | 32 | 500 | 9 | https://www.kaggle.com/c/grasp-and-lift-eeg-detection |

**Total (raw): 16,595 hours → after preprocessing: 10,956 hours / 213,784 samples.**

> **Downstream (not used for pre-training).** NERVE evaluates on 8 datasets spanning 5 tasks that are **deliberately excluded** from the pre-training pool to measure out-of-distribution generalization: **TUSL**, **SEED-V**, **DEAP**, **HCI-Tagging Emotion**, **High-Gamma**, **TUEV**, **BCI-NER Challenge**, **SEED-VIG** (Table 2).

## How to reproduce the pre-training preprocessing

```bash
# 1) Download each of the 27 datasets above (TUSZ + Siena + Neonate require
#    dataset-specific registration; most others are open).
# 2) Clone the NERVE repository
git clone https://github.com/NERVE-2026/NERVE
cd NERVE

# 3) Apply the unified pipeline to every corpus:
#    - Fill missing channels with zeros (target: 128-ch layout)
#    - Band-pass 0.3–75 Hz, notch 50 Hz
#    - Resample to 200 Hz
#    - Z-score normalize per recording
#    - Segment into 1 s patches (P = 200)

# 4) Train the noise-robust neural tokenizer (20 epochs, batch 1024, data stride 200)
#    then launch variability-robust NERVE pre-training
#    (12-layer EPA Transformer, 10 epochs, batch 512, masking ratio 0.5,
#     KoLeo coefficient α = 0.1, data stride 800)
#    on 4× NVIDIA A100-80G.
```

## Key ideas (why NERVE is different)

1. **Noise-robust tokenizer via denoising temporal-spectral prediction.** Gaussian noise is injected into every patch; the tokenizer must reconstruct both the clean time-domain signal and its **DFT-derived normalized spectrum** (real + complex). This covers the full frequency spectrum — unlike LaBraM (phase loss fails to converge) or NeuroLM (no explicit phase modeling).
2. **Variability-robust pre-training with KoLeo regularization.** A Kozachenko–Leonenko entropy term added to masked EEG modeling enforces **inter-subject separability** in the latent space without requiring subject labels.
3. **Electrode-Position-Aware (EPA) attention.** A learnable position-router `P ∈ R^{R×N×d}` with **R=6 cortical-region groups** injects topographic priors into self-attention, giving a sequential low-rank generalization of CBraMod's criss-cross attention (see Appendix F).

## Citation

```bibtex
@inproceedings{anonymous2026nerve,
  title={{NERVE}: Noise-Variability-Robust {EEG} Foundation Model with Electrode-Brain Interactions},
  author={Anonymous},
  booktitle={International Conference on Machine Learning (ICML)},
  note={Under review},
  year={2026}
}
```
