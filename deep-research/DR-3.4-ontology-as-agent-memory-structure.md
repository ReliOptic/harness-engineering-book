# DR-3.4Ch.3: Agent Ontology — 구조화된 메모리와 Schema Validation의 부상 (2025-2026)

**작성일**: 2026-03-17
**관련 챕터**: Ch.3 (Harness and AgentOps Defined), Ch.6 (From Observation to Operational Compiler), Ch.7 (Self-Immune → §9)
**연구 동기**: AI agent 시스템에서 ontology가 단순한 지식 표현 도구를 넘어 harness의 핵심 구성요소로 부상하고 있다. Harness가 "agent의 행동 범위와 기억을 규율하는 운영 구조"라면, ontology는 그 구조가 기댈 수 있는 typed schema — 세계의 형태를 agent에게 알려주는 언어다.

---

## 1. Agent에서 Ontology란 무엇인가

철학적 맥락에서 ontology는 "존재하는 것들의 분류 체계"다. AI agent 시스템에서는 더 실용적으로 정의된다:

> **Agent ontology**: agent가 작동하는 도메인 안에서 유효한 entity, 관계, 제약 조건을 명시적으로 정의한 structured schema. Agent가 "무엇이 존재하는지", "어떤 관계가 가능한지", "어떤 행동이 허용되는지"를 알 수 있게 해주는 규칙집.

2026년 시점에서 이 개념이 다시 주목받는 이유는 단순하다. LLM은 확률론적이다. 같은 질문에 다른 날 다른 답을 낸다. 하지만 enterprise agent가 "Invoice"와 "PurchaseOrder"의 관계를 오늘과 내일 다르게 이해하면 시스템이 무너진다. Ontology는 그 일관성을 강제하는 장치다.

---

## 2. 기존 RAG vs. Ontology RAG — 무엇이 다른가

### 2.1. 일반 RAG의 한계

일반 RAG(Retrieval-Augmented Generation)는 벡터 유사도 검색으로 작동한다. 질문과 가장 "비슷한" 텍스트 청크를 가져온다. 문제는 유사도가 정확성을 보장하지 않는다는 것이다. 두 문장이 통계적으로 가까워도, 의미적으로는 충돌할 수 있다.

Graph RAG는 이 한계를 부분적으로 해소한다. Triplet(주어-관계-목적어)으로 지식을 구조화하고, 검색 시 그래프 경로를 탐색한다. 하지만 Graph RAG는 structure를 자동으로 발견한다 — 즉, ontology를 강제하지 않는다. Agent가 문서에서 스스로 entity와 관계를 추출하므로, 도메인 제약을 위반한 관계가 그래프에 포함될 수 있다.

### 2.2. Ontology RAG

TrustGraph이 명명한 "Ontology RAG"는 schema-first 접근이다. 추출 전에 먼저 ontology를 정의한다 — 어떤 entity 타입이 존재하는지(`Sensor`, `Observation`, `Person`, `Policy`...), 어떤 object property가 허용되는지(`observes`, `hasValue`, `isPartOf`...). LLM이 문서에서 추출하는 모든 entity와 관계는 이 ontology를 통과해야만 knowledge graph에 진입한다.

이 차이는 단순한 방법론적 선택이 아니다. Harness 관점에서 보면:

- **Graph RAG**: 발견 우선 (agent가 세계의 형태를 스스로 학습)
- **Ontology RAG**: 제약 우선 (agent에게 세계의 형태를 미리 알려줌)

후자가 harness와 더 자연스럽게 결합된다. Harness가 agent의 행동을 정의된 경계 안에 묶어두는 장치라면, ontology는 그 경계의 언어 자체다.

---

## 3. 주요 CLI 도구 현황 (2025-2026)

### 3.1. Cognee CLI

- **GitHub**: topoteretes/cognee
- **핵심 명령어**:
  - `cognee-cli add "문서 또는 텍스트"` — 지식 소스 ingestion
  - `cognee-cli cognify` — knowledge graph 생성 (문서 → 그래프)
  - `cognee-cli search "질문"` — 그래프 기반 검색
  - `cognee-cli --ui` — 로컬 UI + MCP 서버 실행

- **Ontology 처리 방식**: "graph first, ontology optional" 철학. Knowledge graph를 먼저 구축한 후, ontology 파일을 선택적으로 주입한다. Ontology가 주입되면 추출된 node를 검증하고, parent class와 object property를 추가한다.

- **주목할 점**: 2025년 12월, Claude Agent SDK와 MCP 통합을 통해 agent의 persistent memory를 Cognee로 관리하는 가이드를 발표했다. MCP 서버를 통해 agent가 직접 Cognee knowledge graph를 read/write할 수 있다.

