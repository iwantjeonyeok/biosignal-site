# 3.2. 현재: 딥러닝 기반 EEG 분석 기술의 급속한 확산


딥러닝은 단순히 분류기를 교체한 것이 아니라, 전통 방식의 근본적인 병목인 수작업 특징 설계를 제거했습니다. 각 딥러닝 아키텍처는 EEG 신호의 특정 약점을 해결하기 위해 발전해왔습니다.

## 아키텍처별 EEG 문제 해결 전략

EEG 신호는 **시간 × 채널**의 2차원 구조를 가집니다. 어떤 차원에서 어떤 패턴을 추출하느냐에 따라 적합한 아키텍처가 달라집니다.

### CNN — 채널 간 공간 패턴 추출

EEG에서 "공간 패턴"이란 여러 채널에 걸쳐 동시에 나타나는 활성화 패턴을 의미합니다. 예를 들어 Motor Imagery에서 C3와 C4의 비대칭적 활성화 패턴이 전형적인 예입니다. CNN의 컨볼루션 연산은 이러한 채널 간 상관관계를 자동으로 학습합니다.

2018년 발표된 **EEGNet**은 CNN 기반 EEG 분석의 대표적 성과입니다. 깊이별 컨볼루션(Depthwise Convolution)과 분리 가능한 컨볼루션(Separable Convolution)을 사용하여 파라미터 수를 최소화하면서도 P300, Motor Imagery, ErrP 등 여러 BCI 패러다임에서 기존 방법과 동등하거나 우수한 성능을 보였습니다.[^1] 소규모 데이터셋에서도 과최적화 없이 작동하는 것이 주요 장점입니다.

### RNN / LSTM — 시간적 연속성 포착

전통적인 창(window) 기반 분석과 달리, RNN(Recurrent Neural Network)과 LSTM(Long Short-Term Memory)은 시퀀스 전체를 순서대로 처리하며 장기 의존성을 표현합니다. 수면 단계 분류나 발작 전조 신호 탐지처럼 수초~수분에 걸친 상태 전환을 추적하는 데 적합합니다. 다만 시퀀스가 길어질수록 기울기 소실(vanishing gradient) 문제가 발생할 수 있어, 이후 Transformer가 이를 보완하는 방향으로 발전했습니다.

### Transformer — 장거리 시간 의존성 처리

Transformer의 Self-Attention 메커니즘은 시퀀스 내 임의의 두 시점 간 관계를 직접 계산합니다. RNN이 순차적으로 정보를 전달하면서 먼 과거 정보를 희석시키는 것과 달리, Transformer는 시퀀스 전체를 한 번에 참조합니다. 이는 EEG에서 자극 제시 후 수백 밀리초에 걸쳐 전개되는 ERP 패턴이나, 장기적 뇌 상태 변화를 모델링하는 데 유리합니다.

### GNN — 채널 간 기능적 연결성 모델링

GNN(Graph Neural Network)은 EEG 채널을 그래프의 노드로 표현하고, 채널 간 기능적 연결성(Functional Connectivity)을 엣지로 모델링합니다. CNN이 전극의 물리적 근접성을 기반으로 패턴을 추출하는 데 반해, GNN은 공간적으로 멀리 떨어진 채널들 사이의 동기화 패턴도 포착할 수 있습니다. 간질 탐지처럼 뇌 네트워크 수준의 이상을 감지해야 하는 태스크에서 특히 효과적입니다.[^2]

## 아키텍처 선택 요약

| 아키텍처 | EEG에서 해결하는 문제 | 주요 활용 태스크 |
|---|---|---|
| **CNN** | 채널 간 공간 패턴, 주파수 특성 | Motor Imagery, ERP, Seizure |
| **RNN / LSTM** | 시간적 연속성, 상태 전환 추적 | Sleep Stage, Seizure |
| **Transformer** | 장거리 시간 의존성, 전역적 맥락 | ERP, Foundation Model 백본 |
| **GNN** | 채널 간 기능적 연결성 | Seizure, Mental Disorder |

## 응용 확장

딥러닝 기반 접근이 실제로 가져온 변화는 다음과 같습니다.

- **임상 정확도 향상**: 간질, ADHD, 우울증 등 질환 진단 모델에서 전통 방법 대비 성능 개선이 보고되고 있습니다.
- **수면 단계 자동화**: 딥러닝 기반 수면 단계 분류 모델들이 숙련된 임상가의 수동 분류 기준(AASM)에 근접한 일치도를 보이기 시작했습니다.
- **실시간 BCI 가능성**: P300, SSVEP, Motor Imagery 기반 BCI에서 낮은 지연 시간과 실용적 정확도를 달성하는 모델들이 등장했습니다.
- **웨어러블 확장**: 단일 채널 또는 소수 채널 EEG로도 실용적인 분류 성능을 달성하는 경량 모델 연구가 활발합니다.

---

[^1]: Lawhern, V.J., et al. (2018). EEGNet: A compact convolutional neural network for EEG-based brain–computer interfaces. *Journal of Neural Engineering*, 15(5), 056013. https://doi.org/10.1088/1741-2552/aace8c

[^2]: Klepl, D., et al. (2022). EEG-GNN: Graph neural networks for classification of electroencephalogram (EEG) signals. *IEEE Engineering in Medicine & Biology Society*. https://doi.org/10.1109/EMBC48229.2022.9871232
