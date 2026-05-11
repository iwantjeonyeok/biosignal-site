# ECG-FM — An Open Electrocardiogram Foundation Model

> **ECG-FM: An Open Electrocardiogram Foundation Model**
> Kaden McKeen, Sameer Masood, Augustin Toma, Barry Rubin, Bo Wang. **JAMIA Open 2025.**

- 논문 (arXiv): https://arxiv.org/abs/2408.05178
- 공식 코드: https://github.com/bowang-lab/ECG-FM

---

## 사전학습 데이터 요약

ECG-FM은 두 개의 공개 데이터셋을 합쳐 **약 87만 개의 ECG(약 175만 개 샘플)**로 사전학습합니다.

- **PhysioNet 2021**: 625,139개 ECG, 178,140명 환자
- **MIMIC-IV-ECG**: 800,035개 ECG, 161,352명 환자
- **최종 사전학습 규모**: 873,706개 ECG → **1,757,054개 샘플** (5초 분할 후)
  - 학습 세트: 699,001개 ECG → **1,405,625개 샘플**

### 전처리 파이프라인

1. 원시 파형(raw waveform) 및 메타데이터(샘플 레이트, 환자 정보 등) 추출
2. 선형 보간(linear interpolation)으로 **500 Hz 리샘플링**
3. **Z-score 정규화** 수행
4. 비중첩 **5초 단위** 세그먼트로 분할 (CMSC 대조학습을 위한 양성 쌍 생성 목적)
5. null 값 또는 상수 리드(constant lead)가 있는 샘플 제거

---

## 사전학습 데이터셋

| 데이터셋 | 환자 수 | ECG 수 | 샘플 수 (전처리 후) | 접근 방법 |
|---------|--------|--------|-------------------|----------|
| PhysioNet 2021 | 178,140명 | 625,139개 | — | 공개 |
| MIMIC-IV-ECG | 161,352명 | 800,035개 | — | PhysioNet 계정 필요 (무료) |
| **합계 (사전학습)** | — | **873,706개** | **1,757,054개** | — |

---

## 모델 구조

ECG-FM은 **CNN 피처 인코더 + Transformer 인코더** 구조를 채택합니다.

- **CNN 피처 인코더**: 원시 파형에서 잠재 표현(latent representation) 추출
- **Transformer 인코더**: BERT-Base 하이퍼파라미터 적용
  - 레이어 수: 12
  - 임베딩 차원: 768
  - Self-attention 헤드: 12
  - FFN 차원: 3,072

---

## 사전학습 방법 (WCR)

ECG-FM은 **세 가지 SSL 목적함수를 결합한 하이브리드 방식 WCR**을 사용합니다.

### 1. wav2vec 2.0 (로컬 대조학습)
- CNN 잠재 표현의 스팬(span)을 마스킹 (시작 토큰 확률 6.5%, 이후 10토큰 마스킹 → 전체 약 49% 마스킹)
- 학습 가능한 코드북(2개 × 320코드)으로 양자화(quantization)
- 마스킹된 토큰에 대해 로컬 컨텍스트로 정답 표현을 예측

### 2. CMSC — Contrastive Multi-Segment Coding (글로벌 대조학습)
- 시간적으로 인접한 ECG 세그먼트를 양성 쌍(positive pair)으로 처리
- 데이터 증강(augmentation) 없이도 파생되므로 **faulty alignment 문제 회피**
- 전역 표현(global representation) 간 시간 불변성(temporal invariance) 학습

### 3. RLM — Random Lead Masking
- 학습 시 ECG 리드를 무작위로 마스킹하는 증강 기법
- 다양한 리드 구성에 대한 강건성 확보

---

## 다운스트림 태스크

| 태스크 | 데이터셋 | 규모 |
|-------|---------|------|
| ECG 해석 레이블 예측 | UHN-ECG | 573,670개 ECG |
| ECG 해석 레이블 예측 | MIMIC-IV-ECG | 787,677개 ECG |
| 좌심실 박출률 감소(LVEF) 예측 | UHN-ECG | 129,121개 ECG |

---

## 실험 결과

| 레이블 | 지표 | 값 |
|-------|-----|---|
| 심방세동(Atrial Fibrillation) | AUROC | 0.996 |
| LVEF ≤ 40% | AUROC | 0.929 |

- 소규모~중규모 데이터 환경에서 태스크 특화 모델 대비 **현저한 성능 우위**
- 데이터셋 간 일반화(cross-dataset generalizability) 검증
- 3× NVIDIA A100 80GB GPU로 200 epoch 사전학습

---

## 재현 방법

```bash
# 1) MIMIC-IV-ECG 접근 (PhysioNet 계정 필요)
#    https://physionet.org/content/mimic-iv-ecg/
# 2) PhysioNet 2021 데이터 다운로드
#    https://physionet.org/content/challenge-2021/
# 3) 코드 클론
git clone https://github.com/bowang-lab/ECG-FM
cd ECG-FM && pip install -r requirements.txt
# 4) 사전학습 실행
python pretrain.py
```

---

## Citation

```bibtex
@article{mckeen2024ecgfm,
  title={ECG-FM: An Open Electrocardiogram Foundation Model},
  author={McKeen, Kaden and Masood, Sameer and Toma, Augustin and Rubin, Barry and Wang, Bo},
  journal={JAMIA Open},
  year={2025},
  url={https://arxiv.org/abs/2408.05178}
}
```
