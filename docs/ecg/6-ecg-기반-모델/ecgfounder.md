# ECGFounder — Electrocardiogram Foundation Model

> **An Electrocardiogram Foundation Model Built on over 10 Million Recordings with External Evaluation across Multiple Domains**
> Jun Li, Aaron Aguirre, Junior Moura, Che Liu, Lanhai Zhong, Chenxi Sun, Gari Clifford, Brandon Westover, Shenda Hong. **NEJM AI 2025.**

- [Paper (arXiv)](https://arxiv.org/abs/2410.04133)
- [Official code](https://github.com/PKUDigitalHealth/ECGFounder)



## Motivation

기존에도 ECG용 foundation model을 제안한 연구들이 있었지만, 학습 데이터의 샘플 수, 환자 수, 진단 라벨의 다양성, 인구통계학적 다양성이 충분하지 않아 실제 임상 환경의 다양한 ECG 분석 문제를 포괄하는 데 한계가 있었다. 또한 foundation model로 인정되기 위해서는 초기 학습 데이터에만 적합한 것이 아니라, 여러 외부 도메인과 다양한 임상 과제로 일반화될 수 있어야 하지만 기존 모델들은 이를 충분히 입증하지 못했다. 특히 웨어러블 기기와 원격 모니터링에서 중요한 single-lead ECG는 multi-lead ECG에 비해 성능 저하가 크다는 문제가 남아 있었다. ECGFounder는 이러한 한계를 해결하기 위해 1,000만 건 이상의 실제 임상 ECG와 전문가 주석을 활용하고, 150개 진단 라벨을 학습 대상으로 구성하여 더 넓은 진단 범위를 갖는 ECG foundation model을 제안한다.

## Architecture Summary

ECGFounder는 10초 길이의 12유도 ECG를 입력받아 일반화 가능한 ECG 표현을 학습하는 Net1D/RegNet 기반 1D ECG 인코더이다. 모델은 단순히 시간축의 파형 변화만 학습하는 것이 아니라, 서로 다른 유도 사이의 관계와 전체 심장 전기 활동의 공간적 패턴까지 함께 반영하도록 설계되었다. 구조적으로는 네트워크 깊이에 따라 블록 수와 채널 수를 단계적으로 조절하는 **RegNet** 구조를 사용하며, bottleneck block, group convolution, channel-wise attention을 통해 ECG의 시간적 특징과 유도 간 공간적 특징을 함께 추출한다. 라벨 없이 신호 자체를 복원하거나 예측하는 자기지도학습 모델이 아니라, HEEDB의 실제 임상 전문가 주석을 활용해 150개 ECG 진단 라벨을 학습하는 **다중 라벨 진단 모델**이다. 실제 ECG 진단은 하나의 기록에 여러 진단명이 동시에 붙을 수 있고, 실제 임상 주석에는 일부 양성 라벨이 누락될 수 있기 때문에, ECGFounder는 라벨이 없는 항목을 무조건 음성으로 처리하지 않도록 **positive unlabeled learning** 기반 손실 함수를 적용한다. 또한 웨어러블 기기와 원격 모니터링 환경에서 중요한 single-lead ECG 분석을 지원하기 위해, 12유도 ECG에서 lead I를 중심으로 limb lead의 전기축 정보를 활용하는 lead augmentation을 적용하여 single-lead ECG에서도 리듬 정보와 전기축 관련 진단 정보를 학습할 수 있도록 설계되었다.

## Pre-training Data Summary

ECGFounder는 **단일 대규모 임상 ECG 데이터베이스인 HEEDB**를 기반으로 학습된다. 
HEEDB는 1,818,247명의 고유 피험자에게서 수집된 10,771,552개의 전문가 주석 ECG로 구성되어 있다. ECG 기록은 대부분 10초 길이의 12-lead clinical ECG이며, 각 ECG에는 심장 전문의와 ECG technician이 제공한 주석이 함께 연결되어 있다. HEEDB의 annotation은 ECG와 연결된 discrete text report 형태로 제공되며, ECG의 morphology, rhythm, diagnostic information을 포함한다. 저자들은 이 주석을 regular expression으로 parsing하여 287개의 independent phrase를 추출한 뒤, 의사 검토를 통해 ECG 설명과 관련 없는 항목을 제거하고 최종 150개의 meaningful label로 정리했다.

- **데이터셋**: Harvard-Emory ECG Database (HEEDB)
- **원시 규모**: 1,818,247명 고유 피험자 · 10,771,552개 ECG 기록 · 대부분 10초 길이의 12유도 임상 ECG · 각 ECG 기록별 discrete text report 형태의 전문가 주석 
- **전처리 후**: ECGFounder 학습에 사용되는 development dataset과 내부 평가용 held-out test dataset으로 분할. Development dataset은 1,319,128명 환자의 7,519,035개 ECG로 구성, test dataset은 146,570명 환자의 834,926개 ECG로 구성. Test dataset은 downstream task용 데이터가 아니라, HEEDB 내부에서 모델의 진단 성능을 평가하기 위한 내부 평가 데이터
 
### Preprocessing procedure
HEEDB 데이터셋을 전처리하는 코드 파일은 별도로 존재하지 않으며, 논문에 작성된 전처리 절차는 아래와 같다.

1. 판독 불가능한 파일, 결측 데이터, 매칭되지 않은 데이터 제거
2. linear interpolation을 통한 ECG signal **500 Hz resampling**
3. residual baseline drift 제거를 위한 **0.5 Hz high-pass filter** 적용
4. high-frequency noise 감소를 위한 **second-order 50 Hz Butterworth low-pass filter** 적용
5. 전기적 간섭 제거를 위한 **50/60 Hz notch filter** 적용
6. 10초 초과 ECG record의 순차적 **10-second window** 분할
7. 10초 미만 ECG sequence에 대한 **zero padding** 적용
8. 각 individual signal segment의 mean과 standard deviation을 이용한 signal 정규화

### Pre-training Datasets

| Dataset | Subjects | Raw scale | #Samples after preprocessing | Rate (Hz) | Access |
|---------|----------|-----------|------------------------------|-----------|--------|
| HEEDB (Harvard-Emory ECG Database) | 1,818,247명 | 10,771,552개 전문가 주석 ECG | Development: 7,519,035 ECGs / Test: 834,926 ECGs | → 500 | https://bdsp.io/content/heedb/1.0/ |

## Downstream Datasets
ECGFounder는 총 12개의 clinical downstream task에서 평가되었다. 이 중 ECG diagnosis 2개 task는 HEEDB 내부 평가와 CODE-test, PTB-XL, PhysioNet Challenge-2017 외부 검증을 기반으로 수행되었고, 나머지 fine-tuning 기반 task는 MIMIC-ECG와 DeepBeat-PPG를 바탕으로 구성되었다.
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
