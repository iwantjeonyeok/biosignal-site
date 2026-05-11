# ECGFounder — Electrocardiogram Foundation Model

> **An Electrocardiogram Foundation Model Built on over 10 Million Recordings with External Evaluation across Multiple Domains**  
> Jun Li, Aaron Aguirre, Junior Moura, Che Liu, Lanhai Zhong, Chenxi Sun, Gari Clifford, Brandon Westover, Shenda Hong.  
> **arXiv:2410.04133v4, 2025.08.04.**

- Paper: https://arxiv.org/abs/2410.04133
- Official code & model: https://github.com/PKUDigitalHealth/ECGFounder
- 핵심 모델명: **ECGFounder**
- 핵심 입력: **12-lead ECG 및 single-lead ECG**
- 핵심 목적: 대규모 임상 ECG와 전문가 annotation을 활용해 ECG 진단, 임상 사건 예측, demographic inference, PPG 기반 rhythm diagnosis까지 확장 가능한 범용 ECG foundation model 구축

## Training Data Summary

ECGFounder는 공개 ECG foundation model을 목표로, **Harvard-Emory ECG Database, HEEDB**를 기반으로 학습되었다. 논문 기준으로 HEEDB는 10,771,552개의 전문가 annotation ECG와 1,818,247명의 unique subjects를 포함하며, 대부분은 10초 길이의 12-lead clinical ECG이다.

- **Training / development corpus:** Harvard-Emory ECG Database, HEEDB
- **Raw scale:** 10,771,552 ECGs • 1,818,247 subjects
- **Final development set:** 7,519,035 ECGs • 1,319,128 patients
- **Internal test set:** 834,926 ECGs • 146,570 patients
- **Committee test set:** 523 ECGs • 523 patients
- **Label scale:** 전문가 annotation에서 추출한 287개 phrase를 검토하여 최종 **150개 meaningful ECG labels**로 정리
- **Model type:** Self-supervised pretraining이라기보다는, 전문가 annotation을 활용한 **large-scale supervised multi-label foundation model training**에 가깝다.

### Label processing and training strategy

ECGFounder의 중요한 특징은 실제 임상 annotation이 완전하지 않다는 점을 고려했다는 것이다. ECG 하나에 실제로 여러 진단 label이 존재할 수 있지만, 전문가 annotation에는 일부 label이 누락될 수 있다. 따라서 ECGFounder는 일반적인 single-label classification이 아니라 **multi-label classification**으로 학습되며, 누락된 label을 단순히 negative로 처리하지 않기 위해 **positive-unlabeled, PU learning** 관점을 도입한다.

1. ECG annotation의 discrete text report에서 정규표현식을 사용해 독립 phrase를 추출한다.
2. 287개 phrase 중 ECG 설명과 무관한 phrase를 제거한다.
3. 최종적으로 rhythm, morphology, diagnostic information을 포함하는 150개 label을 정의한다.
4. 누락 label 문제를 줄이기 위해 positive label augmentation / modified loss weighting을 적용한다.
5. Multi-label classification 방식으로 ECG representation과 diagnostic capability를 함께 학습한다.

### Preprocessing pipeline

논문에서 설명한 ECG 전처리 과정은 다음과 같다.

1. 읽을 수 없는 파일, 결측 데이터, 매칭되지 않는 데이터를 제거한다.
2. ECG sampling frequency를 **500 Hz**로 linear interpolation resampling한다.
3. Baseline drift를 줄이기 위해 **0.5 Hz high-pass filter**를 적용한다.
4. High-frequency noise를 줄이기 위해 **2nd-order 50 Hz Butterworth low-pass filter**를 적용한다.
5. Electrical interference 제거를 위해 **50/60 Hz notch filter**를 사용한다.
6. 10초보다 긴 ECG는 순서대로 **10-second windows**로 자른다.
7. 10초보다 짧은 ECG는 **zero padding**을 적용한다.
8. 각 signal segment의 mean과 standard deviation을 사용해 normalize한 뒤 모델 입력으로 사용한다.

## Model Architecture

ECGFounder는 ECG에 맞춘 **Net1D 기반 architecture**를 사용하며, Net1D는 **RegNet** 계열 구조를 기반으로 한다. ECG는 시간축 정보뿐 아니라 lead 간 공간적 관계도 중요하기 때문에, 모델은 temporal information과 spatial relationship을 함께 학습하도록 설계되었다.

