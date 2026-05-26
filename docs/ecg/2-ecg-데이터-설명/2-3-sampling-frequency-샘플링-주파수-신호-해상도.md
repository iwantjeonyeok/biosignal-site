# 2.3. 샘플링 주파수 (Sampling Frequency)
ECG는 아날로그 신호로 측정되며, 디지털 데이터로 변환하기 위해 일정 간격으로 **샘플링(Sampling)**됩니다. 샘플링 주파수는 **초당 몇 개의 샘플을 기록하는지**를 나타내며, 단위는 **Hz(헤르츠)**입니다.


## 샘플링 주파수별 특징

| 주파수 범위 | 임상 용도 | 장점 | 제한점 |
|-----------|---------|------|--------|
| **100~250 Hz** | 심박수 변이성(HRV) 분석, 웨어러블 | 저전력, 작은 데이터 크기 | 정밀한 파형 분석 제한 |
| **250~500 Hz** | P파, ST-분절 모니터링 | 좋은 신호 품질 | 중간 수준 저장 공간 |
| **500~1,000 Hz** | 표준 임상 진단 (병원용) | P-QRS-T 파형 정확 분석 | 중간 크기 데이터 |
| **≥1,000 Hz** | 연구 및 고주파 ECG | 최고 신호 해상도 | 큰 데이터 크기 |


## 임상 현황

### 표준 임상 가이드라인
- **병원 12-lead ECG**: 일반적으로 **500 Hz** 이상 사용
- **P-QRS-T 파형 분석**: **250~500 Hz** 권장
- **부정맥 감지**: **125~200 Hz**도 QRS 급격한 변화 포착 가능
- **연구 기기**: 대부분 **1,000 Hz** 이상 사용

### 실무 고려사항
샘플링 주파수가 **너무 낮으면**:
- P파의 미세한 시작점 놓침
- R파 피크 위치 오류 (심박수 변이성 분석 왜곡)
- 미세한 부정맥 패턴 미포착


## 데이터셋에서의 다양성

공개 ECG 데이터셋은 다양한 샘플링 주파수를 포함합니다:

- **임상 DB**: 500~1,000 Hz (표준화된 임상 기기)
- **웨어러블 DB**: 100~250 Hz (전력 효율 중심)
- **연구 DB**: 1,000 Hz 이상 (높은 정확도 필요)

머신러닝 모델 개발 시, 입력 신호의 샘플링 주파수가 다르면 **리샘플링(Resampling)** 전처리가 필수입니다.


## 참고 문헌

- [Electrocardiogram Sampling Frequency Range Acceptable for Heart Rate Variability Analysis - NCBI](https://pmc.ncbi.nlm.nih.gov/articles/PMC6085204/)
- [How High Should ECG Sampling Frequency Be for Accurate Results? - Fibion](https://web.fibion.com/articles/ecg-sampling-frequency-hrv-arrhythmia/)
- [Review High-frequency ECG - NASA Technical Reports](https://ntrs.nasa.gov/api/citations/20060056493/downloads/20060056493.pdf)
- [Nyquist Theorem - Advanced Neuroscience](https://uen.pressbooks.pub/advneuro/chapter/nyquist-theorem/)
