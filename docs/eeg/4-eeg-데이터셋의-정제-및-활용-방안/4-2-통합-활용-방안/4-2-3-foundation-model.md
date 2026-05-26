# 4.2.3 Foundation Model (기반 모델)

## 개념

Foundation Model이란 레이블 없이 대규모 데이터를 자기지도학습(Self-Supervised Learning, SSL) 방식으로 사전학습한 범용 모델을 의미합니다. 자연어처리의 GPT·BERT, 컴퓨터 비전의 ViT·MAE와 같이, EEG 영역에서도 수십만 시간 이상의 EEG 데이터로 사전학습된 모델이 등장하고 있습니다.

## Transfer Learning과의 차이

Transfer Learning은 일반적으로 레이블이 있는 소스 데이터셋에서 지도학습으로 사전학습합니다. Foundation Model은 레이블 없이 데이터의 내재적 구조를 학습하는 자기지도학습을 사용하여, 훨씬 더 대규모의 데이터를 활용할 수 있습니다.

| 구분 | Transfer Learning | Foundation Model |
|---|---|---|
| 사전학습 방식 | 지도학습 (레이블 필요) | 자기지도학습 (레이블 불필요) |
| 활용 가능 데이터 규모 | 레이블 데이터로 제한 | 모든 EEG 기록 데이터 활용 가능 |
| 표현의 범용성 | 소스 태스크에 편향 | 다양한 태스크에 적용 가능한 범용 표현 |
| 예시 모델 | EEGNet fine-tuning | LaBraM, BENDR, CBraMod |

## EEG Foundation Model의 자기지도학습 방식

EEG Foundation Model들은 주로 다음과 같은 SSL 목적함수를 사용합니다.

- **Masked Prediction**: 입력 EEG 시퀀스의 일부 구간(또는 채널)을 마스킹하고, 모델이 마스킹된 부분을 복원하도록 학습합니다. 자연어의 BERT, 영상의 MAE와 동일한 원리입니다. LaBraM이 이 방식을 사용합니다.
- **Contrastive Learning**: 동일 신호의 서로 다른 증강(augmentation) 뷰를 유사하게, 다른 신호는 멀어지도록 표현 공간을 학습합니다. BENDR이 EEG에 contrastive 방식을 도입한 초기 사례입니다.
- **Reconstruction**: 원본 신호를 압축된 잠재 공간(latent space)을 통해 복원하는 오토인코더 방식. 신호의 핵심 구조를 압축적으로 학습합니다.

## EEG Foundation Model의 구조적 특징

EEG Foundation Model들은 다양한 채널 수와 샘플링 주파수의 데이터셋을 하나의 모델로 처리하기 위해 다음과 같은 설계를 채택합니다.

- **채널 위치 임베딩**: 전극의 3D 좌표를 임베딩하여 채널 수에 무관하게 동작
- **패치 기반 입력**: EEG 신호를 고정 크기의 시간 패치로 분할하여 Transformer에 입력
- **Transformer 백본**: 장거리 시간 의존성과 채널 간 관계를 동시에 모델링

## 주요 EEG Foundation Model (섹션 6 연계)

섹션 6에서 자세히 소개하는 모델들이 Foundation Model의 대표적 예입니다.

- **LaBraM** (Large Brain Model): 대규모 EEG 데이터에서 masked prediction 방식으로 사전학습. 다양한 다운스트림 태스크에서 fine-tuning 후 state-of-the-art 성능 달성.
- **BENDR**: EEG 특화 contrastive 사전학습. EEG 신호의 시간-공간 표현 학습에 집중.
- **CBraMod**: 다양한 채널 구성의 데이터셋을 처리할 수 있는 범용 EEG 표현 학습 모델.

## 이 방식을 선택하는 상황

- 타깃 태스크의 레이블 데이터가 매우 적을 때 (레이블 효율적 학습)
- 여러 태스크에 하나의 모델을 재사용하고 싶을 때
- 다양한 채널 수, 샘플링 주파수의 데이터셋을 통합 처리해야 할 때
- 기존 지도학습 방식으로는 충분한 일반화 성능을 얻기 어려울 때

## 현재 한계

EEG Foundation Model은 아직 발전 초기 단계입니다. NLP의 GPT처럼 단일 모델이 모든 태스크에서 압도적 성능을 보이는 수준에는 도달하지 못했으며, 사전학습 데이터의 품질과 다양성, 다운스트림 태스크와의 도메인 정렬 문제 등이 현재 연구의 주요 과제입니다.
