# Ch.3 — Harness Engineering과 AgentOps: 정의와 프레임워크

> 상태: 🟢 초고 v1.0 (2026-03)
> 담당: Kiwon
> 목표 분량: 8,000~10,000자

---

## 핵심 메시지

Harness는 failure를 제거하지 않는다. Harness가 하는 일은 failure의 성격을 바꾸는 것이다 — 감지 불가능하고 복구 불가능한 실패(undetectable/unrecoverable failure)를 감지 가능하고 복구 가능한 실패(detectable/recoverable failure)로 재배분한다. 이 재배분이 운영 비용(MTTR, Human Escalation Rate)을 어떻게 구조적으로 전환하는가가 harness engineering의 실무적 핵심이며, 이를 측정하고 통제하는 것이 AgentOps의 출발점이다. 이 챕터는 Ch.4의 의도적 실패 실험을 위한 프레임을 설정하고 가설과 판단 기준을 데이터 수집 이전에 사전에 고정(pre-registration)한다.

---

## §1 Harness Engineering이란 무엇인가 — Operational Envelope의 정의

모델 변수가 더 이상 1차 병목이 아닌 조건에 도달했을 때 무엇을 설계해야 하는가라는 질문은 필연적으로 개념의 경계 문제에 부딪힌다. 대규모 언어 모델(LLM)의 크기 확장에서 에이전트의 신뢰성 보장으로 엔지니어링의 중심이 이동하면서 "harness"라는 단어가 현장에 혼용되고 있으나, 그 정확한 위치는 구분되어야 한다. 이 책에서 harness는 에이전트의 권한, 메모리, 리소스 경계, 복구 경로, 개입 조건을 런타임(runtime)에 명시적으로 관리하는 동적 제어 인프라를 의미하며, 이를 통해 에이전트가 작동하는 허용 공간인 'operational envelope'을 형성한다.

이 정의의 핵심은 "런타임에 명시적으로"라는 한정에 있다. 에이전트가 envelope 안에 머무는 한 권한은 예상 범위 내에 있고 메모리는 오염되지 않으며 리소스 소비는 측정 가능하고 실패가 발생해도 사전에 정의된 복구 경로가 존재한다. OpenClaw 기반 선행 실험에서 필자가 관찰한 실패의 증상들은 다양했으나, 각각의 증상이 발생하기 전 에이전트의 현재 상태가 어디에도 기록되지 않고 있었다는 공통된 선행 조건이 존재했다. Harness의 역할은 에이전트의 런타임 상태를 측정 가능하게 만들어 이 공백을 메우는 것이다.

## §2 경계의 확정: Guardrails, Scaffolding, Orchestration과의 구분

에이전트 인프라스트럭처 패러다임이 부상함에 따라, harness를 인접 개념과 물리적 구현 레이어가 아닌 타이밍과 기능적 관점에서 명확히 분리할 필요가 있다. 

Guardrails는 입출력 필터링을 담당하며 주로 실행이 끝난 후(post-hoc) 작동하여 정책 위반을 포착한다. 프롬프트 인젝션이나 권한 남용을 방어하는 심층 방어(Defense-in-Depth) 구조로 진화했으나, 기본적으로 정적 윤리 필터의 연장선에 있다. 반면 Scaffolding은 실행이 시작되기 전(pre-hoc)에 작동하여 모델을 목적 지향적 에이전트로 조립하는 초기 뼈대 역할을 한다. 시스템 프롬프트 조립, 도구 스키마 구성, 기초적 메모리 구조 설정이 이 단계에서 이루어지며, 단일 에이전트가 긴 대화 속에서 컨텍스트를 잃지 않도록 인지적 제어 루프를 결정한다 (arXiv:2603.05344, Building AI Coding Agents).

Orchestration은 다중 에이전트 체제(MAS)에서 실행 시간 동안 에이전트 간의 메시지 라우팅과 작업 분배를 담당하는 중앙 지휘 평면이다 (arXiv:2601.13671, Orchestration of Multi-Agent Systems). Model Context Protocol(MCP)이나 A2A(Agent-to-Agent) 프로토콜은 이 오케스트레이션 계층에서 이질적인 에이전트 간의 상호운용성과 지식 연결을 표준화한다. 

