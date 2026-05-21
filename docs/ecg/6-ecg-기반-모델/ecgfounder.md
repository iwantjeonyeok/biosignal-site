# ECGFounder — Electrocardiogram Foundation Model

> **An Electrocardiogram Foundation Model Built on over 10 Million Recordings with External Evaluation across Multiple Domains**
> Jun Li, Aaron Aguirre, Junior Moura, Che Liu, Lanhai Zhong, Chenxi Sun, Gari Clifford, Brandon Westover, Shenda Hong. **NEJM AI 2025.**

- Paper (arXiv): https://arxiv.org/abs/2410.04133
- Official code: https://github.com/PKUDigitalHealth/ECGFounder
- Model weights: https://huggingface.co/PKUDigitalHealth/ECGFounder

## Motivation

기존 ECG AI 모델들은 대부분 특정 질환이나 특정 데이터셋 중심으로 설계되어, **범용적인 ECG 진단 능력**과 **다양한 임상 환경으로의 일반화**에 한계가 있다. 또한 학습 데이터의 규모가 충분하지 않아 소수 label 범주에서 성능이 저하되거나, multi-lead ECG에서만 잘 동작하여 single-lead 웨어러블 기기에는 적용하기 어렵다는 문제가 있다.

ECGFounder는 이 문제를 해결하기 위해 두 가지 핵심 전략을 채택한다. 첫째, **1,000만 개 이상의 전문가 주석 ECG**로 구성된 Harvard-Emory ECG Database(HEEDB)를 활용하여 전례 없는 규모의 학습 데이터를 확보한다. 둘째, **150개 진단 label과 multi-label 학습**, **Positive-Unlabeled(PU) learning**, **lead augmentation** 기법을 결합하여 다양한 임상 환경과 웨어러블 기기까지 적용 가능한 범용 ECG foundation model을 구축하는 것을 목표로 한다.

## Architecture Summary

ECGFounder는 **RegNet 기반의 convolution 아키텍처**를 backbone으로 사용한다. RegNet은 uniform scaling 대신 quantized linear model로 최적의 width와 depth를 예측하여, 다양한 모델 크기에서 효율적인 성능을 제공한다.

- **Backbone**: RegNet (quantized linear model로 width/depth 최적화)
- **Block 구조**: Bottleneck blocks + group convolutions + channel-wise attention → 시간적·공간적 표현 풍부화
- **학습 방식**: Multi-label classification (150개 ECG 진단/리듬/형태 label)
- **Positive-Unlabeled (PU) learning**: 불완전한 multi-label annotation 문제 해결. 미주석(unlabeled) 샘플을 단순 negative로 처리하지 않고, positive 미주석 가능성을 반영하여 학습
- **Lead augmentation**: 12-lead ECG에서 lead I를 중심으로 각도 기반으로 6개 추가 리드를 합성하여, single-lead 웨어러블 기기용 모델 학습에 활용. 웨어러블 모델은 파라미터를 축소하여 경량화

## Pre-training Data Summary

ECGFounder는 **단일 대규모 임상 ECG 데이터베이스인 HEEDB**를 기반으로 학습된다. 기존 self-supervised learning 방식과 달리, 심장 전문의와 ECG technician의 실제 임상 주석을 직접 활용하는 **supervised foundation model** 방식을 채택한다.

- **Dataset**: Harvard-Emory ECG Database (HEEDB)
- **Raw scale**: 10,771,552개의 전문가 주석 ECG, 1,818,247명의 고유 환자, 대부분 10초 길이의 12-lead 임상 ECG
- **Label scale**: 심장 전문의 및 ECG technician 주석에서 추출한 **150개의 의미 있는 ECG 진단/리듬/형태 label**
- **Dataset split**: development set 7,519,035 ECGs, test set 834,926 ECGs

### Preprocessing procedure

