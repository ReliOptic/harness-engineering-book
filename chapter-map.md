# Chapter Map — Harness Engineering and AgentOps (v6)

> 각 챕터의 제목, 탐구 질문, 핵심 메시지, 학습 결과, 관련 DR/실험 목록.
> 집필 시 이 문서를 기준으로 방향 확인. writing-plan.md의 요약본.
> v6 넘버링: Part I(Ch.1~4) 논문 계보 + Part II~IV(Ch.5~11) 관찰·실험·도구화.

---

## Preface

**핵심 메시지**: 왜 이 책이 필요한가. 누구를 위한 책인가.
**학습 결과**: 독자가 이 책에서 무엇을 얻을 수 있는지 명확히 이해한다.

---

# Part I — 기반: Agent를 만든 논문들

---

## Ch.1 — Attention과 Context: 모델은 어떻게 보는가

**파일**: `chapters/ch01-attention-and-context.md`
**상태**: 스켈레톤 (Beta 범위)
**Backbone**: Vaswani et al. *Attention Is All You Need* (2017) + Liu et al. *Lost in the Middle* (2024)

**핵심 메시지**: Transformer의 attention 메커니즘이 정보를 처리하는 방식과, 그 구조적 한계가 agent runtime 실패로 이어지는 경로.

**탐구 질문**:
- Attention 메커니즘이 context window에서 정보를 어떻게 선택하는가?
- Lost in the Middle 현상이 agent의 context 활용에 어떤 제약을 만드는가?

**학습 결과**: "왜 context window를 늘려도 agent가 중간 정보를 놓치는가"를 attention 메커니즘으로 설명할 수 있다.

---

## Ch.2 — 압축 렌즈: 모든 언어 모델은 압축기다

**파일**: `chapters/ch02-compression-lens.md`
**상태**: 스켈레톤 (Beta 범위)
**Backbone**: Delétang et al. *Language Modeling Is Compression* (ICLR 2024) + Shannon (1948)

**핵심 메시지**: 언어 모델 = 압축 알고리즘. 이 등가성이 agent runtime 현상을 읽는 정보이론적 렌즈를 제공한다.

**탐구 질문**:
- 왜 더 좋은 모델이 더 잘 압축하는가?
- 정보이론적 어휘가 prompt 최적화와 모델 비교에 어떻게 적용되는가?

**학습 결과**: cross-entropy, KL divergence, bits-per-byte를 모델 비교와 prompt 최적화에 적용할 수 있다.

---

## Ch.3 — 정렬에서 자율로: 모델은 어떻게 행동을 배우는가

**파일**: `chapters/ch03-alignment-to-autonomy.md`
**상태**: 스켈레톤 (Beta 범위)
**Backbone**: Ouyang et al. *InstructGPT* (2022) + Lee et al. *RLAIF* (2023) + Bai et al. *Constitutional AI* (2022)

**핵심 메시지**: 학습 단계의 정렬이 runtime 문제를 해결하지 못하는 구조적 이유. Constitutional AI → Ch.11 self-immune의 계보.

**탐구 질문**:
- 모델이 aligned되었는데 왜 agent가 여전히 실패하는가?
- 학습-runtime 경계의 구조적 차이는 무엇인가?

**학습 결과**: aligned model ≠ reliable agent를 학습-runtime 경계로 설명할 수 있다.

---

## Ch.4 — 도구, 추론, 기억: Agent는 어떻게 행동하는가

**파일**: `chapters/ch04-tools-reasoning-memory.md`
**상태**: 스켈레톤 (Beta 범위)
**Backbone**: Schick et al. *Toolformer* (2023) + Yao et al. *ReAct* (2023) + Shinn et al. *Reflexion* (2023)
**Companion**: Lewis et al. *RAG* (2020)

**핵심 메시지**: 도구 사용, 추론-행동 통합, 자기 성찰의 학술적 기원과, 각 능력이 runtime에서 실패하는 메커니즘.

**탐구 질문**:
- 도구 사용 정확도, multi-step reasoning depth의 측정이 왜 필요한가?
- Reflexion의 task 간 학습과 Ch.11 self-immune의 task 내 면역은 어떻게 다른가?

