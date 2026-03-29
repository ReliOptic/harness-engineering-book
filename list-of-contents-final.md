# List of Contents — 최종본 v4

> **주의**: 이 문서는 polishing 단계의 **목표 구조** (9챕터, 4 Parts)입니다.
> 현재 작업 구조는 **7챕터** (writing-plan.md v5 + chapter-map.md 기준).
> Beta 완성 후 v4 구조 채택 여부를 결정합니다. (2026-03-29 결정)

## *Harness Engineering and AgentOps*
### *Observing What Makes Agents Work — and What Breaks Them*

> 2026년 상반기, agent runtime 생태계의 스냅샷이자 실험서.
> 산업계가 축적한 실무 지식을 집대성하고, 제약 환경에서 실험으로 검증한 기록.
> **9개 챕터 + Preface + Appendices** (목표 구조)

---

## 전체 구조

```
Preface   왜 이 책이 필요한가

Part I — Agent Runtime의 현장
  Ch.1    지금 무슨 일이 일어나고 있는가
  Ch.2    Agent의 작동 원리와 실패 구조
  Ch.3    5변수 프레임워크: 병목은 어디에서 오는가

Part II — 변수의 관찰
  Ch.4    Agent가 모델로부터 무엇을 물려받는가
  Ch.5    Harness Engineering과 AgentOps의 정의

Part III — 의도적 실패 실험
  Ch.6    22개 시나리오: 무엇이 어떤 조건에서 깨지는가
  Ch.7    실험 결과에서 배운 것

Part IV — Operational Compiler와 Self-Immune
  Ch.8    관찰에서 도구로: Operational Compiler
  Ch.9    Harness에서 Agent로: Self-Immune System을 향하여
```

**v3 → v4 구조 변경 사유**:
- Part 이름을 이 책의 언어(runtime, 변수, 실험, Operational Compiler)로 교체
- 구 Ch.2("개념 지도")와 구 Ch.3("일의 구조")의 중복 제거 → Ch.2(작동 원리+실패), Ch.3(5변수+산업 맥락)으로 재배치
- 5변수 프레임워크를 Ch.3의 중심으로 승격 — 산업별 사례는 5변수의 예시로 종속

---

## Preface — 왜 이 책이 필요한가

이 책의 질문, 독자, 그리고 한계를 밝힌다.

- 이 책이 다루는 질문: "어떤 조건에서 무엇이 agent 운영의 1차 병목이 되는가?"
- 이 책이 아닌 것: 교리집도, 튜토리얼도, 벤더 비교표도 아니다
- OpenAI의 harness engineering 연구(2026)를 출발점으로, Chip Huyen의 *AI Engineering*(2025)이 다룬 application layer의 다음 레이어를 다룬다
- 이 책의 독자:
  - **Primary**: Agent runtime을 직접 다루는 builder-operator
  - **확장**: 제품, 인프라, 전략, 마케팅, HR, 재무, 데이터, 창업 — 각자의 본업에서 AI로 일의 구조를 다시 설계하려는 실무자
  - Ch.2–3이 두 독자를 연결한다. Technical reader에게는 용어 정렬, 실무 독자에게는 개념 진입로. Ch.4 이후에서 합류한다
- 이 책을 읽는 법

