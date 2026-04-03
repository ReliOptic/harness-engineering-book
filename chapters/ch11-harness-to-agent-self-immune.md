# Ch.11 — Harness에서 Agent로: Self-Immune System을 향하여

> 상태: 🔴 초고 v0.1 (2026-03-18) — §1~§2 기존 유지, §3~§9 신규 작성
> 담당: Kiwon
> 목표 분량: 8,000~10,000자

---

## 핵심 메시지

Self-immune system이란 agent가 외부 harness의 규칙 없이도 자신의 ARCC 저하를 감지하고, failure budget이 unrecoverable 방향으로 재배분되기 전에 스스로 개입하는 능력이다. 이 능력은 현재의 harness를 통해 점진적으로 주입 가능하다 — 단, 주입이 성립하는 ARCC 하한 조건이 있으며, 그 조건이 충족되지 않으면 self-immune 구조 자체가 새로운 failure source가 된다. Agent-1 → Agent-2 전환은 이 하한 조건의 달성 여부에 의존한다.

## 학습 결과

- Self-immune system의 조작적 정의를 이해한다: ARCC self-estimate + cliff-proximity detection + self-initiated recovery.
- ARCC self-monitoring의 재귀적 한계를 이해한다: self-monitoring 자체가 ARCC를 요구하며, ARCC가 cliff 이하이면 self-monitoring을 신뢰할 수 없다.
- Fig 11 (Model × Harness Scaling) 결과를 해석하고, model capability 증가가 harness의 역할을 방어에서 조정으로 전환시키는 ARCC 조건을 설명할 수 있다.
- Fig 12 (Temporal Stability) 결과를 해석하고, self-immune system의 degradation 조건과 재보정 mechanism의 필요성을 설명할 수 있다.
- Agent-1 → Agent-2 전환의 충분조건과 필요조건을 구분하여 설명할 수 있다.
- 이 책의 실험이 답하지 못한 질문들을 측정 가능한 형태로 정의할 수 있다.

## 집필 노트

- 관련 DR: DR-7.1 (self-healing agent), DR-7.2 (continuous learning), DR-3.4 (ontology as agent memory structure — §9: Agent-2 전환과 ontology 내재화 논증)
- 관련 실험: E12 (self-immune overhead), E20 (mini self-immune)
- 관련 Figure: Fig 9 (Harness ROC), Fig 11 (Harness × Model Scaling), Fig 12 (Temporal Stability)

**Self-immune의 조작적 정의:**
- (1) agent가 현재 실행 context에서 ARCC sub-components(TCA, IFR, MSRD_n, CUE)를 self-estimate한다
- (2) estimate가 cliff threshold에 근접하면 스스로 복구 경로(context reset, task decomposition 재시도, operator escalation 요청)를 실행한다
- (3) 외부 operator intervention 없이 이 루프를 유지한다

**재귀적 한계:**
- Agent가 자신의 ARCC를 estimate하는 것 자체가 ARCC를 요구한다.
- ARCC가 cliff 이하이면 self-estimate도 신뢰할 수 없다. Self-immune이 무너지는 순간에 self-monitoring도 무너진다.
- 이 재귀적 구조가 self-immune system의 하한 조건을 만든다.

**Scaling 연결 (Fig 11):**
- 가설: ARCC가 충분히 높아지면 harness의 역할이 "방어(실패 차단)" → "조정(실행 품질 유지)"으로 전환된다.
- 이 전환이 일어나는 ARCC threshold가 Agent-2 전환의 하한 조건과 일치하는지가 핵심 질문.

**Temporal stability (Fig 12):**
- 72시간 연속 운영에서 self-immune performance 변화.
- "Infinite learning"이 가능하려면 fatigue를 상쇄하는 재보정 mechanism이 필요하다.

---

## Outline

**계획된 섹션:**

1. **실험이 남긴 것 (초고 v0.2 존재)**
2. **현 세대 harness가 아직 풀 수 없는 문제 (초고 v0.1 존재)**
3. **AgentOps → Harness → Agent 내재화: 점진적 경로**
4. **Self-immune system 초기 설계**
5. **Model Capability × Harness Value: Scaling 조건**
6. **Temporal Stability: self-immune은 얼마나 오래 유지되는가**
7. **Agent-1 → Agent-2: 전환 조건의 정식화**
8. **이 책 이후: 미해결 질문들**
9. **집필 과정의 메타 관찰**

