# Ch.3 — Harness Engineering과 AgentOps: 정의와 프레임워크

> 상태: 🔲 skeleton only
> 담당: Kiwon
> 목표 분량: 8,000~10,000자

---

## 핵심 메시지

Harness는 failure를 제거하지 않는다. Harness가 하는 것은 failure의 성격을 바꾸는 것이다 — undetectable/unrecoverable failure를 detectable/recoverable failure로 재배분한다. 이 재배분이 운영 비용(MTTR, Human Escalation Rate)을 어떻게 바꾸는가가 harness engineering의 실무적 핵심이며, 이것을 측정하고 관리하는 것이 AgentOps의 출발점이다. 이 챕터는 Ch.4의 실험 프레임을 설정한다 — 가설과 판단 기준을 데이터 수집 전에 announce한다.

## 학습 결과

- Harness engineering의 정의(operational envelope)와 guardrails/scaffolding/orchestration과의 구분을 설명할 수 있다.
- Failure Budget Reallocation 프레임워크를 이해하고, harness의 효과를 "failure 제거"가 아닌 "failure 성격 전환"으로 설명할 수 있다.
- HOR(Harness Overhead Ratio, token overhead %)의 정의를 이해하고, HOR × RSuccR trade-off에서 optimal configuration을 판단하는 기준을 설명할 수 있다.
- AgentOps의 정의와 MLOps/DevOps와의 차이를 설명할 수 있다.
- Ch.4 실험의 pre-registration 원칙과 task T1/T2/T3/T4 조작적 정의를 이해한다.
- Ground truth 3-layer 구조(test suite → LLM judge → human rater)의 각 역할을 설명할 수 있다.

## 집필 노트

- 관련 DR: DR-3.1 (용어), DR-3.2 (CLI-Anything), DR-3.3 (AgentOps 도구), DR-3.4 (failure taxonomy + ontology as agent memory structure)
- 관련 실험: E05 (harness 있음/없음), E06 (memory 보호), E07 (permission + surface), E08 (token budget sweep)
- 관련 증거: `evidence/case-studies/teamclaws-picoclaw-postmortem.md`, `evidence/case-studies/cli-anything-harness-analysis.md`

**Failure Budget Reallocation 정의 (조작적):**
- 총 failure budget = 주어진 실험 조건에서 발생하는 failure event의 총 수. Harness 유무에 관계없이 이 수치가 유사하게 유지된다는 가설.
- Harness는 이 budget이 어떤 failure taxonomy(6축)로 구성되는가를 재배분한다.
- 6축 taxonomy: tool call failure / context overflow / output format error / silent logical drift / recovery attempted & succeeded / recovery attempted & failed
- Fig 2 (Failure Profile Radar)가 이 재배분을 시각화한다.

**HOR 정의 (조작적):**
- HOR = (harness가 추가하는 token 수) / (base task token 수) × 100%
- HOR은 운영 비용의 직접 구성요소: Cost_compute = Cost_compute_base × (1 + HOR/100)
- HOR × RSuccR trade-off에 optimal point가 존재한다는 가설을 Ch.4에서 검증.
- HOR이 과도하면 token budget을 잠식하고 TCR이 오히려 감소한다 (E20 반례 예고).

**Pre-registration 원칙:**
- Ch.4의 실험은 이 챕터 말미에서 가설과 판단 기준을 announce한다.
- 데이터를 보기 전에 고정된 기준 — post-hoc rationalization 배제의 구조적 장치.
- `experiments/design-specification.md` §7 (Deviation Protocol): announce 이후의 변경은 반드시 기록된다.

**Task 조작적 정의 (§8에서 announce):**
- T1 Code Review: F1 ≥ 0.70 (precision × recall). Ground truth = seeded bug list.
- T2 Multi-Step Reasoning: plan_is_valid = 1 (자동 constraint checker 판정).
- T3 Long-Horizon Execution: 40+ steps, MTGR(Mean Task Goal Retention) ≥ 0.80.
- T4 Synthesis: LLM judge로 factual accuracy 판정 (κ ≥ 0.70 with human rater).

---

## Outline

**계획된 섹션:**

1. **Harness engineering이란 무엇인가 — operational envelope 정의**
   - Harness = agent의 권한, 메모리, 리소스 경계, 복구 경로, 개입 조건을 runtime에 명시적으로 관리하는 구조
   - "Operational envelope"이라는 용어의 의미: agent가 작동하는 허용 공간의 경계
   - Harness가 모델 성능을 보완하는 것이 아니라 관찰 가능성(observability)을 구조화한다는 주장

2. **보호와 enablement의 이중 구조**
   - Harness가 제약이면서 동시에 enabler인 이유
   - 보호: 알려진 실패 패턴의 구조적 차단
   - Enablement: agent가 실패를 복구하고 계속 실행할 수 있는 조건 형성
   - 이 이중 구조가 없으면 harness는 overhead만 추가하는 bureaucracy가 된다 — HOR이 높고 RSuccR이 개선되지 않는 경우

