# 집필계획서 v4 — *Harness Engineering and AgentOps*

## 0. 프로젝트 개요

**제목**
*Harness Engineering and AgentOps*

**부제 후보**
*Observing What Makes Agents Work — and What Breaks Them*

**도입부 시간 앵커**
2026년 3월 13일 (도입 내러티브 기준일. 챕터 제목에는 넣지 않음.)

**책의 성격: 스냅샷이자 실험서**
이 책은 2026년 상반기에 agent runtime을 운영하며 관찰한 것들의 스냅샷이다.
동시에, 체계적 실험을 통해 "agent 시스템이 어떤 조건에서 무엇 때문에 작동하고, 무엇 때문에 깨지는가"를 기록하는 실험서이다.
심층 학문 해석이 아니라, 정직한 관찰과 측정을 다음 단계의 profoundation(실천적 토대)으로 남기는 것이 목적이다.

**레퍼런스**
Chip Huyen, *AI Engineering* (2025).
AIE는 foundation model 위에 application을 만드는 전 과정을 다룬다.
이 책은 AIE가 다루는 영역의 다음 레이어 — agent runtime의 운영 구조, harness 설계, AgentOps — 를 기록한다.
AIE에 대한 shout-out과 함께, 같은 맥락 위에 있는 이야기임을 밝힌다.

**원고 마일스톤**

| 마일스톤 | 목표일 |
| --- | --- |
| Beta manuscript (7챕터 초고) | 2026년 5월 13일 |
| Polished release manuscript | 2026년 6월 30일 |

**주간 투입량**
- Lead author: ~12시간/주
- Experimenter 3명: 각 ~8시간/주
- 총 팀 투입: ~36시간/주

**책의 근본 자세**
이 책은 교리집이 아니라 실험서이다.
미리 결론을 정해놓고 증거를 끼워맞추지 않는다.
관찰하고, 측정하고, 기록하고, 그 기록에서 패턴을 추출한다.

---

## 1. 핵심 탐구 질문과 개념 정의

### 한 줄 논제

Harness engineering은 agent-first 시스템이 실제 제약 조건 아래에서 무엇을 보호하고, 무엇을 가능하게 하며, 어떻게 취약성을 줄이는지를 다루는 설계 및 운영 분야이다.

### 왜 지금이 중요한 시점인가

Agent가 아직 공고히 서지 않았다. Harness engineering이 아직 develop되지 않았다.
바로 이 초기 단계에서 관찰할 수 있는 것이 있다:
agent가 어떤 요소로 구성되는지, 모델과 harness와 surface와 리소스가 어떻게 상호작용하는지를 지금 볼 수 있다.
이것을 지금 알면, agent가 나중에 고도화되었을 때 그것이 어떻게 통제되어야 하는지를 역설적으로 알 수 있다.
그것이 엔지니어링이고, 그것을 할 수 있는 좋은 시점이 바로 지금이다.

### 5변수 프레임워크: 이원론을 넘어서

Agent 시스템의 실용적 품질은 "모델 vs. 운영 구조"의 이원론으로 설명되지 않는다.
최소 다음 5개 변수의 상호작용으로 결정된다:

| 변수 | 설명 |
| --- | --- |
| **모델** | Foundation model의 reasoning, tool use, consistency, confidence 특성 |
| **Harness** | Operational envelope: memory 보호, 권한, 복구, evaluation hook |
| **Product surface** | Agent가 input/output을 주고받는 인터페이스 (CLI, API, 기타) |
| **Operator intervention** | 인간 운영자의 개입 패턴, 타이밍, 효과 |
| **Compute/resource budget** | VM 사양, token budget, API 비용, 네트워크 지연 |

**이 책의 핵심 질문은 "모델과 harness 중 누가 더 중요한가?"가 아니다.**
**"어떤 조건에서 무엇이 1차 병목이 되는가?"이다.**

이것을 실험을 통해 관찰하고 측정한다.

### 핵심 탐구 질문

1. **Agent 시스템의 품질을 결정하는 5개 변수 중, 어떤 조건에서 무엇이 1차 병목이 되는가?** — 이원론이 아닌, 다변수 상호작용을 실험으로 관찰한다.
2. **제약 환경에서는 어떤 병목이 가장 먼저 드러나는가?** — 실용적 사실: threshold가 낮아서 빨리 실패하고, "괜찮다/안 괜찮다"를 빠르게 판별할 수 있다.
3. **AgentOps의 범위와 역할은 무엇이며, 어디까지 확장되는가?** — 함의를 좁히지 않고 열어둔다.
4. **Harness engineering을 통해 AgentOps 기능을 agent 자체에 점진적으로 주입할 수 있는가?** — Self-immune system을 향한 경로.

### 이 책의 관찰 프로그램 (5개 관찰 축)

1. 같은 task에서 **모델을 바꾸면** agent 행동과 failure mode가 어떻게 달라지는가
2. 같은 모델에서 **harness와 surface를 바꾸면** 결과가 어디까지 달라지는가
3. **제약 환경**에서는 어떤 병목이 가장 먼저 드러나는가
4. 어떤 **operator intervention**이 반복 가능해서 reusable runtime aid로 굳어지는가
5. AgentOps의 어떤 기능은 **harness 안으로 부분 내재화**될 수 있는가

### 반드시 포함할 반례

**반례 1 — Task design 문제:**
어떤 실패는 harness나 모델 문제가 아니라 task 자체가 불안정한 경우이다. 질문이 흔들리면 runtime을 아무리 튜닝해도 흔들린다.

