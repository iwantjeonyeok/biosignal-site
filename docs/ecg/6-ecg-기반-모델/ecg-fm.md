# ECG-FM — An Open Electrocardiogram Foundation Model

> **ECG-FM: An Open Electrocardiogram Foundation Model**
> Kaden McKeen, Sameer Masood, Augustin Toma, Barry Rubin, Bo Wang. **JAMIA Open 2025.**

- [Paper (arXiv)](https://arxiv.org/abs/2408.05178)
- [Official code](https://github.com/bowang-lab/ECG-FM)

## Motivation

기존 ECG 분석 모델들은 특정 task에 특화된 방식으로 설계되어, 대규모 annotated dataset을 필요로 한다. Self-supervised learning(SSL) 기반의 foundation model은 사전학습을 통해 이 annotation 부담을 완화할 수 있다. 그러나 당시 open-weight ECG foundation model이 매우 드물었고, 이로 인해 연구자들이 모델을 재현하거나 cross-study 비교를 수행하기가 어려웠다.

ECG-FM은 이 문제를 해결하기 위해 **코드, 모델 가중치(weights), 벤치마크 task를 모두 공개**한 open ECG foundation model이다. 1.5M ECG 데이터로 사전학습하고, MIMIC-IV-ECG 기반의 공개 벤치마크를 함께 제공함으로써 ECG AI 연구의 재현성과 확장성을 높이는 것을 핵심 목표로 한다.

## Architecture Summary

ECG-FM은 **CNN feature encoder + Transformer encoder** 구조를 채택한다.

- **CNN feature encoder**: 원시 ECG 파형에서 잠재 표현(latent representation)을 추출
- **Transformer encoder**: BERT-Base 설정 적용
  - 레이어 수: 12
  - 임베딩 차원: 768
  - Self-attention 헤드: 12
  - FFN 차원: 3,072
- **모델 입력**: 500 Hz로 resampling된 ECG를 5초 단위로 분할한 segment
- **사전학습 방법 (WCR)**: wav2vec 2.0, CMSC, RLM 세 가지 SSL 목적함수를 결합한 하이브리드 방식

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

**사전학습 방법 세부 사항:**

- **wav2vec 2.0 (local contrastive learning)**: CNN 잠재 표현의 span을 마스킹(시작 토큰 확률 6.5%, 이후 10토큰 → 전체 약 49% 마스킹). 두 개의 학습 가능한 코드북(2개 × 320 코드)으로 양자화(quantization)하고, 마스킹된 토큰을 로컬 컨텍스트로 예측하도록 학습.
- **CMSC — Contrastive Multi-Segment Coding (global contrastive learning)**: 시간적으로 인접한 ECG segment를 positive pair로 처리. 데이터 증강(augmentation) 없이 작동하므로 **faulty alignment 문제를 원천 회피**하며, 시간 불변성(temporal invariance) 학습.
- **RLM — Random Lead Masking**: 학습 시 ECG 리드를 무작위로 마스킹하는 증강 기법으로, 다양한 리드 구성에 대한 강건성 확보.

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
