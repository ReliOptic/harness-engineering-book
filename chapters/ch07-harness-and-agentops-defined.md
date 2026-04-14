# Ch.7 — Harness Engineering과 AgentOps: 정의와 프레임워크

> 상태: 🟡 재구성 v2.0 (2026-04) — 세 축 비교(공식 담론/공개 실물 패턴/출간 시장) 구조 반영
> 담당: Kiwon
> 목표 분량: 10,000~12,000자

---

## 핵심 메시지

Harness는 failure를 제거하지 않는다. Harness가 하는 일은 failure의 성격을 바꾸는 것이다 — 감지 불가능하고 복구 불가능한 실패(undetectable/unrecoverable failure)를 감지 가능하고 복구 가능한 실패(detectable/recoverable failure)로 재배분한다. 이 재배분이 운영 비용(MTTR, Human Escalation Rate)을 어떻게 구조적으로 전환하는가가 harness engineering의 실무적 핵심이며, 이를 측정하고 통제하는 것이 AgentOps의 출발점이다. 이 챕터는 Ch.8의 의도적 실패 실험을 위한 프레임을 설정하고 가설과 판단 기준을 데이터 수집 이전에 사전에 고정(pre-registration)한다.

**세 축 비교 구조**: 이 챕터는 harness engineering을 세 가지 축에서 동시에 위치시킨다.
1. **공식 담론** — OpenAI, Anthropic 등이 정의한 harness engineering 원칙과 철학 (§1)
2. **공개 실물 패턴** — CLAUDE.md, AGENTS.md, GEMINI.md, .cursorrules 등 공개 관찰 가능한 harness 구성 파일 (§3)
3. **출간 시장** — 현재 출간된 harness/context engineering 관련 서적이 다루지 않는 운영 개념 (§5)

---

## §1 Harness Engineering이란 무엇인가 — 운영 경계의 정의

모델 변수가 더 이상 1차 병목이 아닌 조건에 도달했을 때 무엇을 설계해야 하는가라는 질문은 필연적으로 개념의 경계 문제에 부딪힌다. 대규모 언어 모델(LLM)의 크기 확장에서 에이전트의 신뢰성 보장으로 엔지니어링의 중심이 이동하면서 "harness"라는 단어가 현장에 혼용되고 있으나, 그 정확한 위치는 구분되어야 한다. 이 책에서 harness는 에이전트의 권한, 메모리, 리소스 경계, 복구 경로, 개입 조건을 런타임(runtime)에 명시적으로 관리하는 동적 제어 인프라를 의미하며, 이를 통해 에이전트가 작동하는 허용 공간인 'operational envelope'을 형성한다.

이 정의의 핵심은 "런타임에 명시적으로"라는 한정에 있다. 에이전트가 envelope 안에 머무는 한 권한은 예상 범위 내에 있고 메모리는 오염되지 않으며 리소스 소비는 측정 가능하고 실패가 발생해도 사전에 정의된 복구 경로가 존재한다. OpenClaw 기반 선행 실험에서 필자가 관찰한 실패의 증상들은 다양했으나, 각각의 증상이 발생하기 전 에이전트의 현재 상태가 어디에도 기록되지 않고 있었다는 공통된 선행 조건이 존재했다. Harness의 역할은 에이전트의 런타임 상태를 측정 가능하게 만들어 이 공백을 메우는 것이다.

2026년 현재, 장기 실행 agent 시스템을 운영하는 조직들은 독립적으로 유사한 아키텍처 분리에 도달하고 있다. 에이전트의 구성 요소를 session(이벤트 로그), harness(agent loop), sandbox(실행 환경), tools(도구 인터페이스)로 분리하고, 각 컴포넌트가 독립적으로 실패하고 교체될 수 있도록 설계하는 패턴이다. 단일 컨테이너에 모든 구성 요소를 결합했을 때 발생하는 문제 — 컨테이너 실패 시 세션 손실, 디버깅 불가, 실행 환경과 인증 정보의 결합으로 인한 보안 경계 부재 — 가 이 분리를 추동했다. 이 4-component 분리는 하나의 컴포넌트가 죽어도 나머지를 살려 교체할 수 있는 구조를 만들며, harness crash 시 session log에서 마지막 이벤트를 읽어 새 harness를 기동하는 복구 경로를 제공한다.

