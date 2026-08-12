# What Time Series Foundation Models Erase: Amplitude, Rhythm Recovery for ECG Diagnosis

**Sangjin Yoon¹, Hyunwoo Seo¹, Chiehyeon Lim¹˒²**  
¹ Ulsan National Institute of Science and Technology, Ulsan, Republic of Korea  
² Pohang University of Science and Technology, Pohang, Republic of Korea

## Abstract

ECG 전용 기반모델은 대규모 사전학습 데이터와 계산 자원을 요구하므로, 사전학습된 일반 시계열 기반모델 (TSFM)을 ECG 진단 테스크에 전이하는 접근이 중요해지고 있다. 그러나 TSFM이 ECG 고유의 진단 정보를 보존하는지는 충분히 규명되지 않았다. 본 연구는 대표적 TSFM인 MOMENT와 LPTM을 PTB-XL에 적용하고, 동결 임베딩에 linear probing을 수행하여 PTB-XL의 네 태스크의 성능과 실패 원인을 분석하였다. TSFM의 인스턴스 정규화는 리드별 절대 진폭과 진폭비를 제거하고, 최종 표현은 RR 기반 박동 간 시간 정보를 충분히 보존하지 못해 전압 기반 진단과 리듬 변이 구분을 제한하였다. 이를 보완하기 위해 본 연구는 리드별 진폭 통계와 RR 분포 및 박동 간 변동 정보를 모델 독립적 보조 특성으로 구성하여 동결 TSFM 임베딩에 주입하는 전이 방법을 제안한다. 그 결과 0.4% 이하의 파라미터 증가만으로 두 모델의 네 태스크 성능을 모두 향상시켰으며, 특히 전압 의존 클래스와 리듬 변이 클래스에서 뚜렷한 회복을 확인하였다. 이는 TSFM의 ECG 적용에서 구조적으로 소실되는 물리량을 명시적으로 복원하는 것이 효율적이고 해석 가능한 도메인 적응 전략임을 보여준다.