- **Backbone:** Net1D
- **Architecture basis:** RegNet / stage-wise network design
- **Input:** 12-lead ECG 또는 single-lead ECG
- **Core design:** depth가 깊어질수록 block 수와 channel 수가 조정되는 stage-wise 구조
- **Representation learning focus:** ECG waveform의 temporal pattern + lead 간 spatial relationship
- **Block characteristics:** group convolution과 channel-wise attention mechanism을 포함한 bottleneck blocks
- **목표:** 다양한 ECG 길이, lead 누락, single-lead 상황에서도 일반화 가능한 ECG representation 학습

## Training Details

ECGFounder의 학습은 실제 임상 annotation의 특성, 즉 noisy annotation, class imbalance, missing labels를 고려해 설계되었다.

| 항목 | 내용 |
|---|---|
| Training objective | Multi-label ECG diagnosis |
| Label categories | 150 ECG diagnostic / rhythm / morphology labels |
| Missing label handling | Positive-unlabeled learning 관점 도입 |
| Loss strategy | Missing positive label의 영향을 줄이기 위한 modified multi-label loss |
| Hyperparameter | γ = 1.5 |
| Optimizer | AdamW |
| Initial learning rate | 0.001 |
| LR decay | 5 epochs마다 10배 감소 |
| Batch size | 1024 |
| Max epochs | 20 epochs |
| Early stopping | Validation loss 기준 |

## Single-lead ECG Model

ECGFounder는 12-lead ECG뿐 아니라 wearable device나 mobile monitoring 환경에서 자주 사용되는 **single-lead ECG**에도 적용될 수 있도록 별도의 lead augmentation 전략을 사용한다.

논문에서는 lead I을 중심축, 즉 0°로 보고, limb lead의 전기축 관계를 이용해 추가적인 lead 정보를 구성한다.

- 기본 single-lead 입력: **lead I**
- 추가적으로 활용한 augmented leads: `aVL`, `-aVR`, `II`, `-III`, `aVF`, `-aVF`
- 학습 방식: HEEDB의 12-lead ECG에서 lead I을 추출하고, 50% 확률로 나머지 augmented lead 중 하나를 함께 넣어 학습
- 목적: single-lead ECG에서도 arrhythmia뿐 아니라 axis deviation 관련 정보를 더 잘 학습하도록 함
- 적용 맥락: wearable ECG device에서 업로드된 ECG를 cloud-based system에서 분석하는 방식

## Training / Validation Dataset

| Dataset | Purpose | Scale | Notes |
|---|---:|---:|---|
| HEEDB | Main training / development | 10,771,552 ECGs • 1,818,247 subjects | 전문가 annotation 기반 대규모 ECG database |
| Development set | Model development | 7,519,035 ECGs • 1,319,128 patients | HEEDB에서 구성 |
| Internal test set | Internal validation | 834,926 ECGs • 146,570 patients | HEEDB에서 구성 |
| Committee test set | Expert comparison | 523 ECGs • 523 patients | ECG cardiologist committee annotation 사용 |
| CODE-test | External 12-lead validation | 827 ECGs • 827 patients | Brazil TNMG 기반, 6개 common arrhythmia labels |
| PTB-XL | External 12-lead validation | 21,837 ECGs • 18,885 patients | Germany clinical ECG dataset |
| PhysioNet Challenge 2017 | External single-lead validation | 3,658 test ECGs | AliveCor single-lead ECG, rhythm classification |

## Downstream datasets

ECGFounder는 단순 ECG diagnosis만이 아니라, 다양한 downstream task에 fine-tuning되어 평가되었다.

| Dataset | Purpose | Scale |
|---|---|---:|
| MIMIC-IV-ECG | Age / sex / CKD / CHD / LVEF / NT-proBNP 등 downstream tasks | 800,035 ECGs • 161,352 patients |
| MIMIC-ECG-Age | Age regression / age classification | 800,035 ECGs |
| MIMIC-ECG-Sex | Sex classification | 800,035 ECGs |
| MIMIC-ECG-CKD | Chronic kidney disease detection | 266,876 ECGs |
| MIMIC-ECG-CHD | Chronic heart disease detection | 266,876 ECGs |
| MIMIC-ECG-LVEF | LVEF regression / abnormal classification | 75,413 ECGs |
| MIMIC-ECG-NTproBNP | NT-proBNP regression / abnormal classification | 58,861 ECGs |
| DeepBeat-PPG | Cross-modality AF detection | 536,399 PPGs • 132 patients |

## Downstream tasks

논문에서 ECGFounder는 총 12개 clinical downstream task에 적용되었다.

- **ECG diagnosis**
  - 12-lead ECG diagnosis
  - 1-lead ECG diagnosis
- **Demographics detection**
  - Age regression
  - Age > 65 classification
  - Sex classification
