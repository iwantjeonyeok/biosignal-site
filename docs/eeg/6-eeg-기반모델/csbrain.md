# CSBrain — Cross-scale Spatiotemporal Brain Foundation Model

> **CSBrain: A Cross-scale Spatiotemporal Brain Foundation Model for EEG Decoding**
> Yuchen Zhou, Jiamin Wu, Zichen Ren, Zhouheng Yao, Weiheng Lu, Kunyu Peng, Qihao Zheng, Chunfeng Song, Wanli Ouyang, Chao Gou. **NeurIPS 2025.**

- [Paper (arXiv)](https://arxiv.org/abs/2506.23075)
- [Official code](https://github.com/yuchen2199/CSBrain)
- [Downstream preprocessing folder](https://github.com/yuchen2199/CSBrain/tree/main/preprocessing)

## Motivation

CBraMod를 포함한 기존 EEG 기반모델들은 NLP 및 컴퓨터 비전에서 성공을 거둔 **단일 스케일 밀집(dense) 모델링 패러다임**을 그대로 차용한다. 그러나 이는 EEG 신경 활동의 핵심 특성, 즉 **크로스 스케일 시공간 구조**를 간과한다. EEG 태스크 패턴은 시간 스케일 면에서 수십 밀리초의 짧은 이벤트 관련 전위(ERP)부터 수 초에 걸친 느린 뇌파 리듬까지 다양하고, 공간 스케일 면에서도 단일 전극 근방의 국소 피질 반응부터 여러 뇌 영역에 분산된 상호작용까지 아우른다. 이러한 다중 스케일 구조를 무시하고 단일 스케일로 표현하면 표현력이 부족하고 태스크 간 일반화가 약해진다는 것이 CSBrain의 핵심 문제 인식이다.

## Architecture Summary

CSBrain은 두 가지 핵심 컴포넌트를 교대로 쌓는 구조를 가진다. 첫 번째는 **Cross-scale Spatiotemporal Tokenization(CST)**이다. 국소 시간 윈도우와 해부학적 뇌 영역을 기준으로 다중 스케일의 시공간 특징을 추출하고, 이를 컴팩트한 스케일 인식 토큰(scale-aware token)으로 집계한다. 서로 다른 시간·공간 스케일의 정보를 별도의 토큰 표현으로 유지함으로써 스케일 다양성을 보존한다. 두 번째는 **Structured Sparse Attention(SSA)**이다. 서로 다른 시간 윈도우 간, 그리고 서로 다른 뇌 영역 간의 의존성을 선택적으로 포착하는 희소 어텐션으로, 관련 없는 패치 간 허위 상관(spurious correlation)을 제거하면서 다중 스케일 의존성을 효율적으로 모델링한다. CST와 SSA를 반복적으로 쌓아 점진적으로 다중 스케일 의존성을 통합한다. 사전학습은 CBraMod와 동일한 TUEG 코퍼스(>9,000시간)에서 마스크 오토인코딩 목표로 수행되며, 11개 EEG 태스크·16개 데이터셋에서 평가된다.

## Pre-training Data Summary

CSBrain은 **CBraMod와 동일한 사전학습 코퍼스 및 전처리 파이프라인**을 채택한다:

- **데이터셋:** Temple University Hospital EEG Corpus (TUEG)
- **전처리 후:** **EEG 세그먼트 1,109,545개 (>9,000시간)** — CBraMod와 완전히 동일한 풀.
- 사전학습 목표: masked autoencoding, 50% 마스킹, 4× A100에서 40 에폭.

### Preprocessing (paper §3.1)
1. Band-pass **0.3–75 Hz**, notch filter **60 Hz**.
2. **200 Hz**로 리샘플링; 비중첩 **30초** 윈도우로 분할.
3. 진폭을 100 µV로 clipping하여 범위를 [-1, 1]로 조정.

CSBrain README는 TUEG 사전학습 전처리에 대해 **"CBraMod를 따르라"**고 명시하고 있다: <https://github.com/wjq-learning/CBraMod/blob/main/preprocessing/preprocessing_tueg_for_pretraining.py>

CSBrain 저장소의 [`preprocessing/`](https://github.com/yuchen2199/CSBrain/tree/main/preprocessing) 폴더에는 CBraMod에서 다루지 않은 **다운스트림** 데이터셋 3종(**HMC**, **Siena**, **TUSL**)의 스크립트만 포함되어 있다.

## Pre-training Dataset

| Dataset | Segments | Hours | Rate (Hz) | Access |
|---------|----------|-------|-----------|--------|
| TUEG (Temple Univ. Hospital EEG Corpus) | 1,109,545 | >9,000 | 200 (after resampling) | Free registration → <https://isip.piconepress.com/projects/nedc/html/tuh_eeg/> |

## Downstream datasets (16 datasets / 11 tasks — not used for pre-training)

BCIC-IV-2a, PhysioNet-MI, SHU-MI, FACED, SEED-V, CHB-MIT, Siena, ISRUC, HMC, BCIC2020-3, SEED-VIG, MentalArithmetic, Mumtaz2016, TUEV, TUAB, TUSL. HMC/Siena/TUSL는 CSBrain의 `preprocessing/` 폴더를, 나머지는 [CBraMod preprocessing folder](https://github.com/wjq-learning/CBraMod/tree/main/preprocessing)를 참고한다.

## How to reproduce the pre-training preprocessing

```bash
# 1) TUH에서 TUEG를 다운로드한다(무료, 등록 필요).
# 2) CBraMod를 clone하고 TUEG 전처리 스크립트를 실행한다:
git clone https://github.com/wjq-learning/CBraMod
python CBraMod/preprocessing/preprocessing_tueg_for_pretraining.py
# 3) CSBrain을 clone하고 사전학습을 시작한다:
git clone https://github.com/yuchen2199/CSBrain
cd CSBrain && bash sh/pretrain_CSBrain.sh
```

## Citation

```bibtex
@inproceedings{zhou2025csbrain,
  title={{CSBrain}: A Cross-scale Spatiotemporal Brain Foundation Model for {EEG} Decoding},
  author={Zhou, Yuchen and Wu, Jiamin and Ren, Zichen and Yao, Zhouheng and Lu, Weiheng and Peng, Kunyu and Zheng, Qihao and Song, Chunfeng and Ouyang, Wanli and Gou, Chao},
  booktitle={Advances in Neural Information Processing Systems (NeurIPS)},
  year={2025}
}
```