Harness는 이 세 개념과 달리 실행이 진행되는 동안 에이전트 프로세스 전체의 런타임 상태를 지속적으로 관리하고 궤적을 감싸 안는 역할을 수행한다. 구현 레이어에서 이 개념들이 중첩될 수는 있으나, 디버깅 과정에서 어떤 레이어에서 어떤 실패가 감지되어야 하는가를 혼동하지 않기 위해 이 개념적 분리는 엄격하게 유지되어야 한다.

## §3 CLI-Anything 방법론: 대상 중심적(Target-Centric) Harness의 독립적 수렴

Harness 설계의 구체적 사례로서 HKUDS 팀의 CLI-Anything 프로젝트는 중요한 좌표를 제공한다. 기존의 하네스 접근이 주로 에이전트를 감싸 인지나 메모리를 보조하는 데 집중했다면, 이 프로젝트는 인간 중심의 복잡한 소프트웨어 환경 자체를 에이전트가 직접 제어할 수 있는 결정론적 인터페이스(CLI+JSON)로 개조하는 '대상 중심적' 어댑터로 하네스를 재정의했다. 

이는 필자가 관찰한 런타임 상태 관리의 필요성과 정확히 동일한 방향으로의 독립적 수렴을 의미한다. 구조화, 경량성, 자기 서술성, 결정론적 작동 등의 속성을 요구하는 CLI-Anything의 7단계 자율 생성 파이프라인은, 에이전트 친화적인 환경을 구축함으로써 컨텍스트 엔트로피를 통제하고 모델의 추론 부담을 덜어준다. 다른 문제 맥락에서 출발했음에도 동일한 설계 원칙에 도달했다는 사실은, 이러한 형태의 harness가 특정 프로젝트의 임시방편이 아니라 에이전트 런타임의 구조적 취약점에 대한 보편적 응답임을 입증한다.

## §4 Ontology와 메모리 구조: Harness의 의미론적 언어

Harness가 에이전트 행동의 물리적 경계를 제어한다면, 온톨로지(Ontology)는 그 경계를 기술하고 메모리를 보호하는 의미론적 규칙집으로 기능한다. 확률론적 LLM이 일관성 있게 작동하려면 사전에 정의된 스키마와 제약 조건을 통과한 데이터만이 지식 그래프에 편입되어야 한다 (arXiv:2505.24478, Cognee; arXiv:2512.13564, Memory in the Age of AI Agents).

일반적인 텍스트 유사도 기반의 RAG가 지식을 단순히 발견하는 것에 그친다면, Ontology RAG는 엄격한 제약을 우선하여 에이전트의 영구 메모리를 구조화한다. Cognee나 TrustGraph와 같은 도구들은 메모리 변형(mutation)이 발생하기 전 스키마 검증을 강제하는 시맨틱 방화벽 역할을 수행하며, 이는 다중 에이전트 환경에서 맥락의 손실 없이 정보를 교환하게 하는 필수적인 공유 언어가 된다. 이 구조화된 기억은 단순한 정보 검색을 넘어 에이전트가 자신의 상태를 자가 교정하고 진화하기 위한 전제 조건이다.

## §5 Failure Budget Reallocation — Harness 효과의 재규정

실험 데이터는 "harness를 적용하면 실패가 감소한다"는 단순한 명제를 기각한다. Harness가 작동하는 환경에서 특정 실패의 표면적 빈도는 줄어들지만, 실제로는 실패가 다른 범주로 재분류된 것에 가깝다. Failure Budget Reallocation 프레임워크는 주어진 조건에서 발생하는 실패 이벤트의 총량은 유사하게 유지된다는 가설 위에 서 있다.

필자는 실패를 6축 분류 체계(taxonomy)로 나누어 관찰했다: tool call failure, context overflow, output format error, silent logical drift, recovery attempted & succeeded, recovery attempted & failed. 이 중 운영 비용이 가장 높은 것은 silent logical drift다. 발생과 감지 사이의 간격이 길어 오류가 누적된 후 전체 파이프라인을 폐기해야 하기 때문이다. Harness는 이 치명적인 silent logical drift의 비중을 낮추고, 실패를 발생 즉시 포착하여 복구 루프로 진입시키는 recovery attempted 영역으로 예산을 재배분한다. 이 프레임워크는 단순히 표면적 성공률을 과장하는 대신 실패의 본질적 전환을 명시적으로 추적하게 한다.

## §6 AgentOps와 운영 지표 (HOR, MTTR)