이 책의 harness 정의는 이 산업적 분리 패턴보다 넓다. 산업계의 4-component는 "에이전트 시스템의 부품은 무엇인가"에 답하는 아키텍처 분해이며, 자사 모델과 자사 인프라에 최적화된 구조다. 이 책의 독자는 모델을 선택해야 하고, 자원 제약 아래에서 운영해야 하며, 인간 개입의 시점을 결정해야 한다. 이 세 조건이 Ch.5에서 도입한 네 영역 — 모델 능력(inbound), 실행 환경 제약(boundary), 사용자 접점(outbound), 피드백 루프(return) — 을 harness 정의 안에 포함하는 이유다. 제약 환경에서는 envelope의 경계가 더 좁고, 경계 위반의 결과가 더 즉각적이며, harness 설계의 trade-off가 더 선명하게 드러난다.

## §2 경계의 확정: Guardrails, Scaffolding, Orchestration과의 구분

에이전트 인프라스트럭처 패러다임이 부상함에 따라, harness를 인접 개념과 물리적 구현 레이어가 아닌 타이밍과 기능적 관점에서 명확히 분리할 필요가 있다. 

Guardrails는 입출력 필터링을 담당하며 주로 실행이 끝난 후(post-hoc) 작동하여 정책 위반을 포착한다. 프롬프트 인젝션이나 권한 남용을 방어하는 심층 방어(Defense-in-Depth) 구조로 진화했으나, 기본적으로 정적 윤리 필터의 연장선에 있다. 반면 Scaffolding은 실행이 시작되기 전(pre-hoc)에 작동하여 모델을 목적 지향적 에이전트로 조립하는 초기 뼈대 역할을 한다. 시스템 프롬프트 조립, 도구 스키마 구성, 기초적 메모리 구조 설정이 이 단계에서 이루어지며, 단일 에이전트가 긴 대화 속에서 컨텍스트를 잃지 않도록 인지적 제어 루프를 결정한다 (arXiv:2603.05344, Building AI Coding Agents).

Orchestration은 다중 에이전트 체제(MAS)에서 실행 시간 동안 에이전트 간의 메시지 라우팅과 작업 분배를 담당하는 중앙 지휘 평면이다 (arXiv:2601.13671, Orchestration of Multi-Agent Systems). Model Context Protocol(MCP)이나 A2A(Agent-to-Agent) 프로토콜은 이 오케스트레이션 계층에서 이질적인 에이전트 간의 상호운용성과 지식 연결을 표준화한다. 

Harness는 이 세 개념과 달리 실행이 진행되는 동안 에이전트 프로세스 전체의 런타임 상태를 지속적으로 관리하고 궤적을 감싸 안는 역할을 수행한다. 구현 레이어에서 이 개념들이 중첩될 수는 있으나, 디버깅 과정에서 어떤 레이어에서 어떤 실패가 감지되어야 하는가를 혼동하지 않기 위해 이 개념적 분리는 엄격하게 유지되어야 한다.

## §3 공개 Harness 패턴의 비교: CLAUDE.md, AGENTS.md, GEMINI.md, .cursorrules

> **축: 공개 실물 패턴** — 2026년 현재 공개적으로 관찰 가능한 harness 구성 파일의 구조 비교.

§1-§2의 정의가 개념의 경계를 확정했다면, 이 절은 그 개념이 현장에서 어떤 물리적 형태로 구현되고 있는지를 공개 관찰 가능한 패턴에서 추적한다. 2026년 현재, 에이전트 런타임을 제어하는 harness의 가장 직접적인 표현은 프로젝트 루트에 배치되는 구성 파일이다. 필자가 관찰한 네 가지 주요 패턴은 각각 다른 설계 철학을 반영하면서도 구조적 수렴을 보인다.

