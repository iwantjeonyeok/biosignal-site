# emg2pose: A Large and Diverse Benchmark for Surface Electromyographic Hand Pose Estimation

> **emg2pose: A Large and Diverse Benchmark for Surface Electromyographic Hand Pose Estimation**
> Sasha Salter, Richard Warren, Collin Schlager, Adrian Spurr, Shangchen Han, Rohin Bhasin, Yujun Cai, Peter Walkington, Anuoluwapo Bolarinwa, Robert Wang, Nathan Danielson, Josh Merel, Eftychios Pnevmatikakis, Jesse Marshall **NeurIPS 2024 Datasets and Benchmarks Track**

- 논문 (arXiv): https://arxiv.org/pdf/2412.02725
- 공식 코드: https://github.com/facebookresearch/emg2pose

## Pre-training Data Summary

EMG2Pose는 wrist-worn surface EMG(sEMG) 신호를 이용하여 손의 pose 또는 joint angle을 추정하기 위해 구축된 대규모 공개 데이터셋입니다. 일반적인 EMG gesture classification 데이터셋과 달리, EMG2Pose는 discrete class label을 예측하는 것이 아니라 **continuous hand pose / joint angle regression**을 목표로 합니다.

- **emg2pose**: 193명, 16채널, 2kHz, Wrist sEMG + Hand pose labels, **431 GB**
- **최종 사전학습 규모**: 약 431 GB
  - 약 370시간의 recording scale
  - 25,253개의 HDF5 File

## Preprocessing Pipeline

1. EMG2Pose HDF5 recording과 `metadata.csv`를 불러옴
    - 전체 데이터는 **25,253개의 HDF5 file**로 구성
    - 각 HDF5 file은 하나의 hand, 하나의 stage에 대한 time-aligned data를 포함
    - `metadata.csv`에는 train/val/test split 정보가 포함
2. **sEMG signal 추출**
    - 16-channel wrist sEMG
    - Sampling rate: **2 kHz**
    - Bit depth: **12 bits**
    - Maximum signal amplitude: **6.6 mV**
3. **Analog band-pass filter 적용**
    - Digitization 이전에 적용
    - -3 dB cutoff: **20 Hz and 850 Hz**
4. **Dataset-level sEMG preprocessing**
    - 공개 dataset에 포함된 sEMG는 **40 Hz high-pass filtered** 상태
    - Noise floor의 standard deviation이 **1**이 되도록 rescaling
    - Left-hand EMG data는 wrist band 착용 방향에 따른 polarity reversal을 보정하기 위해 sign flip 적용
5. **Joint angle label processing**
    - Motion capture data는 26-camera motion capture system으로 수집
    - Motion capture sampling rate: **60 Hz**
    - Offline inverse kinematics, 즉 IK solver를 이용해 hand joint angles 추정
    - Joint angles에는 residual jitter 제거를 위해 **15 Hz low-pass filter** 적용
    - Joint angles는 sEMG sampling rate와 맞추기 위해 **2 kHz로 temporal upsampling / linear interpolation**
6. 고정길이 trajectory 단위로 분할
    - Evaluation: **5-second trajectories** 사용
        - 2 kHz 기준 **10,000 samples**
    - Training: **1–6 seconds non-overlapping trajectories** 사용
        - 2 kHz 기준 **2,000–12,000 samples**
    - Training trajectory length는 모델별 hyperparameter로 최적화
    - Motion capture data가 없는 time-point는 제외
7. 모델 입력 형식에 맞게 HDF5 또는 tensor format으로 사용
    - Input: wrist sEMG sequence
    - Label: hand joint angle sequence
    - Task: pose regression 또는 pose tracking

## Pre-training Dataset

| 데이터셋 | Subject 수 | Stage 수 | Channel 수 | 접근 방법 |
|---------|--------|--------|-------------------|----------|
| EMG2Pose | 193명 | 29 | 16 | 공개 |


**모델 구조 및 학습 방법 (EMG2Pose benchmark / vemg2pose baseline)**