**반례 2 — Compute saturation 문제:**
어떤 실패는 모델이나 harness가 아니라 compute 포화 문제이다. VM 과부하, CPU 불안정, agent 충돌이 그 예이다. TeamClaws/PicoClaw 실패는 이 반례의 직접적 사례이다. 이 경우 AgentOps는 observability만이 아니라 resource governance여야 한다.

### 핵심 용어 정의

**Harness**
Memory, privacy, 권한, 핵심 context를 보호하면서 bounded capability, 재현성, 복구를 가능하게 하는 설계된 operational envelope.
나아가, AgentOps의 기능을 agent 내부에 점진적으로 주입하는 구조적 프레임워크이기도 하다.

**AgentOps**
비결정적 agent runtime을 **관찰 가능하고, 통제 가능하고, 복구 가능하고, 자원 인식적**으로 운영하기 위한 실천 규율.
Logging만이 아니라, intervention policy, permission design, recovery path, cost/latency discipline, compute overload control, self-reporting을 포함한다.
MLOps/DevOps에서 파생되었으나 그것보다 넓으며, 궁극적으로 harness를 통해 agent 자체에 내재화되는 방향으로 진화한다.

**Agent-first product surface**
Agent가 input을 안정적으로 해석하고 구조화된 feedback을 받을 수 있도록 설계된 제품 표면.
현재 인류가 알고 있는 가장 효과적인 형태는 CLI이다.
그러나 CLI를 대체하거나 확장할 수 있는 더 나은 형태가 있지 않을까? — 이 질문을 열어둔다.

**Operational Fieldkit**
제약 실험에서 반복적으로 확인된 실패 패턴과 운영 교훈을 범용 도구로 구체화한 CLI 유틸리티 레이어.
**Harness에 직접 한 번에 embedding하는 것이 아니다.**
Lesson learned를 통해 Fieldkit이 계속 업데이트되고, CLI만 업데이트하면 더 나은 self-immune 시스템으로 올라갈 수 있다.
이 제품을 개발함으로써 skill로 쓸 수 있는 능력들을 어떻게 극대화할 수 있는지를 harness engineering으로 알아보는 것이 중요하다.
**한 번에 implement하는 것이 아니라, 점진적으로 발전시키는 것이 조건이다.**

---

## 2. 독자 정의

### Primary reader

**Technical builder-operator**: agent runtime을 직접 다루는 사람.

- Agent runtime 실험 중인 엔지니어 (OpenClaw, Claude Code, nanobot 등)
- Open-source agent 빌더 및 운영자 — 특히 tool 연결 및 확장
- Agent-first application을 설계하는 product/technical lead

**이 독자의 월요일 아침 문제:**
"어제까지 잘 돌던 workflow가 모델 업데이트 후 tool call에서 실패한다. 모델 문제인지 harness 문제인지 compute 문제인지 모르겠다. 그리고 이 agent에 proactivity가 부족한 것 같은데, 어떻게 개선하지?"

### Secondary reader

전략 지향 기술자, 스타트업 팀, 기술 product owner.

### 난이도

LLM, tool use, agent workflow 실무 수준 전제. ML 연구 전문성 미전제.
모든 챕터는 product lead가 이해 가능하면서 builder에게 유용해야 한다.

---

## 3. 포지셔닝

### 이 책의 정체

- Agent runtime 현실의 스냅샷이자 실험서
- 5변수 상호작용을 실험으로 관찰하는 field book
- Harness engineering과 AgentOps의 윤곽을 관찰에 기반하여 그리는 초기 시도
- 관찰 → 측정 → 실패 기록 → Fieldkit 도구화 → agent 내재화의 방법론 경로
- Ch.4-5의 실험 결과가 학술적 실험 설계의 벤치마크가 될 수 있는 수준

### 이 책이 아닌 것

- 교리집이 아니다 (결론을 미리 정하지 않는다)
- "모델 vs. harness" 이원론이 아니다
- AgentOps 백과사전이 아니다
- CLI를 최종 형태로 경직되게 취급하지 않는다

### CLI 열린 포지셔닝

CLI는 현재 가장 효과적인 agent-first surface이다. 그러나 더 나은 형태가 있지 않을까?
다양한 시도를 해보고, agent/harness/모델의 진화에 따라 surface도 진화할 가능성을 열어둔다.

---

## 4. 내러티브 척추와 핵심 사례

### 스냅샷 원칙

2026년 상반기에 벌어지는 일의 스냅샷을 정직하게 기록한다.

### Anchor case: OpenClaw

OpenClaw가 해준 것은 MCP 연결, skills 통합, gateway 아키텍처를 하나의 운영 가능한 시스템으로 엮어준 것이다.
그 시스템을 운영하면서 "모자란 무언가를 채우는 것"이 harness engineering이다.

### 실패 사례: TeamClaws/PicoClaw

Multi-agent orchestration 시도. CPU 과부하, 리소스 과다, agent 충돌로 실패.
이 실패는 **반례 2 (compute saturation)**의 직접적 사례이며, 이 책을 쓰게 된 동기이다.

### 생태계 스냅샷

OpenClaw 주변 프로젝트들 (nanobot, CLI-Anything, OpenClaw-RL, openclaw-agents, openclaw-studio 등)을 deep research로 기록. 2026년 상반기 agent 생태계의 기록적 가치.

---

## 5. 챕터 구조 (7개 챕터)

### 전체 논리 흐름