**학습 결과**: 네 가지 agent 능력의 실패 메커니즘으로 Ch.6 측정 지표의 필요성을 설명할 수 있다.

---

# Part II — 프레임워크: 관찰과 측정

---

## Ch.5 — 왜 다섯 변수인가: 현장에서의 정당화

**파일**: `chapters/ch05-what-is-happening-now.md`
**상태**: 초고 있음 (정밀 수정)
**핵심 메시지**: Part I의 네 갈래 기술사가 현장에서 왜 5변수로 수렴하는지를 2026년 상반기 관찰로 정당화한다.

**탐구 질문**:
- 2026년 상반기 agent runtime 현장은 어떤 상태인가?
- Part I의 기술사가 현장에서 왜 5변수로 수렴하는가?
- 초기 agent runtime의 반복 실패가 무엇을 보여주는가?

**핵심 구성**:
1. 2026년 상반기: agent가 깨지는 풍경
2. Part I에서 이 현장으로: 네 갈래 기술사가 만나는 지점
3. 5변수 프레임워크: 병목 분석의 최소 단위
4. 이원론의 거부와 Agent-1~2 스펙트럼
5. 이 책의 좌표: AI Engineering 이후의 질문

**학습 결과**:
- 현재 agent 생태계를 파악하고, 5변수 프레임워크의 기본 개념을 이해한다.
- Agent-1 ~ Agent-5 스펙트럼에서 현재 배포된 agent가 Agent-1에 머무는 구조적 이유를 설명할 수 있다.

**관련 DR**: DR-1.1, DR-1.2, DR-1.3
**관련 실험**: (없음 — 관찰 및 사례 중심)
**관련 증거**: `evidence/case-studies/openclaw-anchor.md`, `evidence/case-studies/teamclaws-picoclaw-postmortem.md`
**관련 dispatch**: `FD-2026-03-17-002-cli-renaissance.md`, `FD-2026-03-17-002-wide-survey.md`

---

## Ch.6 — Agent가 모델로부터 무엇을 물려받는가

**파일**: `chapters/ch06-nature-agent-inherits.md`
**상태**: 초고 있음 (정밀 수정)
**핵심 메시지**: Agent는 중립적이지 않다. 모델별 행동 차이를 정량적으로 측정하고, Capability Cliff가 존재한다는 것을 관찰한다.

**탐구 질문**:
- 동일한 task에서 모델을 바꾸면 무엇이 어떻게 달라지는가?
- "Agent-Viable Minimum"은 task별로 어떤 capability 수준에서 형성되는가?
- 양자화와 distillation은 agent capability를 어떻게 다르게 깎는가?

**핵심 구성**:
1. 물려받는 경향: reasoning, tool use, consistency, confidence
2. ARCC (Agent-Relevant Capability Composite)
3. Capability Cliff
4. Quantization Tax Curve
5. Distillation Efficiency Frontier
6. Mid-run model switching의 context continuity 붕괴 패턴 (E03)
7. 5변수 중 "모델" 변수가 1차 병목이 되는 조건

**핵심 Figure**: Fig 1 — Agent Capability Cliff
**핵심 지표**: ARCC (TCA, IFR, MSRD_n, CUE), TCR per task type

**학습 결과**:
- 모델 원인의 취약성을 식별하고, ARCC 기반으로 유사한 측정을 설계할 수 있다.
- Capability Cliff의 존재를 이해하고, 양자화 모델의 task 적합성을 판단하는 근거를 갖는다.

**관련 DR**: DR-2.1, DR-2.2, DR-2.3
**관련 실험**: E01, E02, E03, E10

---

## Ch.7 — Harness Engineering과 AgentOps: 정의와 프레임워크

**파일**: `chapters/ch07-harness-and-agentops-defined.md`
**상태**: 초고 있음 (**세 축 비교 중심 재구성**)
**핵심 메시지**: Harness는 failure를 제거하지 않는다. Failure의 성격을 바꾼다 — Failure Budget Reallocation. 세 축 비교(공식 담론/공개 실물 패턴/출간 시장)로 harness engineering의 위치를 확립한다.