3. **Harness를 guardrails, scaffolding, orchestration과 구분**
   - Guardrails: 입출력 필터링 (정적, post-hoc). 실행이 끝난 후 작동.
   - Scaffolding: task 구조 주입 (정적, pre-hoc). 실행 시작 전에 작동.
   - Orchestration: multi-agent routing (실행 시간, 구조적). agent 간 조율에 집중.
   - Harness: operational envelope — 권한·메모리·리소스·복구를 runtime에 동적으로 관리. 세 개념을 포함하되 runtime 상태 관리를 핵심으로 한다.
   - 네 개념이 겹치는 경우와 겹치지 않는 경우: 실제 구현에서의 경계선

4. **Failure Budget Reallocation — harness의 효과를 프레이밍하는 방법**
   - 기존 프레이밍의 문제: "harness가 failure를 줄인다" → 이것은 부분적으로만 맞다
   - Failure Budget Reallocation: 총 failure budget이 유사하게 유지되면서 구성 유형이 바뀐다
   - Failure 6축 taxonomy의 정의와 각 축이 운영 비용에 미치는 영향 (silent drift가 가장 비싸다)
   - Fig 2 예고: Failure Profile Radar가 harness-on/off 전환 시 어떻게 이동하는가
   - 이 프레이밍이 더 정직한 이유: "failure가 줄었다"고 보고하면 보이지 않는 failure가 누적된다

5. **HOR (Harness Overhead Ratio) — harness의 비용을 측정하는 방법**
   - HOR 정의: token overhead 비율. Harness가 도입하는 운영 비용의 1차 지표.
   - HOR × RSuccR trade-off: optimal point가 존재하는가 (Ch.4 실험 가설)
   - HOR = 0은 harness 없음. HOR 과도 → token budget 잠식 → TCR 감소 (E20 예고).
   - 이 trade-off를 실험적으로 측정하는 것이 Fig 8 (Cost-Reliability Frontier)의 역할

6. **AgentOps란 무엇인가 — profession으로서의 정의**
   - AgentOps = 비결정적 agent runtime을 관찰·통제·복구·자원인식적으로 운영하는 규율
   - MLOps와의 차이: MLOps는 모델 lifecycle 관리. AgentOps는 실행 중인 agent의 runtime 행동 관찰과 개입.
   - DevOps와의 차이: DevOps는 코드 배포 파이프라인. AgentOps는 실행 상태 관리.
   - MTTR(Mean Time To Recovery)과 HER(Human Escalation Rate)이 AgentOps의 1차 지표인 이유: 엔지니어의 on-call rotation에 직접 영향을 미치는 operational metric이기 때문.

7. **Harness 부재의 비용: TeamClaws/PicoClaw 사후 분석**
   - 5변수 프레임워크로 실패를 재진단: 실제 1차 병목은 어디에 있었는가
   - Failure Budget Reallocation 관점의 분석: harness가 있었다면 failure가 어떤 유형으로 재배분되었을까
   - CLI-Anything의 독립적 수렴: 다른 맥락에서 같은 문제를 발견하고 같은 방향으로 수렴한 사례
   - 독립 수렴이 의미하는 것: harness engineering은 특정 프로젝트의 ad-hoc 해결책이 아니다

8. **Ch.4 실험 프레임 설정 — 가설과 판단 기준의 pre-registration**
   - Task 조작적 정의 announce: T1(Code Review, F1≥0.70), T2(Multi-Step, plan validity), T3(Long-Horizon 40+ steps), T4(Synthesis)
   - 12개 Figure의 구조와 각 Figure가 답하는 confirmatory 가설
   - 판단 기준 고정의 과학적 근거: 같은 데이터로 여러 가설을 검증하면 type I error가 증가한다
   - Ground truth 3-layer 구조: test suite (100% coverage, 자동) → LLM judge (~30%, cohen's κ ≥ 0.70) → human rater (stratified sample, κ ≥ 0.70)
   - Deviation Protocol: 이 announce 이후 기준을 변경할 경우 반드시 기록하고 confirmatory에서 exploratory로 분류 이동

---

**핵심 Figure:**

- **Fig 2** (Ch.3에서 예고, Ch.4/5에서 실현) — Failure Profile Radar: harness-off vs. harness-on의 failure 6축 radar 비교 + Panel C (MTTR, HER operational translation)

<!-- 섹션별 초고는 /draft ch03 N 으로 작성 -->

## 참조

- `deep-research/DR-3.1-harness-terminology.md`
- `deep-research/DR-3.2-cli-anything-harness.md`
- `deep-research/DR-3.3-agentops-landscape.md`
- `deep-research/DR-3.4-ontology-as-agent-memory-structure.md`
- `evidence/case-studies/teamclaws-picoclaw-postmortem.md`
- `evidence/case-studies/cli-anything-harness-analysis.md`
- `experiments/design-specification.md` — §1 (Task specification), §3 (Ground truth 3-layer), §7 (Deviation protocol)
- `experiments/figure_expansion.md` — Figure 2 재설계 (Failure Profile Radar + Operational Translation)
- `experiments/framework/harness.py`
- `experiments/framework/ground_truth.py`