```
Ch.1  지금 무슨 일이 일어나고 있는가 (스냅샷, 생태계)
  ↓
Ch.2  Agent는 모델로부터 무엇을 물려받는가 (관찰, 측정)
  ↓
Ch.3  Harness engineering이란 무엇인가 + AgentOps란 무엇인가
      (정의 → Ch.4-5의 실험을 위한 프레임 설정)
  ↓
Ch.4  의도적 실패 실험: 20개 시나리오
      (제약 환경에서 AgentOps와 harness engineering이 겪는 상황들)
  ↓
Ch.5  실험 결과에서 배운 것: AgentOps와 Harness의 실무
      (Ch.4 실험의 분석, 패턴 추출, computation 요구사항)
  ↓
Ch.6  관찰에서 도구로: Operational Fieldkit (도구화 방법론)
  ↓
Ch.7  Harness → Agent 내재화 → Self-Immune System
```

**핵심 변경:** Ch.3에서 AgentOps와 harness engineering을 먼저 정의한 뒤, Ch.4에서 본격적으로 실험을 돌리고, Ch.5에서 분석한다. Ch.4-5가 이 책의 실험적 무게중심이다.

---

### Chapter 1. 지금 무슨 일이 일어나고 있는가

**핵심 메시지:** Agent-friendly product surface의 초기 형태가 부상하는 시점을 기록한다.

**핵심 구성:**
1. 2026년 상반기: agent 운영의 현재 풍경
2. OpenClaw — 무엇이 특별하고 무엇이 아직 모자란가
3. 생태계 스냅샷: OpenClaw 주변 프로젝트들
4. TeamClaws/PicoClaw — 이 책을 쓰게 된 이유
5. 왜 지금이 중요한가 — harness engineering 초기에 알 수 있는 것
6. 5변수 프레임워크 소개
7. Agent-1 ~ Agent-5 방향 설정
8. AIE shout-out

**필요한 deep research:**
- `DR-1.1`: "OpenClaw ecosystem 2026" — OpenClaw를 벤치마크하거나 대안으로 나온 프로젝트 전수 조사. nanobot, CLI-Anything, OpenClaw-RL, openclaw-agents, openclaw-studio, openclaw-mission-control 등.
- `DR-1.2`: "Agent-first product surface landscape 2026" — CLI 이외에 agent-friendly surface로 시도되고 있는 것들 (A2UI, Canvas, voice-first 등).
- `DR-1.3`: "Chip Huyen AI Engineering reception and impact" — AIE 이후의 논의 흐름, 이 책의 포지셔닝 근거.

**학습 결과:** 독자는 현재 agent 생태계를 파악하고, 왜 이 시점에서 harness engineering이 필요한지 설명할 수 있다.

---

### Chapter 2. Agent가 모델로부터 무엇을 물려받는가

**핵심 메시지:** Agent는 중립적이지 않다. 모델별 행동 차이를 정량적으로 측정하고 스냅샷으로 기록한다.

**핵심 구성:**
1. 물려받는 경향: reasoning, tool use, consistency, confidence
2. OpenRouter 기반 모델 교체 실험 — SOTA, mid-tier, open-source, distilled, quantized
3. 정량 측정 결과: 동일 task에서의 행동 차이
4. Edge 조건과 전문화 문제
5. 5변수 중 "모델" 변수가 1차 병목이 되는 조건

**필요한 deep research:**
- `DR-2.1`: "LLM agent behavioral benchmarks 2026" — 모델별 agent 행동 비교 기존 연구/벤치마크.
- `DR-2.2`: "OpenRouter model routing strategies" — OpenRouter의 모델 선택 및 routing 메커니즘.
- `DR-2.3`: "Model distillation and quantization effects on agent tool use" — distillation/quantization이 tool call 안정성에 미치는 영향.

**학습 결과:** 독자는 모델 원인의 취약성을 식별하고, 자신의 환경에서 유사한 측정을 설계할 수 있다.

---

### Chapter 3. Harness Engineering과 AgentOps: 정의와 프레임워크

**핵심 메시지:** Ch.4-5의 실험을 위해, harness engineering과 AgentOps를 먼저 정의하고 실험 프레임을 설정한다.

**핵심 구성:**
1. Harness engineering이란 무엇인가 — operational envelope 정의
2. 보호와 enablement의 이중 구조
3. Harness를 guardrails, scaffolding, orchestration과 구분
4. AgentOps란 무엇인가 — profession으로서의 정의
   - AgentOps operator가 하는 일의 구체적 목록
   - Resource governance가 AgentOps의 핵심 일부임을 명시
5. 5변수 프레임워크에서 harness와 AgentOps의 위치
6. Harness 부재의 비용: TeamClaws/PicoClaw 사후 분석 (반례 2)
7. CLI-Anything HARNESS.md — 독립적 수렴 사례
8. Ch.4-5에서 실험할 것에 대한 프레임 설정: "무엇을 의도적으로 실패시킬 것인가"

**필요한 deep research:**
- `DR-3.1`: "Harness/guardrails/scaffolding terminology in agent systems 2025-2026" — 기존 용어 사용 현황.
- `DR-3.2`: "CLI-Anything HARNESS.md methodology analysis" — HKUDS의 harness 정의와 구현 방법론.
- `DR-3.3`: "AgentOps landscape: existing frameworks and tools 2026" — LangSmith, Weights & Biases Weave, AgentOps.ai 등 기존 도구.
- `DR-3.4`: "Agent runtime failure taxonomies" — 기존 agent 실패 분류 체계.

