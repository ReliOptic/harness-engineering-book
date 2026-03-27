# Chapter Map — Harness Engineering and AgentOps

> 각 챕터의 제목, 탐구 질문, 핵심 메시지, 학습 결과, 관련 DR/실험 목록.
> 집필 시 이 문서를 기준으로 방향 확인. writing-plan.md의 요약본.

---

## Preface

**핵심 메시지**: 왜 이 책이 필요한가. 누구를 위한 책인가.
**학습 결과**: 독자가 이 책에서 무엇을 얻을 수 있는지 명확히 이해한다.

---

## Ch.1 — 지금 무슨 일이 일어나고 있는가

**파일**: `chapters/ch01-what-is-happening-now.md`
**핵심 메시지**: Agent-friendly product surface의 초기 형태가 부상하는 시점을 기록한다.

**탐구 질문**:
- 2026년 상반기 agent runtime 현장은 어떤 상태인가?
- OpenClaw는 무엇을 가능하게 했고 무엇이 아직 모자란가?
- TeamClaws/PicoClaw 실패는 무엇을 보여주는가?

**핵심 구성**:
1. 2026년 상반기: agent 운영의 현재 풍경
2. OpenClaw — 무엇이 특별하고 무엇이 아직 모자란가
3. 생태계 스냅샷: OpenClaw 주변 프로젝트들
4. TeamClaws/PicoClaw — 이 책을 쓰게 된 이유
5. 왜 지금이 중요한가 — harness engineering 초기에 알 수 있는 것
6. 5변수 프레임워크 소개
7. Agent-1 ~ Agent-5 방향 설정
8. AIE shout-out (Chip Huyen, AI Engineering, 2025)

**학습 결과**:
- 현재 agent 생태계를 파악하고, 왜 이 시점에서 harness engineering이 필요한지 설명할 수 있다.
- 5변수 프레임워크의 기본 개념을 이해한다.
- ARCC와 Capability Cliff의 개념을 예비적으로 이해한다.
- Agent-1 ~ Agent-5 스펙트럼에서 현재 배포된 agent가 Agent-1에 머무는 구조적 이유를 설명할 수 있다.

**관련 DR**: DR-1.1, DR-1.2, DR-1.3
**관련 실험**: (없음 — 관찰 및 사례 중심)
**관련 증거**: `evidence/case-studies/openclaw-anchor.md`, `evidence/case-studies/teamclaws-picoclaw-postmortem.md`
**관련 dispatch**: `FD-2026-03-17-002-cli-renaissance.md`, `FD-2026-03-17-002-wide-survey.md`

---

## Ch.2 — Agent가 모델로부터 무엇을 물려받는가

**파일**: `chapters/ch02-nature-agent-inherits.md`
**핵심 메시지**: Agent는 중립적이지 않다. 모델별 행동 차이를 정량적으로 측정하고, Capability Cliff가 존재한다는 것을 관찰한다.

**탐구 질문**:
- 동일한 task에서 모델을 바꾸면 무엇이 어떻게 달라지는가?
- "Agent-Viable Minimum"은 task별로 어떤 capability 수준에서 형성되는가?
- 양자화와 distillation은 agent capability를 어떻게 다르게 깎는가?

**핵심 구성**:
1. 물려받는 경향: reasoning, tool use, consistency, confidence
2. ARCC (Agent-Relevant Capability Composite) — 모델을 vendor tier가 아닌 연속 capability spectrum으로 측정하는 방법
   - TCA (Tool Call Accuracy), IFR (Instruction Following Rate), MSRD_n (Multi-Step Reasoning Depth), CUE (Context Utilization Efficiency)
3. Capability Cliff — TCR이 특정 ARCC 이하에서 선형이 아닌 급락하는 패턴. task별 cliff position이 다르다.
4. Quantization Tax Curve — 동일 base model의 FP16→Q8→Q4→Q2 경로에서 agent capability가 깎이는 비율
5. Distillation Efficiency Frontier — 동일 parameter budget에서 distillation vs. quantization의 agent viability 비교
6. Mid-run model switching의 context continuity 붕괴 패턴 (E03)
7. 5변수 중 "모델" 변수가 1차 병목이 되는 조건

