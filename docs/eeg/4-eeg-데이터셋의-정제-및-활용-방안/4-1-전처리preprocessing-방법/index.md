# 4.1. 전처리(Preprocessing) 방법

EEG 데이터는 센서 수, 샘플링 주파수, 기록 길이, 채널 배치 등에서 데이터셋마다 다양한 특성을 지니고 있습니다. 이러한 차이를 효과적으로 처리하기 위해 전처리(Preprocessing) 과정이 필수적이며, 주요 방법은 다음과 같습니다.

| 방법 | 설명 |
| --- | --- |
| [4.1.1 Sampling Frequency 및 Duration 통일](4-1-1-sampling-frequency-및-duration-통일.md) | 샘플링 주파수 및 기록 시간 표준화 |
| [4.1.2 채널 수(Lead) 차이에 따른 처리](4-1-2-채널-수lead-차이에-따른-처리.md) | 데이터셋 간 채널 수 차이 처리 |
| [4.1.3 Noise Filtering](4-1-3-noise-filtering.md) | 잡음 제거 필터링 기법 |
| [4.1.4 Normalization & Imputation](4-1-4-normalization-imputation.md) | 정규화 및 결측값 보완 |
