# NeuroLM — Multi-task EEG Foundation Model with an LLM backbone

> **NeuroLM: A Universal Multi-task Foundation Model for Bridging the Gap between Language and EEG Signals**
> Wei-Bang Jiang, Yansen Wang, Bao-Liang Lu, Dongsheng Li. **ICLR 2025.**

- [Paper (OpenReview)](https://openreview.net/forum?id=Io9yFt7XH7)
- [Official code](https://github.com/935963004/NeuroLM)
- [Preprocessing scripts folder](https://github.com/935963004/NeuroLM/tree/main/dataset_maker)

## Motivation

LaBraM 등 기존 EEG 기반모델들은 분류나 회귀 등 단일 유형의 태스크를 처리하기 위해 태스크별 출력 헤드를 별도로 붙이는 구조를 채택한다. 이 방식은 모델이 수행할 수 있는 태스크를 사전에 고정해야 하며, 새로운 태스크가 등장할 때마다 헤드 재설계와 재학습이 필요하다. LLM이 자연어 지시문(instruction)을 통해 번역·요약·질의응답 등 다양한 태스크를 단일 모델로 처리하는 것처럼, EEG 신호를 하나의 "외국어"로 간주하여 LLM 백본에 통합하면 멀티태스크 BCI 시스템을 자연스럽게 구현할 수 있다는 것이 핵심 동기다. NeuroLM은 EEG와 언어 사이의 간극을 메우는 첫 멀티태스크 EEG 기반모델을 제안한다.

## Architecture Summary

NeuroLM은 세 단계 학습 파이프라인으로 구성된다. 첫 번째 단계에서는 **텍스트 정렬 신경 토크나이저**를 학습한다. 벡터 양자화 시간-주파수 예측(VQ-TFP, Vector-Quantized Temporal-Frequency Prediction) 방식으로 EEG 패치를 이산 신경 토큰으로 압축하는데, 이 토큰 공간이 텍스트 토큰 공간과 정렬되도록 설계된다. 두 번째 단계에서는 동결(frozen)된 VQ 인코더가 생성한 EEG 토큰을 LLM에 입력하여, **다채널 자기회귀(multi-channel autoregression)** 방식으로 인과적 EEG 표현을 사전학습한다. 세 번째 단계에서는 자연어 지시문과 EEG 토큰을 함께 입력하는 **멀티태스크 인스트럭션 튜닝**으로 이상 감지, 사건 분류, 감정 인식 등 다양한 다운스트림 태스크에 적응시킨다. 최대 규모인 NeuroLM-XL은 1.7B 파라미터로, EEG 신호 처리 모델로는 당시 최대 규모다. 약 25,000시간의 대규모 EEG 코퍼스(TUEG 전체 포함)에서 사전학습되었다.

## Pre-training Data Summary

NeuroLM은 LaBraM의 데이터 수집 철학을 계승하되 규모를 **약 10배**로 확장한다. 기존 공개 코퍼스에 더해 TUEG 전체(≈24,000시간)를 추가로 사용하며, 전처리 후 총합은 **~25,000시간**으로 발표 당시 공개 EEG 사전학습 풀 중 최대 규모였다.

### Preprocessing (paper §3.2 "Data Preprocessing")
- Band-pass filter 0.1–75 Hz
- Notch filter 50 Hz 또는 60 Hz (데이터 수집 지역에 따라)
- **200 Hz**로 리샘플링
- 100으로 나누어 정규화 (µV 단위 → 약 [-1, 1] 범위)

NeuroLM의 사전학습 데이터 변환 스크립트는 [`dataset_maker/prepare_TUH_pretrain.py`](https://github.com/935963004/NeuroLM/blob/main/dataset_maker/prepare_TUH_pretrain.py)이며, 다운스트림 데이터셋 스크립트(`prepare_TUAB.py`, `prepare_TUEV.py`, `prepare_SEED.py`, `prepare_HMC.py`, `prepare_TUSL.py`, `prepare_workload.py`)도 같은 폴더에 있다.

## Pre-training Datasets (Table 6 of the paper)

논문 Table 6 원문 컬럼 구성: Dataset / #Channel / Rate (Hz) / Time (h) / Description

| # | Dataset | #Subjects | Hours | #Ch | Rate (Hz) | Description | Download |
|---|---------|:---------:|------:|:---:|:---------:|-------------|----------|
| 1 | **TUEG** — TUH EEG Corpus (Obeid & Picone, 2016) | 14,987 | ~24,000 | 17–23 | 250–1024 | 26,846건의 임상 EEG 레코딩; 단일 최대 기여 데이터셋 | <https://isip.piconepress.com/projects/nedc/html/tuh_eeg/> |
| 2 | SEED Series (Zheng et al., 2018; Liu et al., 2021; 2022) | [SEED-IV](../seed-iv.md):15 / SEED-V:20 / SEED-GER:8 / SEED-FRA:8 | 170.54 | 62 | 1000 | Emotion recognition; 감정 유발 영상; ESI NeuroScan (LaBraM 대비 SEED-V 포함, SEED 본편 제외) | <https://bcmi.sjtu.edu.cn/home/seed/> |
| 3 | BCI Competition IV-1 (Blankertz et al., 2007) | 7 | 8.21 | 59 | 1000 | Motor imagery: left hand, right hand, foot + idle state | <https://www.bbci.de/competition/iv/#dataset1> |
| 4 | Emobrain (Savran et al., 2006) | 16 | 4.94 | 64 | 1024 | Multimodal emotion (IAPS); EEG + fNIRS; Biosemi Active 2 | <https://www.eecs.qmul.ac.uk/mmv/datasets/emobrain/> |
| 5 | Grasp and Lift EEG Challenge (Luciw et al., 2014) | 12 | 11.72 | 32 | 500 | Grasp-and-lift (GAL) trials; BrainAmp amplifier | <https://www.kaggle.com/c/grasp-and-lift-eeg-detection> |
| 6 | Inria BCI Challenge (Margaux et al., 2012) | 26 | 29.98 | 56 | 600 | P300-based BCI speller; Ag/AgCl sensors | <https://www.kaggle.com/c/inria-bci-challenge> |
| 7 | EEG Motor Movement/Imagery Dataset (Schalk et al., 2004) | 109 | 47.3 | 64 | 160 | Motor movement & imagery (both fists / feet); 2 baseline tasks (eyes open / closed); BCI2000 | <https://physionet.org/content/eegmmidb/1.0.0/> |
| 8 | Raw EEG Data (Trujillo, 2020) | — | 34.35 | 64 | 256 | Information-Integration & Rule-Based categorization tasks | <https://openneuro.org/datasets/ds003490> |
| 9 | Resting State EEG Data (Trujillo et al., 2017) | 22 | 3.04 | 64 | 256 | Resting state; 8 min (4 min eyes-closed + 4 min eyes-open) | <https://openneuro.org/datasets/ds003478> |
| 10 | Siena Scalp EEG Database (Detti et al., 2020) | 14 | 30.47 | 31 | 512 | Epilepsy patients; EB Neuro & Natus Quantum LTM amplifiers | <https://physionet.org/content/siena-scalp-eeg/1.0.0/> |
| 11 | SPIS Resting State Dataset (Torkamani-Azar et al., 2020) | 10 | 0.83 | 64 | 2048 | Resting (eyes-closed / open) + 105-min SART attention task; fixed-sequence and varying ISIs | <https://github.com/mastaneht/SPIS-Resting-State-Dataset> |
| 12 | Target Versus Non-Target (Korczowski et al., 2019) | 50 | 16 | 32 | 512 | Brain Invaders P300 BCI; oddball paradigm; adaptive Riemannian Geometry (no-calibration) | <https://zenodo.org/record/2649069> |
| 13 | Self-collected EEG corpus (Jiang et al. 2021/2023; Luo et al. 2022; Li et al. 2021; Tao & Lu, 2020) | 140+ | 342.23 | 62 | 1000 | Various paradigms; ESI NeuroScan system (SJTU lab) | Not publicly released |

**총계 (전처리 후): ≈25,000시간.**

> **LaBraM과의 데이터 중복 관련 참고사항.** NeuroLM은 LaBraM의 TUH 하위 코퍼스 분할(TUAR/TUEP/TUSZ/TUSL) 대신 **TUEG 전체 코퍼스**를 사용하며, MoBI와 SEED-V는 다운스트림 평가 세트로 쓰이므로 사전학습 풀에서 제외한다.

## How to Reproduce the Pre-training Preprocessing

```bash
# 1) 위 데이터셋을 다운로드한다. TUEG 접근 권한 신청 필요(무료).
git clone https://github.com/935963004/NeuroLM
cd NeuroLM && pip install -r requirements.txt
# 2) TUEG를 pickle 파일로 변환한다
python dataset_maker/prepare_TUH_pretrain.py  --input_dir /path/to/tueg --output_dir /path/to/pkl
# 3) (선택사항) 텍스트 코퍼스도 함께 준비한다
python text_dataset_maker/prepare.py
# 4) neural tokenizer 학습 → causal pre-training → instruction tuning
python train_vq.py && python train_pretrain.py && python train_instruction.py
```

## Citation

```bibtex
@inproceedings{jiang2025neurolm,
  title={{NeuroLM}: A Universal Multi-task Foundation Model for Bridging the Gap between Language and {EEG} Signals},
  author={Jiang, Wei-Bang and Wang, Yansen and Lu, Bao-Liang and Li, Dongsheng},
  booktitle={The Thirteenth International Conference on Learning Representations (ICLR)},
  year={2025}
}
```
