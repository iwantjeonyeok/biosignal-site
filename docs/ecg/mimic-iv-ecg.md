# MIMIC-IV-ECG

# 1. Dataset Information

MIMIC-IV-ECG dataset은 Beth Israel Deaconess Medical Center (BIDMC)에서 수집된 대규모 의료 데이터셋의 일부로, ECG 데이터뿐만 아니라 응급실(ED) 및 중환자실(ICU) 입원 환자 정보를 포함합니다. 이 데이터셋은 2008년부터 2022년까지의 실제 임상 데이터를 기반으로 하며, 364,627명의 환자에 대한 정보가 포함되어 있습니다. 개인정보 비식별화(deidentification)를 통해 연구자가 안전하게 데이터에 접근하고 분석할 수 있도록 설계되었습니다. MIMIC-IV는 MIMIC-III의 후속 버전으로, 데이터 조직을 모듈화하고 사용 편의성을 향상하기 위해 여러 구조적 변경이 이루어졌습니다.

# 2. Dataset Basic Information

## 2.1 Data Information

| # of Subjects | # of Leads | Sampling Frequency (Hz) | Recording Duration (min) | File Fomat |
| --- | --- | --- | --- | --- |
| More than 80,000 (80,035 records) | 12 | Fixed 500 Hz | 10 seconds | .dat (ECG) .hea (Metadata) |

## 2.2 Data Statistics

MIMIC-IV-ECG 데이터셋은 machine_measurements.csv 내 report_0부터 report_17 열에 ECG 기기가 자동으로 생성한 진단 문구와 waveform_note_links.csv 내 전문의 수준 라벨 혹은 임상적 진단을 포함하고 있습니다. 고정된 label이 아닌 텍스트 소스가 제공되어 그 안에서 원하는 label을 추출할 수 있습니다. Rhythm 뿐만 아니라 전도 차단 (Conduction Blocks), 형태학적 이상 (Morphological Abnormalities), 심실 비대 (Chamber Hypertrophy) 등 다양한 의학적 label을 포함합니다.

## 2.3 Raw Dataset


!!! note ""
    ```
    MIMIC-IV-ECG/mimic-iv-ecg-diagnostic-electrocardiogram-matched-subset-1.0/mimic-iv-ecg-diagnostic-electrocardiogram-matched-subset-1.0/
    
    ├── files/ 
    
    │ ├── p1000/
    
    │ │ ├── p10000032/
    
    │ │ │ ├── s40689238/
    
    │ │ │ │ ├── 40689238.dat
    
    │ │ │ │ └── 40689238.hea
    
    │ │ │ ├── s44458630/
    
    │ │ │ │ ├── 44458630.dat
    
    │ │ │ │ └── 44458630.hea
    
    │ │ │ └── s49036311/
    
    │ │ │ │ ├── 49036311.dat
    
    │ │ │ │ └── 49036311.hea
    
    │ │ ├── p10000117/
    
    │ │ │ └── …
    
    │ │ │ │ └── …
    
    │ │ └── …
    
    │ ├── p1001/
    
    │ │ └── …
    
    │ └── … (1,000 폴더)
    
    ├── LICENSE.txt 
    
    ├── machine_measurements_data_dictionary.csv
    
    ├── machine_measurements.csv
    
    ├── record_list.csv
    
    ├── RECORDS
    
    ├── SHA256SUMS.txt 
    
    └── waveform_note_links.csv
    
    1,000 directories in 1 directory, ? files
    ```


각 레코드는 500Hz 샘플링 주파수 기준으로 기록된 12 리드 ECG 신호를 포함하며, 다음 두 파일로 구성되어 있습니다: 

- .dat 파일: ECG 신호 자체를 저장
- .hea 파일: 레코드의 메타데이터 (샘플 수, 레이블, 채널 정보 등)를 저장

## 2.4 Raw Dataset Example

## 2.5 Preprocessed Dataset


!!! note ""
    ```
    MIMIC-IV-ECG/ 
    ├── csv_files/
    │   ├── 40000017_data.csv
    │   ├── 40000029_data.csv
    │   └── 40000035_data.csv
    │   ... (total ? files)
    ├── channels_info.csv
    └── MIMIC-IV-ECG_pretrain.npz
    
    1 directories, ? files
    ```


csv_files 폴더에는 개별 신호 데이터를 담고 있는 ()_data.csv 파일이 포함되어 있습니다. 해당 데이터는 pretrain을 위한 용도로 사용되며, 위의 모든 데이터를 통합하여 라벨 정보와 함께 MIMIC-IV-ECG_pretrain.npz 파일로 정리하였습니다.

# 3. Applications and Use Cases

주어진 label을 이용하면, Arrhythmia detection 뿐만 아니라 ECG disease diagnosis도 진행할 수 있습니다. MIMIC-IV-ECHO 데이터셋을 같이 이용하면 Detection of regional wall motion abnormalities (RWMA), Risk stratification for Acute coronary events을 진행할 수 있습니다.

| 인용 논문 | 연구 과제 | 모델 구조 | 방법론 |
| --- | --- | --- | --- |
| Tian et al. (2024) [^1] | Arrhythmia & Abnormality detection (+ Generate textual explanations for ECG patterns and findings) | Signal-Language Architecture (ECG Encoder + Knowledge Encoder + Label Query Network) | 1. Employed a Large Language Model (LLM) to unify ECG signals and medical text 2. Allowed text queries for disease likelihood3. GPT-based explanations with Grad-CAM visualization to enhance interpretability |
| Carbonati et al. (2024) [^2] | 1. Detection of regional wall motion abnormalities (RWMA) 2. Detection of global RV hypokinesis 3. Risk stratification for future acute coronary events | Convolutional Neural Network (modified ResNet-101) | 1. Integrated echocardiography reports with ECG data to predict wall motion abnormalities, rather than relying on ECG alone 2. Defined stepwise classification for LVEF cutoffs and RWMA localization
  
   |

[^1] 이 논문은 단일 모델로 다수의 ECG 질환을 커버하는 파운데이션 모델 개념을 ECG 분야에 적용하여 zero-shot 진단과 모델 해석 가능성을 함께 제안합니다.
[^2] MIMIC-IV-ECG와 MIMIC-IV-ECHO 등을 연계해, 단순히 부정맥이나 EF 추정뿐 아니라 국소적 벽운동 이상(RWMA)까지 ECG로 예측하는 접근법을 제안합니다.

# 4. References

[^1]: Tian, Y., Li, Z., Jin, Y., Wang, M., Wei, X., Zhao, L., Liu, Y., Liu, J., & Liu, C. (2024). Foundation model of ECG diagnosis: Diagnostics and explanations of any form and rhythm on ECG. Cell Reports Medicine, 5(12), 101875. [https://doi.org/10.1016/j.xcrm.2024.101875](https://doi.org/10.1016/j.xcrm.2024.101875)

[^2]: Carbonati, T., Eslami, P., Waks, J. W., Fiorina, L., Chaudhari, A., Henry, C., Johnson, A. E. W., Pollard, T., Gow, B., Mark, R. G., Horng, S., & Greenbaum, N. R. (2024). Deep neural networks detect regional wall motion abnormalities and preclinical cardiovascular disease from 12-lead ECGs. medRxiv. [https://doi.org/10.1101/2024.05.31.24308304](https://doi.org/10.1101/2024.05.31.24308304)