# 4.1.3. Noise Filtering

원본 ECG 신호는 전극 접촉 불량, 근육 움직임(motion artifact), 전력선 간섭(50/60Hz), 기저선 이동(baseline wander) 등 다양한 노이즈를 포함합니다. 이러한 노이즈는 모델의 학습을 방해하고 진단 정확도를 저하시키므로 제거가 필수적입니다.



## Bandpass Filtering

ECG 신호의 진단 정보는 0.5Hz~40Hz 범위에 집중되어 있습니다. **Bandpass filter**는 이 범위만 통과시키고 나머지 주파수 성분을 감쇠시킵니다.

Butterworth filter는 ECG 필터링에 가장 널리 사용되는 방식으로, 통과 대역에서 매끄러운 응답을 제공하며 높은 주파수 노이즈와 DC 노이즈를 효과적으로 제거합니다. 5차 Butterworth bandpass filter (0.5Hz~40Hz)가 임상 표준이며, Chebyshev filter 대비 신호의 부드러움과 정확성 간 더 나은 균형을 제공합니다.

**필터 특성:**
- 저주파 차단: 기저선 이동 제거 (0.5Hz 이상)
- 고주파 차단: 근육 떨림, 전자 기기 노이즈 제거 (40Hz 이상)
- 통과 대역: QRS, T파, P파 정보 보존
  

## Adaptive Filtering

신호 특성이 시간에 따라 변할 때 고정 필터의 효과가 제한됩니다. **Adaptive filter**는 신호 통계에 기반해 실시간으로 필터 계수를 조정합니다.

최소 평균제곱(LMS, Least Mean Square) 알고리즘이 적응형 필터링에 널리 사용되며, 기저선 이동이나 운동 아티팩트 같은 시변(time-varying) 노이즈를 동적으로 추정하고 제거합니다. 특히 Holter 모니터링이나 웨어러블 기기처럼 환자 움직임이 많은 환경에서 고정 필터보다 우수한 성능을 보입니다.



## Wavelet Denoising

Wavelet 변환은 신호를 시간-주파수 영역으로 분해하여 노이즈만 선택적으로 제거할 수 있습니다. 이산 웨이블릿 변환(DWT)을 이용해 신호를 decompose하고, 노이즈 계수를 threshold 처리(shrinkage)로 억제한 후 역변환합니다.

Discrete Wavelet Denoising은 신호의 세부 특징을 보존하면서 광대역 노이즈를 효과적으로 제거하여, 특히 고주파 아티팩트가 많은 데이터에 효과적입니다.


