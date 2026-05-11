# HeartLang — ECG Language Model

> **Reading Your Heart: Learning ECG Words and Sentences via Pre-training ECG Language Model**
> Jiarui Jin, Haoyu Wang, Hongyan Li, Jun Li, Jiahui Pan, Shenda Hong. **ICLR 2025.**

- Paper (OpenReview): https://openreview.net/forum?id=6Hz1Ko087B
- Paper (arXiv): https://arxiv.org/abs/2502.10707
- Official code: https://github.com/PKUDigitalHealth/HeartLang
- Pre-trained checkpoints: https://huggingface.co/PKUDigitalHealth/HeartLang/tree/main
- QRS-Tokenizer script: https://github.com/PKUDigitalHealth/HeartLang/blob/main/QRSTokenizer.py
- Downstream preprocessing scripts folder: https://github.com/PKUDigitalHealth/HeartLang/tree/main/datasets/dataset_preprocess

## Pre-training Data Summary

Unlike conventional ECG self-supervised learning methods that slice ECG signals with **fixed-size and fixed-step time windows**, HeartLang treats **heartbeats as words** and **rhythms as sentences**. It is pre-trained on a **single large-scale ECG corpus** and learns ECG representations through two stages: **vector-quantized heartbeat reconstruction (VQ-HBR)** and **masked ECG sentence pre-training**.

- **Dataset:** MIMIC-IV-ECG Diagnostic Electrocardiogram Matched Subset
- **Raw scale:** 800,035 12-lead ECG recordings • 161,352 subjects • 10-second ECG segments • sampled at 500 Hz
- **After preprocessing:** all records are downsampled to **100 Hz** and converted into QRS-based **ECG sentences**. The pre-training split is **720,031 training ECGs** and **80,004 validation ECGs**.
- **ECG sentence format:** each heartbeat patch is treated as an **individual ECG word**; 12-lead heartbeat words are concatenated into an ECG sentence with maximum sequence length **l = 256** and heartbeat window size **t = 96**.
- **ECG vocabulary:** VQ-HBR uses an **8,192-entry codebook** with **128-dimensional collective ECG words**. In validation, the effectively used ECG vocabulary contains **5,394 discrete ECG words**.

### Preprocessing pipeline (paper §3.1, §4.1 + official README + `QRSTokenizer.py`)

1. Start from MIMIC-IV-ECG, which contains 10-second 12-lead ECG recordings sampled at 500 Hz.
2. Replace `NaN` and `Inf` values in ECG recordings with the average of six neighboring points.
3. Downsample all ECG records to **100 Hz** before QRS-tokenization.
4. Apply the QRS-Tokenizer: use lead I, apply a **5–20 Hz band-pass filter**, perform moving wave integration with a Ricker wavelet, square the integration signal, and detect QRS complexes from local maxima that pass the refractory-period and threshold criteria.
5. For each detected QRS index, segment heartbeat patches independently for each lead. The midpoint between adjacent QRS indices is used as the interval boundary.
6. If a segmented heartbeat interval is shorter than **t = 96**, zero-pad it to the required length.
7. Concatenate heartbeat patches from the 12 leads to form an ECG sentence. If the sequence is shorter than **l = 256**, zero-filled patches are added; if it is longer than **l = 256**, it is truncated.
8. Train the ECG vocabulary through **VQ-HBR**: map individual ECG words to collective ECG words using vector quantization and reconstruct the original heartbeat patches.
9. Perform **masked ECG sentence pre-training**: randomly mask 50% of individual ECG words and train HeartLang to predict the corresponding collective ECG word indices.

The official README gives the MIMIC-IV preprocessing command with `mimic_preprocess.py`; ECG sentence generation is performed with [`QRSTokenizer.py`](https://github.com/PKUDigitalHealth/HeartLang/blob/main/QRSTokenizer.py), VQ-HBR training with [`scripts/vqhbr/MIMIC-IV.sh`](https://github.com/PKUDigitalHealth/HeartLang/tree/main/scripts/vqhbr), and masked ECG sentence pre-training with [`scripts/pretrain/MIMIC-IV.sh`](https://github.com/PKUDigitalHealth/HeartLang/tree/main/scripts/pretrain).

## Pre-training Dataset

| Dataset | Subjects | Sessions | Raw hours | #Samples after preprocessing | Rate (Hz) | Access |
|---------|----------|----------|-----------|------------------------------|-----------|--------|
| MIMIC-IV-ECG Diagnostic ECG Matched Subset | 161,352 | Not specified in paper | ~2,222 h, derived from 800,035 × 10 s ECGs | 800,035 ECG sentences; 720,031 train + 80,004 valid | 500 → 100 | PhysioNet credentialed access → https://physionet.org/content/mimic-iv-ecg/ |

## Downstream datasets (informational — not used for pre-training)

HeartLang evaluates on six benchmark settings from three public ECG datasets: **PTB-XL Superclass**, **PTB-XL Subclass**, **PTB-XL Form**, **PTB-XL Rhythm**, **CPSC2018**, and **Chapman-Shaoxing-Ningbo (CSN)**. These downstream datasets are used for linear probing and evaluation, not for HeartLang pre-training.

- **PTB-XL:** 21,837 12-lead ECG recordings from 18,885 patients, sampled at 500 Hz for 10 seconds. It is evaluated through four subsets: Superclass (5 classes), Subclass (23 classes), Form (19 classes), and Rhythm (12 classes).
- **CPSC2018:** 6,877 12-lead ECG recordings, sampled at 500 Hz, with durations from 6 to 60 seconds and 9 labels.
- **CSN / Chapman-Shaoxing-Ningbo:** originally 45,152 12-lead ECG recordings; after removing records with “unknown” annotations, the refined benchmark contains 23,026 ECG recordings with 38 labels.

Individual preprocessing scripts for downstream datasets are in the [`datasets/dataset_preprocess`](https://github.com/PKUDigitalHealth/HeartLang/tree/main/datasets/dataset_preprocess) folder, and fine-tuning scripts are in the [`scripts/finetune`](https://github.com/PKUDigitalHealth/HeartLang/tree/main/scripts/finetune) folder.

## How to reproduce the pre-training preprocessing

```bash
# 1) Request credentialed access and download MIMIC-IV-ECG from PhysioNet
#    https://physionet.org/content/mimic-iv-ecg/

# 2) Clone HeartLang
git clone https://github.com/PKUDigitalHealth/HeartLang.git
cd HeartLang

# 3) Set up the environment
conda create -n heartlang python=3.9
conda activate heartlang
pip install -r requirements.txt

# 4) Preprocess MIMIC-IV-ECG
python mimic_preprocess.py \
  --dataset_path <path_to_MIMIC_data> \
  --output_path datasets/ecg_datasets/MIMIC-IV

# 5) Generate ECG sentences with QRS-Tokenizer
python QRSTokenizer.py --dataset_name MIMIC-IV

# 6) Train the ECG vocabulary through VQ-HBR
bash scripts/vqhbr/MIMIC-IV.sh

# 7) Launch masked ECG sentence pre-training
bash scripts/pretrain/MIMIC-IV.sh
```

## Citation

```bibtex
@inproceedings{
  jin2025reading,
  title={Reading Your Heart: Learning {ECG} Words and Sentences via Pre-training {ECG} Language Model},
  author={Jiarui Jin and Haoyu Wang and Hongyan Li and Jun Li and Jiahui Pan and Shenda Hong},
  booktitle={The Thirteenth International Conference on Learning Representations},
  year={2025},
  url={https://openreview.net/forum?id=6Hz1Ko087B}
}
```