**탐구 질문**:
- Harness engineering은 guardrails, scaffolding과 어떻게 다른가?
- AgentOps는 MLOps, DevOps와 어떻게 다른가?
- HOR × RSuccR trade-off에 optimal point가 존재하는가?
- 공식 담론, 공개 실물 패턴, 출간 시장에서 harness engineering은 각각 어떻게 정의되는가?

**핵심 구성**:
1. Harness engineering이란 무엇인가 — operational envelope 정의 (**공식 담론** 축)
2. 보호와 enablement의 이중 구조
3. Harness를 guardrails, scaffolding, orchestration과 구분 (**공개 실물 패턴** 축: CLAUDE.md, AGENTS.md, GEMINI.md, .cursorrules)
4. Failure Budget Reallocation (**출간 시장** 축: 경쟁서가 다루지 않는 운영 개념)
5. HOR (Harness Overhead Ratio)
6. AgentOps란 무엇인가 — Langfuse/AgentOps/Arize 등 실제 도구 생태계
7. 산업계 AgentOps 실무 — 도구화된 것 vs 아직 안 된 것
8. Ch.8 실험 프레임 설정 — 가설과 판단 기준의 pre-registration

**학습 결과**:
- Harness와 AgentOps를 정의하고, Failure Budget Reallocation 프레임으로 harness 효과를 설명할 수 있다.
- HOR의 정의와 HOR × RSuccR trade-off를 이해한다.
- 세 축에서 harness engineering의 위치를 설명할 수 있다.

**관련 DR**: DR-3.1, DR-3.2, DR-3.3, DR-3.4
**관련 실험**: E05, E06, E07, E08
**관련 Figure**: Fig 2 (Failure Profile Radar + Operational Translation)

---

# Part III — 실험: 의도적 실패와 학습

---

## Ch.8 — 의도적 실패 실험: 22개 시나리오

**파일**: `chapters/ch08-deliberate-failure-experiments.md`
**상태**: 초고 있음 (E01~E08 완성)
**핵심 메시지**: 22개 시나리오는 pre-registration 원칙 하에 설계되었다. 실험은 5변수를 격리 조작하며 어떤 변수가 어떤 조건에서 1차 병목이 되는가를 측정한다.

**탐구 질문**:
- 5변수 중 어느 것을 조작하면 어떤 실패가 나타나는가?
- Capability Cliff는 harness-off 조건에서 어떤 형태를 갖는가?
- Failure budget은 harness-on 조건에서 어떻게 재배분되는가?

**핵심 구성**:
- 1막 (E01-E04): 모델 변수 조작
- 2막 (E05-E08): Harness·Surface 변수 조작
- 3막 (E09-E14): 제약 환경의 병목
- 4막 (E15-E17): Operator intervention의 효과
- 5막 (E18-E20): AgentOps 내재화
- 반례 (E21-E22): Task design 문제, Compute saturation 문제

**학습 결과**:
- Pre-registration 원칙을 적용한 deliberate failure experiment를 설계하고 실행할 수 있다.
- Task T1/T2/T3/T4 조작적 정의와 ground truth 3-layer를 이해한다.

**관련 DR**: DR-4.1, DR-4.2, DR-4.3, DR-4.4
**관련 실험**: E01~E22 전체
**관련 Figure**: Fig 1~8 (데이터 생성 책임)
**Pre-registration 파일**: `experiments/design-specification.md`

---

## Ch.9 — 실험 결과에서 배운 것: AgentOps와 Harness의 실무

**파일**: `chapters/ch09-lessons-from-experiments.md`
**상태**: 초고 있음 (정량 분석)
**핵심 메시지**: 실험실 metric → 운영 metric(MTTR, HER) → 비용 metric(TotalCost, CostIndex)의 3단계 번역. Optimal HOR은 존재하며, 그 점 이상에서 harness는 새로운 1차 병목이 된다.

**탐구 질문**:
- 어떤 변수가 어떤 조건에서 1차 병목이었는가?
- Failure budget이 재배분된 방향과 비율은?
- Optimal HOR은 어디에 있으며 cost scenario에 따라 어떻게 달라지는가?

