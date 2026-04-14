# E-meta: 집필 과정의 메타 실험

> **번호**: E-meta (E01~E22 외부. Appendix A 별도 섹션)
> **목적**: 집필 과정 자체를 AgentOps 데이터로 기록하여 Ch.5 cost metric 번역 사례와 Ch.7 §9 내용을 실증
> **기간**: 2026-03-19 ~ 베타 마감 (2026-04-30)
> **배치**: Ch.5 §cost-translation(3-A 1~2문단), Ch.7 §9(3-A/B/C 종합), Appendix A(로그 템플릿)
> **메타 원칙**: 이 실험 자체가 Ch.6 "점진적 도구화" 원칙의 dogfooding이다. 7-agent 상시 가동에서 3-layer on-demand 구조로의 전환 판단이 Ch.6의 주장과 정합하는지를 이 데이터가 검증한다.

---

## 3-A. 아키텍처 전환 판단 기록

### 기록 대상

7-agent 계획(드래프터 7명 병렬 상시 가동)에서 3-layer 구조(Kiwon drafter 1 + Edna editor 1 + Vera/Felix specialist on-demand)로 전환한 판단을 비용 구조로 기록한다.

### 추정 비용 계산 방법

**7-agent 시뮬레이션 추정 token cost (챕터당)**:
- Context 주입량: 챕터 map 섹션 + glossary + 이전 챕터 요약 ≈ 평균 8,000 tokens (input)
- 세션 수: 7 agents × 챕터당 동시 가동
- 평균 iteration: 드래프트 → 용어 불일치 수정 → voice drift 교정 ≈ 3 rounds/챕터
- 추정 총 context: 8,000 × 7 × 3 = 168,000 tokens/챕터 (input only)
- harness overhead(Harness Overhead Ratio): harness context(168,000) / payload(실제 초고 생성 token) ≈ ?
  → 측정 시작점: 3-layer 실측 후 비율 비교

**3-layer 실제 token cost (챕터당)**:
- Drafter 1 session context: 챕터 map + glossary + 이전 챕터 요약 ≈ 8,000 tokens
- Specialist consultation 호출: 챕터당 평균 횟수 × 호출당 token
  → 측정 항목: Vera 호출 횟수/토큰, Felix 호출 횟수/토큰
- Edna 판정: 챕터당 판정 1~3회 × 판정당 context token
- 추정 harness overhead: (8,000 + specialist + editor) / 초고 생성 token

**예상 rework loop 비용**:
- 7-agent: 용어 불일치 발생 확률 ≈ 에이전트 수 증가에 비례. 7개 voice가 동시에 작동할 때 용어 표류(terminology drift) 발생 시 수정 루프 1회당 전체 context 재주입 필요 → 수정 비용이 기하급수적으로 증가.
- 3-layer: 단일 drafter이므로 voice drift는 드래프터 내부에서 통제됨. Edna가 terminology drift를 감지하면 수정 범위가 로컬(해당 섹션)에 한정.
- 비교 공식: `Rework_cost(7-agent) = n_agents × drift_probability × full_context_size` vs `Rework_cost(3-layer) = drift_probability × local_section_size`

### Ch.5 연결

TotalCost 구조의 미니어처. "harness context가 payload보다 커지면 harness overhead이 최적점을 넘는다"는 주장(Ch.5)의 집필 과정 증거. 7-agent 구조에서 harness context(에이전트 간 조율, context 동기화, voice 검증)가 실제 초고 생성 payload를 초과하는 시점을 추정값으로 제시하고, 3-layer 실측값과 비교한다.

### 기록 로그

| 날짜 | 이벤트 | 7-agent 추정 token | 3-layer 실측 token | 메모 |
|------|--------|-------------------|-------------------|------|
| 2026-03-19 | 아키텍처 전환 결정 | (계산값 기입) | N/A | 전환 이전 기준점 |
| | | | | |

---

## 3-B. Voice Consistency 측정

### 기록 대상

단일 drafter 전략에서 voice drift 발생 빈도와, Edna REVISE 판정 중 voice 관련 비율. Voice drift 없이 PASS 비율이 높으면 단일 drafter 전략의 유효성이 확인된다.

### 측정 방법

Edna가 REVISE 판정을 내릴 때, 사유를 다음 카테고리 중 하나로 분류한다:

| 카테고리 | 정의 | 예시 |
|----------|------|------|
| **voice** | AI 문체 8대 금지 패턴 위반, 교수 문체에서 이탈 | 단문 나열, 설교조 종결, 메타 전환 어구 사용 |
| **terminology** | 핵심 용어 조작적 정의 불일치 | 모델 능력 지표, harness overhead, 실패 재분류 정의 충돌 |
| **logic** | 인과 구조 불명확, 논증 단계 누락 | 주장 후 근거 없음, 전제 없는 결론 |
| **evidence** | 실험 참조 오류, 수치 없는 성능 서술 | "훨씬 빠르다", 존재하지 않는 실험 번호 인용 |
| **structure** | 문단 기능 혼합, 섹션 흐름 단절 | 문제 제기 + 결론이 동일 문단, 챕터 간 예고 누락 |

