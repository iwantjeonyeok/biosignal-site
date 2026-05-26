### 4.3.3 Demographic and Biometric Prediction

Demographic and Biometric Prediction은 ECG 신호를 이용해 환자의 인구학적 특성이나 개인 고유의 생체적 특징을 예측하는 downstream task입니다.  
이 항목은 ECG가 심장 질환이나 리듬 이상만을 반영하는 것이 아니라, 나이, 성별, 개인별 ECG 패턴과 같은 환자 특성도 일부 포함할 수 있음을 보여줍니다.

최근 ECG foundation model 연구에서는 ECG를 이용한 age prediction, sex detection, patient identification 등이 downstream task로 사용되었습니다.  
특히 ECGFounder는 age classification, age regression, sex classification을 demographic downstream task로 평가했으며, D-BETA는 ECG recording이 어떤 환자에게 속하는지 예측하는 patient identification task를 수행했습니다.

| 세부 항목 | 설명 | 대표 예시 |
|---|---|---|
| **Age Prediction** | ECG 신호를 이용해 환자의 나이를 예측하는 task입니다. | age classification, age regression |
| **Sex Detection** | ECG 신호를 이용해 환자의 성별을 분류하는 task입니다. | sex classification |
| **Patient Identification** | ECG recording의 개인별 패턴을 이용해 해당 ECG가 어떤 환자에게 속하는지 식별하는 task입니다. | patient ownership prediction |

#### 1) Age Prediction

Age Prediction은 ECG 신호를 바탕으로 환자의 나이를 예측하는 task입니다.  
이 task는 크게 두 가지 방식으로 수행될 수 있습니다. 하나는 특정 나이 기준을 두고 환자를 분류하는 age classification이고, 다른 하나는 실제 나이 값을 직접 예측하는 age regression입니다.

예를 들어 ECGFounder는 MIMIC-ECG-Age dataset을 이용해 age classification과 age regression을 수행했습니다.  
이는 ECG waveform 안에 환자의 생리적 노화나 심장 전기 활동의 변화가 반영될 수 있으며, ECG foundation model이 이러한 정보를 표현으로 학습할 수 있는지 평가하는 데 사용됩니다.

#### 2) Sex Detection

Sex Detection은 ECG 신호를 이용해 환자의 성별을 분류하는 task입니다.  
ECGFounder는 MIMIC-ECG-Sex dataset을 이용해 sex classification을 수행했으며, 이를 demographic downstream task 중 하나로 평가했습니다.

이 task는 ECG 신호에 성별에 따른 심장 전기 생리학적 차이나 신체적 특성이 어느 정도 반영될 수 있음을 보여줍니다.  
다만 sex detection은 질병 진단 자체보다는 모델이 ECG에 포함된 환자 특성을 얼마나 잘 포착하는지 확인하는 보조적 downstream task에 가깝습니다.

#### 3) Patient Identification

Patient Identification은 ECG recording이 어떤 환자에게 속하는지 예측하는 task입니다.  
즉, ECG 신호에 나타나는 개인별 고유 패턴을 이용해 환자 단위의 식별 가능성을 평가합니다.

D-BETA는 PhysioNet 2021 dataset에서 patient identification task를 수행했으며, 이는 ECG encoder가 단순히 질병 label만 학습하는 것이 아니라 개인별 ECG representation을 얼마나 잘 구분하는지도 평가하기 위한 목적을 가집니다.

다만 이 task는 실제 임상 진단 task라기보다는 representation learning 성능을 확인하는 평가에 가깝습니다.  
따라서 ECG downstream task 페이지에서는 age prediction이나 sex detection보다 낮은 우선순위의 보조 항목으로 정리하는 것이 적절합니다.

#### 정리

Demographic and Biometric Prediction은 ECG foundation model이 질병 진단뿐만 아니라 환자의 나이, 성별, 개인별 ECG 패턴과 같은 생체 정보를 학습할 수 있는지 평가하는 항목입니다.  
다만 첨부된 논문들 기준으로는 이 항목이 가장 핵심적인 downstream task라기보다는, ECG representation이 환자 특성을 얼마나 포착하는지 확인하는 보조적 평가에 가깝습니다.

따라서 이 섹션은 ECG Diagnostic Classification이나 Cardiac Function and Clinical State Prediction보다 뒤에 배치하는 것이 자연스럽습니다.
