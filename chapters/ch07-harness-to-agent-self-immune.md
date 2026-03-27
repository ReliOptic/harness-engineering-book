# Ch.7 — Harness에서 Agent로: Self-Immune System을 향하여

> 상태: 🟡 섹션 1 초고 v0.2 (2026-03-18)
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
   - Failure Budget Reallocation으로 재프레이밍된 결과: harness가 막은 것과 막지 못한 것
   - ARCC monitoring 부재가 silent logical drift를 만드는 구조적 이유
   - IFR decay가 MTTR 최소화와 연결되는 경로: 왜 개입이 decay 시작 시점에 가장 효과적인가

2. **현 세대 harness가 아직 풀 수 없는 문제**
   - 규칙 기반 방어의 구조적 한계: 알려진 failure pattern만 차단한다
   - ARCC가 cliff threshold 근처에서 운영되는 agent에 대한 harness의 한계
   - E19 반례가 남긴 질문: task의 암묵적 constraint는 harness가 검증할 수 없다

3. **AgentOps → Harness → Agent 내재화: 점진적 경로**
   - 외부 운영자의 AgentOps 실무가 harness component로 구현되고, 그것이 agent 내부로 주입되는 경로
   - 내재화가 가능한 component: E18(token monitoring), E19(failure detection) — 측정 가능하고 규칙화 가능한 것
   - 내재화가 불가능한 component: IFR decay의 방향 판단 — 규칙이 아니라 context 이해가 필요한 것
   - 이 분류가 self-immune 설계의 범위를 결정한다

4. **Self-immune system 초기 설계**
   - 조작적 정의: ARCC self-estimate + cliff-proximity detection + self-initiated recovery
   - 재귀적 한계: self-monitoring을 신뢰할 수 있는 ARCC 하한 조건
   - E20 (mini self-immune) 결과: 최소 조건에서 무엇이 성립했고 무엇이 성립하지 않았는가
   - Fig 9 (Harness ROC): failure 감지의 precision/recall. Self-immune에서 이것이 agent 내부로 이동한다.

5. **Model Capability × Harness Value: Scaling 조건**
   - Fig 11 결과 해석: ARCC 증가가 harness value를 감소시키는가 vs. 역할을 전환시키는가
   - "방어 → 조정" 전환 가설의 검증: 어떤 ARCC 수준에서 전환이 일어나는가
   - Agent-2 전환의 ARCC 조건: self-immune이 신뢰 가능해지는 capability 하한

6. **Temporal Stability: self-immune은 얼마나 오래 유지되는가**
   - Fig 12 결과: 72시간 연속 운영에서 self-immune performance 변화
   - Harness fatigue의 메커니즘: context 누적인가, rule drift인가, 모델 측 변화인가
   - "Infinite learning"의 조건: fatigue를 상쇄하는 재보정 mechanism의 필요성

7. **Agent-1 → Agent-2: 전환 조건의 정식화**
   - Agent-1: 외부 harness가 관찰하고 개입한다. Operator intervention이 필요하다.
   - Agent-2: agent가 스스로 ARCC를 monitoring하고 복구 경로를 실행한다.
   - 전환의 충분조건: ARCC가 self-monitoring threshold를 초과하고, temporal stability가 운영 horizon 내에서 유지된다
   - 전환의 필요조건: task 자체의 모호성이 제거된다 (E19이 보여준 harness의 한계)
   - DR-3.4 (ontology 내재화)와의 연결: Agent-2 상태에서 agent가 자신의 context 구조를 유지하는 방법

8. **이 책 이후: 미해결 질문들**
   - Cliff-conditional self-immune: ARCC가 cliff 이하로 떨어지는 시점의 복구 전략
   - Multi-agent self-immune coordination: 군집 agent에서 self-immune이 어떻게 작동하는가 (MiroFish 관찰)
   - Proactivity 조건: agent가 다음 task를 스스로 생성하려면 self-monitoring 외에 무엇이 더 필요한가
   - 이 질문들은 이 책이 답하지 않는다. 이 책의 실험들은 그 질문들의 하한 조건을 측정했다.

