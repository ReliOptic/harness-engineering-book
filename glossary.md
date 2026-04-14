# Glossary — 용어 사전

> Appendix B의 live 버전. 집필 진행에 따라 지속 업데이트.
> 새 용어 추가 시 알파벳(영문) 순 유지.
> 출판 버전은 `chapters/appendices/appendix-b-glossary.md`로 동기화.

---

## A

**Agent (에이전트)**
LLM을 중심으로 도구 사용, 메모리, 다단계 추론 능력을 갖춘 자율적 실행 단위.
단순 응답 생성을 넘어 환경과 상호작용하며 목표를 달성한다.

**Agent-1**
현 세대 agent. Tool-using이지만 취약하고 proactivity가 결여되어 있다.
Harness 없이는 반복 실패와 리소스 낭비가 빈번하다.

**Agent-2**
Continuous Learner. Self-immune system을 가지며, collapse 후 자발 복구와 infinite learning이 가능한 단계.
이 책은 Agent-1에서 Agent-2로의 전환 조건을 탐색한다.

**AgentOps**
비결정적 agent runtime을 관찰 가능하고, 통제 가능하고, 복구 가능하고, 자원 인식적으로 운영하기 위한 실천 규율.
Logging만이 아니라 intervention policy, permission design, recovery path, cost/latency discipline, compute overload control, self-reporting을 포함한다.
MLOps/DevOps에서 파생되었으나 그것보다 넓다.

**Agent Capability Composite** *(이 책의 조작적 정의, 기존 벤치마크 조합)*
벤치마�� 점수가 포착���지 못하는 에이전트의 실질적 역량을 측정하기 위한 복합 지표. 아래 4개 기존 측정 축의 조합이다:
- Tool Call Accuracy — Berkeley Function Calling Leaderboard, ToolBench (Qin et al., ICLR 2024)
- Instruction Following Rate — IFEval (Zhou et al., 2023)
- Multi-Step Reasoning Depth — GAIA (Mialon et al., 2023), AgentBench (Liu et al., ICLR 2024)
- Context Utilization Efficiency — τ-bench (Yao et al., 2024)

> 이 복합 지표는 기존 벤치마크들이 각각 측정하는 축을 하나의 스펙트럼으로 결합한 것이다. 저자가 새로 도출한 지표가 아니라, 산업계가 이미 사용하는 측정을 agent 운용 맥락에서 재조합한 것이���.

---

## B

**Balloon Effect (풍선 효과)** *(시스템 사고의 unintended consequence 개념)*
한 변수를 조작하면 다른 변수에서 에러가 터지는 현상.
> 근거: 시스템 사고(Meadows, *Thinking in Systems*, 2008)에서 "fixing one problem creates another"로 설명되는 패턴. Chaos engineering (Basiri et al., IEEE Software, 2016)의 blast radius 관찰과 유사.

---

## C

**성능 급락 (역량 절벽)** *(이 책의 관찰 용어. 관련: emergent abilities의 역방향)*
에이전트 역량이 특정 임계치 이하로 떨어질 때 작업 완료율이 선형이 아닌 급락(비선형 감소)하는 현상. Wei et al. (NeurIPS 2022)이 보고한 emergent abilities가 "역량이 올라갈 때 갑자기 가능해지는 것"이라면, 이 책이 관찰하는 것은 그 역방향 — "역량이 내려갈 때 갑자기 불가능해지는 것"이다.
> 참조: SWE-bench (Jimenez et al., ICLR 2024)에서도 모델 간 성능 격차가 비선형적으로 나타나는 패턴이 보고되었다.

**Compute (컴퓨트)**
5변수 중 하나. VM 사양, token budget, API 비용, 네트워크 지연 등 실행 환경의 물리적 제약.
Compute saturation은 모델이나 harness가 문제가 아닐 때도 실패를 유발한다 — 반례 2(E22).

---

## F