1. 판독 불가능한 파일, 결측 데이터, 매칭되지 않은 데이터 제거
2. Linear interpolation으로 ECG signal을 **500 Hz로 resampling**
3. Baseline drift 제거를 위해 **0.5 Hz high-pass filter** 적용
4. 고주파 잡음 제거를 위해 **second-order 50 Hz Butterworth low-pass filter** 적용
5. 전기적 간섭 제거를 위해 **50/60 Hz notch filter** 적용
6. 10초보다 긴 ECG record는 순차적으로 **10-second window**로 분할, 10초보다 짧으면 **zero padding** 적용
7. 각 signal segment를 해당 segment의 mean과 standard deviation으로 정규화
8. ECG annotation은 정규표현식으로 discrete label을 파싱한 뒤, 의학적으로 의미 있는 label만 선별하여 **150개 label**로 정리

### Pre-training Datasets

| Dataset | Subjects | Raw scale | #Samples after preprocessing | Rate (Hz) | Access |
|---------|----------|-----------|------------------------------|-----------|--------|
| HEEDB (Harvard-Emory ECG Database) | 1,818,247명 | 10,771,552개 전문가 주석 ECG | Development: 7,519,035 ECGs / Test: 834,926 ECGs | → 500 | https://bdsp.io/content/heedb/1.0/ |

## Downstream Datasets

ECGFounder는 pre-training 이후 다양한 외부 데이터셋에서 검증 및 downstream task 평가를 수행한다. 이 데이터셋들은 사전학습에 사용되지 않는다.

| Dataset | Task 유형 | 비고 |
|---------|----------|------|
| CODE-test | 12-lead ECG 진단 (외부 검증) | 평균 AUROC 0.981 달성 |
| PTB-XL | 12-lead ECG 진단 (외부 검증) | 평균 AUROC 0.924 |
| PhysioNet Challenge 2017 | 단일 리드 리듬 분류 | 외부 검증 |
| MIMIC-IV-ECG | Fine-tuning | 다양한 downstream task |
| DeepBeat PPG dataset | Cross-modality 검증 | PPG 기반 심방세동 검출 |

**주요 downstream tasks**: age 회귀/분류, sex 감지, 만성 신장질환(CKD) 검출, 만성 심장질환(CHD) 검출, 좌심실 박출률(LVEF) 회귀/분류, NT-proBNP 회귀/분류, PPG 기반 심방세동 검출

**주요 결과**: 내부 검증 세트에서 80개 진단에 대해 AUROC 0.95 이상 달성. 심방세동(AF) AUROC 0.996, 20개 분류 항목 평균 AUROC 0.968, 심장전문의 평균 F1 0.640 대비 모델 F1 0.677로 우위.

## How to Reproduce the Pre-training Preprocessing

```bash
# 1) HEEDB 접근 신청 및 데이터 다운로드
#    https://bdsp.io/content/heedb/1.0/

# 2) ECGFounder 클론
git clone https://github.com/PKUDigitalHealth/ECGFounder
cd ECGFounder

# 3) 의존성 설치
pip install -r requirements.txt

# 4) 사전학습된 모델 가중치 다운로드 (선택)
#    https://huggingface.co/PKUDigitalHealth/ECGFounder

# 5) 전처리 수행
#    - 불량 파일 제거 (판독 불가, 결측, 매칭 오류)
#    - 500 Hz resampling (linear interpolation)
#    - 0.5 Hz high-pass filter 적용
#    - second-order 50 Hz Butterworth low-pass filter 적용
#    - 50/60 Hz notch filter 적용
#    - 10초 window 분할 및 zero padding
#    - segment 단위 mean/std normalization
#    공식 repository의 README 및 data processing 스크립트 참고

# 6) 학습 또는 fine-tuning 실행
#    공식 repository의 scripts 및 configuration 파일 참고
```

## Citation

```bibtex
@article{li2025ecgfounder,
  title={An Electrocardiogram Foundation Model Built on over 10 Million Recordings with External Evaluation across Multiple Domains},
  author={Li, Jun and Aguirre, Aaron and Moura, Junior and Liu, Che and Zhong, Lanhai and Sun, Chenxi and Clifford, Gari and Westover, Brandon and Hong, Shenda},
  journal={NEJM AI},
  year={2025},
  url={https://arxiv.org/abs/2410.04133}
}
```