**CLAUDE.md** (Anthropic/Claude Code 생태계): 프로젝트의 컨텍스트, voice rules, 도구 사용 규칙, 금지 행동을 자연어로 기술하는 단일 파일. 에이전트가 세션 시작 시 이 파일을 읽어 operational envelope을 구성한다. 특징은 자연어 기반의 유연한 구조와, 프로젝트별 계층적 상속(글로벌 → 프로젝트 → 디렉토리)이다. Lossy compression artifact로서의 성격 — 프로젝트 전체를 수백 줄로 압축 — 은 Ch.2의 정보이론적 프레임과 직접 연결된다.

**AGENTS.md** (OpenAI/Codex 생태계): 코드 생성 에이전트의 행동 규칙을 구조화된 형식으로 정의한다. CLAUDE.md보다 명시적인 규칙 기반 접근을 취하며, 테스트 실행, 린트 규칙, 커밋 메시지 형식 등 개발 워크플로우에 특화된 지침을 포함한다.

**GEMINI.md** (Google/Gemini CLI 생태계): Google의 Gemini CLI 환경에서 프로젝트 컨텍스트를 제공하는 구성 파일. CLAUDE.md와 유사한 자연어 기반 구조를 취하되, Gemini 모델의 특성에 맞춘 지침 체계를 포함한다.

**.cursorrules** (Cursor 생태계): IDE 통합 환경에서 에이전트의 코드 생성 행동을 제어하는 규칙 파일. 파일 단위 규칙 적용, 언어별 스타일 가이드, 프로젝트 구조 설명 등 IDE 컨텍스트에 특화되어 있다.

**네 패턴의 구조적 수렴**: 출발점(CLI, IDE, API)과 설계 철학이 다름에도 네 패턴은 공통된 구조적 요소를 공유한다: (1) 프로젝트 컨텍스트의 압축된 표현, (2) 행동 경계(해야 할 것/하지 말아야 할 것)의 명시, (3) 도구 사용 규칙, (4) 출력 형식 제약. 이 수렴은 harness가 특정 벤더의 설계 선택이 아니라, 에이전트 런타임의 구조적 요구에 대한 독립적 응답임을 시사한다. §1에서 정의한 operational envelope이 현장에서 자연어 기반 구성 파일이라는 형태로 물질화되고 있는 것이다.

**CLI-Anything와의 접점**: HKUDS 팀의 CLI-Anything 프로젝트는 이 공개 패턴들과 다른 방향에서 동일한 문제에 도달했다. 인간 중심의 복잡한 소프트웨어 환경 자체를 에이전트가 직접 제어할 수 있는 결정론적 인터페이스(CLI+JSON)로 개조하는 '대상 중심적' 어댑터로 harness를 재정의한 것이다. 구조화, 경량성, 자기 서술성, 결정론적 작동이라는 속성은 위 네 패턴이 공유하는 구조적 요소와 정확히 일치한다. 다른 문제 맥락에서 출발했음에도 동일한 설계 원칙에 도달했다는 사실은, 이 형태의 harness가 에이전트 런타임의 구조적 취약점에 대한 보편적 응답임을 입증한다.

<!-- TODO: 각 패턴의 구체적 비교 테이블 (항목: context 주입 방식, 계층 구조, 규칙 형식, 도구 제어, 메모리 관리) -->
<!-- TODO: 법적 제약으로 인해 각 패턴의 공개 문서와 커뮤니티 사용례만 참조. 비공개 소스 코드 언급 금지. -->

## §4 Ontology와 메모리 구조: Harness의 의미론적 언어

Harness가 에이전트 행동의 물리적 경계를 제어한다면, 온톨로지(Ontology)는 그 경계를 기술하고 메모리를 보호하는 의미론적 규칙집으로 기능한다. 확률론적 LLM이 일관성 있게 작동하려면 사전에 정의된 스키마와 제약 조건을 통과한 데이터만이 지식 그래프에 편입되어야 한다 (arXiv:2505.24478, Cognee; arXiv:2512.13564, Memory in the Age of AI Agents).

