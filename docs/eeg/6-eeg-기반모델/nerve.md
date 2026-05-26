# NERVE — Noise-Variability-Robust EEG Foundation Model

> **NERVE: Noise-Variability-Robust EEG Foundation Model with Electrode-Brain Interactions**
> Anonymous authors. **NeurIPS 2026 (under review).**

- [Official code (anonymous repo referenced in paper)](https://github.com/NERVE-2026/NERVE)

## Motivation

EEG 신호가 지닌 두 가지 근본적인 난제, 즉 **노이즈(noise)**와 **변동성(variability)**이 기존 EEG 기반모델들의 성능을 제한하고 있다는 문제 인식에서 출발한다. 첫째, 실제 EEG 측정에는 근전도(EMG), 안구전도(EOG), 전력선 간섭 등 다양한 아티팩트 노이즈가 불가피하게 섞인다. 기존 토크나이저들은 이러한 노이즈에 취약하여 EEG 신호의 핵심 주파수 패턴을 제대로 포착하지 못한다(LaBraM의 위상 손실 수렴 실패, NeuroLM의 위상 모델링 부재가 이를 보여준다). 둘째, EEG 신호는 피험자 간 뇌 구조 차이, 동일 피험자의 세션 간 컨디션 변화 등으로 인해 광범위한 변동성을 가진다. 이로 인해 학습된 표현이 특정 피험자나 세션에 과적합되어 범용성이 떨어진다. 세 번째로, 전극의 두피 위 위치(위상학적 정보)가 기존 모델들에서 충분히 활용되지 않았다는 점도 동기로 제시된다.

## Architecture Summary

NERVE는 세 가지 핵심 설계를 통해 위의 문제들을 해결한다.

**노이즈 강건 신경 토크나이저** — 1D-CNN 패치 인코더와 9층 EPA 인코더/3층 EPA 디코더로 구성된 토크나이저를 **잡음 제거 시간-스펙트럼 예측** 방식으로 학습한다. 학습 시 가우시안 노이즈를 패치에 주입하고, 토크나이저가 이를 복원하는 과정에서 시간 영역 신호와 DFT 기반 정규화 스펙트럼(실수부+허수부)을 동시에 재구성하도록 강제한다. 이 방식은 신호의 주파수 위상 정보까지 명시적으로 모델링하는 것이 특징이다.

**변동성 강건 사전학습** — 마스크 EEG 모델링(50% 마스킹) 손실에 **KoLeo(Kozachenko-Leonenko 엔트로피) 정규화 항**을 더한 복합 손실로 사전학습한다. KoLeo 항은 피험자 레이블 없이도 잠재 공간에서 피험자 간 표현이 균등하게 분산되도록 강제하여 변동성에 따른 표현 붕괴를 방지한다.

**전극 위치 인식(EPA) 어텐션** — 학습 가능한 위치 라우터가 두피 위의 전극을 6개 피질 영역 그룹(전두, 측두, 두정, 후두 등)으로 배정하고, 이 위상학적 사전 정보를 셀프 어텐션에 주입한다. 12층 EPA Transformer(히든 차원 200, FFN 차원 800, 10 어텐션 헤드)가 백본이며, 27개 공개 EEG 데이터셋(전처리 후 10,956시간)에서 사전학습된다.

## Pre-training Data Summary

NERVE는 모델이 10가지 세부 응용 분야(seizure detection, gait recognition, emotion recognition, motor imagery, sleep staging, event-type classification, vigilance, workload, mental-disorder diagnosis, grasp-and-lift)를 골고루 경험하도록 태스크 다양성을 의도적으로 고려한 사전학습 코퍼스를 구성한다:

- **공개 EEG 데이터셋 27개 • 원시 데이터 16,595시간**
- **전처리 후: EEG 샘플 213,784개 • 10,956시간** — LaBraM(2,534.78 h)·CBraMod(9,000 h)보다 현저히 크며, 9,000–25,000 h 구간의 다른 모델들과 비슷한 규모다.
- 통합 **128채널** 구성 (데이터셋 간 사용 가능한 전극을 최대한 유지하며, 누락 채널은 0으로 채워 명시적인 "누락 채널 마스크"로 활용).

### Preprocessing Pipeline (paper §3.1, Appendix C.3)
1. **Channel selection** — 최대 128개까지 가능한 한 많은 전극을 유지하고, 누락된 채널은 0으로 채워 누락 채널 마스크로 활용한다.
2. **Band-pass filter** 0.3–75 Hz (저주파 드리프트 제거 + 고주파 근전도/장비 노이즈 억제).
3. **Notch filter** 50 Hz (전력선 노이즈 제거).
4. **200 Hz로 리샘플링.**
5. **Z-score normalization** — 피험자 간·내 변동성 완화.
6. Patch 길이 **P = 200 (1초)**; stride는 noise-robust neural tokenizer에 **1초**, NERVE foundation model에 **4초** 적용. 샘플당 최대 패치 수 256개.

### Pre-training Configuration (paper §3.2, Appendix B.1)
- **Backbone:** 12층 **EPA (Electrode-Position-Aware) Transformer**, hidden dim 200, FFN 800, attention head 10개, **피질 영역 position-router 그룹 6개**.
- **Noise-robust neural tokenizer:** 3층 1D-CNN patch encoder + 9층 EPA encoder / 3층 EPA decoder, 8192×64 codebook, **denoising temporal-spectral prediction** 방식으로 학습 (Gaussian noise augmentation σ=0.05, time-domain 신호와 DFT 기반 정규화 스펙트럼 동시 재구성).
- **사전학습 손실:** masked EEG modeling (마스킹 비율 50%) + 변동성 강건 학습을 위한 **KoLeo 정규화**: `L = L_MEM + α · L_KoLeo`, α = 0.1.
- tokenizer → model 순서로 **4× NVIDIA A100-80G에서 약 5일** 동안 순차 사전학습.

## Pre-training Datasets (Table 7 of the paper)

시간은 Table 7에 기재된 원시 합계이며, 채널 수는 Appendix B.2에 보고된 **실제 사용** 채널 수이다.

| # | Dataset | Task | #Ch (used) | Rate (Hz) | Hours | Download |
|---|---------|------|:---:|:---:|---:|---|
| 1 | Resting State EEG Data (Trujillo 2017) | Raw / resting | 64 | 256 | 3 | <https://openneuro.org/datasets/ds003478> |
| 2 | Neonate (Stevenson 2019) | Seizure detection | 19 | 256 | 57 | <https://zenodo.org/record/4940267> |
| 3 | Siena Scalp EEG (Detti 2020) | Seizure detection | 28 | 512 | 141 | <https://physionet.org/content/siena-scalp-eeg/1.0.0/> |
| 4 | TUSZ (TUH Seizure) | Seizure detection | 20 | 256 | 1,474 | <https://isip.piconepress.com/projects/nedc/html/tuh_eeg/> |
| 5 | 2018 PhysioNet Challenge (You Snooze You Win) | Sleep staging | 6 | 200 | 14,611 | <https://physionet.org/content/challenge-2018/1.0.0/> |
| 6 | SEED | Emotion | 62 | 1000 | 42 | <https://bcmi.sjtu.edu.cn/home/seed/> |
| 7 | SEED-IV | Emotion | 62 | 200 | 42 | <https://bcmi.sjtu.edu.cn/home/seed/> |
| 8 | DREAMER | Emotion | 14 | 128 | 24 | <https://zenodo.org/record/546113> |
| 9 | Emobrain | Emotion | 64 | 1024 | 3 | <https://www.eecs.qmul.ac.uk/mmv/datasets/emobrain/> |
| 10 | BCI Competition IV-2a | Motor imagery | 22 | 250 | 13 | <https://www.bbci.de/competition/iv/#dataset2a> |
| 11 | BCI Competition IV-2b | Motor imagery | 3 | 250 | 26 | <https://www.bbci.de/competition/iv/#dataset2b> |
| 12 | BCI Competition IV-1 | Motor imagery | 59 | 1000 | 14 | <https://www.bbci.de/competition/iv/#dataset1> |
| 13 | SHU-MI | Motor imagery | 32 | 250 | 799 | <https://doi.org/10.6084/m9.figshare.19228725.v3> |
| 14 | Inria BCI Challenge | Event type (P300) | 56 | 600 | 14 | <https://www.kaggle.com/c/inria-bci-challenge> |
| 15 | Target vs Non-Target (Brain Invaders) | Event type (P300) | 32 | 512 | 4 | <https://zenodo.org/record/2649069> |
| 16 | MoBI | Event type (gait) | 60 | 100 | 9 | <https://www.nature.com/articles/sdata201874> (figshare) |
| 17 | BCIC2020-3 | Event type (imagined speech) | 64 | 256 | 272 | <https://osf.io/pq7vb/> |
| 18 | SPIS Resting State | Vigilance | 64 | 256 | 1 | <https://github.com/mastaneht/SPIS-Resting-State-Dataset> |
| 19 | FatigueSet | Vigilance / fatigue | 4 | 256 | 11 | <https://fatigueset.github.io/> |
| 20 | Stew | Workload | 14 | 128 | 4 | <https://ieee-dataport.org/open-access/stew-simultaneous-task-eeg-workload-dataset> |
| 21 | Raw EEG Data (Trujillo 2021) | Workload / categorization | 64 | 256 | 34 | <https://doi.org/10.18738/T8/HAYF5H> |
| 22 | Mental Arithmetic (Zyma 2019) | Workload | 19 | 500 | 2 | <https://physionet.org/content/eegmat/1.0.0/> |
| 23 | Berlin_dsr (Shin 2018) | Workload (discrimination) | 28 | 200 | 5 | <http://doc.ml.tu-berlin.de/simultaneous_EEG_NIRS/> |
| 24 | Berlin_nback (Shin 2018) | Workload (n-back) | 28 | 200 | 8 | <http://doc.ml.tu-berlin.de/simultaneous_EEG_NIRS/> |
| 25 | Berlin_wg (Shin 2018) | Workload (word-generation) | 28 | 200 | 13 | <http://doc.ml.tu-berlin.de/simultaneous_EEG_NIRS/> |
| 26 | Mumtaz2016 (MDD vs HC) | Mental disorder | 19 | 256 | 10 | <https://figshare.com/articles/dataset/EEG_Data_New/4244171> |
| 27 | Grasp and Lift EEG Challenge | Grasp-and-lift recognition | 32 | 500 | 9 | <https://www.kaggle.com/c/grasp-and-lift-eeg-detection> |

**총계 (원시): 16,595시간 → 전처리 후: 10,956시간 / 213,784 샘플.**

> **다운스트림 데이터셋 (사전학습에 미사용).** NERVE는 분포 외 일반화 성능을 측정하기 위해 사전학습 풀에서 **의도적으로 제외**한 5개 태스크에 걸친 8개 데이터셋에서 평가된다: **TUSL**, **SEED-V**, **DEAP**, **HCI-Tagging Emotion**, **High-Gamma**, **TUEV**, **BCI-NER Challenge**, **SEED-VIG** (Table 2).

## How to Reproduce the Pre-training Preprocessing

```bash
# 1) 위 27개 데이터셋을 다운로드한다 (TUSZ + Siena + Neonate는
#    데이터셋별 등록 필요; 나머지 대부분은 공개 접근 가능).
# 2) NERVE 저장소를 clone한다
git clone https://github.com/NERVE-2026/NERVE
cd NERVE

# 3) 모든 코퍼스에 통합 파이프라인을 적용한다:
#    - 누락 채널을 0으로 채운다 (목표: 128채널 레이아웃)
#    - Band-pass 0.3–75 Hz, notch 50 Hz
#    - 200 Hz로 리샘플링
#    - 레코딩별 Z-score 정규화
#    - 1초 패치로 분할 (P = 200)

# 4) noise-robust neural tokenizer를 학습한 뒤 (20 에폭, batch 1024, stride 200)
#    variability-robust NERVE 사전학습을 시작한다
#    (12층 EPA Transformer, 10 에폭, batch 512, masking ratio 0.5,
#     KoLeo coefficient α = 0.1, stride 800)
#    4× NVIDIA A100-80G에서 실행.
```

## Key ideas (why NERVE is different)

1. **Denoising temporal-spectral prediction 기반 noise-robust tokenizer.** 모든 패치에 Gaussian 노이즈를 주입하고, tokenizer가 노이즈 없는 time-domain 신호와 **DFT 기반 정규화 스펙트럼**(실수부 + 허수부)을 동시에 재구성하도록 학습한다. 이를 통해 전체 주파수 스펙트럼을 포괄한다 — LaBraM(위상 손실 수렴 실패)이나 NeuroLM(위상 모델링 부재)과 대비된다.
2. **KoLeo 정규화를 통한 variability-robust 사전학습.** Kozachenko–Leonenko 엔트로피 항을 masked EEG modeling에 추가하여, 피험자 레이블 없이도 잠재 공간에서 **피험자 간 분리성**을 확보한다.
3. **Electrode-Position-Aware (EPA) attention.** 학습 가능한 position-router `P ∈ R^{R×N×d}`가 **R=6 피질 영역 그룹**을 기반으로 위상학적 사전 정보를 셀프 어텐션에 주입한다. CBraMod의 criss-cross attention의 순차적 저랭크 일반화에 해당한다(Appendix F 참조).

## Citation

```bibtex
@inproceedings{anonymous2026nerve,
  title={{NERVE}: Noise-Variability-Robust {EEG} Foundation Model with Electrode-Brain Interactions},
  author={Anonymous},
  booktitle={International Conference on Machine Learning (ICML)},
  note={Under review},
  year={2026}
}
```
