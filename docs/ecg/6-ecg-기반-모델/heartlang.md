# HeartLang — ECG Language Model

> **Reading Your Heart: Learning ECG Words and Sentences via Pre-training ECG Language Model**
> Jiarui Jin, Haoyu Wang, Hongyan Li, Jun Li, Jiahui Pan, Shenda Hong. **ICLR 2025.**

- Paper (OpenReview): https://openreview.net/forum?id=6Hz1Ko087B
- Paper (arXiv): https://arxiv.org/abs/2502.10707
- Official code: https://github.com/PKUDigitalHealth/HeartLang
- Pre-trained checkpoints: https://huggingface.co/PKUDigitalHealth/HeartLang
- QRS-Tokenizer script: https://github.com/PKUDigitalHealth/HeartLang/blob/main/QRSTokenizer.py
- Downstream preprocessing scripts folder: https://github.com/PKUDigitalHealth/HeartLang/tree/main/datasets/dataset_preprocess

## Motivation

기존 ECG self-supervised learning(eSSL) 방법들은 ECG signal을 일반적인 time-series data처럼 다루며, **fixed-size and fixed-step time windows**로 신호를 분할하여 학습하는 방식이 대부분이다. 이 접근법은 ECG 신호가 가진 고유한 **형태(form)와 리듬(rhythm)** 특성, 그리고 heartbeat 간의 내재적 의미 관계를 무시한다는 한계가 있다.

HeartLang은 ECG signal을 하나의 언어처럼 해석한다는 새로운 관점을 제안한다. **heartbeats as words, rhythms as sentences**라는 비유를 바탕으로, 개별 heartbeat의 형태 정보와 heartbeat 시퀀스의 리듬 문맥을 함께 학습하는 framework를 구축하여, annotation 없이도 일반적이고 의미 있는 ECG 표현을 학습하는 것을 목표로 한다.

## Architecture Summary

HeartLang은 **두 단계의 self-supervised learning**으로 구성된다.

**Stage 1 — VQ-HBR (Vector-Quantized Heartbeat Reconstruction)**

- QRS-Tokenizer로 분할된 heartbeat patches를 **vector quantization**으로 collective ECG words에 mapping
- 8,192-entry codebook, 128-dimensional collective ECG words 사용
- 학습 후 validation set에서 실제 사용된 vocabulary: **5,394개의 discrete ECG words**
- 목적: 형태(form) 수준의 ECG vocabulary 구축

**Stage 2 — Masked ECG Sentence Pre-training**

- ECG sentence 내 individual ECG words의 **50%를 random masking**
- 마스킹된 위치의 collective ECG word index를 예측하도록 **Transformer 기반 모델** 학습
- 목적: 리듬(rhythm) 수준의 문맥 표현 학습

**QRS-Tokenizer**는 raw ECG signal에서 QRS complex를 검출하여 의미 단위로 segmentation을 수행하는 핵심 전처리 모듈이며, 이를 통해 역대 최대 규모의 **heartbeat 기반 ECG vocabulary**를 구축한다.

## Pre-training Data Summary

HeartLang은 대규모 임상 ECG 데이터베이스인 **MIMIC-IV-ECG**를 기반으로 사전학습된다. 학습 방식은 VQ-HBR과 masked ECG sentence pre-training의 두 단계로 구성된다.

- **Dataset**: MIMIC-IV-ECG Diagnostic Electrocardiogram Matched Subset
- **Raw scale**: 800,035개의 12-lead ECG recordings, 161,352명의 subjects, 각 recording은 10초 길이, sampling rate 500 Hz
- **After preprocessing**: 모든 ECG recording을 **100 Hz**로 downsample한 뒤, QRS-Tokenizer를 통해 ECG sentences로 변환
- **Dataset split**: **720,031 train ECGs** / **80,004 valid ECGs**
- **ECG sentence format**: 최대 sequence length **l = 256**, heartbeat window size **t = 96**, 12-lead에서 추출한 heartbeat words를 순서대로 연결

### Preprocessing procedure

