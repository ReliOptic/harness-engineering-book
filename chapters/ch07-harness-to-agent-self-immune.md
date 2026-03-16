# Ch.7 — Harness에서 Agent로: Self-Immune System을 향하여

> 상태: 🔲 skeleton only
> 담당: Kiwon
> 목표 분량: 8,000~10,000자

---

## 핵심 메시지

AgentOps 기능을 harness를 통해 agent에 점진적으로 주입하여, agent가 스스로 복구하고 학습하는 self-immune system을 갖게 하는 것이 Agent-2 전환의 핵심 조건이다.

## 학습 결과

- Harness engineering이 Agent-2 전환에 왜 필수적인지 설명할 수 있다.

## 집필 노트

- 관련 DR: DR-7.1 (self-healing agent), DR-7.2 (continuous learning)
- 관련 실험: E20 (mini self-immune)
- Agent-1 → Agent-2 전환 논증이 이 챕터의 핵심
- 집필 과정 자체가 agent와의 협업이었다는 메타 관찰 포함
- FD-2026-03-14-001 (MiroFish) — 군집 시스템에서 self-immune의 중요성

---

## Outline

<!-- /outline ch07 실행 후 여기에 삽입 -->

**계획된 섹션:**

1. 이 책의 실험들이 보여준 유의미한 결과 종합
2. 현 세대 harness가 아직 풀 수 없는 문제
3. AgentOps → Harness → Agent 내재화: 점진적 경로
4. Self-immune system 초기 설계
5. Agent-1 → Agent-2: infinite learning이 가능해지는 조건
6. 이 책 이후: AI agent가 연구와 기록을 자율적으로 수행하는 미래
7. 집필 과정 자체가 agent와의 협업이었다는 메타 관찰

---

<!-- 섹션별 초고는 /draft ch07 N 으로 작성 -->

---

## 섹션 1. 실험이 남긴 것

> 상태: 🔶 초고 v0.1 (2026-03-17)

필자가 이 책의 실험을 설계할 때 확인하려 했던 질문은 하나였다. 동일한 task, 동일한 모델, 동일한 surface 조건에서, harness의 존재 여부가 실패 패턴을 어떻게 바꾸는가. 22개의 시나리오를 다섯 개의 축으로 묶어 실행했다. 실험이 끝나고 나서 필자가 예상한 것과 달랐던 것이 두 가지 있다.

하나는, harness가 생각보다 많은 실패를 막았다. 다른 하나는, harness가 생각보다 훨씬 많은 실패를 막지 못했다.

막은 것들부터 말하면, 그 목록은 비교적 선명하다. 메모리 경계를 위반하는 쓰기 작업, 허가되지 않은 외부 API 호출, 컨텍스트가 포화되었을 때의 자기 순환 호출, 가역성이 낮은 tool 실행 — 이것들은 harness가 approval 레이어를 두거나 schema validation을 적용하는 것만으로 상당 부분 억제됐다. E05부터 E08에 걸친 harness 변수 조작 실험에서, harness가 있는 조건과 없는 조건 사이의 실패 빈도 차이는 예상보다 크고 일관됐다. 이 정도의 방어는 harness가 정적인 규칙 집합만으로도 달성 가능하다는 것을 보여준다.

막지 못한 것들의 목록은 다른 성격을 띤다. 에이전트가 각 단계를 올바른 절차대로 밟으면서도 전체 방향이 틀린 경우 — harness는 이것을 감지하지 못했다. Task decomposition이 초기에 잘못 설정되면, harness는 개별 행동을 정상으로 통과시키면서 전체 결과를 망칠 수 있다. E21에서 필자가 의도적으로 task 자체를 모호하게 설계했을 때 드러난 것이 이것이다. 에이전트는 주어진 task를 "완료"했지만, 완료된 결과는 처음 의도와 달랐다. Harness는 각 행동이 허용된 범위 안에 있는지를 검증하지만, 행동의 방향이 목표와 일치하는지는 검증하지 않는다.

입력 신뢰 경계를 다루는 실험에서도 비슷한 구조적 한계가 나타났다. Harness가 알려진 패턴은 차단했지만, 처음 보는 형태의 입력이 들어왔을 때는 통과시켰다. 규칙 기반 방어는 알려진 공격을 막는 데 최적화되어 있고, 알려지지 않은 것에는 맹목적이다.

이 두 목록을 5변수 프레임워크로 읽으면 다음이 된다. Harness는 알려진 실패 패턴을 구조적으로 차단하는 데 탁월하다. 하지만 알려지지 않은 실패를 다루려면, harness가 규칙을 적용하는 것을 넘어 에이전트 스스로 상황을 평가하는 능력이 필요하다. 그 능력은 현재의 harness 구조에 없다.

Ch.4와 Ch.5의 실험에서 반복적으로 나타난 패턴 하나를 마지막으로 짚는다. Operator intervention이 가장 효과적이었던 시점은 에이전트가 실패한 직후가 아니라, 에이전트가 방향을 잃기 시작하는 시점이었다. 문제는 그 시점을 식별하는 것이 어렵다는 것이다. 에이전트가 방향을 잃고 있을 때, 에이전트의 출력은 여전히 문법적으로 완결되어 있고 tool 호출도 정상으로 보인다. 방향 이탈은 외부에서 바라보면 정상처럼 보인다.

이것이 이 챕터의 출발점이다. Harness가 외부에서 에이전트의 행동을 제약하는 구조만으로는, 에이전트가 방향을 잃었다는 것을 먼저 인식하는 능력을 얻을 수 없다. 그 인식 능력은 에이전트 내부에 있어야 한다. 그것이 없는 한, operator intervention은 반복 가능한 운영 규율이 될 수 없고 개별적인 응급 처치에 머문다.

## 참조

- `deep-research/DR-7.1-self-healing-agents.md`
- `deep-research/DR-7.2-continuous-learning-deployed.md`
- `deep-research/DR-3.4-ontology-as-agent-memory-structure.md` ← **섹션 9: Agent-2 전환과 ontology 내재화 논증** (self-immune의 기준점, continuous learning과의 교차, ontology drift → self-awareness 연결)
- `experiments/axis-5-harness-internalization/E20-mini-self-immune.md`
- `field-dispatches/2026-03/FD-2026-03-14-001-mirofish.md`