**실패 재분류 (실패 예산 재할당)** *(SRE error budget 개념의 확장)*
하네스가 실패 자체를 없애는 것이 아니라, 감지/복구 불가능한 실패를 감지/복구 가능한 실패로 전환하여 운영 비용의 구조를 바꾸는 현상.
> 근거: Google SRE의 "error budget" (Beyer et al., *Site Reliability Engineering*, O'Reilly, 2016) 개념을 agent runtime에 적용. SRE에서 error budget은 허용 가능한 실패의 총량이지만, 이 책에서는 실패의 **유형 전환**(undetectable → detectable)에 초점을 맞춘다.

**Field Dispatch**
집필 기간 중 발생하는 주목할 만한 사건을 짧고 정확하게 기록하는 현장 속보.
분석이 아니라 기록이다. 5분 이내 작성 원칙.
형식: `FD-YYYY-MM-DD-NNN`.

**Five-Variable Framework (5변수 프레임워크)**
Agent 시스템의 실용적 품질을 결정하는 5개 변수:
1. 모델 (Model): reasoning, tool use, consistency, confidence
2. Harness: operational envelope + AgentOps 주입 프레임워크
3. Product surface: agent가 input/output을 주고받는 인터페이스
4. Operator intervention: 인간 운영자의 개입 패턴
5. Compute/resource budget: VM 사양, token budget, API 비용

핵심 질문은 "모델과 harness 중 누가 더 중요한가?"가 아니라 "어떤 조건에서 무엇이 1차 병목이 되는가?"이다.

---

## H

**Harness (하네스)**
Memory, privacy, 권한, 핵심 context를 보호하면서 bounded capability, 재현성, 복구를 가능하게 하는 설계된 operational envelope.
나아가, AgentOps의 기능을 agent 내부에 점진적으로 주입하는 구조적 프레임워크이기도 하다.

**Harness Engineering (하네스 엔지니어링)**
에이전트가 실제 제약 조건 아래에서 무엇을 보호하고, 무엇을 가능하게 하며, 어떻게 취약성을 줄이는지를 다루는 설계 및 운영 분야.

**Harness Overhead Ratio** *(시스템 엔지니어링 overhead 개념의 적용)*
하네스 운영 자체가 소비하는 토큰이나 컴퓨팅 자원의 추가 비율. 이 비율이 너무 높으면 하네스 자체가 1차 병목이 된다.
> 근거: overhead ratio는 시스템 엔지니어링의 일반 개념. LLM 맥락에서는 Helicone, Langfuse 등 observability 도구가 측정하는 "token overhead"와 유사하다. 이 책은 이를 harness 전체의 비용 측정으로 확장한다.

---

## M

**MTTR (Mean Time To Recovery)**
장애 발생 시 시스템이 자체 복구하거나 인간 엔지니어가 개입하여 정상 상태로 되돌리는 데 걸리는 평균 시간. AgentOps의 핵심 운영 지표.

---

## O

**Operational Compiler** *(이 책의 비유. 관련: CLAUDE.md/AGENTS.md 패턴의 산업적 수렴)*
제약 실험에서 반복적으로 확인된 failure pattern과 intervention rule을 실행 가능한 운영 규칙으로 컴파일하는 구조. 한 번에 완결된 harness를 세우는 방식이 아니라, ROI가 검증된 component를 순차적으로 추가하는 점진적 구성이 전제다.
> 근거: Anthropic CLAUDE.md, OpenAI AGENTS.md, Google GEMINI.md, Cursor .cursorrules 등 독립 프로젝트들이 동일한 패턴(반복 실패 → 규칙 문서화 → agent 지침 반영)으로 수렴. everything-claude-code (~84k stars), awesome-cursorrules (~10k stars) 참조.

**운영 경계**
Harness가 agent에게 부여하는 행동 범위. Memory 보호, 권한 경계, 복구 경로, evaluation hook 등으로 구성된다.

**Operator Intervention (운영자 개입)**
5변수 중 하나. 인간 운영자가 agent 실행 중 개입하는 패턴, 타이밍, 효과.
반복 가능한 개입은 Operational Compiler의 컴파일 후보가 된다.

---

## P

**Primary Bottleneck (1차 병목)**
5변수 중 특정 조건에서 agent 시스템 성능을 가장 크게 제한하는 변수.
이 책의 핵심 질문: "어떤 조건에서 무엇이 1차 병목이 되는가?"

**Product Surface**
5변수 중 하나. Agent가 input/output을 주고받는 인터페이스.
2026년 3월 기준, CLI가 가장 효과적인 agent-first surface이다.
더 나은 형태가 있지 않을까 — 이 질문을 열어둔다.

---

## S

**Self-Immune System** *(이 책의 비유. 관련: self-healing, Reflexion, self-refine)*
AgentOps → Harness → Agent 내재화의 경로를 통해 agent가 스스로 복구하고 학습하는 상태. Agent-2 전환의 핵심 조건.
> 근거: Shinn et al., *Reflexion* (NeurIPS 2023, ~443 citations) — agent의 자기 반성 루프. Madaan et al., *Self-Refine* (NeurIPS 2023) — iterative self-improvement. "Self-healing systems"는 autonomic computing (IBM, 2001) 이후 시스템 엔지니어링에서 확립된 개념.

**Snapshot Principle (스냅샷 원칙)**
이 책은 2026년 상반기의 스냅샷이다. 과도한 학문적 해석 없이 관찰된 것을 기록한다.
시점 특정적 관찰에는 "2026년 3월 기준으로" 같은 마커를 넣는다.