**핵심 Figure**:
- **Fig 1 — Agent Capability Cliff** (E01 확장): ARCC scatter plot, task-conditional sigmoid fit, cliff position per task type. harness-off 조건 기준.

**핵심 지표**:
- ARCC (TCA, IFR, MSRD_n, CUE의 weighted composite)
- TCR (Task Completion Rate) per task type (T1/T2/T3)
- ARCC Construct Validation: holdout R² ≥ 0.65 → ARCC 유효

**학습 결과**:
- 모델 원인의 취약성을 식별하고, ARCC 기반으로 자신의 환경에서 유사한 측정을 설계할 수 있다.
- Capability Cliff의 존재를 이해하고, "이 양자화 모델로 이 task는 된다"를 판단하는 근거를 갖는다.

**관련 DR**: DR-2.1, DR-2.2, DR-2.3
**관련 실험**: E01 (Capability Cliff), E02 (frontier vs. distilled), E03 (mid-run switching), E10 (model capability floor for self-monitoring)

---

## Ch.3 — Harness Engineering과 AgentOps: 정의와 프레임워크

**파일**: `chapters/ch03-harness-and-agentops-defined.md`
**핵심 메시지**: Ch.4-5의 실험을 위해, harness engineering과 AgentOps를 먼저 정의하고 실험 프레임을 설정한다.

**탐구 질문**:
- Harness engineering은 guardrails, scaffolding과 어떻게 다른가?
- AgentOps는 MLOps, DevOps와 어떻게 다른가?
- 무엇을 의도적으로 실패시킬 것인가?

**핵심 구성**:
1. Harness engineering이란 무엇인가 — operational envelope 정의
2. 보호와 enablement의 이중 구조
3. Harness를 guardrails, scaffolding, orchestration과 구분
4. AgentOps란 무엇인가 — profession으로서의 정의
5. 5변수 프레임워크에서 harness와 AgentOps의 위치
6. Harness 부재의 비용: TeamClaws/PicoClaw 사후 분석 (반례 2)
7. CLI-Anything HARNESS.md — 독립적 수렴 사례
8. Ch.4-5에서 실험할 것에 대한 프레임 설정

**핵심 메시지**: Harness는 failure를 제거하지 않는다. Failure의 성격을 바꾼다 — Failure Budget Reallocation. HOR(Harness Overhead Ratio)과 MTTR이 AgentOps의 1차 운영 지표다. 이 챕터 말미에서 Ch.4 실험의 가설과 판단 기준을 pre-registration 방식으로 announce한다.

**탐구 질문**:
- Harness engineering은 guardrails, scaffolding과 어떻게 다른가?
- AgentOps는 MLOps, DevOps와 어떻게 다른가?
- HOR × RSuccR trade-off에 optimal point가 존재하는가?
- Pre-registration 원칙이 실험 설계에서 왜 필요한가?

**핵심 구성**:
1. Harness engineering이란 무엇인가 — operational envelope 정의
2. 보호와 enablement의 이중 구조
3. Harness를 guardrails, scaffolding, orchestration과 구분
4. Failure Budget Reallocation — harness의 효과를 프레이밍하는 방법
5. HOR (Harness Overhead Ratio) — harness의 비용을 측정하는 방법
6. AgentOps란 무엇인가 — profession으로서의 정의
7. Harness 부재의 비용: TeamClaws/PicoClaw 사후 분석
8. Ch.4 실험 프레임 설정 — 가설과 판단 기준의 pre-registration

**학습 결과**:
- Harness와 AgentOps를 정의하고, Failure Budget Reallocation 프레임으로 harness 효과를 설명할 수 있다.
- HOR의 정의와 HOR × RSuccR trade-off를 이해한다.
- Ch.4 실험의 pre-registration 원칙과 task T1/T2/T3/T4 조작적 정의를 이해한다.
- Ground truth 3-layer 구조를 이해한다.

**관련 DR**: DR-3.1, DR-3.2, DR-3.3, DR-3.4
**관련 실험**: E05, E06, E07, E08
**관련 Figure**: Fig 2 (Failure Profile Radar + Operational Translation)

---

## Ch.4 — 의도적 실패 실험: 22개 시나리오

