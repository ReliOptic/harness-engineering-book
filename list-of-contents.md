# List of Contents

> **상태**: 최종 목차 (2026-04-17, v6 기반 통합)
> **구조**: 11챕터 + Preface + Appendices, 4 Parts
> **프레임워크**: Harness 중심 분석 구조 — 모델 능력(inbound), 실행 환경 제약(boundary), 사용자 접점(outbound), 피드백 루프(return)의 네 영역
> **참조 모델**: `editorial-learning-curve-guideline.md` — 3단계 학습 곡선(직관 앵커 → 정밀 정의 → 운영 번역)

---

## 전체 구조

```
Preface   왜 이 책이 필요한가

Part I — Agent Runtime의 기술적 전제
  Ch.1    Context Window의 구조적 한계
  Ch.2    정보이론과 토큰 경제
  Ch.3    학습된 정렬이 Runtime에서 깨지는 지점
  Ch.4    도구 사용, 추론, 기억의 실패 경로

Part II — Harness와 AgentOps
  Ch.5    지금 무엇이 일어나고 있는가: Harness의 좌표
  Ch.6    Agent가 모델로부터 물려받는 것
  Ch.7    Harness Engineering과 AgentOps의 정의

Part III — 실험
  Ch.8    의도적 실패 실험 22개
  Ch.9    실험 결과에서 배운 것

Part IV — 운영 구조
  Ch.10   관찰에서 Operational Compiler로
  Ch.11   Harness에서 Agent Self-immune으로

Appendices
```

---

## Preface — 왜 이 책이 필요한가

이 책의 질문, 독자, 그리고 한계를 밝힌다.

- 이 책이 다루는 질문: "어떤 조건에서 무엇이 agent 운영의 1차 병목이 되는가?"
- 이 책이 아닌 것: 교리집도, 튜토리얼도, 벤더 비교표도 아니다
- 이 책의 독자:
  - **Primary**: Agent runtime을 직접 다루는 builder-operator
  - **확장**: 제품, 인프라, 전략, 마케팅, HR, 재무, 데이터, 창업 — 각자의 본업에서 AI로 일의 구조를 다시 설계하려는 실무자