**학습 결과:** 독자는 harness와 AgentOps를 정의하고, Ch.4 실험의 프레임을 이해한다.

---

### Chapter 4. 의도적 실패 실험: 20개 시나리오

**핵심 메시지:** 의도적으로 실패시키고, 무엇이 어떤 조건에서 깨지는지를 체계적으로 기록한다.

**목적:**
- Harness engineering과 AgentOps가 겪어야 하는 어려운 상황들을 미리 실험
- 제약 환경(무료 티어)의 낮은 threshold를 활용한 빠른 feedback
- 5변수 중 어떤 것이 1차 병목인지를 시나리오별로 식별
- 풍선 효과 관찰: 한 요소를 바꾸면 다른 곳에서 에러가 터짐

**20개 실험 시나리오** (→ 섹션 8에서 상세 기술)

**필요한 deep research:**
- `DR-4.1`: "Chaos engineering applied to AI agent systems" — chaos engineering 원리의 agent 시스템 적용 가능성.
- `DR-4.2`: "Google Cloud free tier constraints and failure modes" — GCP 무료 티어의 구체적 제약 사항.
- `DR-4.3`: "Token budget optimization strategies for agent systems" — token 예산 관리 기존 연구.
- `DR-4.4`: "Agent system compute requirements benchmarking" — agent runtime별 CPU/RAM 요구사항.

**학습 결과:** 독자는 자신의 환경에서 의도적 실패 실험을 설계하고 실행할 수 있다. 이 챕터의 실험 설계를 벤치마크하여 학술적 실험을 구축할 수 있다.

---

### Chapter 5. 실험 결과에서 배운 것: AgentOps와 Harness의 실무

**핵심 메시지:** Ch.4의 20개 실험에서 패턴을 추출하고, AgentOps와 harness engineering의 구체적 실무로 전환한다.

**핵심 구성:**
1. 20개 실험 결과 종합: 어떤 변수가 어떤 조건에서 1차 병목이었는가
2. 패턴 추출: 반복되는 실패 유형 분류
3. Computation 요구사항: harness에 요구되는 능력 수준별 필요 사양
4. Token efficiency를 운영 규율로
5. 모델이 논리 회로를 많이 돌릴 때 VM 과부하 — 제어 방법
6. Operator intervention 패턴: 어떤 개입이 반복 가능한 runtime aid가 되는가
7. 무료 티어 → 유료 티어로 갔을 때: 무엇이 개선되고 무엇이 변하지 않는가
8. Harness engineering에 필요한 skill set 정리
9. 학술적 확장 가능성: 이 실험들에서 파생 가능한 논문/공모전 주제

**필요한 deep research:**
- `DR-5.1`: "Agent system failure pattern analysis methodologies" — 실패 패턴 분석 방법론.
- `DR-5.2`: "Compute cost optimization for agent deployments" — agent 배포의 비용 최적화 사례.
- `DR-5.3`: "VM resource management for LLM-based agents" — VM 환경에서 LLM agent의 리소스 관리.

**Ch.4와의 관계:** Ch.4가 실험의 실행과 기록이라면, Ch.5는 분석과 패턴 추출이다. 두 챕터가 이 책의 실험적 무게중심이며, 팀 3명이 5-6주 투입하는 곳이다.

**학습 결과:** 독자는 AgentOps 실무를 이해하고, computation 요구사항을 산정하며, 실험 결과에서 학술적 확장 가능성을 식별할 수 있다.

---

### Chapter 6. 관찰에서 도구로: Operational Fieldkit

**핵심 메시지:** 먼저 직접 써보고, 실패하고, 기록하고, 그 히스토리를 점진적으로 도구로 만든다.

**핵심 구성:**
1. Ch.4-5에서 추출한 반복 실패 패턴 → 도구 후보 식별
2. Operational Fieldkit 설계 원칙
3. **점진적 업데이트 원칙:** Fieldkit은 harness에 한 번에 embedding되는 것이 아니다. CLI로 제공되어 계속 업데이트되고, 그 업데이트가 self-immune 능력을 점진적으로 향상시킨다.
4. Skill로 쓸 수 있는 능력의 극대화 — harness engineering으로 탐색
5. CLI-Anything 방법론 비교

**필요한 deep research:**
- `DR-6.1`: "Developer CLI tool design patterns" — 성공적인 CLI 도구의 설계 패턴.
- `DR-6.2`: "Incremental capability injection in agent systems" — agent에 능력을 점진적으로 주입하는 기존 접근.

**학습 결과:** 독자는 실험 로그에서 도구화 후보를 식별하고, 점진적 Fieldkit 업데이트 전략을 설계할 수 있다.

---

### Chapter 7. Harness에서 Agent로: Self-Immune System을 향하여

**핵심 메시지:** AgentOps 기능을 harness를 통해 agent에 점진적으로 주입하여, agent가 스스로 복구하고 학습하는 self-immune system을 갖게 하는 것이 Agent-2 전환의 핵심 조건이다.

**핵심 구성:**
1. 이 책의 실험들이 보여준 유의미한 결과 종합
2. 현 세대 harness가 아직 풀 수 없는 문제
3. AgentOps → Harness → Agent 내재화: 점진적 경로
4. Self-immune system 초기 설계
5. Agent-1 → Agent-2: infinite learning이 가능해지는 조건
6. 이 책 이후: AI agent가 연구와 기록을 자율적으로 수행하는 미래
7. 집필 과정 자체가 agent와의 협업이었다는 메타 관찰

