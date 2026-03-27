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

**ARCC (Agent-Relevant Capability Composite)**
벤치마크 점수가 포착하지 못하는 에이전트의 실질적 역량을 측정하기 위한 복합 지표. Tool Call Accuracy (TCA), Instruction Following Rate (IFR), Multi-Step Reasoning Depth (MSRD), Context Utilization Efficiency (CUE)로 구성된다.

---

## B

**Balloon Effect (풍선 효과)**
한 변수를 조작하면 다른 변수에서 에러가 터지는 현상.
5변수 프레임워크에서 변수 간 상호작용을 관찰할 때 핵심 지표.

---

## C

**Capability Cliff (역량 절벽)**
ARCC로 측정된 에이전트 역량이 특정 임계치(Threshold) 이하로 떨어질 때 작업 완료율(TCR)이 선형이 아닌 급락(비선형 감소)하는 현상.

**Compute (컴퓨트)**
5변수 중 하나. VM 사양, token budget, API 비용, 네트워크 지연 등 실행 환경의 물리적 제약.
Compute saturation은 모델이나 harness가 문제가 아닐 때도 실패를 유발한다 — 반례 2(E22).

---

## F

**Failure Budget Reallocation (실패 예산 재할당)**
하네스(Harness)가 실패 자체를 없애는 것이 아니라, 감지/복구 불가능한 실패를 감지/복구 가능한 실패로 전환하여 운영 비용의 구조를 바꾸는 현상.

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

**HOR (Harness Overhead Ratio)**
하네스(Harness) 운영 자체가 소비하는 토큰이나 컴퓨팅 자원의 추가 비율. HOR이 너무 높으면 오히려 작업 효율성을 해칠 수 있어 최적점을 찾는 것이 중요하다.

---

## M

**MTTR (Mean Time To Recovery)**
장애 발생 시 시스템이 자체 복구하거나 인간 엔지니어가 개입하여 정상 상태로 되돌리는 데 걸리는 평균 시간. AgentOps의 핵심 운영 지표.

---

## O

**Operational Compiler**
제약 실험에서 반복적으로 확인된 failure pattern과 intervention rule을 실행 가능한 운영 규칙으로 컴파일하는 구조.
한 번에 완결된 harness를 세우는 방식이 아니라, ROI가 검증된 component를 순차적으로 추가하는 점진적 구성이 전제다.

**Operational Envelope**
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

**Self-Immune System**
AgentOps → Harness → Agent 내재화의 경로를 통해 agent가 스스로 복구하고 학습하는 상태.
Agent-2 전환의 핵심 조건.

**Snapshot Principle (스냅샷 원칙)**
이 책은 2026년 상반기의 스냅샷이다. 과도한 학문적 해석 없이 관찰된 것을 기록한다.
시점 특정적 관찰에는 "2026년 3월 기준으로" 같은 마커를 넣는다.
