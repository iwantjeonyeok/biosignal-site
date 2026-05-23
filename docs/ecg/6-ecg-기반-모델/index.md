# ECG 기반 모델

ECG 신호를 대규모 데이터로 사전학습(pre-training)한 파운데이션 모델들을 소개합니다.

| 모델 | 학회/저널 | 사전학습 데이터 규모 | 연구기여 |
|------|-----------|----------------|------|
| [HeartLang](heartlang.md) | ICLR 2025 | 0.8M ECGs(MIMIC-IV-ECG) | QRS-Tokenizer와 ECG vocabulary를 통해 심박 형태와 리듬 수준 표현을 함께 학습하는 ECG language processing 모델 |
| [ECGFounder](ecgfounder.md) | NEJM AI 2025 | 10M+ ECGs (Harvard-Emory ECG DB, ) | 1,000만 개 이상 ECG와 150개 진단 라벨로 학습한 대규모 범용 ECG 진단 모델|
| [ECG-FM](ecg-fm.md) | JAMIA Open 2025 | 0.87M (PhysioNet 2021, MIMIC-IV-ECG) | WCR 사전학습으로 ECG의 표현을 학습하는 open-weight foundation model|