9. **집필 과정의 메타 관찰**
   - 이 책을 쓰는 과정 자체가 agent와 인간의 협업이었다
   - 집필 workflow(outline → draft → revise → voice-check)가 AgentOps 실무 구조와 어떻게 대응하는가
   - 관찰: agent가 draft를 생성하는 속도와 인간 저자가 방향을 수정하는 빈도 사이의 trade-off
   - 이것이 자기 정당화가 아닌 이유: 집필 과정은 이 책의 실험 조건 중 하나였으며, 관찰 사실로 기록된다

---

## 섹션 1. 실험이 남긴 것

> 상태: 🟡 초고 v0.2 (2026-03-18)

필자가 이 책의 실험을 설계할 때 확인하려 했던 질문은 하나였다. 동일한 task, 동일한 모델, 동일한 surface 조건에서, harness의 존재 여부가 failure의 성격을 어떻게 바꾸는가. 22개의 시나리오를 다섯 개의 축으로 묶어 pre-registration 원칙 하에 실행했다. 실험이 끝나고 예상한 것과 달랐던 것이 두 가지 있다.

하나는, harness가 생각보다 많은 failure를 recoverable 범주로 이동시켰다. 다른 하나는, harness가 total failure budget 자체를 줄이지는 못했다.

Failure budget이 재배분된 방향은 일관됐다. Tool call failure와 output format error처럼 구조적으로 감지 가능한 failure는 harness-on 조건에서 recovery attempted 범주로 이동했다. E05부터 E08에 걸친 harness 변수 조작 실험에서, failure 6축 radar의 형태가 변했다 — 면적은 유사하게 유지되었으나 silent logical drift의 비율이 줄고 recovery succeeded의 비율이 늘었다. Harness는 failure를 제거하지 않는다. Failure를 더 비싸지 않은 유형으로 교환한다.

재배분이 일어나지 않은 failure들의 목록은 다른 성격을 띤다. 에이전트가 각 단계를 올바른 절차대로 밟으면서도 전체 방향이 틀린 경우 — 이것은 ARCC sub-components 중 IFR(Instruction Following Rate)의 decay가 단계별로는 감지되지 않다가 task 수준에서 누적되는 패턴이다. E19에서 task 자체를 모호하게 설계했을 때 드러난 것이 이것이다. Harness는 각 tool call의 schema validity를 검증하지만, tool call sequence 전체가 instruction의 암묵적 constraint를 충족하는지는 검증하지 않는다. IFR이 threshold 아래로 내려가는 것을 외부에서 감지하려면, 이미 충분히 낮아진 이후다.

Operator intervention이 가장 효과적이었던 시점은 failure 직후가 아니라 IFR decay가 시작되는 시점이었다. 이것은 MTTR 최소화의 문제다. Failure가 발생한 이후에 개입하면 recovery는 가능하지만 MTTR이 이미 높아진 상태다. IFR decay가 시작되는 시점은 외부에서 바라보면 정상 출력처럼 보인다 — 문법적으로 완결되고 tool call도 schema를 통과한다. 방향 이탈은 구조적으로 감지 가능하지 않다.

이것이 이 챕터의 출발점이다. MTTR을 구조적으로 낮추려면, failure가 발생한 이후의 recovery 속도가 아니라, failure budget이 silent 범주로 이동하기 전의 감지 능력이 필요하다. 그 감지 능력은 외부 harness가 아니라 agent 내부의 ARCC self-monitoring에서 나온다. 현재의 harness 구조는 이것을 제공하지 않는다. 이것이 self-immune system이 필요한 이유이며, 동시에 self-immune system이 어렵다는 이유다.

---

## 참조

- `deep-research/DR-7.1-self-healing-agents.md`
- `deep-research/DR-7.2-continuous-learning-deployed.md`
- `deep-research/DR-3.4-ontology-as-agent-memory-structure.md`
- `experiments/axis-5-harness-internalization/E20-mini-self-immune.md`
- `experiments/figure_expansion.md` — Figure 9 (Harness ROC), Figure 11 (Scaling), Figure 12 (Temporal Stability)
- `experiments/framework/metrics.py`
- `field-dispatches/2026-03/FD-2026-03-14-001-mirofish.md`
