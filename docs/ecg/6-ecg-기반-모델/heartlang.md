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

기존 ECG 기반 딥러닝 모델은 대규모 고품질 라벨 데이터에 의존하며, 특정 데이터셋과 과제에 맞춰 설계되는 경우가 많아 새로운 임상 과제에 일반화하는 데 한계가 있다. 이를 해결하기 위해 ECG 자기지도학습이 발전해왔지만, 대부분의 기존 방법은 ECG를 일반적인 시계열 데이터처럼 취급하여 고정된 크기와 간격으로 신호를 분할한다. 이러한 방식은 ECG의 핵심적인 특성인 개별 심박의 형태 정보와 전체 심장 리듬의 흐름을 충분히 반영하지 못하며, 심박 사이에 존재할 수 있는 잠재적 의미 관계도 약화시킬 수 있다. 특히 ECG 진단에서는 단일 심박의 형태 변화와 여러 심박이 만드는 리듬 패턴이 모두 중요하기 때문에, ECG 신호의 고유한 구조를 반영한 표현학습 방식이 필요하다. HeartLang은 이러한 한계를 해결하기 위해 심박 단위와 리듬 단위를 중심으로 ECG를 재구성하고, 라벨 없이도 심박의 형태 수준 표현과 리듬 수준 표현을 함께 학습하는 새로운 ECG 자기지도학습 프레임워크를 제안한다.

## Architecture Summary

HeartLang은 세 가지 핵심 설계를 통해 위의 문제를 해결한다.

첫째, **QRS-Tokenizer**가 10초 길이의 multi-lead ECG segment에서 QRS complex를 검출하고, 이를 기준으로 각 lead의 심박 구간을 분할한다. 이렇게 얻은 개별 심박 조각은 individual ECG word로 간주되며, 12-lead에서 추출된 ECG word들을 순서대로 연결해 하나의 ECG sentence를 구성한다. 심박수 차이로 인해 문장 길이가 달라지는 문제는 padding과 truncation으로 처리한다.

둘째, **ST-ECGFormer**는 생성된 ECG sentence를 입력받아 ECG word의 표현을 학습하는 Transformer 기반 backbone이다. 각 ECG word는 token embedding으로 변환되고, 여기에 lead 정보를 반영하는 spatial embedding, 시간 구간 정보를 반영하는 temporal embedding, 문장 내 순서를 반영하는 position embedding이 더해진다. 이를 통해 모델은 개별 심박의 파형뿐 아니라, 해당 심박이 어느 lead와 시간 위치에서 나타났는지도 함께 고려한다.

셋째, **ECG vocabulary**는 개별 ECG word를 더 일반화된 collective ECG word로 매핑하기 위해 사용된다. HeartLang은 한쪽 흐름에서는 ECG vocabulary를 통해 얻은 collective ECG word를 decoder로 복원하며 심박의 형태 정보를 학습하고, 다른 흐름에서는 일부 ECG word가 가려진 ECG sentence를 입력받아 해당 위치의 collective ECG word index를 예측한다. 이를 통해 심박의 형태적 의미와 ECG sentence 안에서의 리듬적 문맥 관계를 함께 학습하도록 설계된다.

전체적으로 HeartLang은 QRS-Tokenizer로 ECG sentence를 만들고, ST-ECGFormer로 시공간 정보를 반영하며, ECG vocabulary 기반 복원과 예측 구조를 통해 심박 형태와 리듬 문맥을 함께 학습하는 프레임워크이다.

## Pre-training Data Summary
HeartLang은 MIMIC-IV-ECG를 사용하여 VQ-HBR training과 masked ECG sentence pre-training을 수행한다.

**데이터셋**: MIMIC-IV-ECG
**원시 규모:** 161,352명 피험자 · 800,035개 12-lead ECG recording
**신호 형식:** 500 Hz · 10초 길이 · 12-lead ECG
**사용 목적:** VQ-HBR training 및 masked ECG sentence pre-training
**특징:** ECG recording만 사용하며, clinical report text supervision은 사용하지 않음

### Preprocessing procedure


1. MIMIC-IV-ECG의 raw ECG recording에서 `NaN`과 `Inf` 값은 주변 6개 point의 평균값으로 대체한다.
2. 모든 ECG recording을 500 Hz에서 **100 Hz**로 downsampling한다.
3. **QRS-Tokenizer**를 사용하여 raw ECG recording을 통일된 ECG sentence 형태로 변환한다.
4. QRS detection을 위해 lead I 신호에 **5–20 Hz band-pass filter**를 적용하고, Ricker wavelet 기반 moving wave integration을 수행한다.
5. moving wave integration signal의 local maxima를 탐색하여, refractory period 이후에 QRS detection threshold를 넘는 지점을 QRS complex로 판정한다.
6. 검출된 QRS complex index를 중심으로 각 lead의 심박 구간을 분할한다. 분할된 구간이 time window size인 **t = 96**보다 짧으면 zero padding을 적용한다.
7. 12-lead에서 추출된 개별 심박 조각을 순서대로 연결해 ECG sentence를 구성한다. 논문에서는 ECG sentence의 최대 길이를 **l = 256**, 각 ECG word의 time window size를 **t = 96**으로 설정한다.
8. 문장 길이가 **l**보다 짧으면 zero-filled patch로 padding하고, **l**보다 길면 truncation한다.

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
