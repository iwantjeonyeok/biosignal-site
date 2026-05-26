# 4.1. 전처리(Preprocessing) 방법


EEG 데이터는 수집 목적, 장비, 연구 환경에 따라 샘플링 주파수, 채널 수, 기록 길이가 데이터셋마다 제각각입니다. 여러 데이터셋을 통합하여 단일 모델에 활용하거나 일반화 성능을 높이려면, 이 이질성(heterogeneity)을 제거하는 전처리 과정이 필수적입니다.

전처리는 단순히 입력 형태를 통일하는 것을 넘어, 신호에 섞인 아티팩트를 제거하고 피험자 간 진폭 차이를 보정하여 **모델이 뇌 신호의 의미 있는 패턴에 집중할 수 있도록** 만드는 과정입니다. 잘못된 전처리는 아티팩트를 학습 대상으로 오인하게 만들고, 부정확한 정규화는 특정 피험자 데이터가 모델을 지배하게 만들 수 있습니다.

주요 전처리 단계는 다음과 같습니다.

[4.1.1 Sampling Frequency 및 Duration 통일](4-1-1-sampling-frequency-및-duration-통일.md) — 리샘플링, 윈도잉, 에포킹을 통해 입력 형태 통일

[4.1.2 채널 수(Lead) 차이에 따른 처리](4-1-2-채널-수lead-차이에-따른-처리.md) — 공통 채널 추출, 구면 스플라인 보간, 채널 위치 임베딩

[4.1.3 Noise Filtering](4-1-3-noise-filtering.md) — Bandpass/Notch 필터, ICA를 통한 EOG·EMG·ECG 아티팩트 제거

[4.1.4 Normalization & Imputation](4-1-4-normalization-imputation.md) — Z-score/Min-Max 정규화, 결측 구간 보간 또는 에포크 제거
