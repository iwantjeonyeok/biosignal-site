# PhysioWave: A Multi-Scale Wavelet-Transformer for Physiological Signal Representation

> **PhysioWave: A Multi-Scale Wavelet-Transformer for Physiological Signal Representation**
> Yanlong Chen, Mattia Orlandi, Pierangelo Maria Rapa, Simone Benatti, Luca Benini, Yawei Li **NeurIPS 2025**

- [Paper (OpenReview)](https://arxiv.org/pdf/2506.10351)
- [Official code](https://github.com/ForeverBlue816/PhysioWave)
- [Preprocessing scripts folder](https://github.com/935963004/LaBraM/tree/main/dataset_maker)

## Motivation

기존 EMG 기반 딥러닝 모델들은 gesture recognition, muscle activity classification, hand pose estimation 등 특정 태스크에 맞춰 개별적으로 설계되는 경우가 많았다. 그러나 EMG 신호는 motion artifact, electrode shift, baseline drift와 같은 noise에 취약하고, 근수축에 따른 burst 형태의 sharp transient와 강한 비정상성을 가진다. 이 때문에 단순한 time-domain 분석이나 고정 window 기반 frequency-domain 방법만으로는 EMG의 생리학적으로 중요한 multi-scale time-frequency pattern을 충분히 표현하기 어렵다.

PhysioWave는 이러한 한계를 해결하기 위해 등장했다. Learnable wavelet decomposition을 통해 EMG 신호의 transient burst와 slow fluctuation을 multi-scale feature로 추출하고, frequency-guided masking을 통해 정보량이 높은 구간을 중심으로 자기지도 사전학습을 수행한다. 이를 통해 대규모 EMG 데이터에 특화된 pretrained representation을 학습하고, 다양한 EMG downstream task에서 더 강건한 성능을 얻는 것을 목표로 한다.

## Architecture Summary

PhysioWave는 근전도 신호의 다중 시간-주파수 특징을 학습하기 위해, 학습 가능한 웨이블릿 전처리부와 트랜스포머 인코더를 결합한 구조이다. 입력 근전도 신호는 일정 길이의 구간으로 나누어 사용하며, PhysioWave-EMG에서는 모든 데이터를 8채널, 1024개 샘플 길이, 2 kHz 샘플링 주파수로 통일한다. 또한 기존 방식처럼 고정된 대역통과 필터나 노치 필터를 적용하는 대신, 학습 가능한 웨이블릿 분해가 잡음 억제와 특징 추출을 모델 내부에서 함께 수행하도록 설계되었다.

모델은 여러 후보 웨이블릿 기저 중 입력 신호에 적합한 저주파 통과 필터와 고주파 통과 필터를 선택하고 조합한다. 이를 통해 근전도 신호에 포함된 순간적인 근활성 신호와 느린 변동 성분을 여러 주파수 대역의 하위 신호로 분해한다. 이후 각 하위 대역 특징은 적응형 게이팅과 서로 다른 스케일 간 특징 융합 과정을 거쳐 하나의 웨이블릿 기반 표현으로 통합된다.

사전학습은 주파수 정보를 이용한 마스킹 기반 복원 방식으로 수행된다. 먼저 각 패치의 푸리에 변환을 통해 스펙트럼 에너지를 계산하고, 정보량이 큰 패치가 더 자주 가려지도록 한다. 그런 다음 트랜스포머 인코더는 주변 문맥 정보를 바탕으로 가려진 부분의 특징을 복원하도록 학습된다. 즉, PhysioWave는 원시 근전도 파형 자체를 그대로 복원하는 것이 아니라, 웨이블릿 분해를 통해 얻어진 다중 스케일 특징 표현을 복원하도록 학습된다.

PhysioWave-emg는 Small, Base, Large 세 가지 크기(약 5M, 15M, 37M parameters)로 구성되며, Downstream task에서는 pretrained encoder에 lightweight MLP head를 붙여 end-to-end fine-tuning한다.

## Pre-training Data Summary
NinaPro DB6/DB7/DB8, EMG2Pose, EMG2Qwerty를 포함한 약 823 GB의 공개된 EMG 데이터로 사전학습된다. 
다운스트림 데이터셋 3종(Ninapro DB5, EPN-612, UCI EMG-Gesture)은 사전학습 풀에서 명시적으로 제외된다.

### Uniform preprocessing
1. 기존의 Bandpass filter와 Notch filter **미적용**
2. 각 EMG 채널별 **z-score** 정규화 수행
3. 모든 신호를 **2,000 Hz**로 리샘플링
4. 모든 입력을 **8채널**로 통일
5. Sliding window 방식으로 1024 sample window, 512 sample step 적용

사전학습 전처리 파이프라인은 [`db6_pretrain.py`](https://github.com/ForeverBlue816/PhysioWave/tree/main/EMG/)에 구현되어 있으며, 다운스트림 전용 스크립트(`epn_finetune.py`, `finetune_emg.sh`)도 같은 폴더에 있다.

## Pre-training Datasets

| # | Dataset | #Subjects | Size | #Ch | Rate (Hz) | Task / Description | Download |
|---|---------|:---------:|-------|:---:|:---------:|--------------------|----------|
| 1 | Ninapro DB6 | 10 | 20.3 GB | 14 | 2000 | Hand grasp recognition | <https://ninapro.hevs.ch/index.html> |
| 2 | Ninapro DB7 | 22 | 30.9 GB | 12 | 2000 | Hand(finger, wrist, and grasp) movement recognition | <https://ninapro.hevs.ch/index.html> |
| 3 | Ninapro DB8 | 12 | 23.6 GB | 16 | 1111 | Finger movement estimation | <https://ninapro.hevs.ch/index.html> |
| 4 | EMG2Pose | 193 | 431 GB | 16 | 2000 | Hand pose estimation | <https://github.com/facebookresearch/emg2pose> |
| 5 | EMG2Qwerty | 108 | 317 GB | 16 | 2000 | sEMG-based QWERTY typing / keypress decoding | <https://github.com/facebookresearch/emg2qwerty> |


**총계: ~738시간으로 모든 데이터셋은 공개 접근이 가능하다.**

## How to Reproduce the Pre-training Preprocessing

1. Physiowave를 clone하고 환경 설정 및 'requirements.txt'를 설치한다.
  ```bash
  git clone https://github.com/ForeverBlue816/PhysioWave.git
  cd PhysioWave
  ```
2. 원시 '.mat' 파일을 전처리하고 HDF5 파일로 저장한다.
  ```bash
  python EMG/db6_pretrain.py
  ```
3. 이후 다음 명령어로 EMG 사전학습을 실행한다.
  ```bash
  bash EMG/pretrain_emg.sh
  ```

## Citation

```bibtex
@article{chen2025physiowave,
  title={PhysioWave: A Multi-Scale Wavelet-Transformer for Physiological Signal Representation},
  author={Chen, Yanlong and Orlandi, Mattia and Rapa, Pierangelo Maria and Benatti, Simone and Benini, Luca and Li, Yawei},
  journal={arXiv preprint arXiv:2506.10351},
  year={2025}
}
```
