# TUAB

# 1. Dataset Information

TUAB 데이터셋[^1]은 총 2383명의 성인 환자들을 대상으로 수집된 EEG 데이터를 기반으로 하며, 정상과 이상 상태를 구분하는 이진 분류 과제를 포함합니다. 라벨은 의료진의 진단 보고서를 기반으로 구성되며, 각 세션은 평균 15분 이상, 256Hz 샘플링 속도, 다채널 EDF 포맷으로 저장되어 있습니다. 이 데이터셋은 총 1,084개의 EEG 세션으로 구성되며, 그 중 885개는 정상, 199개는 병리적 이상으로 라벨링되어 있습니다. 정규화된 구조와 실제 임상에서의 EEG 특성을 반영하고 있어 이상 탐지, 분류, 자동 판독 알고리즘 학습에 적합한 환경을 제공합니다.

# 2. Dataset Basic Information

## 2.1 Data Information

| # of Subjects | # of Leads | Sampling Frequency (Hz) | Recording Duration (min) | File Fomat |
| --- | --- | --- | --- | --- |
| 2383 | 23 | 256 | more than 15 min | (EEG).edf, (AAREADME).txt |

## 2.2 Data Statistics

*EEG 전극에 해당하는 데이터만을 사용해 통계 분석을 수행하였습니다.

| Label Type | #of recordings | EEG Mean | EEG Std | EEG Max | EEG Median | EEG Min |
| --- | --- | --- | --- | --- | --- | --- |
| Normal (0) | 1521 | 0.000000 | 0.000059 | 0.002349 | -0.000001 | -0.001923 |
| Abnormal (1) | 1472 | 0.000000 | 0.000073 | 0.002417 | -0.000001 | -0.002055 |
| Total | 2993 | 0.000000   | 0.000066   | 0.002384   | -0.000001   | -0.001988   |

 

## 2.3 Raw Dataset


!!! note ""
    ```
    TUAB/
    └── v3.0.1/
    ├── edf/
    │   ├── eval/
    │   │   ├── abnormal/
    │   │   │   └── 01_tcp_ar/
    │   │   │       ├── aaaaabdo_s003_t000.edf
    │   │   │       ├── aaaaabsk_s007_t000.edf
    │   │   │       └── aaaaabuv_s002_t000.edf
    │   │   │       ... (123 more files)
    │   │   └── normal/
    │   │       └── 01_tcp_ar/
    │   │           ├── aaaaaayx_s002_t000.edf
    │   │           ├── aaaaacad_s003_t000.edf
    │   │           └── aaaaacby_s004_t000.edf
    │   │           ... (147 more files)
    │   └── train/
    │       ├── abnormal/
    │       │   └── 01_tcp_ar/
    │       │       ├── aaaaaaaq_s004_t000.edf
    │       │       ├── aaaaaaaq_s005_t001.edf
    │       │       └── aaaaaaat_s002_t001.edf
    │       │       ... (1343 more files)
    │       └── normal/
    │           └── 01_tcp_ar/
    │               ├── aaaaaaav_s004_t000.edf
    │               ├── aaaaaabn_s005_t000.edf
    │               └── aaaaaaff_s002_t000.edf
    │               ... (1368 more files)
    ├── AAREADME.txt
    └── AAREADME.txt,v
    
    12 directories, 2995 files
    ```


TUAB 데이터셋은 train/test 셋으로 구분되어 있으며 각각 abnormal/normal으로 한 번 더 구분되어 있습니다. 각 폴더 안에는 EDF 파일이 존재하여 EEG 신호 데이터를 포함합니다.

## 2.4 Raw Dataset Example

![f17d727f-c33f-4637-8c0c-4a5df814d5cb.png](tuab/f17d727f-c33f-4637-8c0c-4a5df814d5cb.png)

## 2.5 Preprocessed Dataset


!!! note ""
    ```
    TUAB/
    ├── test_npy_files/
    │   ├── sess1_sub2094_trial0.npy
    │   ├── sess1_sub2098_trial0.npy
    │   └── sess1_sub2099_trial0.npy
    │   ... (273 more files)
    ├── train_npy_files/
    │   ├── sess10_sub150_trial0.npy
    │   ├── sess10_sub208_trial2.npy
    │   └── sess10_sub233_trial0.npy
    │   ... (2714 more files)
    ├── channels.csv
    ├── test_labels.csv
    
    ├── train_labels.csv
    
    ├── TUAB_test.h5
    
    ├── TUAB_train.h5
    
    ├── TUAB_train.npz
    └── TUAB.h5
    ... (4 more files)
    
    1 directories,  3000 files
    ```


# 3. Applications and Use Cases

| 인용 논문 | 연구 과제 | 모델 구조 | 방법론 |
| --- | --- | --- | --- |
| Jiang et al. (2024) [^2] | 범용 EEG 표현 학습 | EEG 전용 사전학습 모델 (LaBraM) | 약 2,500시간의 EEG 데이터를 기반으로 사전학습 후, TUAB, TUEV, 정서 인식 등 다양한 EEG 과제에 전이. 기존 모델 대비 평균 성능 향상. |
| Foumani et al. (2024) [^3] | 노이즈 강건 EEG 표현 학습 | 자가 예측 기반 마스킹 학습 모델 (EEG2Rep) | 의미 보존 마스킹을 통해 EEG 신호의 중요한 구간만을 예측하도록 학습하며, 다양한 공개 데이터셋에서 일반화된 EEG 표현을 확보함. |
| Wang et al. (2025) [^4] | 범용 EEG 사전학습 모델 (foundation model) 구축 | 시공간 attention 분리형 Transformer (CBraMod) | 12개 EEG 데이터셋 기반으로 마스킹 예측 자기지도학습을 수행하고, 시공간 정보 분리 인코딩을 통해 전이 성능을 극대화함. |

# 4. References

[^1]: Silvia López de Diego. **Automated Interpretation of Abnormal Adult Electroencephalograms.** Master’s Thesis, Department of Electrical and Computer Engineering, Temple University, 2017.

[^2]: Jiang, W., Zhao, L.-M., & Lu, B.-L. (2024). **LaBraM: Large Brain Model for Learning Generic Representations with Tremendous EEG Data in BCI.** *International Conference on Learning Representations (ICLR)*.

[^3]: Foumani, N. M., et al. (2024). **EEG2Rep: Enhancing Self-supervised EEG Representation Through Informative Masked Inputs.** *ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD)*.

[^4]: Wang, J., Zhao, S., Luo, Z., et al. (2025). **CBraMod: A Criss-Cross Brain Foundation Model for EEG Decoding.** *International Conference on Learning Representations (ICLR)*. arXiv:2412.07236