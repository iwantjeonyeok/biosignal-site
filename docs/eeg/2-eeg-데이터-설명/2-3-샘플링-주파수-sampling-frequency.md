# 2.3. 샘플링 주파수 (Sampling Frequency)


EEG는 아날로그 전기 신호를 디지털 신호로 변환하여 저장하며, 이때 샘플링 주파수(Sampling Frequency)가 중요합니다. 이는 1초에 몇 번 EEG 신호를 측정할 것인지 나타내는 지표로, 단위는 Hz(헤르츠)입니다.

## Nyquist 정리와 최소 샘플링 요건

신호 이론의 기본 원리인 **Nyquist-Shannon 샘플링 정리**에 따르면, 어떤 주파수 성분을 정확히 재현하려면 해당 주파수의 **최소 2배** 이상으로 샘플링해야 합니다. 예를 들어 100 Hz까지 분석하려면 최소 200 Hz로 샘플링해야 합니다. 실제로는 앨리어싱(aliasing) 방지를 위해 목표 주파수의 2.5~3배를 권장하기도 합니다.

## 대역별 샘플링 주파수 특성

### **128–256 Hz**

- **적용 분야**: 상용 EEG 기기, 감정 인식, 피로도 측정, 수면 분석
- **설명**: Delta~Beta(~30 Hz) 대역 분석에 충분한 시간 해상도를 제공합니다. 예를 들어 DEAP 감정 인식 데이터셋은 원본 512 Hz를 128 Hz로 다운샘플링하여 배포합니다. 실시간 웨어러블 애플리케이션에서 연산 비용을 낮추면서도 충분한 성능을 낼 수 있습니다.

---

### **250–512 Hz**

- **적용 분야**: 간질 탐지(Seizure Detection), 일반 임상 EEG 기록
- **설명**: 임상 현장에서 가장 널리 사용되는 범위입니다. 250 Hz 기록에서 50 Hz로 다운샘플링해도 간질 분류 모델의 정확도가 크게 유지된다는 연구도 있으나, 일반적으로 250 Hz 이상을 권장합니다.[^1]

---

### **500–1000 Hz**

- **적용 분야**: ERP(Event-Related Potential) 분석, 병리적 신호 정밀 탐지
- **설명**: 수십 밀리초 단위로 나타나는 ERP 반응(P300, N200, ERN 등)을 정확히 포착하려면 높은 시간 해상도가 필요합니다. ERP 연구에서 500~1000 Hz로 수집 후 200~500 Hz로 다운샘플링하여 분석하는 방식이 일반적입니다.[^2]

---

### **1000 Hz 이상**

- **적용 분야**: 고주파 성분(High-Frequency Oscillation, HFO) 분석, EMG/잡음 분리
- **설명**: 80 Hz 이상의 HFO는 간질 병소와 밀접한 관련이 있어 이를 탐지하기 위해서는 2000 Hz 이상의 샘플링이 필요한 경우도 있습니다. 그러나 높은 샘플링은 데이터 용량 증가, 연산 비용 증가, 고주파 잡음 성분까지 함께 기록되는 단점이 있습니다.

## 높은 샘플링 주파수가 항상 좋은 것은 아니다

직관과 달리, 샘플링 주파수를 무조건 높이는 것이 항상 유리하지는 않습니다.

- **연산 비용**: 샘플링 주파수가 2배 늘면 데이터 크기와 처리 시간도 비례하여 증가
- **불필요한 노이즈 포함**: 고주파 잡음(근전도, 전극 노이즈 등)이 분석 대상과 함께 기록됨
- **모델 복잡도 증가**: 딥러닝 모델의 입력 시퀀스 길이가 길어져 학습이 어려워질 수 있음
- **불필요한 대역 포함**: 태스크에서 사용하지 않는 고주파 성분까지 포함되어 신호-잡음비(SNR) 저하 가능

따라서 **분석 목적에 따른 최적 샘플링 주파수를 선택**하는 것이 중요합니다.

## 태스크별 권장 샘플링 주파수

| 태스크 | 주요 분석 대역 | 권장 샘플링 주파수 |
|---|---|---|
| 수면 단계 분류 | Delta–Beta (0.5–30 Hz) | 128–256 Hz |
| 감정 인식 | Delta–Gamma (1–45 Hz) | 128–512 Hz |
| Motor Imagery BCI | Alpha–Beta (8–30 Hz) | 250–500 Hz |
| P300/ERP 분석 | 광대역 (0.1–40 Hz) | 500–1000 Hz |
| 간질(Seizure) 탐지 | Delta–Beta + HFO | 250–2000 Hz |
| HFO/고주파 분석 | Gamma 이상 (>80 Hz) | 1000 Hz 이상 |

---

[^1]: Leal, A., et al. (2023). Impact of EEG sampling frequency on the accuracy of automatic seizure detection and classification with deep learning algorithms. *Journal of the Neurological Sciences*. https://doi.org/10.1016/j.jns.2023.120609

[^2]: Pernet, C., et al. (2024). Ten quick tips for clinical electroencephalographic (EEG) data acquisition and signal processing. *PLOS Computational Biology*, 20(10). https://doi.org/10.1371/journal.pcbi.1012381
