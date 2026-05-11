# ECG 기반 모델

ECG 신호를 대규모 데이터로 사전학습(pre-training)한 파운데이션 모델들을 소개합니다.

| 모델 | 학회/저널 | 사전학습 데이터 | 특징 |
|------|-----------|----------------|------|
| [ECG-FM](ecg-fm.md) | JAMIA Open 2025 | 1.5M ECGs (MIMIC-IV-ECG) | Transformer, 하이브리드 대조+생성 SSL, 오픈웨이트 |
| [HeartLang](heartlang.md) | ICLR 2025 | 다중 공개 ECG 데이터셋 | QRS 토크나이저, 하트비트=단어 ECG 언어 모델 |
| [ECGFounder](ecgfounder.md) | NEJM AI 2025 | 10M+ ECGs (Harvard-Emory ECG DB) | 150개 레이블 카테고리, 전문의 수준 진단 |