- **자금**: Pebblebed 주도 $7.5M seed (OpenAI, Facebook AI Research 창업자 참여). 상업용 버전은 ontology auto-generation 지원.

- **연구**: *"Optimizing the Interface Between Knowledge Graphs and LLMs for Complex Reasoning"* (arXiv:2505.24478, 2025)

### 3.2. TrustGraph CLI

- **GitHub**: trustgraph-ai/trustgraph (Apache 2.0)
- **핵심 개념**: Context Core — 지식, 임베딩, 정책, 증거를 하나의 versioned 번들로 패키징. "Context as Code."

- **CLI 워크플로우**:
  1. `tg-add-library-document` — 문서 ingestion (메타데이터: name, description, tags, kind)
  2. `tg-put-config-item --type ontology` — OWL 기반 ontology 로드
  3. `tg-start-flow` — Ontology RAG 플로우 시작 (어떤 ontology를 사용할지 지정)
  4. `tg-invoke-graph-rag "질문"` — knowledge graph 기반 응답 생성

- **Ontology 포맷**: 내부 JSON 포맷 (OWL 구조를 따름). 추출된 entity는 JSON-LD 형태로 출력.
  예시: `{"@type": "Sensor", "id": "sensor_12345", "name": "Temperature Monitor Alpha"}`

- **표준 지원**: W3C SSN/SOSA (Semantic Sensor Network / Sensor, Observation, Sample, Actuator) 온톨로지 지원.

- **릴리즈 이력**:
  - v1.5.8 (2025-11-24): Ontology-based extraction processor 출시 — ML heuristic 대신 도메인 ontology로 추출 로직을 guide.
  - v1.6 (2025-12-04): Streaming 지원 전면화. GraphRAG/DocumentRAG가 token-by-token 실시간 응답 가능.

### 3.3. LobeHub Ontology Skill

- **개념**: Agent "Skill"로 제공되는 typed vocabulary + constraint-driven knowledge graph.
- **작동 방식**: `Person`, `Task`, `Policy` 등 entity 타입과 스키마를 정의. Agent가 메모리를 변경하기 전에 schema validation을 통과해야 함.
- **저장소**: `memory/ontology/graph.jsonl` + `memory/ontology/schema.yaml`
- **CLI 워크플로우**: create / query / relate / validate 명령어 지원.
- **핵심 특징**: "validation before commit" — mutation이 일어나기 전에 반드시 schema를 통과. 이는 harness의 approval mechanism과 구조적으로 동일하다.

### 3.4. OntoGuard (언급된 개념)

"Ontology firewall"로 묘사된다. Agent의 action이 사전 정의된 business rule과 safety policy에 부합하는지 semantic하게 검증한다. 아직 독립적인 오픈소스 프로젝트보다는 enterprise 솔루션에 가까운 것으로 보임 — 추가 검증 필요.

---

## 4. Ontology와 Harness의 교차점

이 리서치의 핵심 관찰은 다음이다:

**Harness가 agent의 행동 boundary를 정의한다면, ontology는 그 boundary의 의미론적 표현이다.**

구체적으로:

| Harness 기능 | Ontology가 담당하는 부분 |
|---|---|
| 메모리 보호 | entity 타입과 관계에 대한 schema constraint |
| 권한 제어 | 허용된 object property와 불허된 관계 정의 |
| 복구 메커니즘 | validation 실패 시 롤백을 위한 versioned context core |
| Evaluation hook | mutation 전 schema validation |

즉, ontology는 harness의 5변수 프레임워크 중 **harness 변수**의 내부 언어로 기능한다. 좋은 harness는 ontology 없이도 작동할 수 있지만, ontology가 있는 harness는 행동의 근거를 explicit하게 기술할 수 있다. Agent가 왜 어떤 행동을 하지 않는지 설명할 수 있다.

---

## 5. Infrastructure as Code → Ontology as Infrastructure

2026년에 새롭게 부상하는 패턴: 전통적인 YAML 기반 IaC(Infrastructure as Code)를 ontology-driven IaC로 대체하는 시도들이 있다. Agent가 인프라를 배포할 때, YAML config를 파싱하는 것이 아니라 도메인 ontology를 이해하고 그 위에서 추론하여 복잡한 시스템을 구성한다.

이는 agent에게 "도구 사용법"이 아니라 "도메인의 구조"를 알려주는 방향이다. 더 범용적이고, 더 견고하고, 더 예측 가능한 agent behavior를 만들 수 있다.

---

