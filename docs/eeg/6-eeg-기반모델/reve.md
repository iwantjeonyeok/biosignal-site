# REVE — Representation for EEG with Versatile Embeddings

> **REVE: A Foundation Model for EEG Adapting to Any Setup with Large-Scale Pre-training on 25,000 Subjects**
> Yassine El Ouahidi, Jonathan Lys, Philipp Thölke, Nicolas Farrugia, Bastien Pasdeloup, Vincent Gripon, Karim Jerbi, Giulia Lioi. **NeurIPS 2025.**

- [Project page](https://brain-bzh.github.io/reve/)
- [Official code](https://github.com/elouayas/reve_eeg)
- [Preprocessing folder](https://github.com/elouayas/reve_eeg/tree/main/preprocessing)

## Motivation

EEG 데이터는 언어나 이미지와 달리 극심한 이질성(heterogeneity)을 지닌다. 수집 기관마다 전극 수(수십 개~수백 개), 전극 배치(10-20, 10-5 등), 샘플링 레이트, 기록 프로토콜이 제각각이기 때문에, 언어·비전 기반모델에서는 당연한 전제였던 "동일 포맷 대규모 코퍼스"가 EEG에서는 성립하지 않는다. 기존 EEG 기반모델들은 이 문제를 단일 전극 설정으로 사전학습 데이터를 제한하거나, 특정 채널 집합으로 강제 정규화하는 방식으로 우회했다. 그 결과 표현 품질이 떨어지고, 특히 파인튜닝 없이 선형 프로브만 붙였을 때의 성능이 매우 낮았다. REVE는 임의의 전극 배치와 임의의 신호 길이를 그대로 수용할 수 있는 아키텍처를 설계하여, EEG 연구에서 표준으로 삼을 수 있는 진정한 범용 사전학습 모델을 제시하는 것을 목표로 한다.

## Architecture Summary

REVE의 핵심 기여는 **4D 위치 인코딩(4D Positional Encoding)**이다. 전극의 두피 위 3차원 좌표(x, y, z)를 공간 위치 정보로, 각 시간 패치의 시간축 인덱스를 1차원 시간 위치 정보로 활용하여 총 4D로 위치를 표현한다. 이 인코딩 방식은 훈련에서 보지 못한 전극 배치나 신호 길이에도 외삽(extrapolation)이 가능하므로, 사전학습 데이터에 없던 장비·설정의 EEG도 처리할 수 있다. 사전학습 목표는 **마스크 오토인코딩(MAE)**이다. 입력 EEG 패치의 일부를 무작위로 마스킹하고 원래 신호를 재구성하는 방식으로, 전처리 후에도 100 µV 이상의 진폭을 클리핑하지 않는 관대한 정규화 정책(15σ 클리핑)을 채택해 실제 임상 신호의 다양성을 최대한 보존한다. 92개 데이터셋·25,000명 피험자·61,415시간의 역대 최대 규모 EEG 코퍼스에서 사전학습되었으며, 10개 다운스트림 태스크(운동 상상, 발작 감지, 수면 단계, 인지 부하, 감정 인식 등)에서 최소한의 파인튜닝만으로 최고 수준의 성능을 달성한다.

## Pre-training Data Summary

REVE는 현재까지 공개된 EEG 사전학습 코퍼스 중 **규모와 다양성 모두에서 압도적인 1위**를 기록한다:

- **92개 데이터셋 • 24,274명 피험자 • 150,833개 세션 • 61,415시간**
- 원시 데이터 **19 TB** → 표준 전처리 후 **6 TB**
- 임상·인지·BCI·연구 분야를 아우르며, 고유 전극명 396종, BrainVision / BioSemi / EDF / GDF / EEGLAB 포맷의 3-10-5 시스템 레코딩 포함.

### Composition (Appendix Table 7)

| Axis | Group | #Subjects | Hours | #Datasets |
|------|-------|-----------|-------|-----------|
| Category | BCI | 791 | 457 | 28 |
| Category | Cognition | 4,193 | 10,376 | 56 |
| Category | Clinic | 19,290 | 50,581 | 8 |
| Platform | TUH (TUEG) | 14,987 | 26,847 | 1 |
| Platform | Physionet | 607 | 22,707 | 2 |
| Platform | OpenNeuro | 4,153 | 10,194 | 56 |
| Platform | MOABB | 711 | 384 | 27 |
| Platform | Other | 3,802 | 1,250 | 6 |
| Channels | [3, 30) | 19,871 | 50,870 | 31 |
| Channels | [30, 80) | 1,781 | 1,516 | 48 |
| Channels | [80, 129] | 2,622 | 9,027 | 13 |
| **Total** | | **24,274** | **61,415** | **92** |

### Preprocessing pipeline (paper §3.1.1)
1. 10초 미만 레코딩 및 다운스트림 태스크에 사용된 레코딩 제외.
2. **200 Hz**로 리샘플링, band-pass filter **0.5–99.5 Hz**, float32로 변환.
3. 각 레코딩 세션 전체 통계를 기반으로 Z-score 정규화.
4. 15 표준편차 초과 값 clipping (CBraMod와 달리 REVE는 100 µV 이상 신호를 *유지*하여 총 약 60,000시간 확보 — CBraMod의 9,000 h, LaBraM의 2,534 h와 대비).
5. 전극의 3D 좌표(10-5 시스템)를 수집하거나 추론; 위치를 특정할 수 없는 레코딩은 제외.

> REVE 저장소에는 데이터셋별 변환 스크립트가 [`preprocessing/`](https://github.com/elouayas/reve_eeg/tree/main/preprocessing) 폴더에 포함되어 있으며 (예: `preprocessing_bciciv2a.py`, `preprocessing_physio.py`, `preprocessing_hmc.py`, `preprocessing_faced.py`, `preprocessing_mumtaz.py`, `preprocessing_speech.py`, `preprocessing_stress.py`, `ISRUC/prepare_ISRUC.py`), 전용 [`preprocessing/README.md`](https://github.com/elouayas/reve_eeg/blob/main/preprocessing/README.md)도 제공된다.

## Platform-level download entry points

92개 데이터셋을 개별적으로 나열하는 대신, REVE는 4개의 주요 허브와 일부 "기타" 출처에서 데이터를 수집한다:

| Platform | #Datasets | Subjects | Hours | License | Entry point / Notes |
|----------|:---------:|--------:|------:|---------|---------------------|
| **TUH (TUEG)** (Obeid & Picone, 2016) | 1 | 14,987 | 26,847 | Free w/ registration | <https://isip.piconepress.com/projects/nedc/html/tuh_eeg/> |
| **PhysioNet** | 2 | 607 | 22,707 | CC-BY 4.0 / CC-BY-NC-SA 4.0 | Siena Scalp EEG (Detti, 2020); ICARE (Amorim et al., 2023) — <https://physionet.org/> |
| **OpenNeuro** | 56 | 4,153 | 10,194 | CC0 | 개별 데이터셋 ID 목록 아래 참조 — <https://openneuro.org/> |
| **MOABB** | 27 | 711 | 384 | BSD 3-Clause | 27개 BCI 데이터셋; moabb 패키지로 자동 다운로드 — <https://github.com/NeuroTechX/moabb> |
| **Other** | 6 | 3,802 | 1,250 | 다양 | NMT (Khan et al., 2022; CC-BY), HMS (Ram et al., 2024; CC-BY-NC 4.0), SparrKULee (Accou et al., 2023; CC-BY-NC 4.0), Inria Large (Dreyer et al., 2023; CC-BY 4.0), THINGS2 (Gifford et al., 2022; CC-BY 4.0), TDBRAIN (Van Dijk et al., 2022; GPL-3.0) |
| **합계** | **92** | **24,274** | **61,415** | | |

### OpenNeuro dataset IDs used by REVE (56 datasets)

논문 Appendix B 기재 ID 및 인용 (일부):

| ID | Citation | ID | Citation |
|----|----------|----|----------|
| ds004706 | Rudoler et al., 2023 | ds004582 | Makowski et al., 2023 |
| ds004356 | Shan et al., 2022 | ds005189 | Helbing et al., 2024 |
| ds003887 | Shatek et al., 2023 | ds004043 | Moerel et al., 2022 |
| ds003885 | Shatek et al., 2021 | ds004357 | Grootswagers et al., 2024 |
| ds003825 | Grootswagers et al., 2022 | ds004816 | Grootswagers et al., 2023a |
| ds004817 | Grootswagers et al., 2023b | ds004840 | Cordoba-Silva et al., 2023 |
| ds005262 | Metwalli et al., 2024 | ds004477 | Papastylianou et al., 2023 |
| ds005273 | Esteban et al., 2024 | ds004561 | Veillette et al., 2023 |
| ds004951 | Haupt et al., 2024 | ds004324 | Chacón & Wriessnegger, 2023 |
| ds005095 | Zhozhikashvili et al., 2024 | ds005509 | Shirazi et al., 2025 |
| ds005506–ds005514 | Shirazi et al., 2024b / Alexander et al., 2017 (7 datasets) | ds001787 | Delorme & Brandmeyer, 2024 |
| ds003690 | Ribeiro & Castelo-Branco, 2021 | ds004603 | Lowe et al., 2023 |
| ds003969 | Delorme & Braboszcz, 2021 | ds004147 | Hassall et al., 2024 |
| ds003004 | Onton & Makeig, 2022 | ds002721 | Daly et al., 2020 |
| ds004152 | Hassall et al., 2022a | ds005089 | Aguado-Lopez et al., 2024 |
| ds004264 | Hassall et al., 2022b | ds004315 | Cavanagh & Jackson, 2022 |
| ds004408 | Bialas et al., 2023 | ds005121 | Siefert et al., 2024 |
| ds003775 | Hatlestad-Hall et al., 2022 | ds004572 | Kekecs & Farahzadi, 2024 |
| ds002778 | Rockhill et al., 2020 | ds003846 | Gehrke et al., 2024 |
| ds004279 | Araya et al., 2023 | ds004148 | Wang et al., 2022 |
| ds004902 | Xiang et al., 2024 | ds002680 | Delorme & Fabre-Thorpe, 2020 |
| ds004284 | Veillette et al., 2022 | ds004395 | Kahana et al., 2023 |
| ds005508 | Shirazi et al., 2024a | ds005697 | Li & Zhao, 2024 |
| ds005620 | Bajwa et al., 2024 | ds005594 | Taylor et al., 2024 |
| ds005586 | Baykan & Schütz, 2024 | | |

각 OpenNeuro ID는 `https://openneuro.org/datasets/<id>` 형태로 접근할 수 있다 (예: <https://openneuro.org/datasets/ds004706>).

### MOABB datasets used by REVE (27 datasets)

| # | Dataset | Citation | Task |
|---|---------|----------|------|
| 1 | AlexMI | Barachant, 2012 | Motor imagery |
| 2 | BNCI2014004 | Leeb et al., 2007 | Motor imagery |
| 3 | BNCI2015001 | Faller et al., 2012 | Motor imagery |
| 4 | BNCI2015004 | Scherer et al., 2015 | Motor imagery |
| 5 | Cho2017 | Cho et al., 2017 | Motor imagery |
| 6 | Lee2019_MI | Lee et al., 2019 | Motor imagery |
| 7 | Liu2024 | Liu et al., 2024 | Motor imagery |
| 8 | Ofner2017 | Ofner et al., 2017 | Motor imagery |
| 9 | Shin2017A | Shin et al., 2016 | Motor imagery |
| 10 | Weibo2014 | Yi et al., 2014 | Motor imagery |
| 11 | Zhou2016 | Zhou et al., 2016 | Motor imagery |
| 12 | Schirrmeister2017 | Schirrmeister et al., 2017 | Motor imagery |
| 13 | Kalunga2016 | Kalunga et al., 2015 | SSVEP |
| 14 | Lee2019_SSVEP | Lee et al., 2019 | SSVEP |
| 15 | Nakanishi2015 | Nakanishi et al., 2015 | SSVEP |
| 16 | BI2014a | Korczowski et al., 2019b | P300 (Brain Invaders) |
| 17 | BI2014b | Korczowski et al., 2019c | P300 (Brain Invaders) |
| 18 | BNCI2014008 | Riccio et al., 2013 | P300 |
| 19 | BNCI2014009 | Aricò et al., 2014 | P300 |
| 20 | BNCI2015003 | Guger et al., 2009 | P300 |
| 21 | EPFLP300 | Hoffmann et al., 2008 | P300 |
| 22 | BI2015a | Korczowski et al., 2019a | P300 (Brain Invaders) |
| 23 | BI2015b | Korczowski et al., 2019c | P300 (Brain Invaders) |
| 24 | Sosulski2019 | Sosulski et al., 2021 | ERP |
| 25 | Lee2019_ERP | Lee et al., 2019 | ERP |
| 26 | Riccio2013 | Riccio et al., 2013 | P300 |
| 27 | Korczowski2019 | Korczowski et al., 2019 | P300 (Brain Invaders) |

다음과 같이 [MOABB](https://moabb.neurotechx.com/) 패키지를 통해 한 줄로 불러올 수 있다:

```python
from moabb.datasets import BNCI2014_001
data = BNCI2014_001().get_data()
```

## How to reproduce the pre-training preprocessing

```bash
# 1) REVE를 설치한다
git clone https://github.com/elouayas/reve_eeg
cd reve_eeg && pip install -e .

# 2) 구성 데이터셋을 다운로드한다
#    - TUEG: TUH EEG 포털에서 접근 권한 신청
#    - OpenNeuro: openneuro-py download --dataset ds004706 --target-dir ...
#    - MOABB: moabb 패키지가 자동으로 처리
#    - Physionet/NMT/HMS 등: preprocessing/README.md 참고

# 3) 각 코퍼스를 REVE가 요구하는 포맷으로 변환한다
python preprocessing/preprocessing_physio.py --input ... --output ...
# (데이터셋마다 반복; preprocessing/README.md 참고)

# 4) 사전학습을 시작한다
python src/train.py +experiment=pretrain_base
```

## Citation

```bibtex
@inproceedings{elouahidi2025reve,
  title={{REVE}: A Foundation Model for {EEG} Adapting to Any Setup with Large-Scale Pre-training on 25{,}000 Subjects},
  author={El Ouahidi, Yassine and Lys, Jonathan and Th{\"o}lke, Philipp and Farrugia, Nicolas and Pasdeloup, Bastien and Gripon, Vincent and Jerbi, Karim and Lioi, Giulia},
  booktitle={Advances in Neural Information Processing Systems (NeurIPS)},
  year={2025}
}
```
