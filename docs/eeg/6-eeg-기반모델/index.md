# EEG 기반 모델

EEG 신호를 대규모 데이터로 사전학습(pre-training)한 파운데이션 모델들을 소개합니다.

| 모델 | 학회/저널 | 사전학습 데이터 | 특징 |
|------|-----------|----------------|------|
| [LaBraM](labram.md) | ICLR 2024 (Spotlight) | ~2,535 h (20개 데이터셋) | VQ 토크나이저 + Masked EEG Modeling |
| [CBraMod](cbramod.md) | ICLR 2025 | >9,000 h (TUEG) | Criss-Cross Attention, 단일 대규모 코퍼스 |
| [NeuroLM](neurolm.md) | ICLR 2025 | ~25,000 h (TUEG + 공개 데이터) | LLM 백본, 멀티태스크 인스트럭션 튜닝 |
| [CSBrain](csbrain.md) | NeurIPS 2025 | >9,000 h (TUEG, CBraMod 동일) | Cross-scale Spatiotemporal 인코딩 |
| [REVE](reve.md) | NeurIPS 2025 | 61,415 h (92개 데이터셋, 24,274명) | 가장 대규모 공개 EEG 사전학습 코퍼스 |
| [NERVE](nerve.md) | ICML 2026 (under review) | 10,956 h (27개 데이터셋) | 노이즈 강인 토크나이저 + KoLeo 정규화 |
