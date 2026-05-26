# 2.5. Annotation (주석, 라벨링 정보)

AI 모델을 학습하기 위해 ECG 데이터셋에는 다양한 주석(annotation) 정보가 포함됩니다. 이러한 주석은 업계 표준(MIT-BIH, AAMI EC57, PhysioNet)을 따르며, 심장 전문의에 의해 수동으로 검증됩니다.



##  박동(Beat) 수준 주석

### MIT-BIH 데이터베이스 Beat Annotation Codes

MIT-BIH 부정맥 데이터베이스는 가장 광범위하게 사용되는 ECG 데이터셋으로, 다음과 같은 beat annotation codes를 사용합니다:

| 코드 | 박동 유형 | 설명 |
|------|---------|------|
| **N** | Normal beat | 정상 동박동(Normal sinus rhythm에서 발생) |
| **L** | Left Bundle Branch Block beat | 좌각차단 박동 |
| **R** | Right Bundle Branch Block beat | 우각차단 박동 |
| **B** | Bundle Branch Block beat (unspecified) | 각차단 박동(미분류) |
| **A** | Atrial premature beat | 심방 조기 박동 |
| **a** | Aberrated atrial premature beat | 변형된 심방 조기 박동 |
| **J** | Nodal (junctional) premature beat | 결절 조기 박동 |
| **S** | Supraventricular premature or ectopic beat | 상심실 조기 또는 이소성 박동 |
| **V** | Premature ventricular contraction | 심실 조기 박동 |
| **F** | Fusion of ventricular and normal beat | 심실박동과 정상박동의 융합 |
| **e** | Atrial escape beat | 심방 탈출 박동 |
| **j** | Nodal (junctional) escape beat | 결절 탈출 박동 |

**주석 절차:**
- 두 명 이상의 경험 많은 심장 전문의가 각각 독립적으로 각 기록을 검토
- 자동 검출 알고리즘의 결과를 수정
- 의견 불일치 시 합의를 통해 최종 분류 결정
- 약 110,000개의 beat annotation 생성

### AAMI EC57 표준 분류

업계 표준인 ANSI/AAMI EC57:1998/(R)2008은 MIT-BIH의 상세 코드를 5개의 Superclass와 15개의 세부 classes로 재분류합니다:

#### Superclass 1: Normal Beat (N)
- **N**: Normal beat (정상 박동)
- **L**: Left bundle branch block beat (좌각차단)
- **R**: Right bundle branch block beat (우각차단)

**특징:**
- 정상 동결절에서 발생하는 박동
- 심박수 60-100 bpm 범위
- PR 간격 일정 (0.12-0.20초)
- QRS 폭 정상 또는 각차단으로 인한 확대

#### Superclass 2: Supraventricular Ectopic Beat (SVEB)
- **A**: Atrial premature beat (심방 조기 박동)
- **a**: Aberrated atrial premature beat (변형 심방 조기 박동)
- **J**: Nodal premature beat (결절 조기 박동)
- **S**: Supraventricular premature beat (상심실 조기 박동)
- **e**: Atrial escape beat (심방 탈출 박동)
- **j**: Nodal escape beat (결절 탈출 박동)

**특징:**
- 심방 또는 AV 결절에서 발생
- 정상 QRS 폭 (심방세동 제외)
- 정상 박동의 주기를 벗어남
- 상대적으로 위험도 낮음

#### Superclass 3: Ventricular Ectopic Beat (VEB)
- **V**: Premature ventricular contraction (심실 조기 박동)

**특징:**
- 심실에서 발생하는 조기 박동
- 폭이 넓은 QRS 복합파 (>120ms)
- 완전 보상 일시정지(compensatory pause) 동반
- 심각도가 높으며 건강 위험 증가

**임상적 중요성:**
- 빈번한 VPC (>1000회/일)는 심근 손상 위험 증가
- 기저 심장 질환 있을 시 예후 악화 가능
- 급성 심근경색 환자에서 특히 주의

#### Superclass 4: Fusion Beat (F)
- **F**: Fusion of ventricular and normal beat (심실-정상 박동 융합)

**특징:**
- 심실 조기 박동과 정상 박동이 동시에 발생
- QRS 폭이 정상과 VPC의 중간 형태
- 결론적으로 분류 어려움을 나타냄

#### Superclass 5: Unknown Beat (Q)
- **Q**: Unclassifiable beat (미분류 박동)
- Paced beat (인공심박동기 박동)
- 신호 품질 문제 등으로 인해 분류 불가능한 박동


##  리듬(Rhythm) 수준 주석

### Rhythm Annotation Codes

개별 박동 외에도 ECG는 리듬 변화를 나타내는 rhythm annotations를 포함합니다. 이는 특정 리듬이 시작되고 끝나는 지점을 표시합니다.

#### 주요 Rhythm 주석

| 코드 | 의미 | 설명 |
|------|-----|------|
| **(AFIB)** | Atrial Fibrillation | 심방세동: 무질서한 기준선, 불규칙한 RR 간격 |
| **(AFL)** | Atrial Flutter | 심방 조동: 톱니 모양의 기준선 |
| **(JRAT)** | Junctional Rhythm | 결절 리듬: AV 결절에서 발생하는 규칙적 리듬 |
| **(SRAT)** | Sinus Rhythm Abnormality | 동리듬 이상 |
| **(VT)** | Ventricular Tachycardia | 심실빈맥: 폭이 넓은 QRS, 심박수 >100 bpm |
| **(ST)** | ST Change | ST 분절 변화 시작/종료 |
| **(T)** | T-wave Change | T파 형태 변화 |
| **(+)** | Rhythm Change | 리듬 변화 발생 |


##  ST 분절 및 QT 변화 주석

### PhysioNet European ST-T Database 표준

#### ST 분절 주석

**ST 상승/하강 표시:**
- 각 ST change 에피소드의 시작점과 종료점 명시
- 절대적 ST level이 아닌 ST deviation 함수로 표현
- Transient (일시적) ST 변화 vs Fixed (고정적) ST 변화 구분

**ST 변화의 종류:**
- **ST Elevation**: J점에서 0.1mV(1mm) 이상 상승
  - 급성 심근경색(STEMI) 의심
  - 관상동맥 폐색 신호
  
- **ST Depression**: 0.05mV 이상 하강
  - 심근 허혈(ischemia)
  - 불안정형 협심증 가능성

#### QT 간격 주석

**QT 데이터베이스 (PhysioNet):**
- P, QRS, T, U파의 onset, peak, end 마커 포함
- 각 기록당 30-50개 선정 박동에 대한 상세 마크업
- 15분 길이의 2-lead ECG 기록, 100개 이상의 기록

**마크업 항목:**
- **P wave**: onset, peak, end
- **QRS complex**: onset, peak (R), end
- **T wave**: onset, peak, end
- **U wave**: 있을 경우 onset, peak, end










