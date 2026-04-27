# 4.1.3 Noise Filtering

EEG 신호는 근전도(EMG), 안구운동(EOG), 전극 접촉 잡음 등의 노이즈가 섞여 있어 필터링이 매우 중요합니다.

- **Bandpass Filter**: 일반적으로 0.5Hz~45Hz 범위의 뇌파 신호를 통과시키는 필터 적용
- **Notch Filter**: 전원 주파수 간섭(60Hz/50Hz)을 제거
- **ICA(Independent Component Analysis)**: 독립 성분 분석을 통한 아티팩트 제거