**앵커 레퍼런스**:
- OpenAI, *Harness Engineering: Leveraging Codex in an Agent-First World* (2026)
- Chip Huyen, *AI Engineering: Building Applications with Foundation Models* (O'Reilly, 2025)

---

# Part I — Agent Runtime의 기술적 전제

> **Part I의 원칙**: 각 챕터는 1~2편의 핵심 논문을 backbone으로 삼는다. 논문을 이해하기 위해 필요한 개념을 3단계 학습 곡선(직관 앵커 → 정밀 정의 → 운영 번역)으로 도입하고, 마지막 섹션에서 반드시 agent operations 실무로 번역한다.

> **Part I과 Part II의 관계**: Part I은 "왜 이런 일이 일어나는가"의 기술적 기반이고, Part II는 "지금 현장에서 무슨 일이 일어나고 있는가"의 관찰 기록이다. Part I 없이 Part II를 읽을 수 있지만, Part I을 거치면 Part II의 관찰이 메커니즘으로 연결된다.

---

## Ch.1 — Context Window의 구조적 한계

**한 줄**: Transformer의 attention 메커니즘이 정보를 처리하는 방식을 이해하고, 그 구조적 한계가 agent runtime에서 어떤 실패로 나타나는지를 연결한다.

**Backbone 논문**:
- Vaswani et al., *Attention Is All You Need* (NeurIPS 2017, ~140,000 citations)
- Liu et al., *Lost in the Middle: How Language Models Use Long Contexts* (TACL 2024, ~1,500 citations)

**이 챕터가 도입하는 개념**: embedding, dot product similarity, softmax, K-Q-V mechanism, multi-head attention, positional encoding, U-shaped attention curve

**챕터 종료 시 독자 상태**: "왜 context window를 늘려도 agent가 중간 정보를 놓치는가"를 attention 메커니즘으로 설명할 수 있다.

### §1. 단어가 숫자가 되는 순간 — embedding과 벡터 공간
### §2. 주의를 기울인다는 것 — Attention 메커니즘의 해부
### §3. 여러 관점으로 동시에 보기 — Multi-Head Attention
### §4. 순서를 기억하는 방법 — Positional Encoding
### §5. 긴 입력에서 무엇이 사라지는가 — Lost in the Middle
### §6. Agent Operations를 위한 시사점

---

## Ch.2 — 정보이론과 토큰 경제

**한 줄**: 언어 모델이 확률적 텍스트 생성기인 동시에 압축 알고리즘이라는 사실을 정보이론으로 보이고, 이 등가성이 agent runtime 현상을 읽는 하나의 해석 렌즈가 됨을 보여준다.

**Backbone 논문**:
- Delétang et al., *Language Modeling Is Compression* (ICLR 2024)
- Shannon, *A Mathematical Theory of Communication* (1948)

**이 챕터가 도입하는 개념**: information content, entropy, cross-entropy, KL divergence, arithmetic coding, autoregressive chain rule, bits-per-byte, compression ratio

**챕터 종료 시 독자 상태**: "왜 더 좋은 모델이 더 잘 압축하는가"를 수식으로 설명할 수 있고, 이것을 prompt 최적화와 모델 비교에 적용할 수 있다.

### §1. 정보량: 놀라움을 측정하는 방법
### §2. 엔트로피: 놀라움의 평균 비용
### §3. Cross-Entropy와 KL Divergence: 틀린 모델의 대가
### §4. Arithmetic Coding: 확률이 압축된 파일이 되는 과정
### §5. Autoregressive 구조: 언어 모델은 태생적 압축기다
### §6. Bits-per-Byte: 모델을 비교하는 보편 척도
### §7. Agent Operations를 위한 시사점

---

## Ch.3 — 학습된 정렬이 Runtime에서 깨지는 지점

**한 줄**: RLHF에서 Constitutional AI까지의 계보를 따라, 모델이 행동을 학습하는 메커니즘을 이해하고, 학습 단계의 정렬이 왜 runtime 문제를 해결하지 못하는지를 규명한다.

**Backbone 논문**:
- Ouyang et al., *Training Language Models to Follow Instructions with Human Feedback* (InstructGPT, NeurIPS 2022, ~18,000 citations)
- Lee et al., *RLAIF: Scaling Reinforcement Learning from Human Feedback with AI Feedback* (2023)
- Bai et al., *Constitutional AI: Harmlessness from AI Feedback* (Anthropic, 2022, ~3,000 citations)

**챕터 종료 시 독자 상태**: "모델이 aligned되었는데 왜 agent가 여전히 실패하는가"를 학습-runtime 경계의 구조적 차이로 설명할 수 있다. Constitutional AI의 self-critique가 Ch.11 self-immune의 이론적 선행 좌표임을 이해한다.

### §1. 모델에게 지시를 따르게 가르치기 — InstructGPT와 RLHF
### §2. 인간 없이 스케일하기 — RLAIF
### §3. 스스로 교정하기 — Constitutional AI
### §4. 학습 정렬이 Runtime 문제를 풀지 못하는 구조적 이유

---

## Ch.4 — 도구 사용, 추론, 기억의 실패 경로

**한 줄**: Agent의 세 가지 핵심 능력 — 도구 사용, 추론-행동 통합, 자기 성찰과 기억 — 의 학술적 기원을 이해하고, 각 능력이 runtime에서 어떻게 실패하는지를 연결한다.

**Backbone 논문**:
- Schick et al., *Toolformer* (NeurIPS 2023, ~2,600 citations)
- Yao et al., *ReAct* (ICLR 2023, ~5,250 citations)
- Shinn et al., *Reflexion* (NeurIPS 2023, ~1,400 citations)

**Companion**: Lewis et al., *Retrieval-Augmented Generation* (NeurIPS 2020, ~7,000 citations)

**챕터 종료 시 독자 상태**: 도구 사용 정확도, instruction following rate, multi-step reasoning depth의 측정이 왜 필요한지를 각 능력의 실패 메커니즘으로 설명할 수 있다.

### §1. 도구를 사용하는 법을 스스로 배우기 — Toolformer
### §2. 생각하면서 행동하기 — ReAct
### §3. 실패에서 배우기 — Reflexion
### §4. 외부 기억 장치 — RAG와 그 너머
### §5. Agent Operations를 위한 시사점: 세 능력의 실패 지도

---

# Part II — Harness와 AgentOps

> **Part II의 원칙**: Part I이 기술적 기반을 깔았다면, Part II는 그 기반이 2026년 현장에서 어떤 모습으로 나타나는지를 관찰하고 측정하는 장이다. Part I에서 확립한 개념을 전제하되, 각 개념은 한 문장 재도입으로 충분하다.

---

## Ch.5 — 지금 무엇이 일어나고 있는가: Harness의 좌표

**한 줄**: Part I이 깔아둔 기술적 전제가 현장의 agent runtime에서 왜 harness 중심 분석 구조로 수렴하는지를 2026년 상반기 관찰로 정당화한다.

**이 챕터의 중심 질문**: "Attention, 압축, 정렬, 도구 사용이라는 기술적 역사가 현장에서 부딪힐 때, 병목 분석의 구조는 왜 harness를 중심으로 네 영역(inbound/boundary/outbound/return)으로 수렴하는가?"

### §1. 2026년 상반기: agent가 깨지는 풍경
### §2. Part I에서 이 현장으로: 기술적 전제가 만나는 지점
### §3. Harness 중심 분석 구조: 네 영역의 정의
### §4. 이원론의 거부와 Agent-1/Agent-2 스펙트럼
### §5. 이 책의 좌표: AI Engineering 이후의 질문

**학습 결과**: Harness 중심 분석 구조로 자신의 환경에서 agent 병목을 식별할 수 있다. "왜 harness engineering이 필요한가"를 자신의 업무 맥락에서 설명할 수 있다.

---

## Ch.6 — Agent가 모델로부터 물려받는 것

**한 줄**: 네 영역 중 inbound(모델 능력) 변수를 격리하여 관찰한다. 네 가지 관찰 지표(도구 사용 정확도, instruction following rate, multi-step reasoning depth, context 활용 효율)를 정의하고, 비선형 성능 급락을 측정한다.

**Part I 해석 연결**:
- 도구 사용 정확도의 배경: Ch.4 §1 Toolformer
- Instruction following rate의 배경: Ch.3 §1 InstructGPT
- Multi-step reasoning depth의 배경: Ch.4 §2 ReAct
- Context 활용 효율의 배경: Ch.1 §5 Lost in the Middle
- 성능 급락의 해석 렌즈: Ch.2 §3 cross-entropy

### §1. 물려받는 경향: reasoning, tool use, consistency, calibration
### §2. 모델 관찰 지표 — 네 항목의 정의와 측정
### §3. 성능 급락 — 선형이 아닌 급락이 발생하는 조건
### §4. Quantization Tax Curve
### §5. Distillation Efficiency Frontier
### §6. Mid-run model switching의 context continuity 붕괴
### §7. 모델 변수가 1차 병목이 되는 조건 — 그리고 아닌 조건

**학습 결과**: 네 가지 모델 관찰 지표 기반의 측정을 설계할 수 있다. 모델이 1차 병목인 조건과 아닌 조건을 구분할 수 있다.

---

## Ch.7 — Harness Engineering과 AgentOps의 정의

**한 줄**: harness와 intervention 변수를 정의한다. 실패 재분류 프레임워크로 harness의 효과를 재규정하고, Ch.8 실험의 가설을 pre-register한다.

**Part I 해석 연결**:
- Harness 정의의 배경: Ch.3 §4 "학습 정렬이 runtime 문제를 풀지 못하는 이유"
- Ontology RAG / semantic firewall: Ch.4 §4 RAG의 한계
- AgentOps 관측 체계: Ch.2 §3 KL divergence

### §1. Harness Engineering이란 무엇인가 — 운영 경계의 정의
### §2. Guardrails, Scaffolding, Orchestration과의 구분
### §3. Ontology와 메모리 구조
### §4. 실패 재분류
### §5. AgentOps와 운영 지표 (harness overhead, MTTR, HER)
### §6. 산업계 AgentOps 실무: 도구화된 것과 아직 안 된 것
### §7. Ch.8 실험 프레임 설정 — 가설과 판단 기준의 Pre-registration

**학습 결과**: Harness와 AgentOps를 정의하고, 실패 재분류로 harness 효과를 설명할 수 있다.

---

# Part III — 실험

---

## Ch.8 — 의도적 실패 실험 22개

**한 줄**: 변수를 격리 조작하며 어떤 변수가 어떤 조건에서 1차 병목이 되는가를 측정한다.

**Part I 연결** (인과 확정이 아니라 해석 가설):
- E05 memory leakage — Ch.1 attention 메커니즘의 잔류 activation
- E08 자기평가 정확도 급락 — Ch.3 self-critique 루프의 runtime 한계
- E09 goal drift — Ch.1 Lost in the Middle과 Ch.4 ReAct 루프의 장기 실행 한계

### §1. 실험 설계 원칙: 왜 의도적으로 실패시키는가
### §2. 실험 환경: GCP 무료 티어, OpenRouter, 측정 인프라
### §3. 1막 — 모델·harness·surface 변수 격리 (E01~E07)
### §4. 2막 — 자원 제약 하에서 self-immune의 최소 조건 (E08~E12)
### §5. 3막 — 개입의 반복 가능성과 내재화 (E13~E18)
### §6. 반례 — task design과 compute saturation (E19~E20)

**학습 결과**: 의도적 실패 실험을 설계하고 실행할 수 있다.

---

## Ch.9 — 실험 결과에서 배운 것

**한 줄**: 실험실 지표 → 운영 지표 → 비용 지표의 3단계 번역.

### §1. 22개 실험 결과 종합: 어떤 변수가 어떤 조건에서 1차 병목이었는가
### §2. 실패 재분류 정량 분석
### §3. 운영 metric 번역: MTTR과 Human Escalation Rate
### §4. 비용 metric 번역: TotalCost와 optimal harness overhead
### §5. Component ablation: 무엇이 얼마나 기여하는가
### §6. Token efficiency를 운영 규율로
### §7. Scaling과 temporal stability
### §8. 학술적 확장 가능성 — exploratory 발견 목록

**학습 결과**: 3단계 지표 번역 체계를 이해하고, component ablation에서 Operational Compiler 구성 우선순위를 도출할 수 있다.

---

# Part IV — 운영 구조

---

## Ch.10 — 관찰에서 Operational Compiler로

**한 줄**: 반복 실패 패턴을 실행 가능한 운영 규칙으로 컴파일한다.

### §1. 반복 실패 패턴에서 도구화 후보 식별
### §2. Operational Compiler 설계 원칙
### §3. 점진적 업데이트: Pareto frontier를 따라 이동하는 전략
### §4. Skill로 쓸 수 있는 능력의 극대화
### §5. Harness configuration의 산업적 수렴

| 파일 | 프로젝트 | 역할 |
|------|----------|------|
| `CLAUDE.md` | Anthropic Claude Code | 프로젝트 수준 agent 지침 |
| `AGENTS.md` | OpenAI Codex CLI | 디렉토리 수준 agent 규칙 |
| `GEMINI.md` | Google Gemini CLI | 프로젝트 수준 agent 지침 |
| `.cursorrules` | Cursor | IDE-native harness |
| `.windsurfrules` | Windsurf | IDE-native harness |
| `copilot-instructions.md` | GitHub Copilot | copilot 행동 지침 |

### §6. 도구화해야 할 것과 도구화하면 안 되는 것

**학습 결과**: Operational Compiler 구성 우선순위를 결정하고, 점진적 업데이트 전략을 설계할 수 있다.

---

## Ch.11 — Harness에서 Agent Self-immune으로

**한 줄**: Agent-1에서 Agent-2로의 전환 조건.

**Part I 해석 연결** (이 챕터에서 Part I의 투자가 회수된다):
- Self-critique의 계보: Ch.3 Constitutional AI — 같은 문제 의식의 연장
- Reflexion과의 구분: Ch.4 §3 Reflexion = task 간 학습 / Self-immune = task 내 감지
- 재귀적 한계의 해석 렌즈: Ch.2의 cross-entropy 프레임

### §1. 실험이 남긴 것
### §2. 현 세대 harness가 아직 풀 수 없는 문제
### §3. AgentOps → Harness → Agent 내재화: 점진적 경로
### §4. Self-immune system 초기 설계
### §5. Model Capability × Harness Value: Scaling 조건
### §6. Temporal Stability: self-immune은 얼마나 오래 유지되는가
### §7. Agent-1 → Agent-2: 전환 조건의 정식화
### §8. 이 책 이후: 미해결 질문들
### §9. 집필 과정의 메타 관찰

**학습 결과**: self-immune system의 조작적 정의와 재귀적 한계를 이해하고, Agent-1 → Agent-2 전환 조건을 설명할 수 있다.

---

## Appendices

| Appendix | 내용 |
|----------|------|
| A — 실험 로그 템플릿 | 네 영역, 교차검증, pre-registration 포함 |
| B — 용어 사전 | 전체 용어의 조작적 정의 |
| C — Figure 목록과 해석 가이드 | 모든 Figure의 읽는 법과 재현 조건 |
| D — 참조 프로젝트 목록 | GitHub 프로젝트 전체 (stars, URL, 인용 맥락) |
| E — 참고문헌 | 논문, 서적, 기술 블로그 전체 목록 |