## 6. Multi-Agent 환경에서의 Ontology: 공유 언어로서

단일 agent에서도 ontology는 유용하지만, multi-agent 시스템에서 ontology의 역할은 질적으로 다르다. Agent들이 서로 다른 맥락에서 정보를 교환할 때, 공유된 ontology가 없으면 "Invoice"가 한 agent에게는 `{id, amount, vendor}`, 다른 agent에게는 `{invoice_number, total, supplier}`로 해석될 수 있다. 의미는 같지만 구조가 달라서 정보가 소실된다.

ACP(Agent Client Protocol)나 MCP(Model Context Protocol) 같은 표준화 레이어가 이 문제를 해소하려 하지만, protocol 레벨의 표준화만으로는 부족하다. 교환되는 **내용의 의미**를 공유하는 ontology가 함께 있어야 agent 간 정보 교환이 context를 잃지 않는다.

---

## 7. 아직 해결되지 않은 문제들

이 영역에서 실무적으로 주목해야 할 미해결 문제들:

1. **Ontology drift**: 시스템이 운영되면서 실제 데이터가 ontology와 어긋나기 시작할 때의 처리 전략이 아직 확립되지 않았다. Cognee의 memory auto-optimization이 일부 해소하려 하지만, 한계가 있다.

2. **Cold start 문제**: 새로운 도메인에 ontology를 처음 정의할 때의 비용. 전문가 없이 auto-generation으로 얼마나 커버 가능한가? 아직 상업용 솔루션 영역에 머물러 있다.

3. **Ontology vs. Agent flexibility의 트레이드오프**: Ontology가 엄격할수록 agent가 예측 가능하지만, 새로운 상황에 적응하는 능력이 떨어진다. 이 tension을 어떻게 관리할 것인가는 harness 설계의 핵심 질문이다.

4. **Evaluation의 부재**: Ontology-grounded agent와 그렇지 않은 agent의 성능 차이를 측정하는 표준 benchmark가 없다. 관찰은 많지만 측정이 부족하다.

---

## 8. 이 리서치가 책에서 가지는 의미

이 내용은 Ch.3(Harness 정의)에서 ontology를 harness의 의미론적 기반으로 소개하는 데 활용할 수 있다. 동시에 Ch.6(Operational Compiler)에서 구체적인 도구 — Cognee, TrustGraph — 를 실험 맥락으로 연결할 수 있다.

주의: 이 영역은 2025-2026년에 급격히 성장 중이다. Cognee의 MCP 통합, TrustGraph의 Context Core 개념은 현재 진행형이며, 책의 Beta 마감(2026-05-13) 시점까지 생태계가 더 바뀔 수 있다. 스냅샷임을 명시하고 쓰는 것이 맞다.

---

## 9. Ontology와 Agent-2 전환: 핵심 연결 논증

**→ Ch.7 연결: DR-7.1(self-healing agents), DR-7.2(continuous learning)**

이 섹션은 ontology 기능이 단순한 기술적 도구를 넘어, Ch.7이 주장하는 Agent-1 → Agent-2 전환의 필요 조건임을 설명한다.

### 9.1. Self-immune은 "건강한 상태의 정의"를 필요로 한다

Ch.7의 self-immune system 논증은 "agent가 스스로 복구하고 학습한다"는 것이 핵심이다. 그런데 복구는 기준점 없이 작동하지 않는다. 무엇으로 돌아가는 것이 복구인가?

현재 Agent-1 세대에서 harness는 이 기준점을 외부에서 강제한다. Schema validation은 harness 레이어에서 일어난다. Agent는 자신이 어떤 제약 안에서 작동하는지 알지 못한다 — 단지 거부당하거나 허용될 뿐이다.

Agent-2의 조건은 이 기준점이 agent 내부로 이동하는 것이다. Agent 스스로 "이 entity 관계는 도메인 schema와 어긋난다"고 인식하고, 행동 전에 자기 교정한다. Ontology는 그 내부 기준점의 형식 언어다. Ontology가 없으면, agent가 내면화할 수 있는 "올바른 상태의 모양"이 존재하지 않는다.

### 9.2. Continuous learning(DR-7.2)은 구조화된 기억을 전제로 한다

DR-7.2가 기술한 지속 학습 아키텍처 — 특히 PRAXIS의 절차적 기억 — 는 `(상태, 행동, 결과)` 트리플을 저장하고 재활용한다. 이때 "상태"를 어떻게 표현하는가가 학습의 일반화 가능성을 결정한다.