Edna 판정 후 수정 iteration마다 사유 카테고리를 기록한다. voice 비율이 낮으면(≤20%) 단일 drafter 전략의 유효성이 확인된다. voice 비율이 높으면(≥40%) drafter context 주입 방식 재검토 신호.

### Ch.6 연결

점진적 도구화 원칙의 실증. Specialist를 상시 가동하지 않고 on-demand로 호출하는 전략이 voice consistency를 보존했는지를 이 데이터가 검증한다. specialist 상시 가동 = voice drift 위험 증가(다수 목소리가 동시에 개입)라는 Ch.6의 주장이 집필 과정에서 재현되는지 확인한다.

---

## 3-C. Edna 판정 분포

### 기록 대상

챕터별 PASS / REVISE / REJECT 판정 횟수와 사유. 판정 분포가 harness(Edna) 작동 여부와 drafter context 주입 품질의 지표가 된다.

### 측정 방법

각 판정에 대해 다음 항목을 기록한다:

| 항목 | 설명 |
|------|------|
| 대상 챕터 + 섹션 | 예: Ch.1 §3 |
| 판정 결과 | PASS / REVISE / REJECT |
| 1차 사유 | voice / terminology / logic / evidence / structure 중 하나 |
| 수정 후 재판정 iteration 횟수 | PASS까지 몇 번 수정이 필요했는가 |

### 판정 로그

| 챕터 | 섹션 | 판정 | 1차 사유 | Iteration 수 | 날짜 | 메모 |
|------|------|------|----------|-------------|------|------|
| Preface | 전체 | | | | | |
| Ch.1 | §1 | | | | | |
| Ch.1 | §2 | | | | | |
| Ch.1 | §3 | | | | | |
| Ch.1 | §4 | | | | | |
| Ch.1 | §5 | | | | | |
| Ch.1 | §6 | | | | | |
| Ch.1 | §7 | | | | | |
| Ch.1 | §8 | | | | | |
| Ch.2 | §1 | | | | | |
| Ch.3 | §1 | | | | | |
| Ch.4 | §1 | | | | | |
| Ch.5 | §1 | | | | | |
| Ch.6 | §1 | | | | | |
| Ch.7 | §1 | | | | | |

### 해석 기준

- **REVISE 비율 높음 (≥50%)**: harness(Edna)가 작동 중. 품질 기준이 실제로 적용되고 있다는 신호.
- **REJECT 비율 높음 (≥20%)**: drafter context 주입 부족 신호. 챕터 map 섹션, glossary, 이전 챕터 요약의 주입 방식을 재검토한다.
- **PASS 비율 높음 (≥70%) + voice 사유 낮음**: 단일 drafter 전략의 유효성 확인.
- **voice 사유 비율 높음 (≥40%)**: AI 문체 8대 금지 체크리스트를 drafter context에 재주입.

### Ch.3 연결

harness overhead × RSuccR trade-off의 미니어처 데이터. Edna를 추가하는 것(harness overhead 증가)이 REVISE iteration 감소(RSuccR 향상)로 이어지는지, 그리고 그 교환이 순 비용 절감인지 증가인지를 3-A의 token cost 데이터와 결합하여 분석한다.

---

## 결과 배치 계획

| 데이터 | 배치 위치 | 분량 |
|--------|-----------|------|
| 3-A (아키텍처 전환 비용) | Ch.5 cost metric 번역 섹션 | 1~2문단 |
| 3-A + 3-B + 3-C 종합 | Ch.7 §9 "집필 과정의 메타 관찰" | 섹션 전체 |
| 로그 템플릿 | Appendix A | 테이블 형식 |

---

## Appendix A 로그 템플릿 (초안)

```markdown
## E-meta 판정 로그

**기록 기간**: YYYY-MM-DD ~ YYYY-MM-DD
**총 섹션 수**: N
**총 판정 수**: N (PASS: N, REVISE: N, REJECT: N)

### 요약 통계
- PASS 비율: N%
- REVISE 비율: N%
- REJECT 비율: N%
- 평균 iteration to PASS: N회
- REVISE 사유 분포: voice N% / terminology N% / logic N% / evidence N% / structure N%

### 판정 로그
[판정 로그 테이블]

### 아키텍처 비용 요약 (3-A)
- 7-agent 추정 token cost (챕터당): N tokens
- 3-layer 실측 token cost (챕터당): N tokens
- harness overhead 비교: 7-agent N / 3-layer N
- 절감 비율: N%
```