**핵심 구성**:
1. 22개 실험 결과 종합: 5변수별 병목 분포
2. Failure Budget Reallocation 정량 분석
3. 운영 metric 번역: MTTR과 Human Escalation Rate
4. 비용 metric 번역: TotalCost와 optimal HOR
5. Component ablation: 무엇이 얼마나 기여하는가
6. Token efficiency를 운영 규율로
7. Scaling과 temporal stability
8. 학술적 확장 가능성

**학습 결과**:
- 실험실 metric → 운영 metric → 비용 metric 번역 체계를 이해하고 적용할 수 있다.
- HOR × RSuccR optimal point를 판단하는 방법을 이해한다.

**관련 DR**: DR-5.1, DR-5.2, DR-5.3
**관련 실험**: E01~E22 분석
**관련 Figure**: Fig 1~2, 4~5, 8~12 (분석 책임)

---

# Part IV — 도구화: 운영 구조의 구축

---

## Ch.10 — 관찰에서 도구로: Operational Compiler

**파일**: `chapters/ch10-from-observation-to-operational-compiler.md`
**상태**: 초고 있음 (**§5 공개 harness 비교 강화**)
**핵심 메시지**: Operational Compiler는 HOR × RSuccR pareto frontier를 따라 점진적으로 구성된다. §5에서 공개 실물 패턴(CLAUDE.md, AGENTS.md, GEMINI.md, .cursorrules) 비교를 통해 산업적 수렴을 확인한다.

**탐구 질문**:
- Ch.9 ablation 결과에서 어떤 component를 먼저 도구화해야 하는가?
- 도구화해야 할 것과 도구화하면 안 되는 것의 기준은?
- 공개 harness 패턴에서 관찰되는 공통 구조는 무엇인가?

**핵심 구성**:
1. 반복 실패 패턴 → 도구화 후보 식별 (marginal ROI 기준)
2. Operational Compiler 설계 원칙 (HOR 관리 포함)
3. 점진적 업데이트 원칙: pareto frontier를 따라 이동하는 전략
4. Skill로 쓸 수 있는 능력의 극대화
5. **산업적 수렴: 공개 harness 패턴 비교** (CLAUDE.md, AGENTS.md, GEMINI.md, .cursorrules)

**학습 결과**:
- Ablation 결과에서 Operational Compiler 구성 우선순위를 결정할 수 있다.
- 도구화 대상이 아닌 것(task 모호성, compute saturation)을 구분할 수 있다.

**관련 DR**: DR-6.1, DR-6.2
**관련 실험**: E18, E19, E20
**관련 Figure**: Fig 8 (Cost-Reliability Frontier), Fig 10 (Ablation)

---

## Ch.11 — Harness에서 Agent로: Self-Immune System을 향하여

**파일**: `chapters/ch11-harness-to-agent-self-immune.md`
**상태**: 초고 있음 (미해결 질문 정리)
**핵심 메시지**: Self-immune system = agent 내부의 ARCC self-monitoring + cliff-proximity detection + self-initiated recovery. Agent-1 → Agent-2 전환의 실질적 조건.

**탐구 질문**:
- ARCC self-monitoring의 재귀적 한계는 무엇인가?
- 어떤 AgentOps 기능이 harness 내재화가 가능하고 어떤 것은 불가능한가?
- Agent-1 → Agent-2 전환의 충분조건과 필요조건은 무엇인가?

**핵심 구성**:
1. 실험이 남긴 것 — Failure Budget Reallocation 재프레이밍
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
- Agent-1 → Agent-2 전환 조건(충분/필요)을 구분하여 설명할 수 있다.

**관련 DR**: DR-7.1, DR-7.2, DR-3.4(§9)
**관련 실험**: E12, E20
**관련 Figure**: Fig 9, Fig 11, Fig 12

---

## Appendices

| Appendix | 파일 | 내용 |
|----------|------|------|
| A | `appendix-a-experiment-log-template.md` | 실험 로그 템플릿 (v4: 5변수, 교차검증 포함) |
| B | `appendix-b-glossary.md` | 용어 사전 |
| C | `appendix-c-diagrams.md` | 다이어그램 모음 |
| D | `appendix-d-reference-projects.md` | 참조 프로젝트 목록 |
| E | `appendix-e-deep-research-prompts.md` | Deep research 프롬프트 전체 목록 |
