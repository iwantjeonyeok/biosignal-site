
# 4.3.4 Robustness and Generalization Evaluation
Robustness and Generalization Evaluation은 ECG foundation model이 실제 환경에서 얼마나 안정적으로 작동하는지 평가하는 task입니다.  
앞선 항목들이 "무엇을 예측하는가"에 초점을 둔다면, 이 항목은 "어떤 환경에서도 잘 예측할 수 있는가"를 확인하는 평가 설정에 가깝습니다.실제 임상 환경에서는 항상 깨끗한 12-lead ECG만 사용되는 것은 아닙니다. 일부 lead가 누락될 수 있고, 움직임이나 전극 접촉 문제로 noise가 포함될 수 있으며, wearable device나 mobile ECG처럼 1-lead 또는 fewer-lead ECG만 제공되는 경우도 있습니다. 따라서 최근 ECG foundation model 연구에서는 모델이 다양한 lead 구성, noisy signal, 외부 dataset, 새로운 질환, 적은 label 환경에서도 잘 일반화되는지를 중요한 평가 기준으로 사용합니다.


#### 1) Single-lead / Fewer-lead ECG Evaluation

Single-lead / Fewer-lead ECG Evaluation은 표준 12-lead ECG가 아닌 제한된 lead 조건에서 모델의 성능을 평가하는 방식입니다.  
일반적인 병원 ECG는 12개의 lead를 사용하지만, wearable device, mobile ECG, Holter monitor, 응급 현장 ECG 등에서는 더 적은 수의 lead만 제공되는 경우가 많습니다. 따라서 이 평가는 ECG foundation model이 12-lead ECG에만 의존하지 않고, 1-lead, 2-lead, 3-lead, 6-lead ECG에서도 진단 정보를 안정적으로 추출할 수 있는지 확인하는 데 중요합니다.

#### 2) Lead-missing ECG Evaluation

Lead-missing ECG Evaluation은 ECG recording에서 일부 lead가 누락된 상황을 가정하고, 모델이 진단 성능을 유지할 수 있는지 평가하는 방식입니다.  
실제 환경에서는 전극 부착 오류, 측정 장비 문제, 데이터 저장 오류 등으로 인해 일부 lead가 정상적으로 기록되지 않을 수 있습니다. TolerantECG는 이러한 상황을 반영하기 위해 원본 ECG에서 일부 lead를 masking한 lead-missing 조건을 만들고, PTB-XL의 여러 classification level에서 성능을 평가했습니다. 이 평가는 ECG foundation model이 완전한 12-lead 입력이 없어도 안정적인 representation을 만들 수 있는지 확인하는 데 중요합니다.

#### 3) Noisy / Low-quality ECG Evaluation

Noisy / Low-quality ECG Evaluation은 noise나 artifact가 포함된 ECG에서도 모델이 안정적으로 작동하는지 평가하는 방식입니다.
ECG 신호는 환자의 움직임, 전극 접촉 불량, 호흡, 근전도 잡음, 측정 환경의 차이 등으로 인해 쉽게 손상될 수 있습니다.TolerantECG는 noisy ECG 조건과 lead-missing & noisy ECG 조건을 따로 구성하여 모델 성능을 평가했습니다. 이러한 평가는 모델이 잘 정제된 연구용 ECG뿐만 아니라, 실제 임상이나 wearable 환경에서 발생하는 불완전한 ECG 신호에도 견고하게 대응할 수 있는지 확인하는 데 필요합니다.




