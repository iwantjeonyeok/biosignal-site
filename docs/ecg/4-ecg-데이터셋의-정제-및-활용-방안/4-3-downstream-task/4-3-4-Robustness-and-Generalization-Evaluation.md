
# 4.3.4 Robustness and Generalization Evaluation

Robustness and Generalization Evaluation은 ECG foundation model이 실제 환경에서 얼마나 안정적으로 작동하는지 평가하는 항목입니다.  
앞선 항목들이 "무엇을 예측하는가"에 초점을 둔다면, 이 항목은 "어떤 환경에서도 잘 예측할 수 있는가"를 확인하는 평가 설정에 가깝습니다.

실제 임상 환경에서는 항상 깨끗한 12-lead ECG만 사용되는 것은 아닙니다.  
일부 lead가 누락될 수 있고, 움직임이나 전극 접촉 문제로 noise가 포함될 수 있으며, wearable device나 mobile ECG처럼 1-lead 또는 fewer-lead ECG만 제공되는 경우도 있습니다.  
따라서 최근 ECG foundation model 연구에서는 모델이 다양한 lead 구성, noisy signal, 외부 dataset, 새로운 질환, 적은 label 환경에서도 잘 일반화되는지를 중요한 평가 기준으로 사용합니다.

| 세부 항목 | 설명 | 대표 예시 |
|---|---|---|
| **Single-lead / Fewer-lead ECG Evaluation** | 12-lead ECG가 아닌 1-lead, 2-lead, 3-lead, 6-lead ECG 조건에서 모델 성능을 평가하는 방식입니다. | single-lead ECG, 2-lead ECG, 6-lead ECG |
| **Lead-missing ECG Evaluation** | 표준 12-lead ECG 중 일부 lead가 누락된 상황에서도 모델이 진단 성능을 유지하는지 평가하는 방식입니다. | missing lead, masked lead |
| **Noisy / Low-quality ECG Evaluation** | noise나 artifact가 포함된 ECG 신호에서도 모델이 안정적으로 작동하는지 평가하는 방식입니다. | noisy ECG, corrupted ECG |
| **Cross-dataset / External Validation** | 학습 또는 개발에 사용한 dataset이 아닌 외부 dataset에서 모델의 일반화 성능을 평가하는 방식입니다. | PTB-XL, CPSC2018, CSN, CODE-test, MIT-BIH |
| **Zero-shot / Few-shot Diagnosis** | 추가 학습 없이 새로운 dataset이나 질환을 진단하거나, 매우 적은 label만으로 target dataset에 적응하는지 평가하는 방식입니다. | zero-shot diagnosis, few-shot fine-tuning |
| **Low-resource Evaluation** | 전체 training data가 아니라 1%, 10% 등 제한된 label만 사용해 downstream task 성능을 평가하는 방식입니다. | 1% training data, 10% training data |

#### 1) Single-lead / Fewer-lead ECG Evaluation

Single-lead / Fewer-lead ECG Evaluation은 표준 12-lead ECG가 아닌 제한된 lead 조건에서 모델의 성능을 평가하는 방식입니다.  
일반적인 병원 ECG는 12개의 lead를 사용하지만, wearable device, mobile ECG, Holter monitor, 응급 현장 ECG 등에서는 더 적은 수의 lead만 제공되는 경우가 많습니다.

따라서 이 평가는 ECG foundation model이 12-lead ECG에만 의존하지 않고, 1-lead, 2-lead, 3-lead, 6-lead ECG에서도 진단 정보를 안정적으로 추출할 수 있는지 확인하는 데 중요합니다.  
예를 들어 HeartLang은 1, 2, 3, 6, 12개 lead 조합에서 downstream task 성능을 비교했으며, TolerantECG는 2-lead MIT-BIH Arrhythmia Database를 사용해 lead가 제한된 환경에서의 성능을 평가했습니다.

#### 2) Lead-missing ECG Evaluation

