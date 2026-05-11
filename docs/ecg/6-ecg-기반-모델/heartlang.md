# HeartLang — ECG Language Model

> **Reading Your Heart: Learning ECG Words and Sentences via Pre-training ECG Language Model**
> Jiarui Jin, Haoyu Wang, Hongyan Li, Jun Li, Jiahui Pan, Shenda Hong. **ICLR 2025.**

- Paper (OpenReview): https://openreview.net/forum?id=6Hz1Ko087B
- Paper (arXiv): https://arxiv.org/abs/2502.10707
- Official code: https://github.com/PKUDigitalHealth/HeartLang
- Pre-trained checkpoints: https://huggingface.co/PKUDigitalHealth/HeartLang
- QRS-Tokenizer script: https://github.com/PKUDigitalHealth/HeartLang/blob/main/QRSTokenizer.py
- Downstream preprocessing scripts folder: https://github.com/PKUDigitalHealth/HeartLang/tree/main/datasets/dataset_preprocess

## Pre-training Data Summary

기존 ECG self-supervised learning 방법들은 ECG signal을 일반적인 time-series data처럼 보고, **fixed-size and fixed-step time windows**로 잘라서 학습하는 경우가 많다. 반면 HeartLang은 ECG signal을 하나의 언어처럼 해석한다. 즉, **heartbeats as words** 그리고 **rhythms as sentences**라는 관점에서 heartbeat 단위의 의미와 rhythm 단위의 문맥을 함께 학습한다.

HeartLang은 하나의 대규모 ECG corpus인 **MIMIC-IV-ECG**를 기반으로 pre-training된다. 학습 과정은 크게 두 단계로 구성된다. 첫 번째는 **vector-quantized heartbeat reconstruction (VQ-HBR)**이며, heartbeat 형태 정보를 담는 **ECG vocabulary**를 만드는 단계이다. 두 번째는 **masked ECG sentence pre-training**이며, ECG sentence 일부를 mask한 뒤 해당 위치의 collective ECG word를 예측하도록 학습하는 단계이다.

- **Dataset:** MIMIC-IV-ECG Diagnostic Electrocardiogram Matched Subset
- **Raw scale:** 800,035개의 12-lead ECG recordings • 161,352명의 subjects • 각 recording은 10초 길이 • sampling rate는 500 Hz
- **After preprocessing:** 모든 ECG recording을 **100 Hz**로 downsample한 뒤, QRS-Tokenizer를 사용해 QRS 기반 **ECG sentences**로 변환한다. 논문 기준 dataset split은 **720,031 train ECGs**와 **80,004 valid ECGs**이며, valid set은 VQ-HBR training 단계에서 사용된다.
- **ECG sentence format:** 각 heartbeat patch는 **individual ECG word**로 취급된다. 12-lead에서 추출한 heartbeat words를 순서대로 연결해 하나의 ECG sentence를 만들며, 최대 sequence length는 **l = 256**, heartbeat window size는 **t = 96**이다.
- **ECG vocabulary:** VQ-HBR 단계에서는 **8,192-entry codebook**과 **128-dimensional collective ECG words**를 사용한다. validation set에서 실제로 사용된 ECG vocabulary는 **5,394개의 discrete ECG words**로 보고된다.

### Preprocessing pipeline (paper §3.1, §4.1 + official README + `QRSTokenizer.py`)

