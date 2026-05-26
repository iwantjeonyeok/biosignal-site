 4.1.4. Normalization & Imputation

## Normalization

### 목적

ECG 신호의 진폭 범위는 기록 장비, 전극 위치, 환자의 신체 임피던스에 따라 크게 달라집니다. Normalization은 이러한 스케일 차이를 제거하여 신경망의 학습 안정성을 향상시킵니다.

### 주요 방법

**Z-score Normalization (표준화):**
$$x_{norm} = \frac{x - \mu}{\sigma}$$

평균을 0, 표준편차를 1로 변환합니다. 신경망 학습에 가장 널리 권장되며, 신호의 통계적 특성을 유지하면서 스케일을 정규화합니다.

**Min-Max Scaling (정규화):**
$$x_{norm} = \frac{x - x_{min}}{x_{max} - x_{min}}$$

신호를 [0, 1] 범위로 스케일합니다. 신호의 절대값 범위가 중요한 경우 유용하지만, 이상값(outlier)에 민감합니다.

arXiv의 "Exploring Best Practices for ECG Pre-Processing in Machine Learning"에 따르면, **Z-score normalization이 Min-Max 대비 ECG 학습에서 더 안정적인 수렴을 보입니다**. Lead 또는 환자별로 독립적으로 정규화하는 것이 표준 관행입니다.

## Imputation

### 결측 원인

결측 구간은 전극 탈락 또는 임피던스 급등으로 인한 포화(saturation) 구간, 피험자 움직임으로 인한 대용량 아티팩트 구간, 기기 오류 또는 데이터 저장 실패 등으로 발생합니다.

### 처리 방법

**Linear Interpolation (선형 보간)**
결측 구간의 시작과 끝값을 직선으로 연결합니다. 짧은 결측(수십 ms 이하)에 적합하며 계산이 빠릅니다.

**Polynomial Interpolation (다항 보간)**
주변 샘플들을 다항식으로 피팅하여 결측 구간을 채웁니다. 선형 보간보다 자연스럽지만, 고구간에서는 발진(overfitting)이 발생할 수 있습니다.

**Epoch Rejection (구간 제거)**
결측 또는 과도한 아티팩트가 포함된 에포크 전체를 학습에서 제거합니다. 결측 구간이 길거나 보정의 신뢰도가 낮을 때 가장 안정한 방법입니다.

**Masking (마스킹)**
Transformer 기반 모델에서는 결측 위치에 마스크 토큰을 부여하여 모델이 해당 위치를 무시하도록 학습합니다.
