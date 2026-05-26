# 2.5. 다운스트림 태스크 설명 (Downstream Task)


EEG 기반 연구에서 사용되는 다운스트림 태스크는 목적에 따라 크게 세 가지 범주로 분류할 수 있습니다.

| 범주 | 대표 태스크 | 핵심 특성 |
|---|---|---|
| **임상·진단** | Seizure Detection, Abnormal Detection, Sleep Stage, Mental Disorder | 병리적 패턴 탐지, 임상 의사결정 보조 |
| **BCI·인터랙션** | Motor Imagery, P300 Speller, ErrP Detection, Imagined Speech, Gait Prediction | 사용자 의도 해독, 실시간 제어 |
| **인지·감정 분석** | Emotion Recognition, Mental/Cognitive Workload, Vigilance Estimation, Galvanic Response | 정신 상태 정량화, HCI |

---

## 임상·진단 태스크

### **1) Seizure Detection**

- **정의**: EEG에서 간질(발작) 여부를 탐지하는 과제
- **분야**: 임상진단, 실시간 경보, 신경 자극 제어
- **특징**: Spike, sharp wave, burst-suppression 등 발작 관련 뇌파 패턴을 포착하여 조기 경고에 활용합니다. 발작 패턴은 수 초에서 수 분에 걸쳐 나타나며, 시작 부위에 따라 파형 형태가 다양합니다.

---

### **4) Abnormal Detection**

- **정의**: EEG 내에서 병리적으로 비정상적인 신호를 자동으로 탐지하는 과제
- **분야**: 신경 질환 조기 진단, EEG 데이터 품질 관리
- **특징**: 비정상 spike-wave, burst, 서파 활동 등 다양한 이상 패턴을 분류합니다. 정상 EEG와의 이진 분류 문제로 구성되는 경우가 많으며, TUAB(Temple University Abnormal EEG Corpus) 같은 대규모 임상 데이터셋이 벤치마크로 활용됩니다.

---

### **9) Mental Disorder Diagnosis**

- **정의**: 우울증, 조현병, ADHD 등 정신질환의 유무나 정도를 EEG로 분류
- **분야**: 정신과 진단 보조, 뇌 기반 생체표지자(Biomarker) 탐색
- **특징**: 연결성 약화, 비선형성, 복잡도 저하 등 비정상 패턴을 탐지합니다. 기존 임상 진단과 달리 객관적 신호 기반 보조 도구로서의 가능성이 연구되고 있으며, 개인 간 변이가 커서 높은 난이도의 과제입니다.

---

### **11) Sleep Stage Detection**

- **정의**: EEG로 수면 단계를 자동으로 분류하는 과제 (Wake, N1, N2, N3, REM)
- **분야**: 수면장애 진단, 수면 질 평가, 수면 모니터링
- **특징**: 수면 단계별로 고유한 주파수 패턴이 나타납니다. N2에서는 수면 방추(Sleep Spindle, 11–16 Hz, 주로 12–14 Hz)와 K-complex가 특징적이며, N3(서파수면)에서는 0.5–2 Hz의 고진폭(>75 μV) Delta파가 에포크의 20% 이상을 차지합니다. REM에서는 낮은 진폭의 혼합 주파수 패턴과 급속 안구운동이 관찰됩니다. 미국수면의학회(AASM)는 30초 에포크 단위로 수면 단계를 분류하는 기준을 표준화했으며, 이것이 자동화 모델의 골드 스탠더드로 사용됩니다.[^3]

---

## BCI·인터랙션 태스크

### **10) Motor Imagery Classification**

- **정의**: 움직임을 실제로 하지 않고 상상만 했을 때의 뇌파를 분류하는 과제
- **분야**: 뇌-컴퓨터 인터페이스(BCI), 재활 로봇, 의수·외골격 제어
- **특징**: 운동 피질의 Sensorimotor Rhythm이 변화하는 패턴(ERD/ERS)을 분석합니다. 손, 발, 혀 등을 상상할 때 해당 운동 피질의 Mu(8–12 Hz) 및 Beta(13–30 Hz) 리듬이 억제(ERD)되고, 동작 완료 후 회복(ERS)되는 패턴이 핵심 특징입니다.

---

### **12) P300 Speller**

- **정의**: 사용자가 주목한 자극에 대한 P300 반응을 탐지하여 문자를 입력하는 시스템
- **분야**: 전신 마비/ALS 환자 의사소통 보조
- **특징**: P300은 목표 자극 제시 후 약 250–500 ms 사이에 나타나는 양의 전위(positive deflection)로, 특히 두정엽(P3, Pz, P4)에서 강하게 관찰됩니다.[^1] 다수의 자극 중 사용자가 주목한 자극에만 P300이 유발되는 odd-ball 패러다임을 이용합니다.

---

### **7) Error-Related Potentials (ErrP) Detection**

- **정의**: 사용자 또는 시스템이 오류를 범했을 때 발생하는 ERP를 탐지하는 과제
- **분야**: BCI 보정, 인간-로봇 상호작용 오류 감지
- **특징**: ErrP는 크게 두 성분으로 구성됩니다. 오류 반응 직후(약 50–150 ms) 전두중심부(FCz)에서 나타나는 **ERN(Error-Related Negativity, 또는 Ne)**과, 이후 200–400 ms에 나타나는 양의 성분인 **Pe(Error Positivity)**입니다.[^2] BCI 피드백 맥락에서는 피드백 후 200–300 ms에 FRN(Feedback-Related Negativity)이 관찰되기도 합니다. 이 신호를 실시간으로 탐지하면 BCI 시스템이 스스로 오류를 인식하고 보정할 수 있습니다.