**필요한 deep research:**
- `DR-7.1`: "Self-healing and self-recovering AI agent architectures" — 기존 self-healing agent 연구.
- `DR-7.2`: "Continuous learning in deployed agent systems" — 배포된 agent의 지속 학습 사례.

**학습 결과:** 독자는 harness engineering이 Agent-2 전환에 왜 필수적인지 설명할 수 있다.

---

## 6. Agent-1 ~ Agent-5 프레임워크

| 레벨 | 작업 라벨 | 이 책에서의 역할 |
| --- | --- | --- |
| Agent-1 | Early Agent | 현 세대: tool-using이지만 취약, proactivity 결여 |
| Agent-2 | Continuous Learner | Self-immune system, collapse 후 자발 복구, infinite learning |
| Agent-3 | Domain Expert | 한정 영역 고속 역량, harness 전문화 |
| Agent-4 | Superhuman Researcher | 인간 실무자 초과 |
| Agent-5 | Collective | 조직 규모 조율 |

Ch.1에서 도입, Ch.7에서 Agent-1→2 전환에 집중.

---

## 7. 증거 전략

### 관찰 원칙

- 결론을 미리 정하지 않는다
- 결과가 예상과 다르면 결과를 기록한다
- 단일 실행에서 일반화할 때 반드시 잠정적으로 표시
- 반례를 적극적으로 포함한다

### 챕터-증거 매핑

| 챕터 | 1차 증거 | Deep research |
| --- | --- | --- |
| Ch.1 | OpenClaw anchor, TeamClaws 실패, 생태계 survey | DR-1.1, DR-1.2, DR-1.3 |
| Ch.2 | 모델 교체 실험 (Cluster A) | DR-2.1, DR-2.2, DR-2.3 |
| Ch.3 | Cluster C, D + TeamClaws postmortem + CLI-Anything | DR-3.1~3.4 |
| Ch.4 | **20개 의도적 실패 실험** | DR-4.1~4.4 |
| Ch.5 | Ch.4 결과 분석 + computation 측정 | DR-5.1~5.3 |
| Ch.6 | 반복 실패 패턴 → Fieldkit 설계 | DR-6.1, DR-6.2 |
| Ch.7 | 전체 종합 + self-recovery 초기 실험 | DR-7.1, DR-7.2 |

---

## 8. 실험 프로그램: 20개 의도적 실패 시나리오

> 이 20개 시나리오가 Ch.4의 핵심이며, Ch.5 분석의 입력이다.
> 각 시나리오는 5변수 중 어떤 것을 조작하는지 명시한다.

### 관찰 축별 실험 배치

#### 축 1: 모델을 바꾸면 무엇이 달라지는가 (Ch.2 주력)

| # | 시나리오 | 조작 변수 | 예상 관찰 |
| --- | --- | --- | --- |
| E01 | 동일 GitHub issue triage를 SOTA vs. 소형 모델로 실행 | 모델 | Tool call 패턴, 완료율 차이 |
| E02 | 동일 코드 리뷰를 frontier vs. distilled 모델로 실행 | 모델 | 리뷰 품질, 환각률 차이 |
| E03 | 동일 multi-step CLI 작업을 quantized vs. full 모델로 실행 | 모델 | 중간 단계 실패 지점 비교 |
| E04 | 모델을 mid-run에서 교체 (workflow 중간에 모델 스위칭) | 모델 | Context 연속성 깨짐 패턴 |

#### 축 2: Harness와 surface를 바꾸면 무엇이 달라지는가 (Ch.3, Ch.4)

| # | 시나리오 | 조작 변수 | 예상 관찰 |
| --- | --- | --- | --- |
| E05 | 동일 task를 harness 있음 vs. 없음(raw model)으로 실행 | Harness | 실패 빈도, 복구 가능성 차이 |
| E06 | Memory 보호 해제 상태에서 multi-turn 대화 | Harness | Context leakage 패턴 |
| E07 | Permission boundary를 점진적으로 넓혀가며 실행 | Harness | 안전하지 않은 행동 발생 임계치 |
| E08 | 동일 task를 CLI vs. 다른 surface(API, webhook)로 실행 | Surface | 입출력 안정성 차이 |

#### 축 3: 제약 환경에서 가장 먼저 드러나는 병목 (Ch.4 주력)

| # | 시나리오 | 조작 변수 | 예상 관찰 |
| --- | --- | --- | --- |
| E09 | Token budget을 50%로 제한하여 동일 task 실행 | Resource | 품질 저하 시작 지점 |
| E10 | Token budget을 25%로 제한 | Resource | 완료 불가능 임계치 |
| E11 | VM CPU를 1코어로 제한하고 복합 task 실행 | Resource | Compute saturation 발생 조건 |
| E12 | VM RAM을 512MB로 제한 | Resource | OOM 발생 패턴, agent 충돌 양상 |
| E13 | 네트워크 지연을 인위적으로 추가 (API latency 시뮬레이션) | Resource | Timeout 처리, 재시도 행동 |
| E14 | 동시에 2개 agent를 같은 VM에서 실행 | Resource | 충돌, 리소스 경쟁 (TeamClaws 재현) |

#### 축 4: Operator intervention의 효과 (Ch.5 주력)

