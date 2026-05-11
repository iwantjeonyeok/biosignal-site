# ECG-FM — An Open Electrocardiogram Foundation Model

> **ECG-FM: An Open Electrocardiogram Foundation Model**
> Kaden McKeen, Sameer Masood, Augustin Toma, Barry Rubin, Bo Wang. **JAMIA Open 2025.**

- 논문 (arXiv): https://arxiv.org/abs/2408.05178
- 공식 코드: https://github.com/bowang-lab/ECG-FM

## Pre-training Data Summary

ECG-FM은 두 개의 공개 데이터셋을 결합한 **약 87만 개의 ECG**로 사전학습합니다. 모든 ECG는 10초 길이이며, 전처리 후 5초 단위로 분할되어 **총 약 175만 개의 샘플**이 사전학습에 사용됩니다.

- **PhysioNet 2021**: 625,139개 ECG, 178,140명 환자
- **MIMIC-IV-ECG**: 800,035개 ECG, 161,352명 환자
- **최종 사전학습 규모**: 873,706개 ECG → **1,757,054개 샘플** (5초 분할 후)
  - 학습 세트: 699,001개 ECG → **1,405,625개 샘플**

## Preprocessing pipeline

1. 원시 파형(raw waveform) 및 메타데이터(샘플 레이트, 환자 정보 등) 추출
2. 선형 보간(linear interpolation)으로 **500 Hz 리샘플링**
3. **Z-score 정규화** 수행
4. 비중첩 **5초 단위** 세그먼트로 분할 (CMSC 대조학습의 양성 쌍 생성 목적)
5. null 값 또는 상수 리드(constant lead)가 포함된 샘플 제거
6. 환자-시간 계층화(patient-temporal stratification)로 학습/검증/테스트 분리

## Pre-training Dataset

| 데이터셋 | 환자 수 | ECG 수 | 샘플 수 (전처리 후) | 접근 방법 |
|---------|--------|--------|-------------------|----------|
| PhysioNet 2021 | 178,140명 | 625,139개 | — | 공개 |
| MIMIC-IV-ECG | 161,352명 | 800,035개 | — | PhysioNet 계정 필요 (무료) |
| **합계 (사전학습)** | — | **873,706개** | **1,757,054개** | — |

**모델 구조 및 사전학습 방법 (WCR)**

ECG-FM은 **CNN 피처 인코더 + Transformer 인코더** 구조이며, BERT-Base 설정(레이어 12개, 임베딩 차원 768, 어텐션 헤드 12개, FFN 3,072)을 사용합니다. 사전학습은 세 가지 SSL 목적함수를 결합한 **하이브리드 방식 WCR**을 적용합니다.

- **wav2vec 2.0**: 잠재 표현의 스팬을 마스킹하고 로컬 대조손실로 복원 학습 (전체 약 49% 마스킹)
- **CMSC**: 시간적으로 인접한 ECG 세그먼트를 양성 쌍으로 처리하는 글로벌 대조학습 (데이터 증강 없음, faulty alignment 회피)
- **RLM**: 학습 시 ECG 리드를 무작위로 마스킹하는 증강 기법

## Downstream datasets (informational — not used for pre-training)

ECG-FM은 아래 세 가지 다운스트림 태스크로 평가하며, 이 데이터셋들은 사전학습에는 사용되지 않습니다.

| 태스크 | 데이터셋 | ECG 수 | 비고 |
|-------|---------|--------|------|
| ECG 해석 레이블 예측 | UHN-ECG | 573,670개 | 심장전문의 over-read 레이블 |
| ECG 해석 레이블 예측 (벤치마크) | MIMIC-IV-ECG | 787,677개 | 공개 벤치마크로 릴리즈 |
| 좌심실 박출률 감소(LVEF) 예측 | UHN-ECG | 129,121개 | 심초음파 보고서 연계 (±7일) |

**주요 결과**: 심방세동(AF) AUROC 0.996, LVEF ≤40% AUROC 0.929. 소~중규모 데이터 환경에서 태스크 특화 모델 대비 현저한 성능 우위.

## How to reproduce the pre-training preprocessing

```bash
# 1) MIMIC-IV-ECG 접근 (PhysioNet 계정 필요, 무료)
#    https://physionet.org/content/mimic-iv-ecg/
# 2) PhysioNet 2021 데이터 다운로드
#    https://physionet.org/content/challenge-2021/
# 3) 코드 클론
git clone https://github.com/bowang-lab/ECG-FM
cd ECG-FM && pip install -r requirements.txt
# 4) 전처리 실행 (500 Hz 리샘플링, Z-score 정규화, 5초 분할)
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