EMG2Pose는 wrist sEMG 신호를 이용해 hand pose 또는 joint angle sequence를 예측하는 sEMG-to-pose regression benchmark입니다. 입력은 2 kHz, 16-channel wrist sEMG이며, 출력은 motion capture 기반 hand joint angle sequence입니다.

논문에서는 NeuroPose, SensingDynamics, vemg2pose 세 가지 baseline을 제시하며, 핵심 모델인 vemg2pose는 joint angle을 직접 예측하는 대신 **joint angular velocity**를 예측한 뒤 이를 적분하여 joint angle prediction을 생성합니다.

- **sEMG featurizer**: Causal strided convolutional featurizer를 이용해 2 kHz sEMG를 50 Hz feature sequence로 down-sampling
- **TDS network**: Time-Depth Separable Convolution network를 사용하여 시간축 EMG feature 추출
- **LSTM decoder**: 현재 sEMG feature와 이전 joint angle prediction을 입력으로 받아 다음 joint angular velocity를 예측
- **Autoregressive prediction**: 예측된 velocity를 이전 joint angle에 더해 다음 joint angle을 생성
- **Regression task**: Initial state까지 모델이 직접 예측하며, sEMG만으로 hand pose trajectory를 추정
- **Tracking task**: Initial ground-truth pose가 주어진 상태에서 이후 hand pose trajectory를 추적
- **Loss function**: Joint angle L1 loss와 fingertip landmark Euclidean loss를 함께 사용
- **Training trajectory**: 1–6초 non-overlapping trajectories 사용
- **Evaluation**: 5초 trajectory에서 mean absolute joint angular error와 mean Euclidean landmark distance 평가
- **Hyperparameter search**: Training window length는 2 kHz 기준 **2000–12000 samples** 범위에서 탐색되며, learning rate, gradient clipping, decoder type도 함께 최적화
- **Rotation augmentation**: Device placement 변화에 대한 일반화를 높이기 위해 training 시 sEMG channel을 공간적으로 -1, 0, 1만큼 rotation하는 augmentation을 적용
- **vemg2pose selected setting**: 최종 vemg2pose는 velocity prediction, **TDS + LSTM** 구조를 사용하며, window length는 **11790 samples**로 설정

## How to Reproduce the Pre-training Preprocessing

```bash
# 1) EMG2Pose 공식 코드 클론
git clone https://github.com/facebookresearch/emg2pose
cd emg2pose
# 2) 환경 설치
conda env create -f environment.yml
conda activate emg2pose
pip install -e .
pip install -e emg2pose/UmeTrack
# 3) Sanity Check Train / Eval
python -m emg2pose.train \
train=True \
eval=True \
experiment=tracking_vemg2pose \
trainer.max_epochs=5 \
data_split=mini_split \
data_location="${HOME}/emg2pose_dataset_mini"
# 4) EMG2Pose 공식 데이터셋 다운
cd ~ && curl https://fb-ctrl-oss.s3.amazonaws.com/emg2pose/emg2pose_dataset.tar -o emg2pose_dataset.tar
tar -xvf emg2pose_dataset.tar
# 5) 사전학습 실행
python -m emg2pose.train \
train=True \
eval=True \
experiment=tracking_vemg2pose \
data_location="${HOME}/emg2pose_dataset"
# 6) 사전학습된 Checkpoints 불러오기
cd ~ && curl "https://fb-ctrl-oss.s3.amazonaws.com/emg2pose/emg2pose_model_checkpoints.tar.gz" -o emg2pose_model_checkpoints.tar.gz
tar -xvzf emg2pose_model_checkpoints.tar.gz
```

## Citation

```bibtex
@inproceedings{salteremg2pose,
  title={emg2pose: A Large and Diverse Benchmark for Surface Electromyographic Hand Pose Estimation},
  author={Salter, Sasha and Warren, Richard and Schlager, Collin and Spurr, Adrian and Han, Shangchen and Bhasin, Rohin and Cai, Yujun and Walkington, Peter and Bolarinwa, Anuoluwapo and Wang, Robert and others},
  booktitle={The Thirty-eight Conference on Neural Information Processing Systems Datasets and Benchmarks Track}
}
}

```
