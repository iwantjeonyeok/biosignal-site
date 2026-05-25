# EEG 기반 모델

EEG 신호를 대규모 데이터로 사전학습(pre-training)한 파운데이션 모델들을 소개합니다.

| 모델 | 학회/저널 | 사전학습 데이터 규모 | 연구 기여 |
|------|-----------|----------------|------|
| [LaBraM](labram.md) | ICLR 2024 (Spotlight) | ~2,535 h (20개 데이터셋) | 최초격의 EEG 파운데이션 모델  |
| [CBraMod](cbramod.md) | ICLR 2025 | >9,000 h (단일 데이터셋 TUEG) | 전극간 공간적 상관 반영을 위한 Criss-cross Attention |
| [NeuroLM](neurolm.md) | ICLR 2025 | ~25,000 h (TUEG + 12개의 추가 공개 데이터) | LLM을 활용한 Multi-task Instruction Tuning |
| [CSBrain](csbrain.md) | NeurIPS 2025 | >9,000 h (단일 데이터셋 TUEG) | EEG 시그널의 다양한 스케일 정보 학습을 위한 파운데이션 모델 |
| [REVE](reve.md) | NeurIPS 2025 | 61,415 h (92개 데이터셋, 피실험자 24,274명) | 시그널 수집 간 다양한 채널 구성 반영 및 적응 위한 파운데이션 모델 |
| [NERVE](nerve.md) | NeurIPS 2026 (under review) | 10,956 h (27개 데이터셋) | 시그널 수집 간 잡음, 변동성, 다양한 채널 구성에 강건한 파운데이션 모델 |