| # | 시나리오 | 조작 변수 | 예상 관찰 |
| --- | --- | --- | --- |
| E15 | 동일 실패 상황에서: 개입 없음 vs. 힌트 제공 vs. 직접 수정 | Intervention | 복구 성공률, 소요 시간 비교 |
| E16 | 반복 실패에 규칙 기반 자동 개입 적용 | Intervention | 자동화 가능한 개입의 범위 |
| E17 | Agent에게 자기 상태 보고를 요청 (self-reporting) | Intervention | Agent 자기 인식의 정확도 |

#### 축 5: AgentOps 기능의 harness 내재화 가능성 (Ch.6, Ch.7)

| # | 시나리오 | 조작 변수 | 예상 관찰 |
| --- | --- | --- | --- |
| E18 | Token 사용량 자동 보고 기능을 harness에 추가 | Harness (내재화) | Self-reporting 정확도, overhead |
| E19 | 실패 감지 + 자동 재시도 로직을 harness에 추가 | Harness (내재화) | Self-recovery 성공률 |
| E20 | E18+E19를 결합하여 "mini self-immune" 구성 | Harness (내재화) | 통합 동작 안정성, Agent-2 전환 가능성 |

#### 반례 전용 실험

| # | 시나리오 | 조작 변수 | 예상 관찰 |
| --- | --- | --- | --- |
| E21 | 모호한 task 정의로 실행 (task design 문제 반례) | Task design | Harness/모델과 무관한 실패 |
| E22 | 완벽한 harness + SOTA 모델이지만 VM 1코어 (compute 반례) | Resource | 모든 것이 좋아도 compute가 부족하면 실패 |

### 실험 로그 템플릿

| 필드 | 설명 |
| --- | --- |
| Experiment ID | E01~E22 |
| Date | 실행 날짜 |
| Task | 구체적 task 설명 |
| 조작 변수 | 5변수 중 무엇을 조작했는가 |
| 통제 변수 | 나머지 변수의 고정 조건 |
| Model | 모델명 + provider |
| Harness config | Harness 구성 상세 |
| Surface | CLI / API / 기타 |
| Compute environment | VM 사양, 티어, CPU/RAM |
| Tool usage | 어떤 tool, 몇 회 |
| Success / failure | 결과 |
| Failure type | 분류 |
| Primary bottleneck | 5변수 중 어떤 것이 1차 병목이었는가 |
| Balloon effect | 풍선 효과 관찰 여부 |
| Token usage | 입출력 token |
| Human intervention | 개입 여부, 종류, 효과 |
| Recovery | 시도된 복구, 성공 여부 |
| Lesson learned | 핵심 교훈 |
| Target chapter | 사용될 챕터 |
| Experimenter | 실험자 (A, B, C 중) |
| Cross-validation | 교차검증 실험자 |

---

## 9. 팀 설계와 교차검증

### 역할

| 역할 | 담당 | 핵심 책임 |
| --- | --- | --- |
| **Lead author / Concept owner** | Kiwon | 논제, 챕터 논리, 최종 voice, Ch.1/3/6/7 primary writing |
| **Experimenter A** | TBD | E01~E08 primary, E09~E14 cross-validation |
| **Experimenter B** | TBD | E09~E16 primary, E01~E08 cross-validation |
| **Experimenter C** | TBD | E17~E22 primary, E15~E16 cross-validation |

### 교차검증 설계

모든 핵심 실험은 primary experimenter가 실행하고, 다른 experimenter가 교차검증한다.
교차검증은 동일 조건에서 재현 또는 다른 조건에서 비교 실행으로 수행한다.

```
Experimenter A: E01~E08 실행 → Experimenter B가 E03, E05 교차검증
Experimenter B: E09~E16 실행 → Experimenter A가 E11, E14 교차검증
Experimenter C: E17~E22 실행 → Experimenter B가 E19, E20 교차검증
```

### 팀 성장 원칙

이 실험 과정은 팀원들이 AgentOps와 harness engineering에 대해 알아가며 성장하는 과정이다.
실험자들과 디베이트하면서 성장해나가는 것이 이 프로젝트의 부가 가치이다.

---

## 10. 태스크 기반 일정

> 주차별이 아니라 **해야 하는 일 중심**으로 서술한다.

### Phase 1: 기반 구축

**해야 하는 일:**
- 제목, 부제, 핵심 탐구 질문 확정
- 7챕터 구조 동결
- GitHub repo 생성, 폴더 구조 배포
- 실험 로깅 템플릿 생성 + OpenRouter 환경 셋업
- 팀원 3명 역할 확정, 교차검증 배정
- 20개 실험 시나리오 최종 확정
- Deep research DR-1.1~1.3 실행

**산출물:** 프로젝트 브리프, 챕터 맵, 실험 시트, repo 초기 커밋

---

### Phase 2: 스냅샷과 모델 관찰 (Ch.1, Ch.2)

**해야 하는 일:**
- OpenClaw 생태계 deep research (DR-1.1) 완료
- OpenClaw anchor notes + TeamClaws 실패 기록 정리
- Chapter 1 초고 작성
- 모델 교체 실험 E01~E04 실행 (Experimenter A primary)
- Deep research DR-2.1~2.3 실행
- Chapter 2 초고 작성
- E03 교차검증 (Experimenter B)

**산출물:** Ch.1 draft, Ch.2 draft, E01~E04 로그, 생태계 스냅샷

---

### Phase 3: 정의 프레임 (Ch.3)

**해야 하는 일:**
- Deep research DR-3.1~3.4 실행
- Harness engineering 정의 + AgentOps 정의 작성
- TeamClaws/PicoClaw 사후 분석 (반례 2 포함)
- CLI-Anything HARNESS.md 분석
- Harness 다이어그램 제작
- E05~E08 실행 (Experimenter A primary), E05 교차검증 (Experimenter B)
- Chapter 3 초고 작성