---

## §1 실험이 남긴 것

> 상태: 🟡 초고 v0.2 (2026-03-18)

필자가 이 책의 실험을 설계할 때 확인하려 했던 질문은 하나였다. 동일한 task, 동일한 모델, 동일한 surface 조건에서, harness의 존재 여부가 failure의 성격을 어떻게 바꾸는가. 22개의 시나리오를 다섯 개의 축으로 묶어 pre-registration 원칙 하에 실행했다. 실험이 끝나고 예상한 것과 달랐던 것이 두 가지 있다.

harness는 failure budget의 구성을 recoverable 방향으로 이동시켰지만, 총량은 변하지 않았다.

Failure budget이 재배분된 방향은 일관됐다. Tool call failure와 output format error처럼 구조적으로 감지 가능한 failure는 harness-on 조건에서 recovery attempted 범주로 이동했다. E05부터 E08에 걸친 harness 변수 조작 실험에서, failure 6축 radar의 형태가 변했다 — 면적은 유사하게 유지되었으나 silent logical drift의 비율이 줄고 recovery succeeded의 비율이 늘었다. Harness는 failure를 제거하지 않는다. Failure를 더 비싸지 않은 유형으로 교환한다.

재배분이 일어나지 않은 failure들의 목록은 다른 성격을 띤다. 에이전트가 각 단계를 올바른 절차대로 밟으면서도 전체 방향이 틀린 경우 — 이것은 ARCC sub-components 중 IFR(Instruction Following Rate)의 decay가 단계별로는 감지되지 않다가 task 수준에서 누적되는 패턴이다. E21에서 task 자체를 모호하게 설계했을 때 드러난 것이 이것이다. Harness는 각 tool call의 schema validity를 검증하지만, tool call sequence 전체가 instruction의 암묵적 constraint를 충족하는지는 검증하지 않는다. IFR이 threshold 아래로 내려가는 것을 외부에서 감지하려면, 이미 충분히 낮아진 이후다.

Operator intervention이 가장 효과적이었던 시점은 failure 직후가 아니라 IFR decay가 시작되는 시점이었다. 이것은 MTTR 최소화의 문제다. Failure가 발생한 이후에 개입하면 recovery는 가능하지만 MTTR이 이미 높아진 상태다. IFR decay가 시작되는 시점은 외부에서 바라보면 정상 출력처럼 보인다 — 문법적으로 완결되고 tool call도 schema를 통과한다. 방향 이탈은 구조적으로 감지 가능하지 않다.

이것이 이 챕터의 출발점이다. MTTR을 구조적으로 낮추려면, failure가 발생한 이후의 recovery 속도가 아니라, failure budget이 silent 범주로 이동하기 전의 감지 능력이 필요하다. 그 감지 능력은 외부 harness가 아니라 agent 내부의 ARCC self-monitoring에서 나온다. 현재의 harness 구조는 이것을 제공하지 않는다. 이것이 self-immune system이 필요한 이유이며, 동시에 self-immune system이 어렵다는 이유다.

---

## §2 현 세대 harness가 아직 풀 수 없는 문제

> 상태: 🟡 초고 v0.1 (2026-03-18)

필자가 이 책의 실험을 설계하면서 가장 오래 고민한 것 중 하나는 반례를 어디에 배치할 것인가였다. Harness가 무엇을 할 수 있는지를 기록하는 것과, harness가 무엇을 할 수 없는지를 기록하는 것은 동일한 무게를 가져야 한다. §1에서 기술한 failure budget 재배분 — harness-on 조건에서 silent logical drift가 줄고 recovery succeeded가 늘었다는 관찰 — 은 그 조건이 성립하는 범위 안에서만 유효하다. 그 범위 밖에 있는 문제들이 존재한다.

