# HeartLang — ECG Language Model

> **Reading Your Heart: Learning ECG Words and Sentences via Pre-training ECG Language Model**
> Jiarui Jin, Haoyu Wang, Hongyan Li, Jun Li, Jiahui Pan, Shenda Hong. **ICLR 2025.**

- [Paper (OpenReview)](https://openreview.net/forum?id=6Hz1Ko087B)
- [Official code](https://github.com/PKUDigitalHealth/HeartLang)
- [Preprocessing scripts folder](https://github.com/PKUDigitalHealth/HeartLang/tree/main/datasets/dataset_preprocess)

## Motivation

기존 ECG 기반 딥러닝 모델은 대규모 고품질 라벨 데이터에 의존하며, 특정 데이터셋과 과제에 맞춰 설계되는 경우가 많아 새로운 임상 과제에 일반화하는 데 한계가 있다. 이를 해결하기 위해 ECG 자기지도학습이 발전해왔지만, 대부분의 기존 방법은 ECG를 일반적인 시계열 데이터처럼 취급하여 고정된 크기와 간격으로 신호를 분할한다. 이러한 방식은 ECG의 핵심적인 특성인 개별 심박의 형태 정보와 전체 심장 리듬의 흐름을 충분히 반영하지 못하며, 심박 사이에 존재할 수 있는 잠재적 의미 관계도 약화시킬 수 있다. 특히 ECG 진단에서는 단일 심박의 형태 변화와 여러 심박이 만드는 리듬 패턴이 모두 중요하기 때문에, ECG 신호의 고유한 구조를 반영한 표현학습 방식이 필요하다. HeartLang은 이러한 한계를 해결하기 위해 심박 단위와 리듬 단위를 중심으로 ECG를 재구성하고, 라벨 없이도 심박의 형태 수준 표현과 리듬 수준 표현을 함께 학습하는 새로운 ECG 자기지도학습 프레임워크를 제안한다.

## Architecture Summary

HeartLang의 핵심은 ECG를 “심박은 단어, 리듬은 문장”으로 바라보는 **ECG 언어 처리** 구조다. 이 관점에 따라 **QRS-Tokenizer**는 원시 12유도 ECG에서 QRS Complex를 찾아 실제 심박이 나타나는 위치를 기준으로 신호를 나눈다. 이렇게 나뉜 개별 심박 조각은 ECG 단어가 되고, 여러 ECG 단어를 시간 순서에 따라 연결한 것은 ECG 문장이 된다. 심박수에 따라 ECG 문장의 길이가 달라질 수 있으므로, 길이가 짧으면 빈 조각을 채우고 길이가 길면 일부를 잘라 입력 길이를 맞춘다. 생성된 ECG 문장은 **ST-ECGFormer**에 입력된다. ST-ECGFormer는 각 ECG 단어의 파형 정보뿐 아니라, 해당 심박이 어느 유도에서 나온 것인지, ECG 기록의 어느 시간 위치에 있는지, 그리고 문장 안에서 어떤 순서를 가지는지를 함께 반영하는 트랜스포머 기반 구조다. 이를 통해 HeartLang은 개별 심박의 형태와 여러 심박이 이어지며 만들어내는 리듬 흐름을 함께 학습한다. 사전학습은 ECG vocabulary를 이용해 심박 형태를 학습하는 **VQ-HBR** 단계와, 일부 ECG 단어를 가리고 예측하면서 리듬 문맥을 학습하는 **masked ECG sentence pre-training** 단계로 구성된다. 후속 평가에서는 총 3개 공개 ECG 데이터셋의 6개 벤치마크 설정에서 성능을 검증한다.

## Pre-training Data Summary
HeartLang은 MIMIC-IV-ECG를 사용하여 VQ-HBR training과 masked ECG sentence pre-training을 수행한다.

- **데이터셋:** MIMIC-IV-ECG Diagnostic ECG Matched Subset
- **원시 규모:** 161,352명 피험자 · 800,035개 12유도 ECG 기록 · 각 기록 10초 길이 · 500 Hz 샘플링
- **전처리 후:** 전체 ECG 기록을 100 Hz로 다운샘플링한 뒤, QRS-Tokenizer를 통해 800,035개의 ECG sentence로 변환. 학습/검증 데이터는 9:1로 분할되어 720,031개 train sample과 80,004개 validation sample로 사용됨

### Preprocessing Pipeline


1. MIMIC-IV-ECG의 raw ECG recording에서 `NaN`과 `Inf` 값은 주변 6개 point의 평균값으로 대체.
2. 모든 ECG recording을 500 Hz에서 **100 Hz**로 downsampling.
3. **QRS-Tokenizer**를 사용하여 raw ECG recording을 통일된 ECG sentence 형태로 변환.
4. QRS detection을 위해 lead I 신호에 **5–20 Hz band-pass filter**를 적용하고, Ricker wavelet 기반 moving wave integration을 수행.
5. moving wave integration signal의 local maxima를 탐색하여, refractory period 이후에 QRS detection threshold를 넘는 지점을 QRS complex로 판정.
6. 검출된 QRS complex index를 중심으로 각 lead의 심박 구간을 분할. 분할된 구간이 time window size인 **t = 96**보다 짧으면 zero padding을 적용
7. 12-lead에서 추출된 개별 심박 조각을 순서대로 연결해 ECG sentence를 구성. 논문에서는 ECG sentence의 최대 길이를 **l = 256**, 각 ECG word의 time window size를 **t = 96**으로 설정.
8. 문장 길이가 **l**보다 짧으면 zero-filled patch로 padding하고, **l**보다 길면 truncation을 적용해 길이를 통일

공식 README 기준으로 MIMIC-IV preprocessing은 `mimic_preprocess.py`로 수행하고, ECG sentence generation은 [`QRSTokenizer.py`](https://github.com/PKUDigitalHealth/HeartLang/blob/main/QRSTokenizer.py)로 수행한다.

## Pre-training Dataset

| Dataset | Subjects | Raw hours | #Samples after preprocessing | Rate (Hz) | Access |
|---------|----------|-----------|------------------------------|-----------|--------|
| MIMIC-IV-ECG Diagnostic ECG Matched Subset | 161,352명 | 약 2,222시간 (800,035 × 10초) | 800,035 ECG sentences (720,031 train / 80,004 valid) | 500 → 100 | PhysioNet credentialed access (무료) → https://physionet.org/content/mimic-iv-ecg/ |

## Downstream Datasets
HeartLang은 아래 3개의 공개 ECG 데이터셋에서 총 6가지 benchmark setting으로 평가된다. PTB-XL은 Superclass, Subclass, Form, Rhythm 네 가지 task로 나누어 사용되며, CPSC2018과 Chapman-Shaoxing-Ningbo(CSN)는 각각 9개 label, 38개 label 분류 task로 평가된다.
Downstream dataset preprocessing code와 fine-tuning scripts는 아래 링크를 참고한다.

- Downstream dataset preprocessing code: [`datasets/dataset_preprocess`](https://github.com/PKUDigitalHealth/HeartLang/tree/main/datasets/dataset_preprocess)  
- Fine-tuning scripts: [`scripts/finetune`](https://github.com/PKUDigitalHealth/HeartLang/tree/main/scripts/finetune)

## How to Reproduce the Pre-training Preprocessing

```bash
# 1) MIMIC-IV-ECG 접근 (PhysioNet credentialed access 필요, 무료)
# https://physionet.org/content/mimic-iv-ecg/

# 2) HeartLang 클론
git clone https://github.com/PKUDigitalHealth/HeartLang.git
cd HeartLang

# 3) 환경 설정
conda create -n heartlang python=3.9
conda activate heartlang
pip install -r requirements.txt

# 4) MIMIC-IV-ECG 전처리
python mimic_preprocess.py \
  --dataset_path <path_to_MIMIC_data> \
  --output_path datasets/ecg_datasets/MIMIC-IV

# 5) QRS-Tokenizer로 ECG sentences 생성
python QRSTokenizer.py --dataset_name MIMIC-IV

# 6) VQ-HBR 학습 (ECG vocabulary 구축)
bash scripts/vqhbr/MIMIC-IV.sh

# 7) Masked ECG sentence pre-training 실행
bash scripts/pretrain/MIMIC-IV.sh
```

## Citation

```bibtex
@inproceedings{
  jin2025reading,
  title={Reading Your Heart: Learning {ECG} Words and Sentences via Pre-training {ECG} Language Model},
  author={Jiarui Jin and Haoyu Wang and Hongyan Li and Jun Li and Jiahui Pan and Shenda Hong},
  booktitle={The Thirteenth International Conference on Learning Representations},
  year={2025},
  url={https://openreview.net/forum?id=6Hz1Ko087B}
}
```
