
> **ECG-FM: An Open Electrocardiogram Foundation Model**
> Kaden McKeen, Sameer Masood, Augustin Toma, Barry Rubin, Bo Wang. **JAMIA Open 2025.**

- [Paper (arXiv)](https://arxiv.org/abs/2408.05178)
- [Official code](https://github.com/bowang-lab/ECG-FM/.)
- [Preprocessing scripts folder](https://github.com/Jwoo5/fairseq-signals)

## Motivation

기존 ECG 분석 모델은 특정 task에 맞춰 설계되는 경우가 많아, 새로운 임상 과제에 적용하려면 여전히 많은 라벨 데이터와 추가 학습이 필요하다. Foundation model은 자기지도 사전학습을 통해 이러한 부담을 줄일 수 있지만, ECG 분야에서는 공개된 모델 가중치와 코드가 부족해 재현성과 연구 간 비교 가능성이 낮다는 문제가 있다. 또한 기존 생성 기반 자기지도학습은 마스킹된 신호 복원에 집중해 국소적 구조 학습에 치우칠 수 있고, 대조 학습 기반 방법은 데이터 증강 과정에서 ECG의 생리학적 의미가 왜곡되는 문제가 발생할 수 있다. ECG-FM은 이러한 한계를 보완하기 위해 생성 기반 학습과 대조 학습을 결합한 hybrid self-supervised learning 방식으로 사전학습된 open-weight ECG foundation model을 제안하고, ECG foundation model의 활용 장벽을 낮추며 다양한 ECG downstream task에서의 재현 가능한 비교 기준을 제공하는 것을 목표로 한다.

**Architecture Summary**

ECG-FM은 **wav2vec 2.0** 구조를 기반으로 한 transformer-based ECG foundation model이다. 입력 ECG waveform은 CNN feature extractor를 거쳐 latent representation으로 변환되고, 이후 BERT-like Transformer encoder를 통해 문맥 정보가 반영된 ECG representation으로 인코딩된다. 모델은 총 90.9M parameters규모이며, ECG 신호의 구간별 특징을 Transformer 기반 표현으로 학습하도록 설계된다.사전학습은 WCR(W2V + CMSC + RLM)이라는 **hybrid self-supervised learning** 방식으로 이루어진다. **wav2vec 2.0 objective**는 CNN latent representation의 일부 구간을 masking하고, 주변 문맥을 이용해 해당 위치의 quantized target을 구별하도록 학습하여 ECG의 local pattern을 포착한다. 반면 **CMSC**는 시간적으로 인접한 ECG segment를 positive pair로 두고 global representation 간 contrastive learning을 수행하여, 심장 기능과 관련된 전역적 의미 표현을 학습한다. 이 방식은 augmentation을 사용하지 않아 생리학적 의미가 왜곡되는 faulty alignment 문제를 줄이는 역할을 한다. 또한 **RLM**은 사전학습 중 각 ECG lead를 확률적으로 masking하는 ECG-specific augmentation 전략이다. 이를 통해 모델은 특정 lead 조합에만 의존하지 않고 다양한 lead 구성에서도 안정적인 표현을 학습할 수 있으며, 표준 12-lead ECG뿐 아니라 일부 lead만 존재하는 reduced lead setting에서도 fine-tuning될 수 있는 유연성을 갖는다. 

**Pre-training Data Summary**

ECG-FM은 두 개의 공개 데이터셋을 결합한 **약 87만 개의 ECG**로 사전학습한다. 5초 단위로 분할 후 **총 약 175만 개의 샘플**이 실제 학습에 사용된다.

- **데이터셋**: PhysioNet 2021, MIMIC-IV-ECG
- **원시 규모**: PhysioNet 2021(87,662개 · ECG피험자 수 NR), MIMIC-IV-ECG(800,035개 ECG · 161,352명 피험자)
- **전처리 후**: 873,706개 ECG, 5초 단위로 분할된 1,757,054개 sample

-Preprocessing procedure

1. 원시 파형(raw waveform) 및 메타데이터(sample rate, 환자 정보 등) 추출
2. 선형 보간(linear interpolation)으로 **500 Hz resampling**
3. **Z-score normalization** 수행
4. 비중첩 **5초 단위 segment** 분할 (CMSC contrastive learning의 positive pair 생성 목적)
5. null 값 또는 상수 리드(constant lead)가 포함된 샘플 제거


-Pre-training Datasets

| Dataset | Subjects | RAW ECG 수 | Rate (Hz) | Access |
|---|---:|---:|---:|---|
| PhysioNet 2021 | 178,140명 | 625,139개 | → 500 | 공개 → https://physionet.org/content/challenge-2021/ |
| MIMIC-IV-ECG | 161,352명 | 800,035개 | → 500 | PhysioNet 계정 필요 (무료) → https://physionet.org/content/mimic-iv-ecg/ |


**Downstream Datasets**

ECG-FM은 UHN-ECG와 MIMIC-IV-ECG의 2개 데이터셋을 기반으로, UHN-ECG interpretation, MIMIC-IV-ECG machine reads, UHN-ECG reduced LVEF의 총 3개 downstream task에서 평가되었다.

**How to Reproduce the Pre-training Preprocessing**
```bash
# 1) ECG-FM 공식 구현체인 fairseq-signals 설치
git clone https://github.com/Jwoo5/fairseq-signals
cd fairseq-signals
pip install --editable ./
pip install pandas scipy wfdb pyarrow

# 2) PhysioNet 2021 데이터 다운로드 및 전처리
#    https://physionet.org/content/challenge-2021/
python fairseq_signals/data/ecg/preprocess/preprocess_physionet2021.py \
    /path/to/physionet2021/ --dest /path/to/output --workers $N

# 3) MIMIC-IV-ECG 데이터 다운로드 및 전처리 (PhysioNet credentialed access 필요)
#    https://physionet.org/content/mimic-iv-ecg/
python fairseq_signals/data/ecg_text/preprocess/preprocess_mimic_iv_ecg.py \
    /path/to/mimic-iv-ecg --dest /path/to/output

# 4) W2V+CMSC+RLM (WCR) 사전학습 실행
fairseq-hydra-train --config-dir examples/w2v_cmsc/config/pretraining \
    --config-name w2v_cmsc_rlm
```

**Citation**

```bibtex
@article{mckeen2024ecgfm,
  title={ECG-FM: An Open Electrocardiogram Foundation Model},
  author={McKeen, Kaden and Masood, Sameer and Toma, Augustin and Rubin, Barry and Wang, Bo},
  journal={JAMIA Open},
  year={2025},
  url={https://arxiv.org/abs/2408.05178}
}
```