규칙 기반 방어의 구조적 한계는 정의에서 나온다. Harness는 알려진 failure pattern을 알려진 방식으로 차단한다. 이것은 강점이면서 동시에 harness가 다룰 수 없는 영역의 경계를 만든다. E14에서 관찰한 것처럼 반복 가능한 failure — tool call schema 위반, timeout, output format error — 는 규칙으로 포착되고 자동 재시도로 처리된다. 문제는 처음 본 failure다. 패턴으로 등록되지 않은 실패는 harness를 통과한다. 규칙이 없으면 차단도 없다.

이것이 추상적인 한계처럼 들릴 수 있으나, FCR-004(맥락 구분 실패)에서 구체적인 형태로 발생했다. 뉴스 브리핑 에이전트가 "삼성 식기세척기 A/S 접수"라는 입력을 받았다. SOUL.md에 설정된 파이프라인은 "모든 입력을 요약하고 KG 시트에 적재하라"였다. 에이전트는 "삼성", "오작동", "원인파악"을 추출하고 KG 스키마에 맞게 채워 넣었다 — 성실하게, 정확하게. 문제는 이 입력이 KG에 적재할 대상이 아니라는 판단이 선행되지 않았다는 것이다. Harness에는 "이것이 뉴스인가, 개인 용무인가"를 묻는 intent gate가 없었다.

이 사례에서 harness가 실패한 것은 아니다. Harness는 설계된 대로 정확히 작동했다. 실패는 harness 설계 자체에 있었다 — "무엇을 할 것인가"를 지시하기 전에 "할 것인가 말 것인가"를 판단하는 게이트가 없었다. 이 구분이 중요한 이유는, intent classification이 규칙으로 구현하기 어렵기 때문이다. "외부 뉴스/산업 동향"과 "개인 용무"의 경계는 문맥에 따라 이동한다. 삼성 관련 기사는 적재 대상이고 삼성 식기세척기 A/S는 적재 비대상이다. 이 경계를 하드코딩된 규칙으로 표현하는 것은 가능하지 않다 — 경계가 얼마나 많은지, 그리고 경계가 얼마나 빠르게 이동하는지를 생각하면.

ARCC가 cliff threshold 근처에서 운영되는 agent에 대한 harness의 한계는 더 근본적이다. Harness는 agent의 tool call sequence를 관찰하고 schema validity를 검증한다. 각 단계가 구조적으로 올바르다면 harness는 통과 신호를 보낸다. 그러나 E09에서 설계한 goal drift 관찰이 예고하는 것처럼, 각 단계의 schema validity와 전체 방향의 correctness는 별개의 문제다. 40개 step이 모두 tool call schema를 통과하면서 초기 목표로부터 멀어질 수 있다 — IFR decay가 step 단위로는 감지되지 않고 task 수준에서 누적되기 때문이다. Harness가 이것을 감지하려면 각 step의 결과가 아니라 step들의 방향성을 평가해야 한다. 방향성 평가는 규칙이 아니라 context 이해를 요구한다.

E21은 이 한계의 반례로 설계되었다. Task 자체를 모호하게 정의하면 — 실험자가 의도적으로 암묵적 constraint를 포함한 instruction을 제공하면 — harness와 모델이 모두 정상인 상황에서도 실패가 발생한다. Harness는 각 tool call의 schema validity를 검증하지만, tool call sequence 전체가 instruction의 암묵적 constraint를 충족하는지는 검증하지 않는다. 이것은 harness의 결함이 아니다. Tool call schema는 명시적 구조이고, 암묵적 constraint는 context에 내재된 의미다. Harness가 접근할 수 있는 층과 접근할 수 없는 층이 다르다.

현 세대 harness가 풀 수 없는 문제들의 공통 구조는 하나다. Harness는 명시적으로 표현된 것을 검증하고, 명시적으로 등록된 패턴을 차단한다. 입력의 의미 분류, tool call 방향의 drift, task constraint의 암묵성 — 이것들은 명시적 구조 레이어가 아니라 semantic 레이어에 있다. Harness가 semantic 레이어에서 작동하려면 context를 이해해야 하고, context 이해는 agent 자신의 ARCC에 의존한다. 이것이 §1에서 예고한 질문으로 다시 돌아오는 지점이다. Self-immune이 필요한 이유는, harness가 닿지 않는 레이어에서 발생하는 실패들이 존재하기 때문이다.

---

## §3 AgentOps → Harness → Agent 내재화: 점진적 경로