**산출물:** Ch.3 draft, harness diagram, E05~E08 로그

---

### Phase 4: 의도적 실패 실험 (Ch.4) — 이 책의 무게중심

**해야 하는 일:**
- Deep research DR-4.1~4.4 실행
- E09~E16 실행 (Experimenter B primary)
- E17~E22 실행 (Experimenter C primary)
- 교차검증: A→E11/E14, B→E19/E20
- 반례 실험 E21, E22 실행
- 풍선 효과 관찰 및 기록
- Chapter 4 초고 작성

**산출물:** Ch.4 draft, E09~E22 전체 로그, 풍선 효과 기록

---

### Phase 5: 실험 분석과 AgentOps 실무 (Ch.5)

**해야 하는 일:**
- Deep research DR-5.1~5.3 실행
- 20개 실험 결과 종합 분석
- 패턴 추출: 반복 실패 유형 분류
- Computation 요구사항 정리
- 1차 병목 변수 분석표 작성
- Harness engineering skill set 정리
- 학술적 확장 가능성 정리
- Chapter 5 초고 작성

**산출물:** Ch.5 draft, 패턴 분류표, computation 요구사항표, 학술 확장 노트

---

### Phase 6: Fieldkit과 미래 방향 (Ch.6, Ch.7)

**해야 하는 일:**
- Deep research DR-6.1~6.2, DR-7.1~7.2 실행
- 반복 실패 패턴 → Fieldkit 도구 후보 매핑
- Operational Fieldkit 설계 노트 작성
- Chapter 6 초고 작성
- 전체 교훈 종합, self-immune system 초기 서술
- Agent-1→2 전환 논증
- Chapter 7 초고 작성

**산출물:** Ch.6 draft, Ch.7 draft, Fieldkit 설계 노트

---

### Phase 7: 통합과 Beta

**해야 하는 일:**
- 챕터 간 용어 통일
- 5변수 프레임워크의 일관된 적용 확인
- 반례가 적절히 포함되어 있는지 확인
- 모든 챕터를 성공 기준에 대조
- 서문 작성
- Beta 원고 패키지 준비

**산출물:** Beta manuscript, 개정 챕터 맵, 그림/표 목록

---

## 11. Deep Research 프롬프트 종합

| ID | 챕터 | 프롬프트 |
| --- | --- | --- |
| DR-1.1 | Ch.1 | "OpenClaw를 벤치마크하거나 대안으로 등장한 open-source personal AI agent 프로젝트들을 2025-2026년 GitHub에서 전수 조사하라. 각 프로젝트의 아키텍처, 차별점, star 수, 활성도를 비교하라." |
| DR-1.2 | Ch.1 | "CLI 이외에 agent-first product surface로 시도되고 있는 형태들을 조사하라. A2UI, Canvas, voice-first, GUI automation 등. 각각의 장단점과 현재 성숙도를 분석하라." |
| DR-1.3 | Ch.1 | "Chip Huyen의 AI Engineering(2025)이 출간 이후 AI engineering 커뮤니티에 미친 영향과 후속 논의를 조사하라. 특히 agent 관련 내용의 반응." |
| DR-2.1 | Ch.2 | "LLM을 agent로 사용할 때 모델별 행동 차이를 벤치마크한 기존 연구나 프로젝트를 조사하라. SWE-bench, WebArena, ToolBench 등의 agent 벤치마크에서 모델별 결과 차이." |
| DR-2.2 | Ch.2 | "OpenRouter의 모델 routing 메커니즘, 지원 모델 목록, pricing, 그리고 agent workflow에서의 사용 사례를 조사하라." |
| DR-2.3 | Ch.2 | "Model distillation과 quantization이 LLM의 tool call 안정성, function calling 정확도에 미치는 영향에 대한 기존 연구를 조사하라." |
| DR-3.1 | Ch.3 | "Agent 시스템에서 guardrails, scaffolding, harness, orchestration layer라는 용어가 각각 어떻게 사용되고 있는지 2025-2026년 블로그, 논문, 프레임워크 문서에서 조사하라." |
| DR-3.2 | Ch.3 | "HKUDS CLI-Anything 프로젝트의 HARNESS.md를 분석하라. Harness 정의, 구현 원칙, 테스트 방법론을 요약하고 이 책의 harness 정의와 비교하라." |
| DR-3.3 | Ch.3 | "AgentOps 관련 기존 도구와 프레임워크를 조사하라: LangSmith, Weights & Biases Weave, AgentOps.ai, Helicone, Braintrust 등. 각각이 다루는 범위와 한계." |
| DR-3.4 | Ch.3 | "AI agent runtime 실패를 분류하는 기존 taxonomy가 있는지 조사하라. 없다면 관련 분야(distributed systems, chaos engineering)의 실패 분류를 참고하라." |
| DR-4.1 | Ch.4 | "Chaos engineering 원리(Netflix Chaos Monkey 등)를 AI agent 시스템에 적용한 사례나 연구를 조사하라. 의도적 실패 주입의 방법론." |
| DR-4.2 | Ch.4 | "Google Cloud 무료 티어의 구체적 제약 사항 (CPU, RAM, 네트워크, 시간 제한)과 해당 환경에서 agent를 운영할 때 겪는 실패 패턴을 조사하라." |
| DR-4.3 | Ch.4 | "Agent 시스템에서 token budget을 관리하고 최적화하는 전략에 대한 기존 연구나 실무 사례를 조사하라." |
| DR-4.4 | Ch.4 | "LLM 기반 agent runtime의 CPU/RAM 요구사항을 벤치마크한 자료를 조사하라. 특히 tool use가 활발한 agent의 리소스 소비 패턴." |
| DR-5.1 | Ch.5 | "Agent 시스템의 실패 패턴을 분석하는 방법론을 조사하라. Root cause analysis, failure mode analysis 등 기존 방법론의 agent 적용." |
| DR-5.2 | Ch.5 | "Agent 배포의 compute cost 최적화 사례를 조사하라. 특히 API 호출 비용, inference 비용, 인프라 비용의 trade-off." |
| DR-5.3 | Ch.5 | "VM 환경에서 LLM 기반 agent의 리소스 관리 방법을 조사하라. cgroup, container, resource limits 등." |
| DR-6.1 | Ch.6 | "개발자용 CLI 도구의 성공적 설계 패턴을 조사하라. 특히 self-describing, composable, JSON output 등의 원칙." |
| DR-6.2 | Ch.6 | "Agent에 능력을 점진적으로 주입하는 접근 방법에 대한 기존 연구를 조사하라. Skill injection, capability bootstrapping 등." |
| DR-7.1 | Ch.7 | "Self-healing 또는 self-recovering AI agent 아키텍처에 대한 기존 연구를 조사하라. 자동 복구 메커니즘의 설계 패턴." |
| DR-7.2 | Ch.7 | "배포된 agent 시스템에서의 continuous learning 사례를 조사하라. Online learning, feedback loop, 지속적 개선 메커니즘." |

