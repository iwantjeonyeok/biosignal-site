# LaBraM — Large Brain Model

> **Large Brain Model for Learning Generic Representations with Tremendous EEG Data in BCI**
> Wei-Bang Jiang, Li-Ming Zhao, Bao-Liang Lu. **ICLR 2024 (Spotlight).**

- [Paper (OpenReview)](https://openreview.net/forum?id=QzTpTRVtrP)
- [Official code](https://github.com/935963004/LaBraM)
- [Preprocessing scripts folder](https://github.com/935963004/LaBraM/tree/main/dataset_maker)

## Motivation

기존 EEG 기반 딥러닝 모델들은 특정 데이터셋과 태스크에 맞춰 개별적으로 설계되는 것이 일반적이었다. 이는 모델 규모를 키우기 어렵게 만들고, 학습된 표현의 범용성을 심각하게 제한한다. 반면 자연어 처리나 컴퓨터 비전 분야에서는 대규모 비지도 사전학습을 통해 태스크 무관한 범용 표현을 학습하는 기반모델 패러다임이 큰 성공을 거뒀다. LaBraM은 이 격차를 해소하기 위해 등장했다. 약 20개의 공개 EEG 데이터셋을 통합·정규화하여 ~2,500시간 규모의 대규모 사전학습 코퍼스를 구성하고, 이 데이터로 단일한 통합 EEG 기반모델을 학습함으로써 BCI 분야 전반에 걸쳐 전이 가능한 표현을 획득하는 것을 목표로 한다.

## Architecture Summary

LaBraM은 EEG 신호를 채널 단위의 패치로 분할하여 처리한다. 각 채널의 짧은 시간 구간이 하나의 패치가 되며, 서로 다른 채널 수와 샘플링 레이트를 가진 이질적 데이터셋을 통일된 방식으로 입력받을 수 있다. 사전학습은 두 단계로 이루어진다. 첫 번째 단계에서는 **벡터 양자화 신경 스펙트럼 예측(VQNSP, Vector-Quantized Neural Spectrum Prediction)** 방식으로 신경 토크나이저를 학습한다. 이 토크나이저는 연속적인 EEG 패치를 의미론적으로 풍부한 이산 신경 코드(neural code)로 압축 인코딩한다. 두 번째 단계에서는 입력 패치의 일부를 무작위로 마스킹한 뒤, 마스크된 위치의 원래 신경 코드를 예측하는 마스크 EEG 모델링(Masked EEG Modeling)으로 Transformer 인코더를 사전학습한다. 모델 크기는 Transformer의 깊이와 히든 차원을 조절하여 Base(5.8M), Large(46M), Huge(369M) 세 가지로 제공된다. 다운스트림 태스크 적응 시에는 태스크별 헤드를 붙이고 파인튜닝하는 표준적인 방식을 따른다.

## Pre-training Data Summary

LaBraM은 **약 20개의 공개·자체 수집 데이터셋**에서 수집한 **~2,534.78시간** 분량의 EEG로 사전학습된다(vector-quantized neural tokenizer 학습 단계와 masked-EEG modeling 단계 모두에 사용). 다운스트림 데이터셋 4종(TUAB, TUEV, SEED-V, MoBI)은 사전학습 풀에서 명시적으로 제외된다.

### Uniform preprocessing
1. Band-pass filter 0.1–75 Hz
2. Notch filter 50 Hz
3. **200 Hz**로 리샘플링
4. µV 단위로 스케일링 후 약 [-1, 1] 범위로 clipping (단위: 100 µV)

사전학습 전처리 파이프라인은 [`dataset_maker/make_h5dataset_for_pretrain.py`](https://github.com/935963004/LaBraM/blob/main/dataset_maker/make_h5dataset_for_pretrain.py)에 구현되어 있으며, 다운스트림 전용 스크립트(`make_TUAB.py`, `make_TUEV.py`)도 같은 폴더에 있다.

## Pre-training Datasets

| # | Dataset | #Subjects | Hours | #Ch | Rate (Hz) | Task / Description | Download |
|---|---------|:---------:|-------|:---:|:---------:|--------------------|----------|
| 1 | BCI Competition IV-1 (Blankertz et al., 2007) | 7 | 8.21 | 59 | 1000 | Motor imagery: left hand, right hand, foot + idle state | <https://www.bbci.de/competition/iv/#dataset1> |
| 2 | Emobrain (Savran et al., 2006) | 16 | 4.94 | 64 | 1024 | Emotion recognition (IAPS stimuli); EEG + fNIRS; Biosemi Active 2 | <https://www.eecs.qmul.ac.uk/mmv/datasets/emobrain/> |
| 3 | Grasp and Lift EEG Challenge (Luciw et al., 2014) | 12 | 11.72 | 32 | 500 | Grasp-and-lift (GAL) trials; BrainAmp amplifier | <https://www.kaggle.com/c/grasp-and-lift-eeg-detection> |
| 4 | Inria BCI Challenge (Margaux et al., 2012) | 26 | 29.98 | 56 | 600 | P300-based BCI speller; Ag/AgCl sensors; VSM-CTF system | <https://www.kaggle.com/c/inria-bci-challenge> |
| 5 | EEG Motor Movement/Imagery Dataset (Schalk et al., 2004) | 109 | 47.3 | 64 | 160 | Motor movement & imagery (both fists / feet); 2 baseline tasks (eyes open / closed); BCI2000 system | <https://physionet.org/content/eegmmidb/1.0.0/> |
| 6 | Raw EEG Data (Trujillo, 2020) | — | 34.35 | 64 | 256 | Information-Integration & Rule-Based categorization tasks | <https://openneuro.org/datasets/ds003490> |
| 7 | Resting State EEG Data (Trujillo et al., 2017) | 22 | 3.04 | 64 | 256 | Resting state; 8 min (4 min eyes-closed + 4 min eyes-open) | <https://openneuro.org/datasets/ds003478> |
| 8 | SEED Series (Zheng & Lu, 2015; Zheng et al., 2018; Liu et al., 2022) | [SEED](../seed.md):15 / SEED-IV:15 / SEED-GER:8 / SEED-FRA:8 | 166.75 | 62 | 1000 | Emotion recognition; video-elicited; ESI NeuroScan (SEED-V는 downstream eval로 제외) | <https://bcmi.sjtu.edu.cn/home/seed/> |
| 9 | Siena Scalp EEG Database (Detti et al., 2020) | 14 | 30.47 | 31 | 512 | Epilepsy patients; EB Neuro & Natus Quantum LTM amplifiers | <https://physionet.org/content/siena-scalp-eeg/1.0.0/> |
| 10 | SPIS Resting State Dataset (Torkamani-Azar et al., 2020) | 10 | 0.83 | 64 | 2048 | Resting (eyes-closed / open) + 105-min SART attention task; Ag/AgCl active electrodes | <https://github.com/mastaneht/SPIS-Resting-State-Dataset> |
| 11 | Target Versus Non-Target (Korczowski et al., 2019) | 50 | 16 | 32 | 512 | Brain Invaders P300 BCI; oddball paradigm; adaptive Riemannian Geometry (no-calibration); g.USBamp amplifier | <https://zenodo.org/record/2649069> |
| 12 | TUAR — TUH Artifact Corpus (Buckwalter et al., 2021) | — | 92.22 | 23 | 256 | TUEG subset; 5 artifact types: eye movement, muscle, chewing, electrode pop, background noise | <https://isip.piconepress.com/projects/tuh_eeg/html/downloads.shtml> |
| 13 | TUEP — TUH Epilepsy Corpus (Veloso et al., 2017) | 200 | 591.22 | 19–23 | 256 | TUEG subset; epilepsy (100명) vs. non-epilepsy (100명) binary classification | <https://isip.piconepress.com/projects/tuh_eeg/html/downloads.shtml> |
| 14 | TUSZ — TUH Seizure Corpus (Shah et al., 2018) | — | 1138.53 | 19–23 | 256 | Seizure events manually annotated: start/stop time, channel, seizure type | <https://isip.piconepress.com/projects/tuh_eeg/html/downloads.shtml> |
| 15 | TUSL — TUH Slowing Corpus (von Weltin et al., 2017) | — | 20.59 | 23 | 256 | TUEG subset; slowing event annotations | <https://isip.piconepress.com/projects/tuh_eeg/html/downloads.shtml> |
| 16 | Self-collected EEG (Jiang et al. 2021/2023; Luo et al. 2022; Li et al. 2021; Tao & Lu, 2020) | 140+ | 342.23 | 62 | 1000 | Various paradigms; ESI NeuroScan system (SJTU lab) | Not publicly released |

**총계: ~2,534.78시간.** TUH 하위 코퍼스 전체(TUAR/TUEP/TUSZ/TUSL)에 접근하려면 [Temple University Hospital EEG Corpus](https://isip.piconepress.com/projects/nedc/html/tuh_eeg/)에 무료 등록이 필요하다.

## How to reproduce the pre-training preprocessing

1. 위 링크에서 각 데이터셋을 다운로드한다(TUAR/TUEP/TUSZ/TUSL는 TUH 접근 신청 필요).
2. LaBraM을 clone하고 `requirements.txt`를 설치한다.
3. 원시 `.cnt`/`.edf`/`.bdf` 파일을 HDF5 패치로 변환한다:
   ```bash
   python dataset_maker/make_h5dataset_for_pretrain.py \
       --input_dir /path/to/raw \
       --output_dir /path/to/h5
   ```
4. `run_vqnsp_training.py` 실행 후 `run_labram_pretraining.py`로 사전학습을 시작한다.

## Citation

```bibtex
@inproceedings{jiang2024labram,
  title={Large Brain Model for Learning Generic Representations with Tremendous EEG Data in BCI},
  author={Jiang, Wei-Bang and Zhao, Li-Ming and Lu, Bao-Liang},
  booktitle={The Twelfth International Conference on Learning Representations (ICLR)},
  year={2024}
}
```
