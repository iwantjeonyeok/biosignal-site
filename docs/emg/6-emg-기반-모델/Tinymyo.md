# TinyMyo — A Tiny Foundation Model for Flexible EMG Signal Processing at the Edge

> **TinyMyo: A Tiny Foundation Model for Flexible EMG Signal Processing at the Edge**
> Matteo Fasulo, Giusy Spacone, Thorir Mar Ingolfsson, Yawei Li, Luca Benini, and Andrea Cossettini **arXiv preprint**

- 논문 (arXiv): https://arxiv.org/pdf/2512.15729
- 공식 코드: https://github.com/pulp-bio/BioFoundation

## Pre-training Data Summary

TinyMyo는 세 개의 공개 sEMG 데이터셋을 결합한 총 약 **482.2 GB** 규모의 EMG 데이터로 사전학습합니다. 모든 데이터는 2 kHz sampling rate 기준으로 수집되었으며, 전처리 후 1000-sample window, 즉 **0.5초** 길이의 segment로 분할됩니다.

- **Ninapro DB6**: 10명, 14채널, 2kHz, Forearm sEMG, **20.3 GB**
- **Ninapro DB7**: 22명, 12채널, 2kHz, Forearm sEMG, **30.9 GB**
- **EMG2Pose**: 192명, 16채널, 2kHz, Wrist sEMG, **431 GB**
- **최종 사전학습 규모**: 약 482.2 GB
  - 논문에서 최종 segment/sample 개수는 명시하지 않음

## Preprocessing Pipeline

1. 원시 sEMG recording을 불러오고, 데이터셋별 채널 수와 Sampling Rate를 확인
2. **Butterworth band-pass filter** 적용
    - 4차 Butterworth filter
    - 주파수 대역: 20 - 450Hz
3. **Notch filter** 적용
    - 50Hz Notch filter
4. Channel-wise **Min-Max** normalization(각 EMG 채널별로 정규화)
5. 고정길이 window로 segmentation
    - window 길이: **1000 samples**
    - overlap: **50%**
6. 채널 수 통일
    - 16채널로 **Zero-Padding** 적용

## Pre-training Dataset

| 데이터셋 | 환자 수 | Class 수 | Channel 수 | 접근 방법 |
|---------|--------|--------|-------------------|----------|
| Ninapro DB6 | 10명 | 7 | 14 | 공개 |
| Ninapro DB7 | 22명 | 40 | 12 | 공개 |
| EMG2pose | 192명 | 29 | 16 | 공개 |
| **합계 (사전학습)** | 224명 | — | — | — |

**모델 구조 및 사전학습 방법 (TinyMyo)**

TinyMyo는 시계열 EMG 신호를 패치 단위로 분할한 뒤 Transformer 인코더로 표현을 학습하는 구조를 사용합니다. 입력 EMG는 일정 길이의 window로 나뉘며, 각 window는 다시 여러 patch/token으로 변환되어 Transformer에 입력됩니다. 모델은 EMG의 시간적 패턴과 근활성 변화 양상을 latent representation으로 학습하는 것을 목표로 합니다.

사전학습은 EMG 신호의 일부 구간을 가리고 이를 복원하도록 학습하는 **masked reconstruction** 기반 자기지도학습 방식을 사용합니다.

- **Channel-independent patching**: EMG의 각 채널을 독립적으로 temporal patch로 나누고 embedding. 이는 각 EMG 채널이 서로 다른 anatomical location을 반영한다는 점을 고려한 설계.
- **SimMIM-inspired masked reconstruction**: Random subset의 EMG patch token을 learnable mask token으로 대체하고, 주변 visible token 정보를 이용해 masked patch를 복원
- **Reconstruction objective**: 복원 손실은 원본 EMG patch와 예측 patch 사이의 Smooth L1 loss를 기반, visible patch loss는 낮은 가중치로 반영하여 unmasked input 과적합 방지

## Downstream Datasets

TinyMyo는 아래 다운스트림 태스크들로 평가되며 사전학습에 사용된 데어타와는 별개의 데이터셋을 사용하여 일반화 성능을 검증합니다.

| 태스크 | 데이터셋 | Subject 수 | 비고 |
|-------|---------|--------|------|
| 손동작 분류 | Ninapro DB5 | 10명 | 52개 hand-wrist movement 분류
| 손동작 분류 | EPN-612 | 612명 | 5개 hand movement 분류 | 
| 손동작 분류 | UCI-EMG | 36명 | 7개 hand movement 분류 |
| Discrete gesture 분류 | Generic Neuromotor interface, GNI | 100명 | Character-level error rate 평가
| 손 운동학 회귀 | Ninapro DB8 | 12명 | MAE 평가
| Silent speech production | Gaddy Silent Speech Dataset | 1명 | WER 기반 speech synthesis/recognition 평가

**주요 결과**: Ninapro DB5 89.41%, EPN-612 96.74%, UCI-EMG 97.56%의 accuracy를 달성했습니다. 또한 GNI discrete gesture task에서는 CLER 0.144, Ninapro DB8 hand kinematic regression에서는 MAE 8.77, silent speech production에서는 WER 33.54%, silent speech recognition에서는 WER 33.95%를 보고했습니다.

## How to Reproduce the Pre-training Preprocessing

```bash
# 1) 사전학습 데이터 접근
#    TinyMyo pre-training은 Ninapro DB6, Ninapro DB7, EMG2Pose를 사용
#    - NinaPro DB6 / DB7: 공식 NinaPro 데이터셋 접근 필요
#      https://ninapro.hevs.ch/instructions/DB6.html
#    - EMG2Pose: 공개 데이터셋 접근 필요
#      https://github.com/facebookresearch/emg2pose
# 2) TinyMyo 학습 가중치 다운로드
#    https://huggingface.co/PulpBio/TinyMyo/tree/main
# 3) 코드 클론
git clone https://github.com/pulp-bio/BioFoundation
# 4) 환경 설치
conda create -n BioFoundation python=3.10
conda activate BioFoundation
pip install -r requirements.txt
# 5) TinyMyo EMG preprocessing script용 추가 dependency 설치
pip install -r scripts/requirements.txt
# 6) 데이터 경로 설정 - 본인 환경에 맞게 수정
export DATA_PATH=/path/to/your/data
# 7) 사전학습 데이터 전처리
#    TinyMyo pretraining preprocessing:
#    Sampling rate: 2000 Hz
#    Seq_len= 1000 samples = 0.5 s window
#    Stride = 500 samples = 50% overlap
#    HDF5 format으로 변환
# 8) 사전학습 실행
python -u run_train.py +experiment=TinyMyo_pretrain
```

## Citation

```bibtex
@misc{fasulo2026tinymyotinyfoundationmodel,
      title={TinyMyo: a Tiny Foundation Model for Flexible EMG Signal Processing at the Edge},
      author={Matteo Fasulo and Giusy Spacone and Thorir Mar Ingolfsson and Yawei Li and Luca Benini and Andrea Cossettini},
      year={2026},
      eprint={2512.15729},
      archivePrefix={arXiv},
      primaryClass={eess.SP}
}

```