---

## 12. 성공 기준

### 책 수준

이 책이 성공이면 독자가:

1. 5변수 프레임워크로 agent 시스템을 분석하고, 어떤 조건에서 무엇이 1차 병목인지 식별할 수 있다
2. AgentOps를 profession으로 이해하고 구체적 실무를 설명할 수 있다
3. Harness를 설계하는 방법을 이해하고 first-pass harness를 구축할 수 있다
4. 의도적 실패 실험을 자신의 환경에서 설계하고 실행할 수 있다
5. 실험 결과에서 학술적 확장 가능성을 식별할 수 있다
6. Operational Fieldkit의 점진적 개발 전략을 이해한다
7. Agent에 AgentOps 기능을 주입하는 것의 의미와 초기 접근법을 이해한다

### Beta 성공 기준

- 안정적인 7챕터 구조
- 20개 실험 중 최소 15개 완료 및 문서화
- 교차검증 최소 6건 완료
- 5변수 프레임워크가 전 챕터에 일관 적용
- 반례 2건 이상 포함
- 학술 확장 가능성 최소 3건 식별

---

## 13. 핵심 리스크와 통제

| 리스크 | 통제 |
| --- | --- |
| 이원론에 빠짐 (모델 vs. harness) | 5변수 프레임워크를 전 챕터에 적용, 반례 포함 |
| 결론을 미리 정하고 증거 끼워맞춤 | 관찰 원칙: 결과가 예상과 다르면 결과를 기록 |
| 실험 재현 불가 | 교차검증 설계, 실험 로그 상세 기록 |
| Ch.4-5가 데이터 부족 | 20개 시나리오 + 교차검증으로 충분한 양 확보 |
| 학문적 해석에 빠짐 | 스냅샷 원칙: 기록하되 과도하게 해석하지 않음 |
| 팀 동기화 실패 | 교차검증이 자연스러운 sync 포인트 역할 |
| Fieldkit을 한 번에 완성하려 함 | 점진적 업데이트 원칙 명시 |

---

## 14. 부록 제안

- **Appendix A:** 실험 로그 템플릿 (v4: 5변수, 교차검증 포함)
- **Appendix B:** 용어 사전
- **Appendix C:** 다이어그램 (5변수 상호작용, AgentOps→Harness→Agent 내재화)
- **Appendix D:** 참조 프로젝트 가이드
- **Appendix E:** Deep research 프롬프트 전체 목록

---

## 15. 즉시 다음 행동

### 오늘
- 핵심 탐구 질문 확정
- 7챕터 구조 확인
- 20개 실험 시나리오 최종 검토
- GitHub repo 생성

### 이번 주
- 팀원 3명 확정, 역할 배정, 교차검증 배치
- OpenRouter 실험 환경 셋업
- DR-1.1 실행 (OpenClaw 생태계 조사)
- Chapter 1 아웃라인 작성

### 2주 이내
- Ch.1 draft + 생태계 스냅샷
- E01~E04 실행 + 1건 교차검증
- Ch.2 draft 시작

---

## 16. 마무리 선언

이 책은 교리집이 아니라 실험서이다.

"모델이 중요한가, harness가 중요한가"라는 이원론을 넘어서,
**"어떤 조건에서 무엇이 1차 병목이 되는가"**를 5개 변수의 상호작용 속에서 관찰하고 측정한다.

20개의 의도적 실패 실험을 통해 agent 시스템이 어디서 깨지는지를 기록하고,
그 기록에서 harness engineering과 AgentOps의 윤곽을 그린다.

그리고 그 교훈을 Operational Fieldkit으로 점진적으로 도구화하여,
궁극적으로 agent 자체가 self-immune system을 갖추는 경로를 탐색한다.

이 스냅샷이 다음 단계의 profoundation이 된다.
