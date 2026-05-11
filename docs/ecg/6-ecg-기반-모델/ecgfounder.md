# ECGFounder — Electrocardiogram Foundation Model

> **An Electrocardiogram Foundation Model Built on over 10 Million Recordings with External Evaluation across Multiple Domains**  
> Jun Li, Aaron Aguirre, Junior Moura, Che Liu, Lanhai Zhong, Chenxi Sun, Gari Clifford, Brandon Westover, Shenda Hong. **arXiv:2410.04133v4, 2025.**

- Paper (arXiv): https://arxiv.org/abs/2410.04133
- Official code: https://github.com/PKUDigitalHealth/ECGFounder
- Model weights: https://huggingface.co/PKUDigitalHealth/ECGFounder
- Preprocessing scripts folder: 논문 본문에는 별도 전처리 폴더 경로가 명시되어 있지 않으므로, 공식 GitHub 저장소의 README와 코드 구조를 확인해야 함.

## Pre-training Data Summary

ECGFounder는 기존 ECG 모델들이 특정 질환·특정 데이터셋 중심으로 제한되던 문제를 해결하기 위해, **단일 대규모 ECG 데이터베이스인 HEEDB**를 기반으로 학습된 범용 ECG foundation model이다.

- **Dataset:** Harvard-Emory ECG Database (HEEDB)
- **Raw scale:** 10,771,552개의 전문가 주석 ECG • 1,818,247명의 고유 환자 • 대부분 10초 길이의 12-lead 임상 ECG
- **Label scale:** 심장 전문의 및 ECG technician 주석에서 추출한 150개 의미 있는 ECG 진단/리듬/형태 label
- **After preprocessing / split:** development set 7,519,035 ECGs • test set 834,926 ECGs
- **Model input:** 12-lead ECG를 기본으로 하되, lead augmentation을 통해 single-lead ECG 적용 가능성까지 확장
- **Core idea:** 대규모 ECG + 전문가 주석 + multi-label 학습 + positive-unlabeled learning을 결합해 다양한 ECG 관련 task에 전이 가능한 표현을 학습함.

### Preprocessing pipeline (paper §2.1 + official code/repo)

1. 판독 불가능한 파일, 결측 데이터, 매칭되지 않은 데이터를 제거한다.
2. ECG signal의 sampling frequency를 linear interpolation으로 **500 Hz**로 resampling한다.
3. baseline drift를 줄이기 위해 **0.5 Hz high-pass filter**를 적용하고, 고주파 잡음 제거를 위해 **second-order 50 Hz Butterworth low-pass filter**를 적용한다.
4. 전기적 간섭을 제거하기 위해 **50/60 Hz notch filter**를 적용한다.
5. 10초보다 긴 ECG record는 순차적으로 **10-second window**로 자르고, 10초보다 짧은 경우에는 **zero padding**을 적용한다.
6. 모델 입력 전 각 signal segment를 해당 segment의 mean과 standard deviation으로 정규화한다.
7. ECG annotation은 정규표현식으로 discrete label을 파싱한 뒤, 의학적으로 의미 있는 label만 선별하여 최종 **150개 label**로 정리한다.

The exact script used by the authors is not separately specified in the paper text, but the authors provide the official code repository at [`PKUDigitalHealth/ECGFounder`](https://github.com/PKUDigitalHealth/ECGFounder).  
실제 재현 시에는 해당 repository의 README, data processing 관련 파일, 그리고 Hugging Face checkpoint 구조를 함께 확인해야 한다.

## Pre-training Dataset

| Dataset | Subjects | Sessions | Raw scale | #Samples after cleaning | Rate (Hz) | Access |
|---------|----------|----------|-----------|-------------------------|-----------|--------|
| HEEDB (Harvard-Emory ECG Database) | 1,818,247 | Not specified | 10,771,552 expert-annotated ECGs | Development: 7,519,035 ECGs / Test: 834,926 ECGs | Resampled to 500 Hz | Data link → https://bdsp.io/content/heedb/1.0/ |

## Downstream datasets (informational — not used for pre-training)

ECGFounder는 pre-training 이후 여러 외부 검증 및 downstream task에서 평가되었다. 핵심은 단순히 ECG 진단 하나만 수행하는 모델이 아니라, ECG 표현을 기반으로 다양한 임상 task에 전이 가능하다는 점이다.

- **External ECG validation:** CODE-test, PTB-XL, PhysioNet Challenge-2017
- **Fine-tuning dataset:** MIMIC-IV-ECG
- **Cross-modality validation:** DeepBeat PPG dataset
- **Downstream task categories:**  
  ECG diagnosis, demographic detection, clinical event detection, cross-modality cardiac rhythm diagnosis
- **Specific downstream tasks:**  
  age regression/classification, sex detection, chronic kidney disease (CKD) detection, chronic heart disease (CHD) detection, left ventricular ejection fraction (LVEF) regression/classification, NT-proBNP regression/classification, PPG-based atrial fibrillation detection

## How to reproduce the pre-training preprocessing

```bash
# 1) Request HEEDB access and download the dataset
#    https://bdsp.io/content/heedb/1.0/

# 2) Clone ECGFounder
git clone https://github.com/PKUDigitalHealth/ECGFounder
cd ECGFounder

# 3) Install dependencies
#    Follow the official repository README because the exact environment may change.
pip install -r requirements.txt

# 4) Download pretrained model weights
#    https://huggingface.co/PKUDigitalHealth/ECGFounder

# 5) Reproduce the paper-level preprocessing logic
#    - Remove unreadable / missing / unmatched ECG files
#    - Resample ECG signals to 500 Hz
#    - Apply 0.5 Hz high-pass filter
#    - Apply second-order 50 Hz Butterworth low-pass filter
#    - Apply 50/60 Hz notch filter
#    - Segment into 10-second ECG windows
#    - Zero-pad short ECG records
#    - Normalize each signal segment by its own mean and standard deviation

# 6) Run training or fine-tuning
#    Use the official repository scripts and configuration files.
```

## Citation

```bibtex
@article{li2025ecgfounder,
  title={An Electrocardiogram Foundation Model Built on over 10 Million Recordings with External Evaluation across Multiple Domains},
  author={Li, Jun and Aguirre, Aaron and Moura, Junior and Liu, Che and Zhong, Lanhai and Sun, Chenxi and Clifford, Gari and Westover, Brandon and Hong, Shenda},
  journal={arXiv preprint arXiv:2410.04133},
  year={2025}
}
```