일반적인 텍스트 유사도 기반의 RAG가 지식을 단순히 발견하는 것에 그친다면, Ontology RAG는 엄격한 제약을 우선하여 에이전트의 영구 메모리를 구조화한다. Cognee나 TrustGraph와 같은 도구들은 메모리 변형(mutation)이 발생하기 전 스키마 검증을 강제하는 시맨틱 방화벽 역할을 수행하며, 이는 다중 에이전트 환경에서 맥락의 손실 없이 정보를 교환하게 하는 필수적인 공유 언어가 된다. 이 구조화된 기억은 단순한 정보 검색을 넘어 에이전트가 자신의 상태를 자가 교정하고 진화하기 위한 전제 조건이다.

## §5 실패 재분류 — Harness 효과의 재규정

> **축: 출간 시장** — 현재 출간된 harness/context engineering 서적 중 이 프레임워크를 조작적으로 정의한 것은 없다.

실험 데이터는 "harness를 적용하면 실패가 감소한다"는 단순한 명제를 기각한다. Harness가 작동하는 환경에서 특정 실패의 표면적 빈도는 줄어들지만, 실제로는 실패가 다른 범주로 재분류된 것에 가깝다. 실패 재분류 프레임워크는 주어진 조건에서 발생하는 실패 이벤트의 총량은 유사하게 유지된다는 가설 위에 서 있다.

필자는 실패를 6축 분류 체계(taxonomy)로 나누어 관찰했다: tool call failure, context overflow, output format error, silent logical drift, recovery attempted & succeeded, recovery attempted & failed. 이 중 운영 비용이 가장 높은 것은 silent logical drift다. 발생과 감지 사이의 간격이 길어 오류가 누적된 후 전체 파이프라인을 폐기해야 하기 때문이다. Harness는 이 치명적인 silent logical drift의 비중을 낮추고, 실패를 발생 즉시 포착하여 복구 루프로 진입시키는 recovery attempted 영역으로 예산을 재배분한다. 이 프레임워크는 단순히 표면적 성공률을 과장하는 대신 실패의 본질적 전환을 명시적으로 추적하게 한다.

경쟁서와의 좌표: Rothman의 *Context Engineering* (2026, 예정)은 context window 관리를 체계화하지만, 실패의 재배분이라는 프레임은 다루지 않는다. Huyen의 *AI Engineering* (2025)은 application layer의 평가 프레임워크를 제시하지만, runtime 실패의 운영적 전환은 범위 밖이다. 이 책이 실패 재분류를 조작적으로 정의하고 실험적으로 검증하는 것은, 출간 시장에서 아직 점유되지 않은 영역이다.

## §6 AgentOps와 운영 지표 (harness overhead, MTTR)

단일 에이전트의 상태 관리를 넘어, 비결정론적 특성을 지닌 복합 에이전트 시스템을 관측하고 디버깅하며 최적화하는 특화 인프라가 AgentOps다. 모델 자체의 생애주기를 관리하는 MLOps나 결정론적 코드 배포를 다루는 DevOps와 달리, AgentOps는 실행 중인 에이전트의 런타임 행동 관찰과 개입에 집중한다. LangSmith, Weave, AgentOps.ai, Helicone, Braintrust와 같은 프레임워크들은 각각 생태계 통합, 세션 추적, 비용 통제, 평가 주도 테스트 등의 강점을 가지며 이 관측성을 제공한다.

이 운영 규율의 1차 지표는 MTTR(Mean Time To Recovery)과 HER(Human Escalation Rate)이다. 이 지표들은 장애 발생 시 시스템이 자체 복구하거나 인간 엔지니어가 개입해야 하는 시간을 실질적 비용으로 환산한다. 또한 Harness의 운영 비용 자체를 측정하기 위해 harness overhead라는 토큰 오버헤드 비율 지표를 도입한다. harness overhead가 과도하게 높아지면 토큰 예산을 잠식하여 오히려 작업 완료율(TCR)이 감소하는 현상이 발생하므로, harness overhead와 복구 성공률(RSuccR) 사이의 최적점(optimal point)을 찾는 것이 운영 설계의 핵심이다.

## §7 산업계 AgentOps 실무: 도구화된 것과 아직 안 된 것

