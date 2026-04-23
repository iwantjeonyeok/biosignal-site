# 2.5. Annotation (주석, 라벨링 정보)


AI 모델을 학습하기 위해 많은 ECG 데이터셋에는 다양한 주석 정보가 포함됩니다. 대표적인 주석 유형은 다음과 같습니다.

- **부정맥(Arrhythmia) 진단 레이블**
    - 정상 박동(Normal)
    - 심방세동(Atrial fibrillation, AF)
    - 심실빈맥(Ventricular tachycardia, VT)
    - 심방 조기 박동(Atrial premature contraction, APC)
    - 심실 조기 박동(Ventricular premature contraction, VPC)
- **박동(Beat) 유형 라벨링**
    - 개별 심장 박동에 대해 **정상(N), 조기 심실 수축(V), 심방 조기 수축(A)** 등으로 분류
- **ST 분절 및 QT 간격 이상**
    - **ST 상승(ST-elevation)**: 심근경색 가능성
    - **QT 연장(QT prolongation)**: 돌연사 위험 평가
- **리듬(Rhythm) 정보**
    - 정상 동리듬(Normal sinus rhythm, NSR)
    - 심방세동(Atrial fibrillation, AF)
    - 심실 빈맥(Ventricular tachycardia, VT)

이와 같은 공통적인 특성을 바탕으로 다양한 ECG 데이터셋이 존재하며, 각 데이터셋은 리드 개수, 측정 시간, 샘플링 주파수, 주석 유형 등에 따라 차이를 가집니다.