1. **MIMIC-IV-ECG**에서 10초 길이의 12-lead ECG recordings를 사용한다.
2. ECG recording 안의 `NaN`과 `Inf` 값은 주변 6개 point의 평균값으로 대체한다.
3. 모든 ECG record를 **100 Hz**로 downsample한다.
4. **QRS-Tokenizer**를 적용한다. lead I signal에 **5–20 Hz band-pass filter**를 적용하고, Ricker wavelet 기반 moving wave integration을 수행한 뒤, squared integration signal에서 local maxima를 탐색해 QRS complexes를 검출한다.
5. 검출된 QRS index를 중심으로 heartbeat patch를 자른다. 각 lead별로 독립적으로 segmentation하며, 인접한 QRS index 사이의 midpoint를 interval boundary로 사용한다.
6. 잘린 heartbeat interval이 **t = 96**보다 짧으면 zero-padding을 적용해 길이를 맞춘다.
7. 12-lead에서 얻은 heartbeat patches를 순서대로 연결해 하나의 ECG sentence를 만든다. ECG sentence 길이가 **l = 256**보다 짧으면 zero-filled patches를 추가하고, 길면 **l = 256**까지만 사용한다.
8. **VQ-HBR** 단계에서 individual ECG words를 vector quantization으로 **collective ECG words**에 mapping하고, 원래 heartbeat patches를 reconstruction하도록 학습한다.
9. **masked ECG sentence pre-training** 단계에서는 individual ECG words의 50%를 random masking한 뒤, mask된 위치의 collective ECG word index를 예측하도록 HeartLang을 학습한다.

공식 README 기준으로 MIMIC-IV preprocessing은 `mimic_preprocess.py`로 수행하고, ECG sentence generation은 [`QRSTokenizer.py`](https://github.com/PKUDigitalHealth/HeartLang/blob/main/QRSTokenizer.py)로 수행한다. 이후 VQ-HBR training은 [`scripts/vqhbr/MIMIC-IV.sh`](https://github.com/PKUDigitalHealth/HeartLang/tree/main/scripts/vqhbr), masked ECG sentence pre-training은 [`scripts/pretrain/MIMIC-IV.sh`](https://github.com/PKUDigitalHealth/HeartLang/tree/main/scripts/pretrain)을 통해 실행할 수 있다.

## Pre-training Dataset

| Dataset | Subjects | Sessions | Raw hours | #Samples after preprocessing | Rate (Hz) | Access |
|---------|----------|----------|-----------|------------------------------|-----------|--------|
| MIMIC-IV-ECG Diagnostic ECG Matched Subset | 161,352 | 논문에서 별도 명시 없음 | 약 2,222시간으로 계산 가능; 800,035 × 10초 기준 | 800,035 ECG sentences; 720,031 train + 80,004 valid | 500 → 100 | PhysioNet credentialed access → https://physionet.org/content/mimic-iv-ecg/ |

## Downstream datasets (informational — not used for pre-training)

HeartLang은 세 개의 public ECG datasets에서 여섯 개 benchmark setting으로 평가된다. 구체적으로 **PTB-XL Superclass**, **PTB-XL Subclass**, **PTB-XL Form**, **PTB-XL Rhythm**, **CPSC2018**, **Chapman-Shaoxing-Ningbo (CSN)**가 사용된다. 이 datasets는 HeartLang pre-training에는 사용되지 않고, linear probing과 downstream evaluation에 사용된다.

- **PTB-XL:** 18,885명의 patients로부터 수집된 21,837개의 12-lead ECG recordings로 구성된다. 각 recording은 500 Hz로 sampling되었고 길이는 10초이다. 평가 subset은 Superclass 5 classes, Subclass 23 classes, Form 19 classes, Rhythm 12 classes이다.
- **CPSC2018:** 6,877개의 12-lead ECG recordings로 구성된다. 각 recording은 500 Hz로 sampling되었으며, 길이는 6초에서 60초까지 다양하다. 총 9개 label을 사용한다.
- **CSN / Chapman-Shaoxing-Ningbo:** 원본 dataset은 45,152개의 12-lead ECG recordings로 구성된다. MERL 설정을 따라 “unknown” annotation이 있는 records를 제거한 뒤, 최종 benchmark에서는 23,026개의 ECG recordings와 38개 labels를 사용한다.

Downstream dataset preprocessing code는 [`datasets/dataset_preprocess`](https://github.com/PKUDigitalHealth/HeartLang/tree/main/datasets/dataset_preprocess)에 있고, fine-tuning scripts는 [`scripts/finetune`](https://github.com/PKUDigitalHealth/HeartLang/tree/main/scripts/finetune)에 있다.

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

