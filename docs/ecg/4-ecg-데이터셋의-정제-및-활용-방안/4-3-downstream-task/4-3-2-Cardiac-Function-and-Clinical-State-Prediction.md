
# 4.3.2 Cardiac Function and Clinical State Prediction
Cardiac Function and Clinical State Prediction은 ECG 신호를 이용해 단순한 ECG 판독 label을 넘어, 환자의 심장 기능이나 임상 상태를 예측하는 downstream task입니다.  
ECG가 부정맥이나 전도장애를 분류하는 도구에 그치지 않고, 심장 기능 저하, 임상 질환, 급성 심혈관 사건, 바이오마커, 향후 예후 예측에도 활용될 수 있음을 보여줍니다.

최근 ECG foundation model 연구에서는 ECG로부터 LVEF 감소, LVSD, heart failure와 같은 심장 기능 관련 상태를 예측하거나, CKD, CHD, ACS와 같은 임상 질환 및 사건을 예측하는 실험이 수행되었습니다. 또한 NT-proBNP와 같은 검사 수치 기반 바이오마커 예측, future cardiovascular event 또는 mortality prediction처럼 향후 임상 사건을 예측하는 task도 downstream evaluation에 포함되고 있습니다.

| 세부 항목 | 설명 | 대표 예시 |
|---|---|---|
| **Cardiac Function Prediction** | ECG 신호를 이용해 심장의 기능 저하 또는 구조적·기능적 이상과 관련된 상태를 예측하는 task입니다. | LVEF 감소, LVSD, heart failure |
| **Clinical Disease / Event Detection** | ECG 자체의 판독 label이 아니라, ECG와 관련된 환자의 임상 질환 또는 급성 임상 사건을 예측하는 task입니다. | CKD, CHD, ACS |
| **Biomarker Prediction** | ECG와 연결된 검사 수치 또는 생체지표를 예측하는 task입니다. | NT-proBNP |
| **Future Event / Prognosis Prediction** | 현재 ECG를 바탕으로 향후 발생할 수 있는 심혈관 사건이나 예후를 예측하는 task입니다. | future cardiovascular event, mortality, hospitalization |

#### 1) Cardiac Function Prediction

Cardiac Function Prediction은 ECG 신호를 통해 심장의 기능적 상태를 예측하는 task입니다.
대표적으로 LVEF(Left Ventricular Ejection Fraction) 감소 여부, LVSD(Left Ventricular Systolic Dysfunction), heart failure와 같은 항목이 포함됩니다. 이 task는 ECG가 단순히 전기적 리듬 이상을 보여주는 신호가 아니라, 심장의 펌프 기능이나 전반적인 심장 상태와도 관련된 정보를 포함할 수 있음을 보여줍니다.  
예를 들어 ECG-FM은 reduced LVEF 예측을 downstream task로 수행했으며, CREMA는 실제 임상 환경에서 LVSD detection을 평가했습니다. HuBERT-ECG 역시 heart failure처럼 ECG가 직접적인 진단 도구는 아니더라도 보조적인 정보를 제공할 수 있는 질환을 downstream task로 다루었습니다.

#### 2) Clinical Disease / Event Detection

Clinical Disease / Event Detection은 ECG를 이용해 환자의 임상 질환이나 급성 임상 사건을 예측하는 task입니다. 이 항목은 ECG 판독 label 자체를 맞히는 것이 아니라, ECG 신호가 환자의 임상 상태를 얼마나 잘 반영하는지 평가하는 데 초점을 둡니다.
이 task에서 모델이 예측하는 대표적인 대상은 CKD(Chronic Kidney Disease), CHD(Coronary Heart Disease), ACS(Acute Coronary Syndrome) 등입니다. 즉, ECG 신호를 입력으로 사용하여 환자가 만성 신장 질환(CKD)이나 관상동맥질환(CHD)을 가지고 있는지, 또는 급성 관상동맥 증후군(ACS)과 관련된 상태인지 예측하는 방식입니다. ECGFounder는 CKD와 CHD detection을 downstream task로 수행했으며, ECG-FM은 independent evaluation에서 ACS detection을 수행했습니다.

#### 3) Biomarker Prediction

Biomarker Prediction은 ECG 신호를 바탕으로 특정 검사 수치나 생체지표를 예측하는 task입니다.  
대표적인 예시로 NT-proBNP 예측이 있습니다.NT-proBNP는 심장 기능 저하나 심부전과 관련하여 사용되는 대표적인 바이오마커입니다.ECGFounder는 NT-proBNP classification과 regression을 downstream task로 수행했으며, 이는 ECG foundation model이 ECG 판독 label을 넘어서 임상 검사 수치와 관련된 정보를 학습할 수 있는지 평가하는 사례입니다.

#### 4) Future Event / Prognosis Prediction

Future Event / Prognosis Prediction은 현재의 ECG 신호를 바탕으로 향후 발생할 수 있는 심혈관 사건이나 환자의 예후를 예측하는 task입니다.  
대표적으로 future cardiovascular event, hospitalization, mortality prediction 등이 포함됩니다.즉, ECG 신호를 입력으로 사용하여 환자가 향후 심혈관 사건을 겪을 가능성이 있는지, 또는 일정 기간 내 사망 위험이 높은지를 예측하는 방식입니다.이 task는 ECG foundation model이 현재의 진단 label을 맞히는 데 그치지 않고, 환자의 장기적인 위험도나 예후를 예측하는 방향으로 확장될 수 있음을 보여줍니다.

#### 정리

Cardiac Function and Clinical State Prediction은 ECG downstream task의 범위를 기존의 ECG 진단 label 분류에서 환자의 임상 상태 예측으로 확장하는 항목입니다.  
이 항목은 ECG foundation model이 단순히 부정맥, 전도장애, 파형 이상을 분류하는 모델이 아니라, ECG를 통해 심장 기능, 임상 질환, 바이오마커, 향후 예후까지 예측할 수 있는 범용 임상 표현을 학습했는지 평가하는 데 중요합니다.