---

### **14) Imagined Speech Classification**

- **정의**: 발화 없이 머릿속에서 상상한 단어나 문장을 EEG로 분류하는 과제
- **분야**: Silent Speech BCI, 무언어 커뮤니케이션 시스템
- **특징**: 유발되는 ERP가 매우 약하고 개인차가 크기 때문에 고난이도 과제입니다. 현재 연구에서는 단어 수준 분류도 아직 도전적인 과제로 남아 있습니다.

---

### **15) Gait Prediction**

- **정의**: EEG로 보행 의도, 리듬, 속도 등을 예측하는 과제
- **분야**: 외골격 로봇 제어, 재활 보조 시스템, 보행 피드백
- **특징**: MRCP(Movement-Related Cortical Potential)는 보행 시작 약 1–2초 전부터 발생하기 시작하여 운동 직전에 피크에 도달합니다. 이를 선제적으로 탐지하면 외골격 로봇을 의도 발생 시점에 맞춰 제어하는 데 활용할 수 있습니다.

---

## 인지·감정 분석 태스크

### **6) Emotion Recognition**

- **정의**: EEG를 이용해 사용자의 감정 상태(긍정/부정/중립, 또는 Valence-Arousal 공간)를 분류
- **분야**: 감성 컴퓨팅(Affective Computing), 감정 기반 인터랙션, HCI
- **특징**: 감정 유도 자극(영상, 음악 등) 후 나타나는 주파수 및 비대칭 패턴을 분석합니다. 전두엽 Alpha 비대칭(좌우 Alpha 파워 차이)이 정서적 접근(approach)/회피(withdrawal) 경향과 관련된다는 연구가 있습니다. DEAP, SEED 등의 데이터셋이 벤치마크로 널리 사용됩니다.

---

### **5) Mental Workload Classification**

- **정의**: 과제 수행 중의 인지 부하 정도를 분류하는 과제
- **분야**: 조종·운전 중 부하 감시, 맞춤형 교육, 스마트 작업환경
- **특징**: 전두엽 Theta(4–8 Hz) 파워 증가와 두정엽 Alpha(8–13 Hz) 파워 감소가 높은 인지 부하 상태의 대표적 지표로 알려져 있습니다.

---

### **8) Cognitive Workload Estimation**

- **정의**: 문제 해결, 암기, 복잡한 판단 등 고차 인지 수행 시의 뇌 활성도를 연속적으로 추정
- **분야**: 인지 훈련, 학습 피드백 시스템, 작업 적정성 평가
- **특징**: Mental Workload Classification과 유사하나, 이진 분류보다는 연속적 추정(Regression) 문제로 다루는 경우가 많습니다.

---

### **2) Vigilance Estimation / Variability Prediction**

- **정의**: 사용자의 집중도 또는 각성 상태 수준을 추정하거나 시간에 따른 변동성을 분석
- **분야**: 졸음운전 방지, 피로 모니터링, 장시간 작업 안정성 분석
- **특징**: Alpha 파워 증가 및 Theta 파워 증가, Beta 파워 감소가 졸음 및 주의력 저하의 생체 지표로 활용됩니다.

---

### **3) Event Type Classification**

- **정의**: 외부 자극(시각, 청각 등)이나 병리적 이상 이벤트에 대한 뇌 반응을 분류
- **분야**: BCI 인터페이스, 감각 모달리티 분석, 병리적 EEG 이벤트 탐지
- **특징**: ERP 기반 시간적 패턴 또는 병리적 이상 파형(spike, sharp wave 등) 분류에 사용됩니다.

---

### **13) Galvanic Response Recognition**

- **정의**: EEG와 GSR(피부 전도 반응, Galvanic Skin Response) 등의 신호를 통합하여 감정·스트레스 상태를 추정
- **분야**: 스트레스 측정, 감정 기반 인터페이스, 멀티모달 감성 분석
- **특징**: EEG 단독보다 GSR 등 자율신경계 신호와 결합한 멀티모달 접근이 감정 인식 정확도를 높이는 것으로 보고됩니다. DEAP 데이터셋이 EEG+GSR 멀티모달 분석의 대표적 벤치마크입니다.

---

[^1]: Polich, J. (2007). Updating P300: An integrative theory of P3a and P3b. *Clinical Neurophysiology*, 118(10), 2128–2148. https://doi.org/10.1016/j.clinph.2007.04.019

[^2]: Falkenstein, M., Hoormann, J., Christ, S., & Hohnsbein, J. (2000). ERP components on reaction errors and their functional significance: A tutorial. *Biological Psychology*, 51(2–3), 87–107. https://doi.org/10.1016/S0301-0511(99)00031-9

[^3]: Berry, R.B., et al. (2012). *AASM Manual for the Scoring of Sleep and Associated Events: Rules, Terminology and Technical Specifications, Version 2.0.* American Academy of Sleep Medicine. https://aasm.org