- **Clinical event detection**
  - CKD detection
  - CHD detection
  - LVEF regression
  - Abnormal LVEF classification
  - NT-proBNP regression
  - Abnormal NT-proBNP classification
- **Cross-modality diagnosis**
  - PPG signal 기반 atrial fibrillation detection

## Fine-tuning protocol

ECGFounder는 downstream task에 맞게 classification head를 교체한 뒤 fine-tuning된다.

1. Base model의 pretrained parameters를 유지한다.
2. 기존 classification linear layer를 제거한다.
3. Downstream task의 class 수에 맞는 새로운 linear classification head를 추가한다.
4. 두 가지 방식으로 평가한다.
   - **Linear probing:** backbone은 freeze하고 linear head만 학습
   - **Full fine-tuning:** backbone까지 전체 parameter를 업데이트
5. 총 30 epochs 동안 학습한다.
6. Validation metric이 10 epochs 동안 개선되지 않으면 learning rate를 0.1배로 줄인다.
7. Validation set에서 가장 높은 AUC를 보인 checkpoint를 저장한다.

## Key Results

ECGFounder는 internal validation과 external validation 모두에서 강한 성능을 보였다.

- Internal 12-lead validation에서 **80개 diagnosis에 대해 AUROC > 0.95** 달성
- Committee test set의 20개 classification 기준 평균 성능:
  - **AUROC 0.968**
  - **Sensitivity 0.971**
  - **Specificity 0.937**
- Cardiologist comparison에서 ECGFounder 평균 F1은 **0.677**, cardiologist 평균 F1은 **0.640**
- External CODE-test에서 평균 **AUROC 0.981**
- External PTB-XL에서 평균 **AUROC 0.924**
- Single-lead ECG external test에서:
  - Normal sinus rhythm AUROC **0.975**
  - Atrial fibrillation AUROC **0.957**
- MIMIC-IV-ECG downstream tasks에서 baseline model보다 전반적으로 높은 성능을 보임
- Age, sex, NT-proBNP, LVEF, CKD, CHD detection에서 ECG-SimCLR 및 ECG-ResNet 계열 baseline보다 높은 AUROC를 보임

## How to reproduce / use

논문은 code와 model이 공식 GitHub에 공개되어 있다고 명시한다. 단, 실제 실행 방법은 GitHub repository의 최신 README와 checkpoint 제공 방식을 확인해야 한다.

```bash
# 1) Clone ECGFounder official repository
git clone https://github.com/PKUDigitalHealth/ECGFounder
cd ECGFounder

# 2) Install dependencies
# 정확한 dependency 설치 방식은 repository README를 확인해야 함
pip install -r requirements.txt

# 3) Prepare ECG data
# 논문 기준 전처리: 500 Hz resampling, filtering, 10-second windowing, zero padding, normalization

# 4) Load pretrained ECGFounder checkpoint
# checkpoint 경로와 사용법은 repository README 기준으로 확인

# 5) Run inference or fine-tuning
# 12-lead ECG diagnosis, single-lead ECG diagnosis, downstream fine-tuning 등에 활용 가능
```

## Notes for comparison / baseline use

ECGFounder를 ECG foundation model 비교군으로 사용할 때는 다음 점을 주의해야 한다.

- 이 모델은 self-supervised ECG foundation model이라기보다, 대규모 전문가 annotation을 활용한 supervised multi-label foundation model에 가깝다.
- 학습 데이터 규모는 매우 크지만, 주요 개발 데이터가 미국 cohort에 기반하므로 지역, 인종, 병원 환경이 다른 데이터에서의 일반화는 별도 검증이 필요하다.
- Single-lead ECG 성능은 lead augmentation 전략에 의해 강화되었지만, 실제 wearable device 내부에서 직접 실행되는 모델이라기보다는 cloud-based analysis를 전제로 한다.
- 논문은 code와 model 공개를 명시하지만, 실제 checkpoint 다운로드 가능 여부와 inference pipeline의 사용성은 repository에서 직접 확인해야 한다.
- Downstream task 성능 비교 시, ECGFounder가 HEEDB와 MIMIC-IV-ECG처럼 매우 큰 임상 데이터를 활용했다는 점을 고려해야 한다.

## Citation

```bibtex
@article{li2025ecgfounder,
  title={An Electrocardiogram Foundation Model Built on over 10 Million Recordings with External Evaluation across Multiple Domains},
  author={Li, Jun and Aguirre, Aaron and Moura, Junior and Liu, Che and Zhong, Lanhai and Sun, Chenxi and Clifford, Gari and Westover, Brandon and Hong, Shenda},
  journal={arXiv preprint arXiv:2410.04133},
  year={2025}
}
```


