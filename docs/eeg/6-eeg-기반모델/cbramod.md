# CBraMod — Criss-Cross Brain Foundation Model
> **CBraMod: A Criss-Cross Brain Foundation Model for EEG Decoding**
> Jiquan Wang, Sha Zhao, Zhiling Luo, Yangxuan Zhou, Haiteng Jiang, Shijian Li, Tao Li, Gang Pan. **ICLR 2025.**

- [Paper (OpenReview)](https://openreview.net/forum?id=NPNUHgHF2w)
- [Official code](https://github.com/wjq-learning/CBraMod)
- [Preprocessing scripts folder](https://github.com/wjq-learning/CBraMod/tree/main/preprocessing)

## Motivation

기존 EEG 기반모델들이 안고 있는 두 가지 핵심 문제를 해결하는 것이 CBraMod의 출발점이다. 첫째, 대부분의 선행 모델들은 모든 EEG 패치에 걸쳐 공간(채널 간) 의존성과 시간(시계열) 의존성을 동시에 하나의 어텐션 연산으로 처리한다. 그러나 EEG 신호의 공간적 관계(전극 위치와 뇌 기능 지형)와 시간적 패턴(리듬, 스파이크 등)은 본질적으로 서로 다른 성질을 가지므로, 이를 혼합해 모델링하면 각 의존성의 고유한 구조가 희석된다. 둘째, EEG 데이터는 실험마다 채널 수, 샘플링 레이트, 전극 배치가 제각각이어서, 고정된 포맷을 전제로 설계된 모델은 다양한 BCI 태스크 및 데이터셋에 범용적으로 적용하기 어렵다.

## Architecture Summary

CBraMod의 핵심은 **Criss-Cross Transformer** 백본이다. EEG 신호를 패치로 분할한 뒤, 공간 어텐션과 시간 어텐션을 두 개의 독립적인 병렬 메커니즘으로 분리하여 처리한다. 공간 어텐션은 동일 시간대의 전극 간 관계를 모델링하고, 시간 어텐션은 동일 채널 내의 시계열 패턴을 모델링한다. 이 두 어텐션의 출력을 결합함으로써 EEG의 이질적 공간·시간 구조를 각각 온전히 포착한다. 포맷 유연성은 **비대칭 조건부 위치 인코딩(ACPE, Asymmetric Conditional Positional Encoding)**으로 해결한다. 패치의 위치 정보를 입력 포맷에 조건부로 인코딩하기 때문에, 채널 수나 시간 길이가 다른 EEG 데이터도 별도의 재학습 없이 처리할 수 있다. 사전학습은 TUEG 전체 코퍼스(약 9,000시간, 110만 샘플)에서 **패치 기반 마스크 EEG 재구성** 목표로 수행되며, 10개 BCI 태스크(12개 공개 데이터셋)에서 평가된다.

## Pre-training Data Summary

LaBraM(약 20개 데이터셋 통합)과 달리, CBraMod는 **단일하지만 매우 대규모**인 코퍼스로만 사전학습된다:

- **데이터셋:** Temple University Hospital EEG Corpus (TUEG), v2.0.0
- **원시 규모:** 69,652개 임상 EEG 레코딩 • 14,987명 피험자 • 26,846개 세션 • ~27,062시간 (전극 구성 40종 이상, 주로 256 Hz 샘플링)
- **전처리 후:** **EEG 샘플 1,109,545개 (>9,000시간)**, LaBraM 사전학습 풀보다 현저히 큰 규모.

### Preprocessing Pipeline (paper §3.1)

1. 5분 미만 레코딩 제외; 각 레코딩의 첫 1분·마지막 1분 제거.
2. 10–20 계 공통 19채널만 유지: `Fp1, Fp2, F7, F3, Fz, F4, F8, T3, C3, Cz, C4, T4, T5, P3, Pz, P4, T6, O1, O2`.
3. Band-pass filter **0.3–75 Hz**, notch filter **60 Hz**.
4. **200 Hz**로 리샘플링 후 비중첩 **30초** 윈도우로 분할.
5. 진폭이 100 µV를 초과하는 윈도우 제거 후, 100 µV 단위로 정규화하여 값의 범위를 약 [-1, 1]로 조정.

저자들이 사용한 스크립트는 [`preprocessing/preprocessing_tueg_for_pretraining.py`](https://github.com/wjq-learning/CBraMod/blob/main/preprocessing/preprocessing_tueg_for_pretraining.py)에서 확인할 수 있다.

## Pre-training Dataset

| Dataset | Subjects | Sessions | Raw hours | #Samples after cleaning | Rate (Hz) | Access |
|---------|----------|----------|-----------|-------------------------|-----------|--------|
| TUEG (Temple Univ. Hospital EEG Corpus) | 14,987 | 26,846 | ~27,062 | 1,109,545 (>9,000 h) | 256 (mixed) | Free registration → <https://isip.piconepress.com/projects/nedc/html/tuh_eeg/> |

## Downstream Datasets

CBraMod는 10개 BCI 태스크에 걸친 12개 공개 데이터셋(FACED, SEED-V, PhysioNet-MI, SHU-MI, ISRUC, CHB-MIT, BCIC2020-3, Mumtaz2016, SEED-VIG, MentalArithmetic, TUEV, TUAB)에서 평가된다. 각 데이터셋의 개별 전처리 스크립트는 같은 [`preprocessing/`](https://github.com/wjq-learning/CBraMod/tree/main/preprocessing) 폴더에 있다.

## How to Reproduce the Pre-training Preprocessing

```bash
# 1) TUEG 접근 권한을 신청하고 코퍼스를 다운로드한다(무료)
#    https://isip.piconepress.com/projects/nedc/html/tuh_eeg/
# 2) CBraMod를 clone한다
git clone https://github.com/wjq-learning/CBraMod
cd CBraMod && pip install -r requirements.txt
# 3) TUEG 사전학습 전처리 스크립트를 실행한다(스크립트 내 경로 수정 필요)
python preprocessing/preprocessing_tueg_for_pretraining.py
# 4) 사전학습을 시작한다
python pretrain_main.py
```

## Citation

```bibtex
@inproceedings{wang2025cbramod,
  title={CBraMod: A Criss-Cross Brain Foundation Model for EEG Decoding},
  author={Wang, Jiquan and Zhao, Sha and Luo, Zhiling and Zhou, Yangxuan and Jiang, Haiteng and Li, Shijian and Li, Tao and Pan, Gang},
  booktitle={The Thirteenth International Conference on Learning Representations (ICLR)},
  year={2025}
}
```