> 상태: 🔴 초고 v0.1 (2026-03-18)

외부 harness에서 agent 내부로 기능이 이동하는 것이 이 섹션의 주제다. 이 이동이 왜 가능한지, 어떤 기능이 먼저 이동할 수 있는지, 그리고 어떤 기능은 구조적으로 외부에 남아야 하는지를 분석한다.

AgentOps 실무에서 출발한다. 운영자가 반복적으로 수행하는 개입 패턴이 있다 — token 사용량이 threshold에 근접하면 압축을 수행하고, failure가 특정 유형으로 발생하면 retry를 시도하며, IFR이 낮아지는 신호가 보이면 context를 재설정한다. 이 패턴들은 초기에는 운영자의 수동 개입이다. 반복 빈도가 충분히 높아지면 harness component로 구현된다 — 규칙으로 표현 가능하고, 실행 가능하며, 측정 가능한 형태로. Ch.10 Operational Compiler의 설계 원칙이 이 경로를 따른다.

Harness component로 구현된 기능이 agent 내부로 이동하는 것은 다음 단계다. E18이 보여주는 것처럼 token auto-report는 harness component로 구현된 이후, agent 자신이 token 사용량을 tracking하고 threshold를 감지하는 방향으로 내재화할 수 있다. E19의 failure detect auto-retry도 유사한 경로를 따른다 — 외부 harness가 failure를 감지하고 retry를 실행하던 것이, agent 자신이 failure 신호를 인식하고 재시도 경로를 실행하는 방향으로 이동한다.

token 사용량, tool call failure, output format error는 모두 명시적 신호를 추적하는 것이기 때문에 agent가 내부적으로 동일한 감지 로직을 실행할 수 있다 — 외부 harness가 규칙으로 정의했던 것을 agent가 동일 규칙으로 내부에서 실행하는 구조다.

내재화가 불가능한 기능도 있다. IFR decay의 방향 판단 — 지금 실행 중인 작업의 방향이 초기 목표에서 이탈하고 있는가를 판단하는 것 — 은 규칙이 아니라 context 이해를 요구한다. 이것을 agent 내부로 주입하는 것은 결국 agent 자신의 ARCC를 높이는 것과 동일하다. Agent의 ARCC가 충분히 높으면 이것이 내재화 가능해지지만, ARCC가 낮은 상태에서는 이 판단을 agent 내부에 맡길 수 없다. 외부 harness나 operator의 개입이 대신해야 한다.

이 분류 — 내재화 가능한 것과 외부에 남아야 하는 것 — 가 self-immune 설계의 범위를 결정한다. Self-immune은 내재화 가능한 기능들의 집합이며, 그 집합이 어디까지인가는 agent의 ARCC 수준에 따라 달라진다.

---

## §4 Self-immune system 초기 설계

> 상태: 🔴 초고 v0.1 (2026-03-18)

Self-immune system의 조작적 정의는 세 요소의 연결이다. ARCC self-estimate — agent가 현재 실행 context에서 TCA, IFR, MSRD_n, CUE를 스스로 추정한다. Cliff-proximity detection — estimate가 task-specific cliff threshold에 얼마나 근접했는가를 판단한다. Self-initiated recovery — 근접 신호가 임계값을 넘으면 context reset, task decomposition 재시도, 또는 operator escalation 요청 중 하나를 실행한다. 이 세 단계가 외부 operator intervention 없이 유지되는 루프가 self-immune이다.

각 단계의 설계에서 고려해야 할 것들을 구체화한다. ARCC self-estimate를 위해 agent는 자신의 최근 tool call들의 schema validity와 semantic correctness를 돌아보고, instruction constraint 충족 여부를 재평가하며, multi-step chain의 논리적 연속성을 확인해야 한다. 이것은 별도의 self-reflection loop를 요구한다 — task 실행 루프와 병렬로 실행되는, 자신의 실행 품질을 추적하는 루프. 이 루프 자체가 HOR에 추가된다.

Cliff-proximity detection은 self-estimate 결과를 task-specific threshold와 비교하는 단계다. Ch.6에서 측정한 cliff position이 T1, T2, T3에서 다르다는 결과가 여기서 사용된다 — 동일한 ARCC estimate라도 task 유형에 따라 cliff에 가깝거나 멀다는 판단이 달라진다. 이 판단이 올바르려면 agent가 자신이 실행 중인 task의 유형을 정확히 분류할 수 있어야 한다.

