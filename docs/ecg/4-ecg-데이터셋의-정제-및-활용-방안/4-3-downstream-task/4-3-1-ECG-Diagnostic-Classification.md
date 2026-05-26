
# 4.3.1. ECG-Diagnostic-Classification
ECG Diagnostic Classification은 ECG 신호를 바탕으로 심장 질환, 리듬 이상, 전도장애, 파형 이상 등 다양한 진단 label을 분류하는 downstream task입니다.  
최근 ECG foundation model 연구에서는 단순히 정상/비정상을 구분하는 수준을 넘어, PTB-XL의 Superclass, Subclass, Diagnostic label, Rhythm, Form처럼 여러 진단 범주를 세분화하여 모델의 표현 학습 성능을 평가합니다.

**1) Rhythm / Arrhythmia Detection**

Rhythm / Arrhythmia Detection은 ECG 신호에서 심장의 박동 리듬이 정상적인지, 또는 부정맥이 존재하는지를 분류하는 task입니다.  
대표적으로 심방세동(Atrial Fibrillation, AFib), 심방조동(Atrial Flutter), 빈맥(Tachycardia), 서맥(Bradycardia), 조기수축(Premature Beat), 심실빈맥(Ventricular Tachycardia) 등이 포함됩니다.

**2) Form / Morphology Abnormality Detection**

Form / Morphology Abnormality Detection은 ECG 파형의 형태적 이상을 탐지하는 task입니다.  
리듬이 심장 박동의 시간적 패턴을 보는 것이라면, form 또는 morphology는 P wave, QRS complex, ST segment, T wave 등 개별 파형의 모양과 구조적 변화를 분석하는 데 초점을 둡니다.
대표적인 예시로는 ST-T abnormality, T wave inversion, Q wave abnormality, axis deviation, hypertrophy 관련 변화 등이 있습니다. 이 task는 심근허혈, 심근경색, 심실비대, 전기축 이상과 같은 질환을 판단하는 데 중요한 정보를 제공합니다.

**3) Conduction Disturbance Detection**

Conduction Disturbance Detection은 심장의 전기 신호가 정상적인 전도 경로를 따라 전달되는지 평가하는 task입니다.  
전도장애가 발생하면 ECG에서 PR interval, QRS duration, bundle branch pattern 등이 비정상적으로 나타날 수 있습니다.
대표적인 전도장애에는 방실차단(Atrioventricular Block, AV Block), 우각차단(Right Bundle Branch Block, RBBB), 좌각차단(Left Bundle Branch Block, LBBB), fascicular block 등이 있습니다.  

**4) Myocardial Ischemia / Infarction Detection**

Myocardial Ischemia / Infarction Detection은 ECG 신호를 이용해 심근허혈(Myocardial Ischemia), 심근손상(Myocardial Injury), 심근경색(Myocardial Infarction, MI)과 관련된 이상을 탐지하는 task입니다.
ECG에서는 ST elevation, ST depression, T wave inversion, pathological Q wave 등의 변화가 심근허혈이나 심근경색과 관련될 수 있습니다.  
따라서 이 task는 ECG가 단순한 리듬 분석 도구를 넘어, 심근의 혈류 부족이나 손상 여부를 평가하는 임상적 진단 도구로 활용될 수 있음을 보여줍니다.

**5) General ECG Diagnostic Label Classification**

General ECG Diagnostic Label Classification은 특정 질환 하나만을 예측하는 것이 아니라, ECG에 부여된 다양한 진단 label을 동시에 또는 계층적으로 분류하는 task입니다.  
예를 들어 PTB-XL에서는 ECG label을 Diagnostic Superclass, Diagnostic Subclass, Form, Rhythm 등으로 나누어 평가하며, 일부 연구에서는 수십 개에서 100개 이상의 ECG 진단 label을 대상으로 multi-label classification을 수행합니다.
