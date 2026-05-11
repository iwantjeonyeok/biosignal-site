# HeartLang (ICLR 2025)

**Reading Your Heart: Learning ECG Words and Sentences via Pre-training ECG Language Model**

---

## 1. 논문 정보

| 항목 | 내용 |
| --- | --- |
| 제목 | Reading Your Heart: Learning ECG Words and Sentences via Pre-training ECG Language Model |
| 학회 | ICLR 2025 |
| 저자 | Jiarui Jin, Haoyu Wang, Hongyan Li, Jun Li, Jiahui Pan, Shenda Hong |
| 링크 | https://github.com/PKUDigitalHealth/HeartLang |

---

## 2. 모델 개요

HeartLang은 ECG 신호를 자연어처럼 처리하는 새로운 관점의 자기지도 학습(SSL) 프레임워크입니다. 하트비트(heartbeat)를 단어(word), 리듬(rhythm)을 문장(sentence)으로 간주하여 ECG 신호의 형태적·리듬적 표현을 동시에 학습합니다.

기존 ECG SSL 방법들이 고정 크기의 시간 창(time window)으로 신호를 분할하여 ECG 고유의 형태와 리듬 특성을 무시한 것과 달리, HeartLang은 QRS 복합체를 의미 단위로 분할합니다.

---

## 3. 방법론

### QRS-Tokenizer

- 원시 ECG 신호에서 QRS 복합체를 검출해 의미 있는 ECG "문장"을 생성
- 역대 최대 규모의 하트비트 기반 ECG 어휘(vocabulary)를 구축

### 학습 목표

- **Form-level**: 개별 하트비트(단어) 표현 학습
- **Rhythm-level**: 하트비트 시퀀스(문장) 패턴 학습

---

## 4. 실험 결과

6개 공개 ECG 데이터셋에서 평가하였으며, 기존 ECG SSL 방법 대비 경쟁력 있는 성능을 달성했습니다.

---

## 5. 의의

- ECG를 언어처럼 처리하는 새로운 패러다임 제시
- QRS 기반 토크나이저로 ECG 도메인 지식을 학습에 반영
- 코드 및 어휘 데이터 공개