Self-initiated recovery의 세 경로는 각각 다른 조건에서 선택된다. Context reset은 IFR decay가 감지되었으나 task 방향 자체는 여전히 올바를 때 적용한다 — 누적된 context 오염을 제거하고 동일 목표로 재시작. Task decomposition 재시도는 현재 plan이 constraint를 충족하지 못할 때 적용한다 — 더 작은 단계로 task를 분해하고 각 단계를 별도 검증. Operator escalation 요청은 두 경로가 모두 적절하지 않을 때 — 또는 ARCC estimate 자체의 신뢰도가 낮을 때 — 외부 판단을 요청한다.

재귀적 한계는 이 설계의 구조적 취약점이다. Agent가 자신의 ARCC를 estimate하려면 그 estimate를 수행하는 데 필요한 ARCC가 먼저 확보되어야 한다. ARCC가 cliff 이하로 내려간 상황에서는 self-estimate도 신뢰할 수 없다 — cliff에 근접했다는 신호가 나와야 할 때 정상 신호가 나올 수 있다. Self-immune이 가장 필요한 순간이 self-immune이 가장 신뢰하기 어려운 순간이라는 역설이 여기에 있다. 이것이 Agent-2 전환의 ARCC 하한 조건이 존재하는 이유다.

E20(mini self-immune)은 이 설계의 최소 조건 실험이다. 완전한 self-immune 루프가 아니라, token 사용량 monitoring과 간단한 failure detection만을 내재화한 최소 구성에서 무엇이 성립하고 무엇이 성립하지 않는가. 이 실험의 결과가 Ch.9에서 보완된다.

---

## §5 Model Capability × Harness Value: Scaling 조건

> 상태: 🔴 초고 v0.1 (2026-03-18)

Fig 11 (Model × Harness Scaling) — 실험 완료 후 수치 보완

**분석 구조**: ARCC가 증가할 때 harness의 역할이 어떻게 변하는가를 측정한다. 가설은 두 단계의 전환이다. ARCC가 cliff 이하인 구간에서는 harness의 방어 기능이 핵심이다 — failure를 차단하고 recovery를 실행하는 것이 harness의 주된 기여. ARCC가 cliff 이상으로 충분히 높아지면 방어 역할의 기여가 감소하고 조정 역할이 부상한다 — failure가 덜 발생하기 때문에 차단할 것이 줄어들고, 대신 실행 품질을 최적화하는 방향으로 harness의 가치가 이동한다.

이 전환이 일어나는 ARCC threshold가 Agent-2 전환의 하한 조건 후보다. Harness의 역할이 방어에서 조정으로 전환되는 지점에서 agent는 외부 harness에 덜 의존하면서 self-immune 루프를 더 신뢰 가능하게 유지할 수 있다. 이 전환이 발생하는지, 발생한다면 어떤 ARCC 수준에서 발생하는지가 Fig 11이 답하는 질문이다.

> [Fig 11 — 실험 완료 후 수치 보완]

---

## §6 Temporal Stability: self-immune은 얼마나 오래 유지되는가

> 상태: 🔴 초고 v0.1 (2026-03-18)

Fig 12 (Temporal Stability) — 실험 완료 후 수치 보완

**분석 구조**: 72시간 연속 운영에서 동일한 self-immune configuration의 성능이 어떻게 변하는가를 측정한다. Harness fatigue라는 개념이 이 실험의 핵심이다 — self-immune performance가 시간이 지남에 따라 저하된다면, 그 저하의 원인은 무엇인가.

세 가지 가능한 메커니즘을 구분해야 한다. Context 누적 — 장기 운영에서 context가 쌓이면 self-estimate의 정확도가 떨어질 수 있다. Rule drift — harness component의 rule이 운영 환경의 변화에 맞지 않게 되는 것. 모델 측 변화 — 동일한 모델이라도 API 업데이트나 drift가 발생하면 ARCC 분포가 달라질 수 있다. 이 세 메커니즘을 구분하지 않으면 "harness fatigue"라는 현상의 원인을 잘못 진단한다.