> 이 절은 §6의 도구 생태계를 운영 실무의 관점에서 재평가한다.

2026년 현재 AgentOps 도구 생태계에서 도구화가 완료된 영역과 아직 인간 판단에 의존하는 영역 사이의 경계는 선명하다.

**도구화된 것**: 트레이스 수집과 시각화(LangSmith, Weave), 토큰 비용 추적(Helicone), 세션 단위 재현(AgentOps.ai replay), A/B 테스트 기반 프롬프트 평가(Braintrust). 이 도구들이 제공하는 것은 관측성(observability)이다 — 무엇이 일어났는가를 사후에 재구성할 수 있게 한다.

**아직 안 된 것**: 실시간 drift 감지, 자동 복구 판단(재시도 vs 에스컬레이션 vs 중단), 다중 에이전트 환경에서의 오류 전파 추적, harness overhead 최적점의 동적 조정. 이 영역들이 도구화되지 않은 이유는 기술적 난이도만이 아니라, 판단 기준이 task와 context에 의존하여 범용 도구로 추상화하기 어렵기 때문이다.

이 경계가 중요한 이유는 Ch.10의 Operational Compiler가 정확히 이 "아직 안 된 것"의 영역에서 운영 규칙을 점진적으로 도구화하려는 시도이기 때문이다. Ch.8-9의 실험이 측정하는 것은 이 도구화의 효과와 한계다.

<!-- TODO: 도구별 비교 테이블 (항목: 트레이스, 비용, 재현, 평가, 실시간 감지, 자동 복구) -->

## §8 Ch.8 실험 프레임 설정 — 가설과 판단 기준의 Pre-registration

이러한 이론적 토대 위에서, 이어지는 Ch.8의 의도적 실패 실험들은 데이터 수집 이전에 가설과 판단 기준을 고정하는 pre-registration 원칙을 엄격히 따른다. 동일한 데이터에 대한 사후 해석(post-hoc rationalization)으로 인한 제1종 오류 증가를 구조적으로 방지하기 위함이다. 

**Task 조작적 정의:**
- **T1 Code Review:** F1 ≥ 0.70 (precision × recall). 실제 삽입된 버그(seeded bug list)를 기준으로 한 발견율과 오탐지 비율의 조화평균으로 판정.
- **T2 Multi-Step Reasoning:** `plan_is_valid = 1`. 에이전트가 생성한 다단계 계획이 명시적 제약 조건을 모두 충족하는지를 사전 고정된 자동 제약 체커(constraint checker)가 판정.
- **T3 Long-Horizon Execution:** 40+ steps 실행 완료 및 MTGR(Mean Task Goal Retention) ≥ 0.80. 장기 실행 환경에서 각 단계 출력이 초기 목표와 일치하는 비율을 채점.
- **T4 Synthesis:** LLM Judge (claude-sonnet-4-6)에 의한 사실적 정확도(factual accuracy) 판정. 단, 독립적인 2인의 인간 평가자(human rater)와의 Cohen's κ 계수가 0.70 이상일 때만 유효함.

**Ground Truth 3-Layer 구조:**
- **Layer 1 (Test Suite):** F1 scorer, constraint checker, pytest 기반 골 리텐션 스코어러 등 자동화된 코드로 100% 커버리지 검증.
- **Layer 2 (LLM Judge):** T4 합성 과제 및 Layer 1 판정이 모호한 약 30%의 사례에 적용. 인간 평가자와의 일치도(κ ≥ 0.70) 조건을 만족해야 함.
- **Layer 3 (Human Rater):** 계층화 표집(stratified sample)된 15~20%의 결과에 대해 2인의 독립된 평가자가 판정하며, 불일치 시 별도의 해결 프로토콜을 적용함.

이후 분석 과정에서 기준이 변경될 경우 반드시 Deviation Protocol에 따라 기록되며 확증적(confirmatory) 발견에서 탐색적(exploratory) 발견으로 강등된다. 이 실험 프레임은 harness의 네 영역 중 어떤 영역에서 어떤 조건이 1차 병목으로 작용하는지를 정밀하게 타격하기 위한 기반이다.