**파일**: `chapters/ch04-deliberate-failure-experiments.md`
**핵심 메시지**: 22개 시나리오는 pre-registration 원칙 하에 설계되었다 — 가설, 판단 기준, 검정 방법이 데이터 수집 전에 고정되었다. 실험은 5변수를 격리 조작하며 어떤 변수가 어떤 조건에서 1차 병목이 되는가를 측정한다.

**탐구 질문**:
- 5변수 중 어느 것을 조작하면 어떤 실패가 나타나는가?
- Capability Cliff는 harness-off 조건에서 어떤 형태를 갖는가?
- Failure budget은 harness-on 조건에서 어떻게 재배분되는가?
- 제약 환경에서 가장 먼저 드러나는 병목은 무엇인가?
- HOR × RSuccR trade-off에 optimal point가 존재하는가?

**핵심 구성**:
- 1막 (E01-E04): 모델 변수 조작 — Capability Cliff, Quantization Tax, Distillation Frontier
- 2막 (E05-E08): Harness·Surface 변수 조작 — Failure Budget Reallocation, HOR 측정
- 3막 (E09-E14): 제약 환경의 병목 — compute saturation, multi-agent coordination
- 4막 (E15-E17): Operator intervention의 효과 — intervention timing, codification
- 5막 (E18-E20): AgentOps 내재화 — token monitoring, failure detection, mini self-immune
- 반례 (E21-E22): Task design 문제, Compute saturation 문제

**학습 결과**:
- Pre-registration 원칙을 적용한 deliberate failure experiment를 설계하고 실행할 수 있다.
- Task T1/T2/T3/T4 조작적 정의와 ground truth 3-layer를 이해한다.
- Confirmatory analysis와 exploratory 발견을 구분하여 보고할 수 있다.

**관련 DR**: DR-4.1, DR-4.2, DR-4.3, DR-4.4
**관련 실험**: E01~E22 전체
**관련 Figure**: Fig 1~8 (데이터 생성 책임)
**Pre-registration 파일**: `experiments/design-specification.md`

---

## Ch.5 — 실험 결과에서 배운 것: AgentOps와 Harness의 실무

**파일**: `chapters/ch05-lessons-from-experiments.md`
**핵심 메시지**: 실험실 metric → 운영 metric(MTTR, HER) → 비용 metric(TotalCost, CostIndex)의 3단계 번역이 이 챕터의 중심 작업이다. Optimal HOR은 존재하며, 그 점 이상에서 harness는 새로운 1차 병목이 된다.

**탐구 질문**:
- 어떤 변수가 어떤 조건에서 1차 병목이었는가?
- Failure budget이 재배분된 방향과 비율은?
- Optimal HOR은 어디에 있으며 cost scenario에 따라 어떻게 달라지는가?
- 각 harness component의 marginal ROI는 무엇인가?
- 이 결과는 model capability 증가와 시간 경과에 robust한가?

**핵심 구성**:
1. 22개 실험 결과 종합: 5변수별 병목 분포
2. Failure Budget Reallocation 정량 분석
3. 운영 metric 번역: MTTR과 Human Escalation Rate
4. 비용 metric 번역: TotalCost와 optimal HOR
5. Component ablation: 무엇이 얼마나 기여하는가
6. Token efficiency를 운영 규율로
7. Scaling과 temporal stability
8. 학술적 확장 가능성 — exploratory 발견 목록

**학습 결과**:
- 실험실 metric → 운영 metric → 비용 metric 번역 체계를 이해하고 적용할 수 있다.
- HOR × RSuccR optimal point를 판단하는 방법을 이해한다.
- Component ablation 순위에서 Operational Compiler 구성 우선순위를 도출할 수 있다.
- Scaling과 temporal stability 결과를 해석할 수 있다.

**관련 DR**: DR-5.1, DR-5.2, DR-5.3
**관련 실험**: E01~E22 분석
**관련 Figure**: Fig 1~2, 4~5, 8~12 (분석 책임)

---

## Ch.6 — 관찰에서 도구로: Operational Compiler

**파일**: `chapters/ch06-from-observation-to-operational-compiler.md`
**핵심 메시지**: Operational Compiler는 HOR × RSuccR pareto frontier를 따라 점진적으로 구성된다. Ch.5 ablation marginal ROI 순서가 운영 규칙 컴파일의 우선순위를 결정한다. "한 번에 전체 harness"는 HOR을 최적점 이상으로 높인다.