상태 표현이 자유 텍스트라면, 유사한 상태가 다른 표현으로 저장되어 검색에서 누락된다. 상태 표현이 ontology-grounded typed entity라면, 다른 세션에서 다른 agent가 기록한 경험도 동일한 schema 위에서 비교되고 재활용된다. Cognee가 "usage feedback이 edge weight를 업데이트한다"는 memory auto-optimization을 가능하게 만드는 기반이 여기 있다 — feedback을 누적할 수 있는 안정적인 구조가 ontology다.

### 9.3. Agent-1과 Agent-2를 가르는 선

이 논증을 단순화하면:

| | Agent-1 | Agent-2 |
|---|---|---|
| Ontology 위치 | Harness 외부에서 강제 | Agent 내부에 내재화 |
| Validation 시점 | Harness가 commit 전에 차단 | Agent 자신이 행동 전에 확인 |
| Schema 위반 감지 | 외부 guardrail이 탐지 | Agent가 스스로 인식 |
| Drift 처리 | Harness가 롤백 | Agent가 drift를 신호로 읽고 self-correct |

Agent-1에서 Agent-2로 가는 전환 경로는 "AgentOps → Harness → Agent 내재화"(Ch.7 섹션 3)다. Ontology는 이 경로에서 내재화할 수 있는 가장 구체적이고 명시적인 대상이다. Tool permission이나 memory quota 같은 runtime constraint는 context에 따라 달라지지만, domain ontology는 상대적으로 안정적이다 — 그래서 먼저 내재화될 가능성이 높다.

### 9.4. Ontology drift ↔ Self-immune의 피드백 루프

DR-3.4 섹션 7에서 "미해결 문제"로 기록한 ontology drift — 시스템이 운영되면서 실제 데이터가 ontology와 어긋나기 시작하는 현상 — 는 Agent-2 관점에서 다르게 읽힌다.

Agent-1 harness에서 ontology drift는 문제다. 운영자가 감지하고 수동으로 ontology를 업데이트해야 한다.

Agent-2 self-immune system에서 ontology drift는 신호다. Agent가 "내가 알고 있는 세계의 형태와 실제 데이터 사이에 gap이 생겼다"는 것을 감지하는 능력 자체가 self-awareness의 초기 형태다. Drift를 감지하고, 그 패턴을 기록하고, 조건이 맞을 때 ontology update를 제안하는 것 — 이것이 Ch.7의 "agent가 스스로 복구하고 학습한다"는 명제의 가장 구체적인 첫 번째 구현이다.

### 9.5. 집필 방향 메모

Ch.7에서 이 연결을 쓸 때는 다음 순서가 자연스럽다:
1. Harness가 현재 외부에서 강제하는 것들 중 무엇이 내재화 가능한가? (섹션 3에서 열린 질문)
2. Ontology — agent가 "도메인의 형태"를 알고 있다는 것의 의미
3. Self-immune에서 ontology가 없으면 복구의 기준점이 없다는 논증
4. Cognee/TrustGraph의 현재 구현이 Agent-2의 방향을 어떻게 가리키는가
5. 단, 현재 구현과 Agent-2의 완전한 내재화 사이의 gap을 숨기지 않는다

---

## 참고 출처

- [Cognee GitHub](https://github.com/topoteretes/cognee)
- [Cognee Ontology Integration 블로그](https://www.cognee.ai/blog/deep-dives/ontology-ai-memory)
- [TrustGraph Ontology RAG CLI 가이드](https://docs.trustgraph.ai/guides/ontology-rag-cli/)
- [TrustGraph Ontology RAG 개념](https://docs.trustgraph.ai/guides/ontology-rag/)
- [TrustGraph GitHub](https://github.com/trustgraph-ai/trustgraph)
- [LobeHub OpenClaw Ontology Skill](https://lobehub.com/skills/openclaw-skills-ontology)
- [Why Ontology Matters for Agentic AI in 2026 (Ken Huang)](https://kenhuangus.substack.com/p/why-ontology-matters-for-agentic)
- [The 2026 Agent Stack: Why Ontologies Just Became Mission-Critical (Medium)](https://medium.com/@cloudpankaj/the-2026-agent-stack-why-ontologies-just-became-mission-critical-eb8a4a78dd45)
- [2025 Was Agents. 2026 Is Agent Harnesses. (Aakash Gupta, Medium)](https://aakashgupta.medium.com/2025-was-agents-2026-is-agent-harnesses-heres-why-that-changes-everything-073e9877655e)
- [Memory in the Age of AI Agents (arXiv:2512.13564)](https://arxiv.org/abs/2512.13564)
- [Cognee arXiv:2505.24478](https://arxiv.org/abs/2505.24478)