단일 에이전트의 상태 관리를 넘어, 비결정론적 특성을 지닌 복합 에이전트 시스템을 관측하고 디버깅하며 최적화하는 특화 인프라가 AgentOps다. 모델 자체의 생애주기를 관리하는 MLOps나 결정론적 코드 배포를 다루는 DevOps와 달리, AgentOps는 실행 중인 에이전트의 런타임 행동 관찰과 개입에 집중한다. LangSmith, Weave, AgentOps.ai, Helicone, Braintrust와 같은 프레임워크들은 각각 생태계 통합, 세션 추적, 비용 통제, 평가 주도 테스트 등의 강점을 가지며 이 관측성을 제공한다.

이 운영 규율의 1차 지표는 MTTR(Mean Time To Recovery)과 HER(Human Escalation Rate)이다. 이 지표들은 장애 발생 시 시스템이 자체 복구하거나 인간 엔지니어가 개입해야 하는 시간을 실질적 비용으로 환산한다. 또한 Harness의 운영 비용 자체를 측정하기 위해 HOR(Harness Overhead Ratio)이라는 토큰 오버헤드 비율 지표를 도입한다. HOR이 과도하게 높아지면 토큰 예산을 잠식하여 오히려 작업 완료율(TCR)이 감소하는 현상이 발생하므로, HOR과 복구 성공률(RSuccR) 사이의 최적점(optimal point)을 찾는 것이 운영 설계의 핵심이다.

## §7 Ch.4 실험 프레임 설정 — 가설과 판단 기준의 Pre-registration

이러한 이론적 토대 위에서, 이어지는 Ch.4의 의도적 실패 실험들은 데이터 수집 이전에 가설과 판단 기준을 고정하는 pre-registration 원칙을 엄격히 따른다. 동일한 데이터에 대한 사후 해석(post-hoc rationalization)으로 인한 제1종 오류 증가를 구조적으로 방지하기 위함이다. 

**Task 조작적 정의:**
- **T1 Code Review:** F1 ≥ 0.70 (precision × recall). 실제 삽입된 버그(seeded bug list)를 기준으로 한 발견율과 오탐지 비율의 조화평균으로 판정.
- **T2 Multi-Step Reasoning:** `plan_is_valid = 1`. 에이전트가 생성한 다단계 계획이 명시적 제약 조건을 모두 충족하는지를 사전 고정된 자동 제약 체커(constraint checker)가 판정.
- **T3 Long-Horizon Execution:** 40+ steps 실행 완료 및 MTGR(Mean Task Goal Retention) ≥ 0.80. 장기 실행 환경에서 각 단계 출력이 초기 목표와 일치하는 비율을 채점.
- **T4 Synthesis:** LLM Judge (claude-sonnet-4-6)에 의한 사실적 정확도(factual accuracy) 판정. 단, 독립적인 2인의 인간 평가자(human rater)와의 Cohen's κ 계수가 0.70 이상일 때만 유효함.

**Ground Truth 3-Layer 구조:**
- **Layer 1 (Test Suite):** F1 scorer, constraint checker, pytest 기반 골 리텐션 스코어러 등 자동화된 코드로 100% 커버리지 검증.
- **Layer 2 (LLM Judge):** T4 합성 과제 및 Layer 1 판정이 모호한 약 30%의 사례에 적용. 인간 평가자와의 일치도(κ ≥ 0.70) 조건을 만족해야 함.
- **Layer 3 (Human Rater):** 계층화 표집(stratified sample)된 15~20%의 결과에 대해 2인의 독립된 평가자가 판정하며, 불일치 시 별도의 해결 프로토콜을 적용함.

이후 분석 과정에서 기준이 변경될 경우 반드시 Deviation Protocol에 따라 기록되며 확증적(confirmatory) 발견에서 탐색적(exploratory) 발견으로 강등된다. 이 실험 프레임은 5변수 중 어떤 요소가 어떤 조건에서 1차 병목으로 작용하는지를 정밀하게 타격하기 위한 기반이다.
tory) 분석과 탐색적(exploratory) 분석을 명확히 분리하여 보고한다. 이 엄격한 검증 체계는 하네스와 AgentOps가 비용 절감과 신뢰도 향상이라는 상충하는 목표 속에서 어떤 실질적 ROI를 도출하는지 측정하는 척도가 될 것이다.