**탐구 질문**:
- Ch.5 ablation 결과에서 어떤 component를 먼저 도구화해야 하는가?
- HOR × MTTR trade-off를 어떻게 관리하면서 점진적으로 Operational Compiler를 구성하는가?
- 도구화해야 할 것과 도구화하면 안 되는 것의 기준은?
- Skill로 쓸 수 있는 능력을 어떻게 극대화하는가?

**핵심 구성**:
1. Ch.4-5에서 추출한 반복 실패 패턴 → 도구화 후보 식별 (marginal ROI 기준)
2. Operational Compiler 설계 원칙 (HOR 관리 포함)
3. 점진적 업데이트 원칙: pareto frontier를 따라 이동하는 전략
4. Skill로 쓸 수 있는 능력의 극대화
5. CLI-Anything 방법론 비교: 독립적 수렴의 의미

**학습 결과**:
- Ablation 결과에서 Operational Compiler 구성 우선순위를 결정할 수 있다.
- HOR × MTTR trade-off를 관리하는 점진적 업데이트 전략을 설계할 수 있다.
- 도구화 대상이 아닌 것(task 모호성, compute saturation)을 구분할 수 있다.

**관련 DR**: DR-6.1, DR-6.2
**관련 실험**: E18, E19, E20
**관련 Figure**: Fig 8 (Cost-Reliability Frontier), Fig 10 (Ablation)

---

## Ch.7 — Harness에서 Agent로: Self-Immune System을 향하여

**파일**: `chapters/ch07-harness-to-agent-self-immune.md`
**핵심 메시지**: Self-immune system = agent 내부의 ARCC self-monitoring + cliff-proximity detection + self-initiated recovery. 이 능력은 ARCC 하한 조건을 충족할 때만 신뢰 가능하다. 이것이 Agent-1 → Agent-2 전환의 실질적 조건이다.

**탐구 질문**:
- ARCC self-monitoring의 재귀적 한계는 무엇인가?
- 어떤 AgentOps 기능이 harness 내재화가 가능하고 어떤 것은 불가능한가?
- Model capability 증가가 harness의 역할을 전환시키는 ARCC threshold는 어디인가?
- Harness fatigue는 존재하며 어떻게 재보정하는가?
- Agent-1 → Agent-2 전환의 충분조건과 필요조건은 무엇인가?

**핵심 구성**:
1. 실험이 남긴 것 — Failure Budget Reallocation 재프레이밍, MTTR × IFR decay 연결
2. 현 세대 harness가 풀 수 없는 문제
3. AgentOps → Harness → Agent 내재화: 점진적 경로
4. Self-immune system 초기 설계 (조작적 정의 포함)
5. Model Capability × Harness Value: Scaling 조건 (Fig 11)
6. Temporal Stability: self-immune의 수명 (Fig 12)
7. Agent-1 → Agent-2: 전환 조건의 정식화
8. 이 책 이후: 미해결 질문들
9. 집필 과정의 메타 관찰

**학습 결과**:
- Self-immune system의 조작적 정의와 재귀적 한계를 이해한다.
- Fig 11 (Scaling), Fig 12 (Temporal Stability) 결과를 해석할 수 있다.
- Agent-1 → Agent-2 전환 조건(충분/필요)을 구분하여 설명할 수 있다.

**관련 DR**: DR-7.1, DR-7.2, DR-3.4(§9)
**관련 실험**: E12 (self-immune overhead), E20 (mini self-immune)
**관련 Figure**: Fig 9 (Harness ROC), Fig 11 (Scaling), Fig 12 (Temporal Stability)

---

## Appendices

| Appendix | 파일 | 내용 |
|----------|------|------|
| A | `appendix-a-experiment-log-template.md` | 실험 로그 템플릿 (v4: 5변수, 교차검증 포함) |
| B | `appendix-b-glossary.md` | 용어 사전 |
| C | `appendix-c-diagrams.md` | 다이어그램 모음 |
| D | `appendix-d-reference-projects.md` | 참조 프로젝트 목록 |
| E | `appendix-e-deep-research-prompts.md` | Deep research 프롬프트 전체 목록 |
