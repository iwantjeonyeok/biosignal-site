# ECG-FM — An Open Electrocardiogram Foundation Model

> **ECG-FM: An Open Electrocardiogram Foundation Model**
> Kaden McKeen, Sameer Masood, Augustin Toma, Barry Rubin, Bo Wang. **JAMIA Open 2025.**

- [Paper (arXiv)](https://arxiv.org/abs/2408.05178)
- [Official code](https://github.com/bowang-lab/ECG-FM)

## Motivation

기존 ECG 분석 모델들은 특정 task에 특화된 방식으로 설계되어, 새로운 임상 과제로 확장하려면 여전히 많은 라벨 데이터가 필요하다. ECG foundation model은 self-supervised learning을 통해 라벨 없는 ECG에서 구조와 의미를 먼저 학습하고, 이후 다양한 downstream task에 적은 라벨로 전이할 수 있다는 장점이 있다. 하지만 기존 generative SSL은 낮은 수준의 구조 복원에 치우치고, contrastive SSL은 augmentation으로 인해 생리학적 의미가 왜곡되는 faulty alignment 문제가 발생할 수 있다. 또한 ECG 분야는 공개된 code와 pretrained weights가 부족해 재현성과 비교 가능성이 낮다는 문제가 있다. ECG-FM은 이러한 한계를 해결하기 위해 hybrid self-supervised learning으로 사전학습한 open-weight ECG foundation model을 제안하고, ECG foundation model의 활용 장벽을 낮추는 것을 목표로 한다

## Architecture Summary

ECG-FM은 **wav2vec 2.0** 구조를 기반으로 한 transformer-based ECG foundation model이다. 입력 ECG waveform은 CNN feature extractor를 거쳐 latent representation으로 변환되고, 이후 **BERT-like Transformer encoder**를 통해 문맥 정보가 반영된 ECG representation으로 인코딩된다. 모델은 총 **90.9M parameters** 규모이며, ECG 신호의 구간별 특징을 Transformer 기반 표현으로 학습하도록 설계된다.사전학습은 **WCR(W2V + CMSC + RLM)**이라는 hybrid self-supervised learning 방식으로 이루어진다. wav2vec 2.0 objective는 CNN latent representation의 일부 구간을 masking하고, 주변 문맥을 이용해 해당 위치의 quantized target을 구별하도록 학습하여 ECG의 local pattern을 포착한다. 반면 **CMSC**는 시간적으로 인접한 ECG segment를 positive pair로 두고 global representation 간 contrastive learning을 수행하여, 심장 기능과 관련된 전역적 의미 표현을 학습한다. 이 방식은 augmentation을 사용하지 않아 생리학적 의미가 왜곡되는 faulty alignment 문제를 줄이는 역할을 한다. 또한 **RLM**은 사전학습 중 각 ECG lead를 확률적으로 masking하는 ECG-specific augmentation 전략이다. 이를 통해 모델은 특정 lead 조합에만 의존하지 않고 다양한 lead 구성에서도 안정적인 표현을 학습할 수 있으며, 표준 12-lead ECG뿐 아니라 일부 lead만 존재하는 **reduced lead setting**에서도 fine-tuning될 수 있는 유연성을 갖는다. 

## Pre-training Data Summary

ECG-FM은 두 개의 공개 데이터셋을 결합한 **약 87만 개의 ECG**로 사전학습한다. 5초 단위로 분할 후 **총 약 175만 개의 샘플**이 실제 학습에 사용된다.

- **PhysioNet 2021**: 625,139개 ECG, 178,140명 환자
- **MIMIC-IV-ECG**: 800,035개 ECG, 161,352명 환자
- **최종 사전학습 규모**: 873,706개 ECG → **1,757,054개 샘플**
  - 학습 세트: 699,001개 ECG → **1,405,625개 샘플**

### Preprocessing procedure

1. 원시 파형(raw waveform) 및 메타데이터(sample rate, 환자 정보 등) 추출
2. 선형 보간(linear interpolation)으로 **500 Hz resampling**
3. **Z-score normalization** 수행
4. 비중첩 **5초 단위 segment** 분할 (CMSC contrastive learning의 positive pair 생성 목적)
5. null 값 또는 상수 리드(constant lead)가 포함된 샘플 제거
6. 환자-시간 계층화(patient-temporal stratification)로 학습/검증/테스트 분리


### Pre-training Datasets

| Dataset | Subjects | ECG 수 | 샘플 수 (전처리 후) | Rate (Hz) | Access |
|---------|--------|--------|-------------------|-----------|--------|
| PhysioNet 2021 | 178,140명 | 625,139개 | — | → 500 | 공개 → https://physionet.org/content/challenge-2021/ |
| MIMIC-IV-ECG | 161,352명 | 800,035개 | — | → 500 | PhysioNet 계정 필요 (무료) → https://physionet.org/content/mimic-iv-ecg/ |
| **합계 (사전학습)** | — | **873,706개** | **1,757,054개** | — | — |

## Downstream Datasets

ECG-FM은 세 가지 downstream task로 평가하며, 이 데이터셋들은 사전학습에는 사용되지 않는다.

| Task | Dataset | ECG 수 | 비고 |
|-----|---------|--------|------|
| ECG 해석 레이블 예측 | UHN-ECG | 573,670개 | 심장전문의 over-read 레이블 |
| ECG 해석 레이블 예측 (공개 벤치마크) | MIMIC-IV-ECG | 787,677개 | 논문과 함께 공개된 벤치마크 task |
| 좌심실 박출률 감소(LVEF) 예측 | UHN-ECG | 129,121개 | 심초음파 보고서 연계 (±7일 이내) |

**주요 결과**: 심방세동(AF) AUROC 0.996, LVEF ≤40% AUROC 0.929. 소~중규모 데이터 환경에서 task-specific 모델 대비 현저한 성능 우위.

## How to Reproduce the Pre-training Preprocessing

```bash
# 1) MIMIC-IV-ECG 접근 (PhysioNet 계정 필요, 무료)
#    https://physionet.org/content/mimic-iv-ecg/
# 2) PhysioNet 2021 데이터 다운로드
#    https://physionet.org/content/challenge-2021/
# 3) 코드 클론
git clone https://github.com/bowang-lab/ECG-FM
cd ECG-FM && pip install -r requirements.txt
# 4) 전처리 실행 (500 Hz resampling, Z-score normalization, 5초 분할)
python preprocess.py
# 5) 사전학습 실행 (A100 80GB GPU 3개, 200 epoch)
python pretrain.py
```

## Citation

```bibtex
@article{mckeen2024ecgfm,
  title={ECG-FM: An Open Electrocardiogram Foundation Model},
  author={McKeen, Kaden and Masood, Sameer and Toma, Augustin and Rubin, Barry and Wang, Bo},
  journal={JAMIA Open},
  year={2025},
  url={https://arxiv.org/abs/2408.05178}
}
```