Agent-2가 "infinite learning" 가능한 상태라면, 72시간 운영에서 self-immune performance가 저하되지 않거나 오히려 향상되어야 한다. 저하가 관찰된다면 fatigue를 상쇄하는 재보정 mechanism이 필요하다 — context 압축 주기, rule 재검증 트리거, 또는 외부 재보정 주기. 이것이 설계되지 않으면 Agent-2의 "infinite" 학습은 72시간 이후 신뢰할 수 없게 된다.

> [Fig 12 — 실험 완료 후 수치 보완]

---

## §7 Agent-1 → Agent-2: 전환 조건의 정식화

> 상태: 🔴 초고 v0.1 (2026-03-18)

Agent-1에서 Agent-2로의 전환을 정의하기 전에, Agent-1의 작동 방식을 명확히 한다. Agent-1은 tool call을 실행하고 multi-step task를 완수하는 능력이 있지만, 자신의 ARCC 상태를 감지하지 못한다. 외부 harness가 failure를 감지하고 recovery를 실행한다. Operator가 IFR decay를 판단하고 개입 시점을 결정한다. 이 구조에서 agent는 실행자이고 harness와 operator가 감시자다.

Agent-2는 감시자 기능의 일부를 내재화한다. ARCC self-monitoring이 작동하고, cliff-proximity가 감지되며, recovery 경로가 자동 실행된다. Operator는 agent가 escalation을 요청할 때만 개입한다 — HER이 구조적으로 낮아진다.

E10에서 측정하는 ARCC threshold가 이 루프의 하한이다. self-monitoring 루프가 신뢰 가능하게 작동하는 최소 ARCC 수준으로, 이 조건이 충족되지 않으면 self-immune 루프를 추가해도 신뢰 가능한 Agent-2 상태가 되지 않는다 — self-monitoring이 틀린 신호를 내보내고, recovery 경로가 잘못된 상황에서 실행된다. 그 하한을 충족하는 것만으로는 전환이 성립하지 않는다 — self-immune 루프가 외부 개입 없이 72시간 유지된다는 것이 충분조건 후보로 제안되나, 이 기준의 타당성 자체가 Ch.9 결과를 기다리는 미검증 가설이다. 72시간이라는 기준은 임의적이지 않다 — OpenClaw 1세대 실험에서 장애가 72시간 이내에 재현된다는 패턴에서 도출된 운영 horizon이다.

이 두 조건이 달성되지 않으면 self-immune 구조 자체가 새로운 failure source가 된다는 것이 이 챕터의 핵심 경고다. ARCC가 threshold 이하인 상태에서 self-immune을 활성화하면 — 잘못된 self-estimate를 기반으로 잘못된 recovery를 실행하는 루프 — HOR이 증가하고 실제 recovery 성공률은 올라가지 않는다. Agent-1에 harness를 추가하는 것보다 더 나쁜 상태가 될 수 있다.

DR-3.4(ontology as agent memory structure)가 제안하는 것은 Agent-2 상태에서 agent가 자신의 context 구조를 유지하는 방법이다. 자신이 어떤 task를 수행 중이고, 어떤 constraint를 따르고 있으며, 어떤 state에 있는가를 명시적 구조로 유지하는 것이 self-monitoring의 정확도를 높이는 방향이다. 이것은 E20의 결과를 보완할 수 있는 설계 방향이지만, 실험적 검증은 이 책의 범위 밖이다.

---

## §8 이 책 이후: 미해결 질문들

> 상태: 🔴 초고 v0.1 (2026-03-18)

이 섹션은 선언이 아니라 질문의 형식이다. "미래에 연구되어야 한다"는 주장 대신, 각 질문을 검증 가능한 형태로 정의한다. 검증에 필요한 구체적 조건을 명시하는 것이 이 섹션의 기준이다.