**앵커 레퍼런스**:
- OpenAI, *Harness Engineering: Leveraging Codex in an Agent-First World* (2026)
- Chip Huyen, *AI Engineering: Building Applications with Foundation Models* (O'Reilly, 2025)

---

# Part I — Agent Runtime의 현장

---

## Ch.1 — 지금 무슨 일이 일어나고 있는가

**한 줄**: 2026년 상반기, agent runtime 생태계의 현재 풍경을 기록한다.

### §1. Agent 운영의 현재 풍경

CLI-first surface의 부상. Agent-friendly interface가 아직 표준화되지 않은 이유. 2026년 상반기라는 시간 좌표를 명시한다.

**앵커**: Claude Code (Anthropic), Cursor, Windsurf

### §2. Agent framework 생태계: 무엇이 만들어지고 있는가

산업계가 agent 운영을 위해 만든 프레임워크들의 전수 조사.

**앵커 프로젝트** (GitHub stars, 2026년 3월):
- LangChain (~97k) / LangGraph (~25k), AutoGen (Microsoft, ~56k), CrewAI (~44k), DSPy (Stanford, ~33k), LlamaIndex (~30k), Semantic Kernel (Microsoft, ~27k), smolagents (HF, ~26k), Google ADK (~16k), OpenAI Agents SDK (~19k), Pydantic AI (~10k)

### §3. Agent coding tool의 부상

코드를 읽고, 수정하고, 테스트하는 agent가 가장 먼저 실용화된 영역.

**앵커 프로젝트**: Gemini CLI (~96k), OpenHands (~69k), Codex CLI (~67k), Cline (~58k), Aider (~39k), Continue (~30k), SWE-agent (~19k), Claude Code, Cursor
**앵커 논문**: Jimenez et al., *SWE-bench* (ICLR 2024 Oral, ~500 citations)

### §4. 이 책의 좌표: *AI Engineering* 이후의 질문

Chip Huyen의 *AI Engineering*이 foundation model 위 application layer를 다뤘다면, 이 책은 agent runtime의 운영 구조를 다룬다.

**학습 결과**: 2026년 상반기 agent 생태계의 구조를 파악하고, 이 책이 다루는 영역의 좌표를 이해한다.

---

## Ch.2 — Agent의 작동 원리와 실패 구조

**한 줄**: Agent를 구성하는 요소, 작동 루프, 그리고 전통 소프트웨어와 근본적으로 다른 실패 구조를 정의한다.

> 이 챕터는 기존 자동화 경험을 가진 실무자가 agent의 구조적 차이를 이해하는 진입로이자, technical reader가 이 책의 용어를 정렬하는 기준점이다.

### §1. 도구, 자동화, agent — 무엇이 다른가

RPA, 매크로, 챗봇, copilot — 실무자가 이미 경험한 자동화 계층과 agent의 구조적 차이. "Agent"라는 단어가 산업에서 남용되는 현실을 정리하고, 이 책의 조작적 정의를 제시한다.

| 단계 | 사용자 역할 | 실패 시 | 사례 |
|------|-------------|---------|------|
| Chatbot | 질문자 | 다시 질문 | ChatGPT 대화 |
| Copilot | 감독자 | 제안 무시 | GitHub Copilot, Cursor Tab |
| Agent | 위임자 | 결과 확인 후 수정 | Claude Code, Devin |
| Autonomous | 설계자 | 사후 감사 | 아직 신뢰할 수 없는 영역 |

### §2. Agent의 구성 요소: 모델, 도구, 메모리, 행동 루프

모델은 판단 엔진, 도구(tool)는 행동 수단, 메모리는 맥락 유지, 행동 루프(reasoning-acting loop)는 이 셋을 연결하는 운영 구조다.

**앵커 논문**:
- Yao et al., *ReAct: Synergizing Reasoning and Acting in Language Models* (ICLR 2023, ~5,250 citations) — 행동 루프의 원형
- Schick et al., *Toolformer* (NeurIPS 2023, ~2,600 citations) — 도구 사용 학습
- Park et al., *Generative Agents* (UIST 2023, ~3,000 citations) — 관찰 → 반성 → 계획의 메모리 구조

### §3. Tool call의 해부 — agent의 "손"이 작동하는 방식

API 호출, 파일 읽기/쓰기, 웹 검색, 코드 실행. Tool call이 실패할 때 일어나는 일, 그리고 그 실패가 왜 조용한지.

**앵커**: Qin et al., *ToolLLM* (ICLR 2024, ~500 citations), Patil et al., *Gorilla* (NeurIPS 2024, ~500 citations), Berkeley Function Calling Leaderboard

### §4. Agent가 실패하는 방식 — crash가 아니라 drift

Agent의 실패는 전통 소프트웨어와 다르다. 에러를 던지지 않고, 확신 있게 틀린 방향으로 진행한다.

세 가지 전형적 실패 패턴:
1. **목표 표류**(goal drift) — 장기 task에서 초기 목표를 조용히 잃어버린다
2. **맥락 오염**(context contamination) — 이전 대화의 잔재가 다음 판단을 오염시킨다
3. **도구 호출 환각**(tool call hallucination) — 존재하지 않는 API를 확신 있게 호출한다

> **이 절의 역할**: 실패 패턴을 소개하되, 정량적 증거는 Ch.6–7의 실험에서 제시한다. 여기서는 패턴의 구조만 정의한다.

### §5. 비결정성, 불투명성, 통제의 연속체 — agent가 전통 소프트웨어와 다른 세 가지

1. **비결정성**: 동일한 입력에 다른 출력 — 재현이 보장되지 않는 운영 전제
2. **실패의 불투명성**: 에러 코드 없이 실패 — 실패 감지 자체가 설계 대상
3. **통제의 연속체**: on/off가 아니라 permission boundary를 점진적으로 조절

이 세 가지가 "agent를 만드는 것"과 "agent를 운영하는 것" 사이의 간극을 만든다. 그 간극에 harness engineering이 있다. Ch.5에서 정식 정의한다.

**학습 결과**: agent의 구성 요소와 작동 루프를 이해하고, agent의 실패가 전통 소프트웨어와 구조적으로 다른 점을 설명할 수 있다.

---

## Ch.3 — 5변수 프레임워크: 병목은 어디에서 오는가

**한 줄**: Agent runtime의 병목을 만드는 5개 변수를 정의하고, 각 변수가 산업 현장에서 어떤 형태로 나타나는지 관찰한다.

> 5변수 프레임워크는 이 책의 척추다. Ch.4–9의 모든 실험, 분석, 도구화가 이 구조 위에서 움직인다.

### §1. 5변수의 정의: 모델, harness, surface, intervention, compute

"모델 vs. harness" 이원론이 아니라, 어떤 조건에서 무엇이 1차 병목이 되는가를 비교하기 위한 실험 분석 구조.

| 변수 | 설명 | 실무자의 언어 |
|------|------|---------------|
| 모델 | 판단 엔진의 역량 | "어떤 AI를 쓸 것인가" |
| Harness | 운영 경계와 보호 구조 | "agent가 무엇을 할 수 있고 없는가" |
| Product surface | 사용자-agent 인터페이스 | "agent를 어떤 형태로 만나는가" |
| Operator intervention | 인간의 개입 패턴 | "언제 내가 끼어들어야 하는가" |
| Compute | 자원 예산 | "얼마를 쓸 수 있는가" |

### §2. Surface가 병목이 되는 조건

동일한 agent라도 CLI에서는 복잡한 multi-step task를 수행하지만, 채팅 인터페이스에서는 단순 Q&A에 머무는 이유. Surface가 정보 밀도와 피드백 루프의 품질을 결정한다.

**앵커**: Claude Code / Cursor / Cline — 동일 모델, 다른 surface, 다른 결과
**앵커 논문**: WebArena (Zhou et al., ICLR 2024, ~400 citations) — 웹 surface에서 성능 14%

### §3. Operator가 병목이 되는 조건

Agent를 "사용하는" 것이 아니라 "운영하는" 것이라는 관점의 전환. Operator는 task를 위임하고, 결과를 검증하고, 실패 시 개입하고, 개입 패턴을 축적하여 운영 규칙을 갱신하는 사람이다.

이것은 새로운 직무가 아니라, 기존 직무의 확장이다 — 물류 전략기획자는 FMS agent의 operator가 되고, HR 컨설턴트는 보상 분석 agent의 operator가 된다.

### §4. 5변수가 산업 현장에서 만나는 방식

각 산업 영역에서 5변수 중 어떤 것이 1차 병목으로 먼저 드러나는가. Agent가 가장 먼저 적용되는 업무의 공통점: 반복적이고, 구조화되어 있으며, 실패해도 피해가 제한적인 task.

| 영역 | 1차 병목이 되기 쉬운 변수 | Agent가 먼저 들어가는 곳 |
|------|---------------------------|--------------------------|
| 제품·UX·PM | Surface, Intervention | 요구사항 정리, 프로토타이핑 |
| 인프라·클라우드 | Compute, Harness | 모니터링 자동화, 장애 탐지 |
| 데이터·자동화 | 모델, Compute | 전처리, 리포팅, 파이프라인 |
| 전략·사업개발 | Intervention, Surface | 시장 조사, 경쟁사 분석 |
| 마케팅·GTM | Surface, 모델 | 콘텐츠 생성, 캠페인 자동화 |
| HR·조직 | Intervention, Harness | 채용 스크리닝, 보상 분석 |
| 재무·투자 | Harness, Intervention | 데이터 취합, 시나리오 분석 |
| 창업·도메인 | Compute, Surface | MVP 프로토타이핑 |

**앵커**: Shen et al., *HuggingGPT* (NeurIPS 2023, ~1,200 citations), *Agentic AI: Architectures, Taxonomies, and Evaluation* (2025)

### §5. "만드는 것"에서 "운영하는 것"으로 — 간극의 구조

프로토타입을 빠르게 만드는 것과 지속적으로 운영하는 것 사이의 간극. 이 간극의 정체는 Ch.2에서 정의한 세 가지 구조적 차이(비결정성, 불투명성, 통제의 연속체)이며, 이것을 관리하는 구조가 harness다.

독자의 현재 위치: "ChatGPT/Claude로 업무를 자동화하고 있다"
이 책이 데려가는 곳: "5변수 중 어디가 병목인지 식별하고, 그 병목을 관리하는 운영 구조를 설계할 수 있다"

### §6. Agent-1에서 Agent-5까지: 성숙도 스펙트럼

| 레벨 | 이름 | 특징 | 현재 위치 |
|------|------|------|-----------|
| Agent-1 | Early Agent | Tool-using, 취약, proactivity 결여 | ← 대부분 여기 |
| Agent-2 | Continuous Learner | Self-immune, 자발 복구 | 이 책의 목표 |
| Agent-3 | Domain Expert | 한정 영역 고속 역량 | 미래 |
| Agent-4 | Superhuman | 인간 실무자 초과 | 미래 |
| Agent-5 | Collective | 조직 규모 조율 | 미래 |

이 책이 추적하는 질문: Agent-1 → Agent-2 전환은 어떤 조건에서 가능한가.

**학습 결과**: 5변수 프레임워크로 자신의 산업에서 agent 병목을 식별할 수 있다. "왜 harness engineering이 필요한가"를 자신의 업무 맥락에서 설명할 수 있다.

---

# Part II — 변수의 관찰

---

## Ch.4 — Agent가 모델로부터 무엇을 물려받는가

**한 줄**: 5변수 중 "모델" 변수를 격리하여 관찰한다. 모델별 행동 차이와 역량의 비선형적 급락.

### §1. 물려받는 경향: reasoning, tool use, consistency, confidence

**앵커**: Wei et al., *Chain-of-Thought* (NeurIPS 2022, ~14,400 citations), Schick et al., *Toolformer* (~2,600 citations)

### §2. 모델 역량의 연속 스펙트럼으로서의 측정

Tool call accuracy, instruction following rate, multi-step reasoning depth, context utilization efficiency를 복합적으로 측정하여 모델을 연속 스펙트럼 위에 배치하는 방법.

**앵커 벤치마크**: GAIA (~390 citations), AgentBench (ICLR 2024, ~400 citations), IFEval, τ-bench, Berkeley Function Calling Leaderboard

### §3. 역량 절벽 — task completion rate의 비선형적 급락

모델 역량이 특정 임계치 이하로 떨어질 때, 작업 완료율이 급격히 붕괴하는 현상. Task 유형별로 절벽의 위치가 다르다.

### §4. 양자화가 agent 역량을 깎는 비율

FP16 → Q8 → Q4 → Q2 경로에서 tool call 안정성이 벤치마크 점수보다 먼저 훼손되는 패턴.

**앵커**: llama.cpp / ollama / vLLM / Dettmers et al., *GPTQ* (2022)

### §5. 증류 모델의 agent viability

동일 parameter budget에서 증류와 양자화가 agent 운용 가능성을 다르게 깎는 패턴.

### §6. Workflow 중간 모델 교체의 context 연속성 붕괴

### §7. "모델"이 1차 병목이 되는 조건 — 그리고 아닌 조건

**학습 결과**: 모델 기인의 취약성을 식별하고, "이 모델로 이 task는 되는가?"를 판단하는 근거를 갖는다.

---

## Ch.5 — Harness Engineering과 AgentOps의 정의

**한 줄**: 5변수 중 "harness"와 "intervention" 변수를 정의하고, 실험 프레임을 설정한다.

### §1. Harness engineering이란 무엇인가 — operational envelope의 정의

**앵커**: OpenAI *Harness Engineering* (2026) — Context Engineering, Architectural Constraints, Entropy Management

### §2. 보호와 enablement의 이중 구조

### §3. Harness를 guardrails, scaffolding, orchestration과 구분

**앵커**: Guardrails AI (~7k stars), NeMo Guardrails (~4k stars), LangGraph (~25k stars)
**앵커 논문**: MRKL Systems (Karpas et al., 2022, ~450 citations)

### §4. 실패 예산 재할당 — harness 효과의 프레이밍

Harness는 실패를 제거하지 않는다. 실패의 성격을 바꾼다.

### §5. Harness의 운영 비용 — overhead ratio

이 비율이 너무 높으면 harness 자체가 1차 병목이 된다.

### §6. AgentOps란 무엇인가 — profession으로서의 정의

**앵커**: Langfuse (~21k stars), AgentOps (~5k stars), Arize Phoenix (~8k stars), Helicone (~4.4k stars), LangSmith
**앵커 논문**: *AgentOps: Enabling Observability of LLM Agents* (arXiv, 2024), *Design Principles for LLM Observability* (CHI 2025)

### §7. 산업계의 AgentOps 실무: 무엇이 이미 도구화되었는가

관찰, 비용 추적, 평가, 실패 감지가 이미 도구로 존재한다. 아직 도구화되지 않은 영역이 이 책의 실험이 탐색하는 공간이다.

### §8. Ch.6 실험 프레임 설정 — 무엇을 의도적으로 실패시킬 것인가

**앵커**: Nosek et al., *The Preregistration Revolution* (PNAS, 2018)

**학습 결과**: harness와 AgentOps를 정의하고, 실패 예산 재할당 프레임으로 harness 효과를 설명할 수 있다.

---

# Part III — 의도적 실패 실험

---

## Ch.6 — 22개 시나리오: 무엇이 어떤 조건에서 깨지는가

**한 줄**: 5변수를 격리 조작하며 어떤 변수가 어떤 조건에서 1차 병목이 되는가를 측정한다.

### §1. 실험 설계 원칙

**앵커**: Basiri et al., *Chaos Engineering* (IEEE Software, 2016) / Rosenthal et al., *Chaos Engineering* (O'Reilly, 2020)

### §2. 1막 (E01–E04): 모델 변수 조작
### §3. 2막 (E05–E08): Harness와 Surface 변수 조작
### §4. 3막 (E09–E14): 제약 환경의 병목

**앵커**: MetaGPT (ICLR 2024, ~1,000 citations), AutoGen (COLM 2024, ~1,500 citations), ChatDev (ACL 2024, ~464 citations), CAMEL (NeurIPS 2023, ~894 citations)

### §5. 4막 (E15–E17): Operator intervention의 효과
### §6. 5막 (E18–E20): AgentOps 내재화

**앵커**: Shinn et al., *Reflexion* (NeurIPS 2023, ~443 citations), Madaan et al., *Self-Refine* (NeurIPS 2023), *PALADIN* (2025) — 복구율 32.76% → 89.68%

### §7. 반례 (E21–E22): 이 프레임워크가 설명하지 못하는 것

**학습 결과**: 의도적 실패 실험을 설계하고 실행할 수 있다.

---

## Ch.7 — 실험 결과에서 배운 것

**한 줄**: 실험실 지표 → 운영 지표 → 비용 지표의 3단계 번역.

### §1. 22개 실험 결과 종합: 5변수별 병목 분포
### §2. 실패 예산 재할당의 정량 분석

**앵커 논문**:
- Cemri et al., *Why Do Multi-Agent LLM Systems Fail?* (NeurIPS 2025) — 14개 failure mode, 41–86.7% 실패율
- Microsoft, *Taxonomy of Failure Mode in Agentic AI Systems* (2025)
- Winston et al., *Failures in Tool-Augmented LLMs* (AST 2025)
- *Failure Modes in LLM Systems* (arXiv, 2025) — 15개 hidden failure mode

> **Ch.2에서 소개한 실패 패턴(goal drift, context contamination, tool call hallucination)을 이 절에서 정량적으로 검증한다.**

### §3. 운영 지표로의 번역: 평균 복구 시간과 인간 에스컬레이션 비율
### §4. 비용 지표로의 번역: 총비용과 최적 harness overhead

**앵커**: *Survey on Efficient Inference for LLMs* (arXiv, 2024)

### §5. Component ablation: 무엇이 얼마나 기여하는가
### §6. Token efficiency를 운영 규율로

**앵커**: OpenRouter, Helicone (~4.4k stars)

### §7. Scaling과 temporal stability
### §8. 학술적 확장 가능성 — exploratory 발견 목록

**학습 결과**: 3단계 지표 번역 체계를 이해하고, component ablation에서 Operational Compiler 구성 우선순위를 도출할 수 있다.

---

# Part IV — Operational Compiler와 Self-Immune

---

## Ch.8 — 관찰에서 도구로: Operational Compiler

**한 줄**: 반복 실패 패턴을 실행 가능한 운영 규칙으로 컴파일한다.

### §1. 반복 실패 패턴에서 도구화 후보 식별
### §2. Operational Compiler의 설계 원칙
### §3. 점진적 구성: Pareto frontier를 따라 이동하는 전략
### §4. Skill로 쓸 수 있는 능력의 극대화

### §5. Harness configuration의 산업적 수렴

서로 다른 프로젝트들이 독립적으로 유사한 harness pattern에 수렴한 현상.

| 파일 | 프로젝트 | 역할 |
|------|----------|------|
| `CLAUDE.md` | Anthropic Claude Code | 프로젝트 수준 agent 지침 |
| `AGENTS.md` | OpenAI Codex CLI | 디렉토리 수준 agent 규칙 |
| `GEMINI.md` | Google Gemini CLI | 프로젝트 수준 agent 지침 |
| `.cursorrules` | Cursor | IDE-native harness |
| `.windsurfrules` | Windsurf | IDE-native harness |
| `copilot-instructions.md` | GitHub Copilot | copilot 행동 지침 |

**앵커**: everything-claude-code (~84k stars), awesome-cursorrules (~10k stars)

### §6. 도구화해야 할 것과 도구화하면 안 되는 것

**학습 결과**: Operational Compiler 구성 우선순위를 결정하고, 점진적 업데이트 전략을 설계할 수 있다.

---

## Ch.9 — Harness에서 Agent로: Self-Immune System을 향하여

**한 줄**: Agent-1에서 Agent-2로의 전환 조건.

### §1. 실험이 남긴 것
### §2. 현 세대 harness가 풀 수 없는 문제
### §3. AgentOps → Harness → Agent 내재화: 점진적 경로

**앵커**: ReAct (~5,250 citations), Reflexion (~443 citations), Voyager (~1,100 citations), *Survey on Self-Evolving Agents* (2025)

### §4. Self-immune system 초기 설계

**앵커**: R-Guard (ICLR 2025), AgentSpec (ICSE 2026), ToolSafe (2026)

### §5. Self-immune의 재귀적 한계
### §6. 모델 역량 증가가 harness의 역할을 전환시키는 조건
### §7. Agent-1에서 Agent-2로: 전환 조건의 정식화
### §8. 이 책 이후: 미해결 질문들

**앵커**: Generative Agents (Park et al., ~3,000 citations), Xi et al., *Rise and Potential of LLM-Based Agents* (~461 citations)

### §9. 집필 과정의 메타 관찰

**학습 결과**: self-immune system의 조작적 정의와 재귀적 한계를 이해하고, Agent-1 → Agent-2 전환 조건을 설명할 수 있다.

---

## Appendices

| Appendix | 내용 |
|----------|------|
| A — 실험 로그 템플릿 | 5변수, 교차검증, pre-registration 포함 v4 |
| B — 용어 사전 | 전체 용어의 조작적 정의, 약자 없이 풀네임 |
| C — Figure 목록과 해석 가이드 | 모든 Figure의 읽는 법과 재현 조건 |
| D — 참조 프로젝트 목록 | GitHub 프로젝트 전체 (stars, URL, 인용 맥락) |
| E — Deep Research 프롬프트 | DR-1.1 ~ DR-7.2 |
| F — 참고문헌 | 논문, 서적, 기술 블로그 전체 목록 |

---

## v3 → v4 변경 로그

| 문제 | 수정 |
|------|------|
| Part 이름이 책의 언어가 아님 | Runtime, 변수, 실험, Operational Compiler로 교체 |
| Ch.2 §6과 Ch.3 §5의 결론 중복 | Ch.2는 "실패 구조의 정의"에서 끊고, Ch.3이 "그 구조를 관리하는 프레임워크"로 이어받음 |
| Ch.3이 7개 섹션으로 과적 | 5변수를 Ch.3 §1로 승격, 산업 사례를 §4에서 5변수의 예시로 종속 |
| 5변수가 Ch.3 §6에 묻힘 | Ch.3의 제목 자체를 "5변수 프레임워크"로 변경, §1에 배치 |
| Ch.2/Ch.7 failure 논문 이중 인용 | Ch.2는 패턴만 소개, Ch.7에서 정량 증거 제시. 참조 관계 명시 |
| Ch.1→Ch.2 톤 단절 | Ch.2 도입부에 "두 독자를 연결하는 절" 명시, chatbot→agent 스펙트럼으로 자연스러운 진입 |
| Ch.3→Ch.4 기술적 절벽 | Ch.3 §5 "만드는 것에서 운영하는 것으로"가 Ch.4의 기술적 내용을 예고하는 다리 역할 |