1. MIMIC-IV-ECG에서 10초 길이의 12-lead ECG recordings 사용
2. `NaN`과 `Inf` 값을 주변 6개 포인트의 평균값으로 대체
3. 모든 ECG record를 **100 Hz**로 downsample
4. **QRS-Tokenizer** 적용: lead I signal에 **5–20 Hz band-pass filter** → Ricker wavelet 기반 moving wave integration → squared integration signal에서 local maxima 탐색 → QRS complexes 검출
5. 검출된 QRS index를 중심으로 heartbeat patch 분할. 각 lead별로 독립 segmentation, 인접 QRS index 사이의 midpoint를 interval boundary로 사용
6. Heartbeat interval이 **t = 96**보다 짧으면 zero-padding 적용
7. 12-lead heartbeat patches를 순서대로 연결해 ECG sentence 구성. 길이가 **l = 256**보다 짧으면 zero-filled patches 추가, 길면 l = 256까지만 사용
8. **VQ-HBR** 단계: individual ECG words를 vector quantization으로 collective ECG words에 mapping하고 heartbeat patches를 reconstruction하도록 학습
9. **Masked ECG sentence pre-training** 단계: individual ECG words의 50%를 random masking 후, 마스킹된 위치의 collective ECG word index를 예측하도록 학습

공식 README 기준으로 MIMIC-IV preprocessing은 `mimic_preprocess.py`로 수행하고, ECG sentence generation은 [`QRSTokenizer.py`](https://github.com/PKUDigitalHealth/HeartLang/blob/main/QRSTokenizer.py)로 수행한다.

### Pre-training Datasets

| Dataset | Subjects | Raw hours | #Samples after preprocessing | Rate (Hz) | Access |
|---------|----------|-----------|------------------------------|-----------|--------|
| MIMIC-IV-ECG Diagnostic ECG Matched Subset | 161,352명 | 약 2,222시간 (800,035 × 10초) | 800,035 ECG sentences (720,031 train / 80,004 valid) | 500 → 100 | PhysioNet credentialed access (무료) → https://physionet.org/content/mimic-iv-ecg/ |

## Downstream Datasets

HeartLang은 아래 세 개의 공개 ECG 데이터셋에서 여섯 가지 benchmark setting으로 평가된다. 이 데이터셋들은 사전학습에 사용되지 않고, linear probing 및 fine-tuning 평가에만 활용된다.

| Dataset | ECG 수 | Task | 비고 |
|---------|--------|------|------|
| PTB-XL (Superclass) | 21,837개 | 다중 레이블 분류 (5 classes) | 18,885명 환자, 500 Hz, 10초 |
| PTB-XL (Subclass) | 21,837개 | 다중 레이블 분류 (23 classes) | 동일 데이터셋, 세부 분류 |
| PTB-XL (Form) | 21,837개 | 다중 레이블 분류 (19 classes) | 동일 데이터셋, 형태 분류 |
| PTB-XL (Rhythm) | 21,837개 | 다중 레이블 분류 (12 classes) | 동일 데이터셋, 리듬 분류 |
| CPSC2018 | 6,877개 | 분류 (9 labels) | 500 Hz, 6~60초 |
| Chapman-Shaoxing-Ningbo (CSN) | 23,026개 | 분류 (38 labels) | 원본 45,152개에서 unknown 제거 후 |

Downstream dataset preprocessing code: [`datasets/dataset_preprocess`](https://github.com/PKUDigitalHealth/HeartLang/tree/main/datasets/dataset_preprocess)  
Fine-tuning scripts: [`scripts/finetune`](https://github.com/PKUDigitalHealth/HeartLang/tree/main/scripts/finetune)

## How to Reproduce the Pre-training Preprocessing

```bash
# 1) MIMIC-IV-ECG 접근 (PhysioNet credentialed access 필요, 무료)
#    https://physionet.org/content/mimic-iv-ecg/

# 2) HeartLang 클론
git clone https://github.com/PKUDigitalHealth/HeartLang.git
cd HeartLang

# 3) 환경 설정
conda create -n heartlang python=3.9
conda activate heartlang
pip install -r requirements.txt

# 4) MIMIC-IV-ECG 전처리
python mimic_preprocess.py \
  --dataset_path <path_to_MIMIC_data> \
  --output_path datasets/ecg_datasets/MIMIC-IV

# 5) QRS-Tokenizer로 ECG sentences 생성
python QRSTokenizer.py --dataset_name MIMIC-IV

# 6) VQ-HBR 학습 (ECG vocabulary 구축)
bash scripts/vqhbr/MIMIC-IV.sh

# 7) Masked ECG sentence pre-training 실행
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