첫 번째 미해결 질문: ARCC가 cliff 이하로 떨어지는 시점에 self-immune 루프가 어떻게 작동하는가. Self-immune이 신뢰 가능하게 작동하다가 ARCC가 cliff threshold를 건너는 순간 루프의 신뢰도가 함께 무너진다면, 이 전환을 감지하고 외부 escalation을 요청하는 메커니즘이 필요하다. 검증 조건: ARCC가 실험 중 cliff threshold 아래로 내려가도록 설계된 실험에서 self-immune이 잘못된 recovery를 실행하는 비율과, escalation을 요청하는 비율을 측정한다. 현재 E20이 이 방향을 열었으나 ARCC 조절 실험이 별도로 설계되어야 한다.

두 번째 미해결 질문: Multi-agent 환경에서 self-immune은 어떻게 작동하는가. MiroFish에서 수천 개의 agent가 동시에 실행될 때, 개별 agent의 self-immune이 군집 수준의 안정성에 어떻게 기여하는가. 상류 agent가 cliff에 근접했다는 신호를 하류 agent에게 어떻게 전달하는가. 검증 조건: 군집 규모 N=10, 100, 1000에서 개별 agent self-immune 유무가 전체 군집 TCR에 미치는 영향을 측정하는 실험이 필요하다. 단일 agent 환경의 실험 결과가 군집 환경에서 동일한 방향으로 성립하는가는 별도 검증이 요구된다.

세 번째 미해결 질문: Agent가 다음 task를 스스로 생성하려면 self-monitoring 외에 무엇이 더 필요한가. Self-immune이 현재 task의 실행 품질을 유지하는 것이라면, proactivity는 현재 task가 완료된 이후 다음 무엇을 해야 하는가를 스스로 정의하는 능력이다. 검증 조건: self-immune 루프가 안정적으로 작동하는 Agent-2 환경에서, 외부 task 지시 없이 agent가 다음 task를 생성하는 비율과 그 task의 operator-validated appropriateness를 측정한다. 이 질문은 이 책의 preface에서 미해결로 남긴 것이다.

---

## §9 집필 과정의 메타 관찰

> 상태: 🔴 초고 v0.1 (2026-03-18)

이 책은 multi-agent 협업 구조로 작성되었다. 필자가 챕터 방향과 핵심 주장을 설정하고, drafting agent가 섹션별 초고를 생성하며, editor agent가 voice-check와 용어 일관성을 검토하는 3-layer 구조. 이 구조 자체가 AgentOps 실무 원칙의 dogfooding이다.

Token 배분에서 관찰된 패턴이 있다. 한 챕터를 단일 세션에서 완성하려 할 때 context window 후반부에서 drafting agent의 IFR이 저하되는 징후가 나타났다 — 초반 섹션에서 확립한 용어 구분을 후반 섹션에서 혼용하거나, 문체 규칙이 느슨해지는 패턴. 이것은 Ch.6에서 서술하는 IFR decay의 실제 사례다. 섹션 단위로 작업을 분리하고 세션을 전환하는 것이 이 decay를 구조적으로 억제하는 운영 규칙으로 자리잡았다.

Coordination overhead도 측정 가능한 형태로 나타났다. Drafting agent와 editor agent 사이의 revision cycle에서 소요되는 token은 초고 생성 token의 [X]%에 달했다 — 이것이 집필 workflow의 HOR에 해당한다. 이 overhead가 voice consistency 향상으로 정당화되는가는 Chapter-level voice-check 통과율로 측정할 수 있는데, 수치는 Ch.9가 완료된 이후 기록될 예정이다.

집필에 agent를 사용했다는 사실이 이 책의 주장을 강화하지 않는다. Multi-agent 집필 구조가 AgentOps 원칙과 구조적 유사성을 가진다는 것을 관찰 수준에서 기록하는 것이다. 이 구조가 더 나은 책을 만든다는 주장은 별도의 검증 기준을 요구한다 — 그것은 독자의 판단에 위임한다.

---

## 참조

- `deep-research/DR-7.1-self-healing-agents.md`
- `deep-research/DR-7.2-continuous-learning-deployed.md`
- `deep-research/DR-3.4-ontology-as-agent-memory-structure.md`
- `experiments/axis-5-harness-internalization/E20-mini-self-immune.md`
- `experiments/figure_expansion.md` — Figure 9 (Harness ROC), Figure 11 (Scaling), Figure 12 (Temporal Stability)
- `experiments/framework/metrics.py`
- `field-dispatches/2026-03/FD-2026-03-14-001-mirofish.md`
