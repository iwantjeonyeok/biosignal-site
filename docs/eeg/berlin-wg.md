# Berlin (wg)

# 1. Dataset Information

Berlin(wg) 데이터셋[^1]은 단어 생성(word generation) 과제를 기반으로 수집되었습니다. 26명의 피험자에게 주어진 단어의 첫 글자를 바탕으로 가능한 많은 단어를 떠올리는 과제를 수행하였고, baseline 조건과 번갈아 제시되었습니다. 각 세션마다 WG와 baseline 조건이 각각 10번 제시되어 총 60회의 trial이 기록되었습니다.

# 2. Dataset Basic Information

## 2.1 Data Information

| # of Subjects | # of Leads | Sampling Frequency (Hz) | Recording Duration (min) | File Fomat |
| --- | --- | --- | --- | --- |
| 26 | 30 | 200 | 780 | (EEG).mat |

## 2.2 Data Statistics

*EEG 전극에 해당하는 데이터만을 사용해 통계 분석을 수행하였습니다.

| Label Type | #of recordings | EEG Mean | EEG Std | EEG Max | EEG Median | EEG Min |
| --- | --- | --- | --- | --- | --- | --- |
| Baseline (0) | 780     (50.0%) | 10.210522   | 60.298977 | 518.271729  | 11.928608   | -256.831970   |
| Word generation (1) | 780     (50.0%) | 7.007446   | 56.513042 | 493.989349  | 7.842650   | -248.203751 |
| **Total** | 1560 | 8.609 | 58.40601 | 506.130539 | 9.885629 | -252.517861 |

## 2.3 Raw Dataset


!!! note ""
    ```
    Berlin_wg/
    ├── VP001-EEG/
    │   ├── cnt_wg.mat
    │   ├── mnt_wg.mat
    │   └── mrk_wg.mat
    ├── VP002-EEG/
    │   ├── cnt_wg.mat
    │   ├── mnt_wg.mat
    │   └── mrk_wg.mat
    └── VP003-EEG/
    ├── cnt_wg.mat
    ├── mnt_wg.mat
    └── mrk_wg.mat
    ... (23 more directories)
    
    26 directories, 9 files
    ```


mrk_dsr.mat를 통해 trial별 timepoint 정보와 라벨을 알 수 있습니다.

## 2.4 Raw Dataset Example

![image.png](berlin-wg/image.png)

## 2.5 Preprocessed Dataset


!!! note ""
    ```
    Berlin_wg/
    ├── npy_files/
    │   ├── sub01_trial001.npy
    │   ├── sub01_trial002.npy
    │   └── sub01_trial003.npy
    │   ... (1557 more files)
    ├── Berlin_wg.h5
    ├── Berlin_wg.npz
    └── channels.csv
    ... (1 more files)
    
    1 directory, 1564 files
    ```


한 trial(자극)별로 split하고 .npy로 변환하였으며 이 파일명은 labels.csv의 1열과 대응되고, 2열엔 정수형 레이블이 있습니다.

# 3. Applications and Use Cases

| 인용 논문 | 연구 과제 | 모델 구조 | 방법론 |
| --- | --- | --- | --- |
| Rabbani & Islam (2023) [^2] | EEG-NIRS 동시 측정 데이터를 활용한 인지 과제 분류 | CNN, LSTM, GRU 기반 다양한 모델 조합 (CNN-LSTM-GRU 등) | EEG 및 fNIRS 각각 전처리 후 개별 딥러닝 모델 (CNN, LSTM 등)로 특징 학습, 예측 결과들을 융합하여 최종 분류. 3가지 과제(n-back, DSR, WG)에 대해 정확도와 AUC 평가 수행. CNN-LSTM-GRU 구조가 가장 우수한 성능 달성 (Acc 96%, AUC 100%). |

# 4. References

[^1]: Shin, J., von Lühmann, A., Kim, D.-W., Mehnert, J., Hwang, H.-J., & Müller, K.-R. (2018). Simultaneous acquisition of EEG and NIRS during cognitive tasks for an open access dataset. *Scientific Data*, 5, 180003. https://doi.org/10.1038/sdata.2018.3

[^2]: Rabbani, M. H. R., & Islam, S. M. R. (2023). *Deep learning networks based decision fusion model of EEG and fNIRS for cognitive task classification*. Springer Professional. https://www.springerprofessional.de/en/deep-learning-networks-based-decision-fusion-model-of-eeg-and-fn/25558736