Lead-missing ECG Evaluation은 ECG recording에서 일부 lead가 누락된 상황을 가정하고, 모델이 진단 성능을 유지할 수 있는지 평가하는 방식입니다.  
실제 환경에서는 전극 부착 오류, 측정 장비 문제, 데이터 저장 오류 등으로 인해 일부 lead가 정상적으로 기록되지 않을 수 있습니다.

TolerantECG는 이러한 상황을 반영하기 위해 원본 ECG에서 일부 lead를 masking한 lead-missing 조건을 만들고, PTB-XL의 여러 classification level에서 성능을 평가했습니다.  
이 평가는 ECG foundation model이 완전한 12-lead 입력이 없어도 안정적인 representation을 만들 수 있는지 확인하는 데 중요합니다.

#### 3) Noisy / Low-quality ECG Evaluation

Noisy / Low-quality ECG Evaluation은 noise나 artifact가 포함된 ECG에서도 모델이 안정적으로 작동하는지 평가하는 방식입니다.  
ECG 신호는 환자의 움직임, 전극 접촉 불량, 호흡, 근전도 잡음, 측정 환경의 차이 등으로 인해 쉽게 손상될 수 있습니다.

TolerantECG는 noisy ECG 조건과 lead-missing & noisy ECG 조건을 따로 구성하여 모델 성능을 평가했습니다.  
이러한 평가는 모델이 잘 정제된 연구용 ECG뿐만 아니라, 실제 임상이나 wearable 환경에서 발생하는 불완전한 ECG 신호에도 견고하게 대응할 수 있는지 확인하는 데 필요합니다.

#### 4) Cross-dataset / External Validation

Cross-dataset / External Validation은 모델이 학습 또는 개발에 사용한 dataset과 다른 외부 dataset에서도 잘 작동하는지 평가하는 방식입니다.  
ECG dataset은 병원, 국가, 인종, 장비, annotation 기준에 따라 분포가 달라질 수 있기 때문에, 하나의 dataset에서만 높은 성능을 보이는 것은 충분하지 않습니다.

따라서 ECG foundation model 연구에서는 PTB-XL, CPSC2018, CSN, CODE-test, MIT-BIH와 같은 다양한 외부 dataset을 사용해 일반화 성능을 평가합니다.  
이 항목은 모델이 특정 dataset에 과적합된 것이 아니라, 다양한 환경의 ECG 신호에서도 활용 가능한지 확인하는 데 중요합니다.

#### 5) Zero-shot / Few-shot Diagnosis

Zero-shot / Few-shot Diagnosis는 ECG foundation model의 일반화 능력을 평가하는 중요한 방식입니다.  
Zero-shot diagnosis는 target dataset이나 새로운 질환에 대해 추가 학습 없이 바로 진단을 수행하는 방식입니다.  
Few-shot diagnosis는 target dataset의 매우 적은 수의 labeled sample만 사용해 모델을 빠르게 적응시킨 뒤 성능을 평가하는 방식입니다.

KED는 외부 multi-center dataset과 training에서 보지 못한 disease에 대해 zero-shot diagnosis를 수행했으며, 적은 수의 ECG sample만 사용한 few-shot fine-tuning도 평가했습니다.  
D-BETA 역시 여러 ECG dataset에서 zero-shot classification을 수행했습니다.

이 평가는 ECG foundation model이 새로운 병원, 새로운 환자군, 새로운 질환 환경에서도 추가 label을 많이 요구하지 않고 활용될 수 있는지를 보여줍니다.

#### 6) Low-resource Evaluation

Low-resource Evaluation은 downstream task에서 사용할 수 있는 labeled data가 제한된 상황을 가정하여 모델 성능을 평가하는 방식입니다.  
의료 데이터는 annotation 비용이 높고, 전문가 판독이 필요하며, 특정 질환의 경우 label 수가 적을 수 있기 때문에 label-efficient 성능은 중요한 평가 기준입니다.

여러 ECG foundation model 연구에서는 downstream task에서 1%, 10%, 100% training data를 각각 사용해 성능을 비교합니다.  
이 평가는 사전학습된 ECG representation이 적은 labeled data만으로도 효과적으로 활용될 수 있는지 확인하는 데 중요합니다.


