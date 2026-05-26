# 4.1.1. Sampling Frequency 및 Duration 통일

## 개요

ECG 신호는 다양한 의료 기기와 임상 환경에서 수집되기 때문에 sampling frequency(샘플링 주파수)와 recording duration(기록 길이)이 불균일합니다. AI 모델 학습을 위해서는 모든 ECG 신호를 동일한 샘플링 주파수와 길이로 표준화하는 것이 필수적입니다. 이 과정을 거쳐야 모델의 일관성 있는 성능과 일반화 능력이 보장됩니다.

---

## 1. Sampling Frequency 표준화

### 1.1 표준 Sampling Frequency 선택

ECG 신호의 샘플링 주파수는 250Hz, 300Hz, 500Hz 등으로 다양하게 기록됩니다. 최근 연구에 따르면, **딥러닝 기반 ECG 분석에서는 100Hz에서 500Hz 범위의 샘플링 주파수로도 효과적인 결과를 얻을 수 있습니다**.

**권장 샘플링 주파수 선택 기준:**

| 주파수 | 용도 | 장점 | 단점 |
|--------|------|------|------|
| **100 Hz** | 실시간 모니터링, 모바일 장치 | 데이터 용량 최소화, 계산량 감소 | QRS 복합파 세부 정보 손실 가능 |
| **250 Hz** | 임상 표준 (Holter, 일반 ECG) | 임상 표준, 충분한 정보 보존 | 중간 수준의 데이터 용량 |
| **500 Hz** | 고정밀 분석, 연구용 | QRS 및 미세한 파형 정보 보존 | 높은 계산 비용 및 메모리 요구 |

최근 arXiv 논문 "Sampling Matters: The Effect of ECG Frequency on Deep Learning-Based Atrial Fibrillation Detection"의 연구 결과에 따르면, **CNN 기반 딥러닝 모델은 100Hz 또는 250Hz에서도 높은 탐지 정확도를 유지하면서 모델의 복잡도를 크게 감소시킬 수 있습니다**. 따라서 250Hz를 표준 샘플링 주파수로 선택하는 것이 임상적 정확성과 계산 효율성 간의 최적 균형을 제공합니다.

### 1.2 Resampling 기법

원본 샘플링 주파수가 목표 주파수와 다를 경우, resampling을 통해 신호를 변환합니다.

**Upsampling (샘플링 주파수 상향):**
- 목표 주파수가 원본보다 높을 경우 적용
- Interpolation 기법을 사용하여 새로운 샘플 포인트 생성
- **선형 보간(Linear Interpolation)**: 빠르고 간단, 일반적 용도
- **3차 스플라인 보간(Cubic Spline Interpolation)**: 더 부드러운 신호 재구성, 고정밀도 필요 시

**Downsampling (샘플링 주파수 하향):**
- 목표 주파수가 원본보다 낮을 경우 적용
- 샘플링 전에 반드시 Anti-aliasing filter 적용 필요 (일반적으로 Butterworth low-pass filter)
- Nyquist 정리(Nyquist theorem)를 위반하면 aliasing artifact 발생 위험

**수식:**
$$f_{target} = f_{original} \times \frac{N_{target}}{N_{original}}$$

여기서 $f$는 주파수, $N$은 샘플 개수입니다.

---

## 2. Duration (길이) 표준화

### 2.1 고정 길이 Segmentation

ECG 신호의 기록 길이가 다양하므로 (예: 10초~24시간), 고정된 길이로 분할하여 일관된 입력 차원을 갖도록 합니다.

**고정 길이 선택 기준:**

- **10초**: 신속한 부정맥 감지 필요 (응급 상황)
- **30초**: 일반적인 표준 ECG 기록 길이, 대부분의 모델에서 권장
- **2~5분**: 더 긴 리듬 패턴 분석, Holter 모니터링 분석

250Hz 표준화를 기준으로, 30초 고정 길이는 **7,500개의 샘플 포인트(250 × 30 = 7,500)**를 생성합니다. 이는 계산 비용과 정보 보존 간의 최적 균형으로 널리 권장됩니다.

### 2.2 Uniform Segmenting (균등 분할)

30초 이상의 장시간 기록에서는 균등 분할(uniform segmentation)을 적용합니다:

$$\text{Number of Segments} = \frac{\text{Total Duration}}{\text{Segment Length}}$$

예를 들어, 60초 기록을 30초 세그먼트로 나누면:
$$\frac{60\text{s}}{30\text{s}} = 2 \text{ segments}$$

각 세그먼트는 독립적인 학습 샘플로 취급되어 데이터셋 증강 효과를 제공합니다. **Scientific Reports에 발표된 "Beat-wise segmentation of electrocardiogram using adaptive windowing and deep neural network" 연구에서는 적응형 윈도우 기법을 통해 QRS 복합파를 중심으로 한 동적 분할이 가능함을 보였습니다**.

---

## 3. Zero Padding (패딩)

### 3.1 Zero Padding의 필요성

고정 길이보다 짧은 신호는 0을 추가하여 길이를 맞춥니다. 이를 **zero padding**이라 합니다.

예를 들어:
- 목표 길이: 250 Hz × 30초 = **7,500 샘플**
- 실제 신호 길이: 6,200 샘플
- 필요한 padding: 7,500 - 6,200 = **1,300개 0 추가**

### 3.2 Zero Padding의 영향

**장점:**
- 모든 신호를 균일한 차원으로 표준화
- 신경망의 입력 텐서 형태 고정

**주의사항:**
- 과도한 padding (>20% 신호 길이)은 모델 학습에 부정적 영향
- Padding 위치 (선행 vs. 후행): 후행 padding 권장 (신호 정보 우선 보존)
