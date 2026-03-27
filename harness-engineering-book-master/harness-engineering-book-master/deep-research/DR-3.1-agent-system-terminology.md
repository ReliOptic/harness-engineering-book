# **DR-3.1Ch.3: 2025-2026년 에이전트 시스템 핵심 아키텍처 용어 심층 연구 \- Guardrails, Scaffolding, Harness, Orchestration Layer**

## **1\. 서론: 모델 중심주의의 종언과 인프라스트럭처 패러다임의 부상**

2025년에서 2026년으로 이어지는 시기는 인공지능 엔지니어링 생태계에 있어 근본적인 패러다임의 전환기로 기록된다. 과거 몇 년간 인공지능 산업의 발전 궤적은 대규모 언어 모델(LLM)의 매개변수(Parameter) 크기를 물리적으로 확장하고, 사전 학습 데이터의 양을 늘려 모델 자체의 순수한 추론 지능을 극대화하는 '모델 중심(Model-centric)' 접근법에 극도로 편향되어 있었다.1 그러나 2026년에 이르러, 아무리 뛰어난 지능을 갖춘 최첨단 파운데이션 모델이라 할지라도 이를 둘러싼 시스템적 인프라 및 아키텍처가 부재하다면 실제 기업 환경에서 발생하는 복잡하고 다층적인 비즈니스 난제들을 안전하고 일관되게 해결할 수 없다는 뼈아픈 인식이 산업계 전반의 주류로 자리 잡았다.1

이러한 패러다임 전환의 근저에는 자율형 AI 에이전트(Autonomous AI Agent)가 창출하는 전례 없는 기회와 그 이면에 숨겨진 '신뢰 병목(Trust Bottleneck)' 현상이 존재한다.4 단일 질의응답을 넘어 장기적인 계획을 수립하고, 다양한 외부 도구를 자율적으로 호출하며, 심지어 다른 에이전트들과 협업하여 다단계 워크플로우를 수행하는 현대의 에이전트 시스템은 본질적으로 높은 자율성을 띤다.5 그러나 모델의 기저에 깔린 확률론적 텍스트 생성 특성으로 인해, 통제되지 않은 에이전트는 환각(Hallucination), 도구 오남용, 권한 범위를 벗어난 데이터 접근, 그리고 치명적인 보안 사고를 유발할 수 있는 '예측 불가능한 위험 요소'로 전락할 위험을 동시에 내포하고 있다.7

생성형 AI의 발전 속도가 인간의 수동적 검증 속도를 아득히 초월하면서, 엔지니어링의 핵심 과제는 '얼마나 똑똑한 모델을 만들 것인가'에서 '얼마나 신뢰할 수 있고 통제 가능한 시스템을 구축할 것인가'로 이동했다.2 이 과정에서 에이전트의 행동 반경을 제약하고, 인지 과정을 구조화하며, 실행 결과를 검증하고, 다수의 에이전트를 유기적으로 지휘하기 위한 아키텍처 요소들이 필연적으로 대두되었다. 본 보고서는 2025년부터 2026년까지 발표된 방대한 블로그, 최신 학술 논문, 그리고 프레임워크 공식 문서를 포괄적으로 분석하여, 에이전트 시스템을 지탱하는 네 가지 핵심 아키텍처 용어인 **Guardrails(가드레일)**, **Scaffolding(스캐폴딩)**, **Harness(하네스)**, 그리고 \*\*Orchestration Layer(오케스트레이션 계층)\*\*의 기술적 정의, 메커니즘, 그리고 이들이 상호작용하며 창출하는 2차 및 3차적 산업 통찰을 심층적으로 규명한다.

## **2\. Guardrails (가드레일): 정적 윤리 필터에서 동적 런타임 제어 메커니즘으로의 진화**

AI 에이전트 시스템에서 'Guardrails(가드레일)'이라는 용어는 초창기 파운데이션 모델 제공자(예: OpenAI, Anthropic)가 자사 모델의 유해한 콘텐츠 생성이나 편향성, 비윤리적 발언을 방지하기 위해 훈련 단계 또는 단순 프롬프트 필터링 수준에서 적용하던 다소 수동적인 제어 장치로 출발했다.9 그러나 2025년과 2026년을 거치며 엔터프라이즈 환경에서의 에이전트 도입이 본격화됨에 따라, 가드레일의 개념은 단순한 '콘텐츠 필터'를 넘어 조직의 고유한 데이터 보호, 규제 준수(Compliance), 그리고 런타임(Runtime) 환경에서의 동적이고 선제적인 보안 통제 메커니즘으로 급격히 확장되었다.9

### **2.1. 규제 컴플라이언스의 기술적 강제와 런타임 제어의 의무화**

2026년은 인공지능 가드레일이 기업의 '선택적 도입(Optional)' 사안에서 벗어나 '법적 의무(Mandatory)'로 완전히 전환된 원년이다.10 가장 대표적인 사례는 2025년 10월 제정된 SB 243 법안과 AB 489 법안이다. SB 243 법안은 단발성 트랜잭션 응답을 넘어 사용자와 장기적으로 관계를 형성하고 지속적인 상호작용을 이어가는 이른바 '동반자 AI(Companion AI)' 시스템에 대한 강력한 규제를 명시하고 있다.10 더불어 AB 489 법안은 실제 검증된 의료 전문 지식을 갖추지 않았음에도 불구하고, 대화의 맥락이나 뉘앙스를 통해 사용자에게 의료적 전문성을 암시하거나 처방적 조언을 제공하는 AI 시스템의 위험성을 엄격하게 통제하도록 강제한다.10

이러한 규제 환경의 급격한 변화는 가드레일의 아키텍처 설계 방식을 근본적으로 뒤바꾸어 놓았다. 기업은 더 이상 모델이 사전에 정의된 윤리적 지침을 스스로 준수할 것이라는 '희망적 관측' 기반의 거버넌스 프레임워크에 의존할 수 없게 되었다.10 대신, 사용자와 AI 에이전트 간의 상호작용이 사전 승인된 도메인 경계를 벗어나거나 위험한 영역으로 드리프트(Drift)하는 순간을 실시간으로 감지하고, 즉각적으로 개입하여 출력을 차단하거나 행동을 수정하는 물리적인 '런타임 통제(Runtime Control)' 능력을 시스템 내부에 직접 구현해야만 했다.10 이는 가드레일이 모델의 내부 파라미터 튜닝 영역을 벗어나, 애플리케이션 계층에서 모델의 입출력과 시스템 접근을 직접 관장하는 능동적인 보안 방어선으로 편입되었음을 의미한다.7

2025년 발간된 AI 에이전트 인덱스(AI Agent Index) 보고서에 따르면, 프론티어 AI 연구소(OpenAI, Anthropic 등)와 엔터프라이즈 플랫폼 간의 안전성 평가 및 가드레일 구현 방식에는 뚜렷한 차이가 존재한다.12 프론티어 연구소들이 모델 자체의 재앙적 위험(Catastrophic risks)이나 존재론적 정렬(Existential alignment) 문제에 집중하여 시스템 카드를 발행하는 반면, 엔터프라이즈 플랫폼은 옵션 형태의 가드레일을 제공하면서도 샌드박싱(Sandboxing)이나 격리(Containment) 환경과 결합된 구체적인 런타임 제어 인프라를 구축하는 데 사활을 걸고 있다.12

### **2.2. OWASP LLM 취약점 대응 및 엔터프라이즈 위협 모델링**

자율적 에이전트 시스템은 과거의 전통적인 소프트웨어가 직면하지 않았던 완전히 새로운 형태의 공격 벡터와 보안 취약점을 발생시킨다. 메모리를 사용하고, 외부 도구를 호출하며, 자율적인 결정을 내리는 에이전트는 프롬프트 인젝션(Prompt Injection), 데이터 유출(Data Leaks), 도구 오남용(Tool Abuse), 모델 드리프트(Model Drift), 환각에 기반한 비정상적 검색(Uncontrolled Retrieval) 등 치명적인 프로덕션 위험에 지속적으로 노출된다.7 Datadog의 2025년 가이드라인에 따르면, 엔터프라이즈 가드레일은 OWASP(Open Worldwide Application Security Project)가 정의한 주요 LLM 보안 위협들을 방어하는 핵심 기제로 작용한다.11

현대의 가드레일은 크게 보안 가드레일(Security Guardrails)과 안전 가드레일(Safety Guardrails)로 구분되어 상호 보완적으로 작동한다.11 안전 가드레일이 유해하거나 독성이 있는 콘텐츠의 출력을 차단하는 데 집중한다면, 보안 가드레일은 시스템의 무결성을 보호하는 데 초점을 맞춘다. 특히 OWASP가 지목한 LLM01:2025(프롬프트 인젝션), LLM02:2025(민감 데이터 유출), LLM07:2025(시스템 프롬프트 유출), 그리고 LLM06:2025(과도한 권한 행사, Excessive Agency) 공격을 방어하기 위해 가드레일은 애플리케이션의 도메인 경계를 엄격히 설정하고, 공격자의 권한 상승 시도를 무력화하며, 독점적 데이터의 외부 유출을 원천 차단하는 역할을 수행한다.11

### **2.3. 심층 방어 (Defense-in-Depth) 5계층 아키텍처**

최신 에이전트 가드레일 아키텍처의 가장 두드러진 특징은 단일 실패점(Single Point of Failure)이 전체 시스템의 붕괴로 이어지는 것을 막기 위해, 전통적인 사이버 보안의 핵심 원칙인 '심층 방어(Defense-in-Depth)' 전략을 도입했다는 점이다.7 단일 가드레일 메커니즘에만 의존하는 것은 극도로 위험하며, 입력과 출력은 물론 런타임 실행의 전 과정을 아우르는 다중 방어막이 필수적이다.14

2026년에 발표된 에이전트 안전 아키텍처 논문(arXiv:2603.05344)에 따르면, 최첨단 가드레일 시스템은 모델의 추상적인 추론 단계부터 사용자 정의 스크립트 실행 단계에 이르기까지 점진적으로 촘촘해지는 5개의 독립적인 방어 계층으로 설계된다.13 각 계층은 독립적으로 작동하며, 어느 한 계층이 우회되더라도 나머지 계층이 공격을 탐지하고 차단하는 구조를 갖는다.

| 방어 계층 (Defense Layer) | 계층별 핵심 방어 메커니즘 및 제어 로직 | 방어 대상 및 해결하는 보안 위협 |
| :---- | :---- | :---- |
| **Layer 1: Prompt-Level Guardrails (프롬프트 수준 가드레일)** | 에이전트의 보안 정책, 행동 안전성 지침을 시스템 프롬프트에 주입. Git 워크플로우 통제, '편집 전 읽기(Read-before-edit)' 규칙, 오류 복구 프로세스 강제. | 입력 가드레일로서 프롬프트 인젝션(LLM01:2025) 방어, 악의적 의도 생성 차단 및 초기 컨텍스트 오염 방지.11 |
| **Layer 2: Schema-Level Tool Restrictions (스키마 수준 도구 제한)** | 서브 에이전트별로 허용된 도구의 화이트리스트(allowed\_tools) 적용. 플랜 모드(Plan-mode) 화이트리스트 강제 및 MCP(Model Context Protocol) 기반의 도구 발견 게이팅(Discovery Gating). | 에이전트의 과도한 권한 행사(Excessive Agency, LLM06:2025) 방지, 인가되지 않은 외부 시스템에 대한 원천적 접근 차단.11 |
| **Layer 3: Runtime Approval System (런타임 승인 시스템)** | 수동, 반자동, 자동 승인 레벨의 계층적 설정. 위험 패턴(Danger rules), 특정 명령어 및 접두사(Prefix) 규칙 감시. 지속적이고 영구적인 권한 검증 절차 수행. | 런타임 보호로서, 자율적이고 비가역적인 파괴적 시스템 명령어(예: 파일 삭제, 스키마 변경)의 무단 실행 방어.13 |
| **Layer 4: Tool-Level Validation (도구 수준 유효성 검증)** | 도구 실행 직전의 DANGEROUS\_PATTERNS 블랙리스트 기반 차단. 오래된 정보 읽기(Stale-read) 감지, 출력값 자르기(Output truncation) 및 엄격한 타임아웃 규칙 적용. | 시스템 과부하(DoS), 메모리 초과, 도구의 오남용, 그리고 오래된 컨텍스트에 기반한 잘못된 물리적 실행 차단.13 |
| **Layer 5: Lifecycle Hooks (생명주기 훅)** | 도구 실행 전 프로세스 차단(Exit code 2 활용). 인수 변이(Argument mutation) 검사, 안전한 JSON 표준 입력(stdin) 프로토콜을 통한 최종 명령어 무결성 검증. | 사용자 정의 스크립트 및 운영체제 레벨에서의 최종적인 악성 페이로드 실행 방어. 마지막 방어선(Last-line defense) 역할 수행.13 |

이러한 5계층 심층 방어 구조는 기존의 정적인 가드레일을 완전히 대체하였다. 모델 경화(Model hardening) 기법이나 지시어 계층 구조 미세조정(Instruction hierarchy fine-tuning)만으로는 악의적인 도구 결과물이 다른 도구의 결과를 덮어쓰는 정교한 섀도잉 공격(Shadowing attacks)을 막을 수 없다.14 따라서 정보 흐름 제어(Information flow control)와 지속적인 모니터링이 결합된 다층적 런타임 가드레일 체계야말로 2026년 에이전트 보안 설계의 가장 근본적인 원칙으로 채택되고 있다.14

## **3\. Scaffolding (스캐폴딩): 모델을 목적 지향적 에이전트로 조립하는 구조적 뼈대**

가드레일이 에이전트가 넘어서는 안 될 행동의 '경계선'과 보안 정책을 정의한다면, 'Scaffolding(스캐폴딩)'은 변덕스럽고 확률론적인 대규모 언어 모델을 신뢰할 수 있으며 명확한 목표 지향성(Goal-directed)을 지닌 작업자(Worker)로 변환하기 위해 외부에서 감싸는 '구조적 뼈대' 혹은 '지원 아키텍처'를 의미한다.16

### **3.1. 에이전트 조립의 기점: "첫 프롬프트 이전(Before the first prompt)"**

2025년과 2026년의 선도적인 프레임워크 문서 및 학술 논문들에서 스캐폴딩은 매우 엄밀한 시간적, 구조적 의미로 정의된다. 2026년 터미널 기반 AI 코딩 에이전트 구조를 다룬 OpenDev의 연구(arXiv:2603.05344)에 따르면, 스캐폴딩은 \*\*"에이전트가 첫 번째 사용자 프롬프트를 처리하기 전(Before the first prompt)에 완전히 조립(Assembled)되는 과정과 그 결과물로서의 아키텍처"\*\*를 지칭한다.13

단일 LLM의 API 호출은 그 자체로는 외부 데이터베이스를 쿼리할 수 없고, 과거의 대화를 기억하지 못하며, 복잡한 작업을 여러 단계로 쪼개어 계획하는 인지적 구조를 가지지 않는다.5 스캐폴딩은 바로 이러한 생형(Raw) 언어 모델의 근본적인 한계를 극복하기 위해 설계된 코드로, 관측과 행동의 루프(Observation/Action Loops)를 부여하여 모델의 능력을 증강시킨다.16 구체적으로 스캐폴딩 조립 단계에서는 에이전트의 성격을 규정하는 시스템 프롬프트가 컴파일되고, 에이전트가 활용할 수 있는 외부 도구들의 스키마(Tool Schemas)가 빌드되며, 필요한 경우 특정 도메인을 담당할 하위 에이전트(Subagents)들이 레지스트리에 등록되는 일련의 초기화 작업이 완결된다.13

OpenDev의 아키텍처 사례를 보면, 모든 에이전트(메인 에이전트 및 서브 에이전트)는 추상 베이스 클래스인 BaseAgent를 상속받은 MainAgent 인스턴스로 생성된다.13 스캐폴딩 과정에서 시스템은 allowed\_tools 매개변수를 통해 에이전트가 접근할 수 있는 도구를 필터링하여 스키마를 구성(ToolSchemaBuilder)하고, 메시지 주입을 위한 스레드 안전 큐를 생성하며, 일반 처리, 사고(Thinking), 비판(Critique), 비전 언어 모델(VLM) 등 다양한 역할을 수행할 HTTP 클라이언트 슬롯을 지연 초기화(Lazy initialization) 방식으로 설정한다.13 이 모든 구조적 조립이 끝난 후에야 비로소 에이전트의 대화 생명주기(Conversation lifecycle)가 시작될 수 있다.13

### **3.2. 인지적 제어 루프(Cognitive Control Loop)와 스캐폴딩의 유형**

스캐폴딩의 가장 핵심적인 기능은 에이전트가 정보를 처리하고 결정을 내리는 방식, 즉 '인지적 제어 루프(Cognitive Control Loop)'를 아키텍처적으로 정의하는 것이다.17 일반적인 검색 증강 생성(RAG) 파이프라인과 달리 에이전트 시스템은 루프 기반의 순환적 추론 과정을 거치며, 스캐폴딩은 목적하는 태스크의 성격에 따라 다양한 형태로 설계되어 에이전트의 행동 패턴을 결정짓는다.16

연구 자료에 나타난 대표적인 스캐폴딩의 유형과 그 특성은 다음과 같이 분류된다.16

| 스캐폴딩 유형 (Scaffold Type) | 구조적 특징 및 인지 메커니즘 | 최적 적용 사례 및 장단점 |
| :---- | :---- | :---- |
| **Baseline Scaffold (기준 스캐폴딩)** | 에이전트가 물리적 행동(Action)을 취하기 전에 반드시 계획(Planning) 및 반영(Reflection) 단계를 거치도록 강제하는 다단계 추론 루프 구조. | 복잡한 논리적 문제 해결에 적합. 에이전트의 추론 지원 능력을 극대화하지만 처리 지연(Latency)이 발생할 수 있음.16 |
| **Action-only Scaffold (행동 전용 스캐폴딩)** | 계획과 반영 단계를 완전히 제거하고, 외부 입력에 즉각적으로 반응하여 도구를 호출하는 단일 반응형 루프로 작동. | 원시적인 실행 능력을 테스트하거나 지연 시간이 극도로 짧아야 하는 단순 반복 태스크에 유용. 복잡한 추론 지원 부족.16 |
| **Pseudoterminal Scaffold (의사-터미널 스캐폴딩)** | 에이전트에게 실시간 상태를 유지하는 터미널 쉘(Shell)에 대한 직접적인 인터페이스를 제공하는 특수 아키텍처. | 다중 명령어 워크플로우 등 능동적인 시스템 상호작용이 필요한 태스크에 이상적. 명령어 집약적 환경에서 에이전트의 표현력 극대화.16 |
| **Web Search Scaffold (웹 검색 스캐폴딩)** | 에이전트의 정적 훈련 데이터를 넘어선 실시간 외부 지식이 필요할 때, 온디맨드 인터넷 쿼리 모듈을 지식 증강 능력으로 내재화한 구조. | 최신 정보 탐색 및 외부 데이터베이스 기반의 사실 관계 검증이 필수적인 동적 지식 워크플로우에 최적화.16 |

이러한 각 스캐폴딩 루프 내부에는 계획과 추론 모듈 외에도, 과거의 정보를 회상하기 위한 메모리 모듈(Memory & context), 외부 API 및 지식 베이스와의 도구 통합 모듈(Tool integration), 그리고 행동 결과를 평가하는 피드백 제어 모듈이 핵심 계층으로 제공되어 에이전트의 척추 역할을 수행한다.16

### **3.3. 컨텍스트 엔지니어링: 메모리 유지와 추론 붕괴의 방지**

스캐폴딩 설계에서 결코 간과할 수 없는 영역이 바로 컨텍스트 엔지니어링(Context Engineering)이다.13 에이전트가 복잡하고 장기적인 태스크를 수행하다 보면, 관측 결과와 도구의 반환값이 끝없이 누적되어 프롬프트 토큰의 한계를 위협하는 '컨텍스트 비대화(Context Bloat)' 현상이 발생한다.18 컨텍스트가 임계치를 넘어서면 모델의 주의력 메커니즘이 희석되어 추론 능력이 급격히 저하되거나 모델이 자신이 수행해야 할 본래의 지시사항을 잊어버리는 지시 사항 소실(Instruction Fade-out) 현상을 겪게 된다.13

이를 구조적으로 방지하기 위해 최신 스캐폴딩 아키텍처는 정교한 컨텍스트 관리 서브시스템을 내장한다. OpenDev 스캐폴딩의 사례를 살펴보면, 네 가지 핵심 서브시스템이 이 역할을 담당한다. 첫째, 시스템 프롬프트를 모듈화하여 조립하는 'Prompt Composer', 둘째, 세션 간 연속성을 보장하는 지식 축적 저장소인 'Memory', 셋째, 오래된 관측치나 덜 중요한 맥락 정보를 점진적으로 축소하여 토큰 예산을 동적으로 회수하는 5단계 'Compaction(압축)' 시스템, 넷째, 대화가 길어짐에 따라 에이전트가 본연의 행동 지침을 망각하지 않도록 이벤트 기반으로 문맥을 환기시켜 주는 'System Reminders' 메커니즘이다.13

또한, 멀티 에이전트 구조로 확장될 경우, 스캐폴딩을 구성하는 토큰 모니터링 미들웨어(Token Monitoring middleware)는 대화 문맥이 모델 제한의 특정 비율(Percentage)에 도달하는 즉시 자동적인 요약(Summarization)이나 절단(Truncation) 이벤트를 트리거하여 시스템의 붕괴를 사전에 차단한다.17 요컨대, 2026년 기준 스캐폴딩은 단순한 프롬프트 엔지니어링을 초월하여, 모델이 장시간 동안 일관된 인지 능력을 유지할 수 있도록 메모리와 지각을 관리하는 종합적인 초기화 인프라스트럭처로 진화하였다.16

## **4\. Harness (하네스): 런타임 오케스트레이션과 검증의 결정적 인프라**

2025년 중반까지만 해도 스캐폴딩과 하네스(Harness)라는 용어는 개발자들 사이에서 혼용되는 경향이 짙었다. 그러나 2026년에 들어서며 두 용어는 엄격한 아키텍처적 경계를 갖추게 되었다. 스캐폴딩이 에이전트의 첫 프롬프트 도착 이전 "초기 조립(Assembly)"과 정적 구조에 관한 것이라면, **Harness(하네스)는 그 이후 발생하는 역동적인 "런타임 오케스트레이션(Runtime Orchestration Layer)"의 실체**를 의미한다.13

하네스는 상태를 유지하지 못하는(Stateless) LLM을 상태가 지속되고, 도구를 능숙하게 사용하며, 스스로의 오류를 교정할 수 있는 영속적 에이전트로 탈바꿈시키는 핵심 런타임 인프라스트럭처이다.13 하네스는 스캐폴딩을 통해 조립된 핵심 추론 루프를 런타임에 감싸고(Wraps), 도구의 실제 실행(Dispatching tools)을 조율하며, 실행 중에 발생하는 거대한 컨텍스트를 압축하고, 앞서 언급된 가드레일의 안전 불변성(Safety Invariants)을 턴(Turn)마다 강제하는 등 "실행 시점의 모든 제어 로직"을 관장한다.13

### **4.1. Harness-First Engineering (하네스 우선 엔지니어링)의 폭발적 대두**

2026년 에이전트 기반 소프트웨어 개발의 성패를 가른 가장 강력한 패러다임은 'Harness-First Engineering(하네스 우선 엔지니어링)'의 등장이다.4 이 방법론은 인간 개발팀이 수동으로 코드를 검증할 수 있는 물리적 속도보다 AI 에이전트가 코드를 생성하고 시스템을 변경하는 속도가 압도적으로 빨라지면서 발생한 심각한 **'신뢰 병목(Trust Bottleneck)'** 현상을 극복하기 위해 탄생했다.4

과거의 프로그래머들이 어셈블리어를 직접 작성하던 시절을 지나 컴파일러의 자동화를 신뢰하게 된 것은 컴파일러가 '엄격하고 정밀한 문법적 의미(Semantics)'를 바탕으로 동작했기 때문이다.4 반면 AI 에이전트는 무제한적인 자연어를 입력받아 실행 가능한 코드로 변환한다. 이 과정에서 에이전트가 명확한 명세 없이 느낌이나 분위기만으로 코드를 짜는 이른바 "바이브 코딩(Vibe-coding)"을 수행하고, 이를 검증 절차 없이 곧바로 프로덕션 환경에 배포해 버리는 "욜로 배포(Yolo-deploys)" 사태가 속출했다.4

이러한 재앙적 상황을 통제하기 위해 엔지니어링의 패러다임이 급변했다. 인간 리뷰어가 에이전트가 생성한 코드를 한 줄씩 읽는 수동적이고 확장 불가능한 방식에서 벗어나, 엔지니어의 핵심 역량은 \*\*"수 초 내에 높은 신뢰도로 생성된 코드의 정합성을 자동으로 판별할 수 있는 검증 제약 조건, 즉 '하네스(Harness)'를 설계하는 것"\*\*으로 이동했다.4 인간은 더 이상 에이전트가 수정한 코드의 차이(Diff)를 직접 읽지 않는다. 대신 하네스가 출력한 결과물(어떤 불변성이 통과되었는지, 어떤 시뮬레이션 시드가 테스트되었는지, 원격 측정 데이터가 무엇을 확인했는지)을 EXPLAIN ANALYZE 결과를 읽듯 분석하고 아키텍처를 승인하는 역할을 담당하게 되었다.4

### **4.2. 하네스 기반의 4대 검증 루프 방법론**

하네스 중심의 개발론에서 검증(Verification)은 인간의 수동 검사에서 벗어나 하네스가 주도하는 지속적인 기계적 '검증 루프(Verification Loop)'로 진화했다. 에이전트가 코드를 생성하면 하네스가 이를 즉각 검증하고, 프로덕션의 원격 측정 데이터가 실제 성능을 확인하며, 오류가 발견되면 피드백 루프를 통해 하네스를 업데이트한 뒤 에이전트가 재시도하는 순환 체계가 완성된 것이다.4

Datadog 블로그 및 산업 리서치에 따르면, 시스템의 복잡도와 실패 비용의 심각성에 따라 런타임 하네스에 탑재되는 자동화된 검증 방법론은 크게 네 가지로 분류된다.4

| 검증 방법론 (Verification Method) | 하네스 내 작동 원리 및 특징 | 산업 적용 사례 및 정량적 성과 |
| :---- | :---- | :---- |
| **결정론적 시뮬레이션 테스트 (DST)** | 에이전트가 수정한 코드를 바탕으로 수백만 번의 시뮬레이션을 실행하여 시스템의 핵심 보장이 무너지지 않는지 결정론적으로 검증하는 극도의 안전망. | **Helix 프로젝트:** 에이전트가 인간 리뷰어보다 월등히 빠르게 개발을 진행하면서도 Kafka 의미론적 보장을 훼손하지 않고 피크 디스크 처리량의 93%를 달성.4 |
| **공식 명세 및 불변성 (Formal Specs & Invariants)** | 시스템에서 반드시 참(True)이어야 하는 명시적 규칙(불변성)을 인간 엔지니어가 하네스에 하드코딩. 하나의 불변성을 추가함으로써 향후 에이전트가 유발할 수 있는 버그 클래스 전체를 영구적으로 차단하여 시간이 지날수록 가치가 복리처럼 증가함. | **Salesforce 판매 에이전트:** 스키마, 허용된 필드, 특정 의도에 필수적인 제약 조건을 하네스에 명시. 모호하거나 위험한 형태의 쿼리를 런타임에 즉각 거부하여 데이터 오염을 완벽히 방어.8 |
| **섀도우 평가 (Shadow Evaluation)** | 에이전트가 진화시킨 코드를 실제 라이브 트래픽의 복제본을 활용해 '섀도우' 환경에서 테스트. 모델링된 동작과 실제 세계의 실행 결과가 완벽히 일치하는지 배포 전 최종 확인. | **redis-rust:** 에이전트가 생성한 Redis 호환 서버에 섀도우 검증 계층을 구축하여, 프로덕션 수준의 대기 시간을 유지하면서도 메모리 사용량을 87%나 획기적으로 감축.4 |
| **관측성 기반 피드백 루프 (Observability-driven Feedback)** | 로그, 메트릭, 분산 추적(Traces) 등 프로덕션의 원격 측정 데이터를 하네스 루프의 최종 통제 계층으로 활용. 관측성이 없으면 루프가 닫히지 않는다는 원칙 하에 모델과 현실의 불일치를 실시간 교정. | **BitsEvolve (Datadog):** LLM 기반 진화형 옵티마이저. 민감 데이터 스캐닝에서 1.53배, 시계열 예측 모델(Toto)에서 1.57배, 수집 기능에서 10배의 놀라운 속도 향상을 검증과 함께 달성.4 |

### **4.3. 복잡한 스캐폴딩을 압도하는 심플한 하네스의 힘**

최신 에이전트 개발 트렌드에서 얻을 수 있는 가장 중요한 교훈 중 하나는, "심플한 하네스가 복잡한 스캐폴딩보다 종종 더 뛰어난 성과를 낸다"는 점이다.2 파운데이션 모델의 기저 지능은 이미 훌륭하며, 핵심은 모델의 변동성을 제어하고 작업을 최적화하는 하네스의 튜닝에 있다.2

LangChain의 심층 연구(Improving Deep Agents with harness engineering)에 따르면, 코딩 에이전트 deepagents-cli의 평가에서 기반 언어 모델을 gpt-5.2-codex로 완전히 고정시킨 채로 하네스의 시스템 프롬프트, 도구, 그리고 미들웨어(자기 검증 및 추적 기능 강화)의 노브(Knob)만을 튜닝하는 실험을 진행했다.20 그 결과 Terminal Bench 2.0 벤치마크 점수가 52.8점에서 66.5점으로 무려 13.7점이나 상승하며, 에이전트의 성능 순위가 상위 30위 밖에서 최상위권인 Top 5로 도약하는 쾌거를 이루었다.20 이는 에이전트의 성패가 모델 자체의 업그레이드보다 하네스의 설계 역량에 달려 있음을 방증한다.

따라서 2026년 하네스 설계 철학은 세 가지 핵심 원칙으로 수렴했다.2 첫째, \*\*최소한의 필수 개입(Minimal necessary intervention)\*\*이다. 모호함은 모델이 스스로 판단하도록 맡기되, 돌이킬 수 없는 파괴적 행동이나 보안 경계를 넘을 때만 하네스가 단호하게 개입한다. 둘째, \*\*점진적 노출(Progressive disclosure)\*\*이다. 초기 세션에는 극히 제한된 도구와 권한만 부여하고, 에이전트의 성과가 신뢰성을 입증함에 따라 점진적으로 권한을 확장한다. 셋째, 인간의 승인(Human-in-the-loop), 파일 시스템 접근, 서브 에이전트 호출 등은 전적으로 하네스 인프라를 통해 중앙 통제하는 것이다.2

이러한 설계 원칙은 수 시간, 수일에 걸쳐 작동하는 장기 실행 에이전트(Long-running agents)의 경우 더욱 빛을 발한다. Anthropic의 연구는 코딩 에이전트가 겪는 전형적인 4가지 실패 모드와 이를 해결하기 위한 하네스의 통제 메커니즘을 다음과 같이 분석했다.21

| 장기 실행 에이전트의 전형적 실패 모드 | 하네스를 통한 런타임 제어 및 해결책 (Harness Solutions) |
| :---- | :---- |
| 프로젝트 전체가 완성되지 않았음에도 너무 일찍 승리(완료)를 선언해버림. | 입력 명세를 바탕으로 세부 기능 리스트가 담긴 구조화된 JSON 파일(tests.json)을 강제 설정. 하네스가 에이전트에게 "한 번에 단 하나의 기능만" 작업하도록 제한 루프 강제. |
| 세션을 종료하면서 환경을 버그가 있거나 문서화되지 않은 엉망인 상태로 방치함. | 초기 git 저장소와 진행 노트를 필수적으로 작성하도록 강제. 세션 시작 시 진행 노트와 커밋 로그를 읽고 개발 서버의 기본 테스트를 실행하도록 하네스 훅 설정. 세션 종료 시 git 커밋 강제화. |
| 꼼꼼한 테스트 없이 기능의 상태를 성급하게 "완료(Done)"로 마킹함. | 기능 리스트 파일 기반의 철저한 자가 검증(Self-verify) 루프 의무화. 하네스의 테스트 모듈을 통과한 경우에만 "통과(Passing)" 마킹을 허용. |
| 앱 실행 방법을 찾지 못해 컨텍스트 내에서 막대한 시간을 낭비함. | 스캐폴딩 단계에서 init.sh 스크립트를 작성하게 하고, 세션 시작 시 하네스가 이 스크립트를 우선적으로 읽고 실행 환경을 구성하도록 프로세스 정립. |

## **5\. Orchestration Layer (오케스트레이션 계층): 다중 에이전트 체제의 중앙 지휘 평면**

단일 에이전트 내에서 가드레일이 방어를, 스캐폴딩이 골격을, 하네스가 런타임 검증을 충실히 수행한다고 하더라도, 현대 엔터프라이즈 환경의 거대하고 복합적인 프로세스를 단일 에이전트 모델 하나에 전담시키는 것은 태생적인 한계를 수반한다. 단일 에이전트 시스템(Single-agent system)에 다수의 역할을 몰아넣을 경우, 도메인 과부하(Domain overload)로 인한 과도한 일반화, 다단계 추론의 중첩으로 인한 심각한 지연 현상(Latency), 복잡한 거버넌스 얽힘, 그리고 다양한 민감 데이터 저장소에 대한 중앙 집중식 접근 허용으로 인한 막대한 보안 노출 위험이 발생한다.22

이러한 중앙 집중화된 AI의 한계를 극복하고 확장성(Scalability)을 확보하기 위해, 시스템 설계의 패러다임은 역할이 분리된 여러 에이전트가 협력하는 다중 에이전트 시스템(Multi-Agent Systems, MAS)으로 진화했다.22 그리고 이 독립적이고 전문화된 에이전트들 사이의 타이밍 조율, 정보 교환, 상태 관리, 정책 집행을 총괄하며 시스템을 하나의 유기적인 목표 지향적 집단으로 묶어내는 제어 평면(Control plane)이 바로 \*\*'Orchestration Layer(오케스트레이션 계층)'\*\*이다.23

### **5.1. 역할 기반 스쿼드(Squad)의 구성과 오케스트레이션의 효과**

2026년의 비즈니스 프로세스 자동화는 특정 부서를 넘어서 외부 이해관계자와 수많은 레거시 시스템을 가로질러 동시에 진행된다.26 오케스트레이션 계층은 단일 목적의 거대 에이전트를 폐기하고, 인간의 전문 조직 구조를 모방하여 복잡한 목표를 구조화된 워크플로우로 분해(Task decomposition)한 뒤, 고도로 최적화된 전문 에이전트 '스쿼드(Squad)'를 구성하여 작업을 할당한다.22

예를 들어 기업의 조달 워크플로우(Procurement workflow)는 더 이상 단일 챗봇이 처리하지 않는다. 대신, 외부 벤더와 조건을 논의하는 '협상 에이전트', 협상된 계약 조건의 적법성을 검증하는 '법무 에이전트', 사내 규제 및 보안 요구사항을 대조하는 '컴플라이언스 에이전트', 최종 트랜잭션을 실행하는 '결제 처리 에이전트', 그리고 이 모든 스쿼드의 작업을 분배하고 결과를 취합하여 인간 결재권자에게 보고하는 '관리자(Manager) 에이전트'가 팀을 이루어 동시다발적으로 작업을 수행한다.27 오케스트레이션 계층은 이들 사이에서 동적인 배선(Dynamic wiring), 에이전트 간의 교차 메모리 스토리지 공유, 그리고 책임의 이관(Transferring responsibilities)을 담당하는 배관(Plumbing) 역할을 수행한다.24

다중 에이전트 오케스트레이션의 도입 효과는 파괴적이다. IBM 리서치의 2026년 데이터에 따르면, 잘 설계된 오케스트레이션 계층을 기반으로 다중 에이전트 시스템을 도입한 기업은 기존 베이스라인 대비 압도적인 성능 향상을 기록했다.30

| 평가지표 (Performance Metric) | 단일 에이전트 (Single Agent) 방식 | 다중 에이전트 시스템 (Multi-Agent MAS) | 오케스트레이션의 기술적 근거 |
| :---- | :---- | :---- | :---- |
| **시스템 아키텍처** | 모든 역할을 수행하려는 제너럴리스트 | 정의된 역할을 수행하는 특화된 전문가 스쿼드 | 역할 분리로 인한 도메인 과부하 해소 및 평행 추론 기능 활용 22 |
| **프로세스 이관 (Hand-offs)** | 베이스라인 (복잡성 높음) | **45% 감소** | 오케스트레이션 계층의 상태 관리(State management) 유닛을 통한 매끄러운 책임 이관 25 |
| **의사 결정 속도 (Decision speed)** | 베이스라인 (병목 발생) | **3배 향상 (3x faster)** | 다중 에이전트의 병렬적 추론(Parallel reasoning) 및 동시성 작업 분배 22 |
| **오류율 (Error rate)** | 베이스라인 (과도한 일반화 오류) | **60% 감소** | 특정 도메인에 하이퍼 최적화된 지식 및 도구 접근으로 환각 최소화 22 |
| **처리량 (Throughput)** | 1x 수준 | **10-50배 (10-50x) 급증** | 오케스트레이터의 인텔리전트 라우팅 및 동적 스케일링을 통한 탄력적 자원 할당 24 |

### **5.2. 관측성(Observability)과 지식 그래프(Knowledge Graphs)의 결합**

오케스트레이션 계층이 단순히 작업만 나누어 주는 수준을 넘어 지능적인 제어 평면으로 기능할 수 있는 이유는 관측성(Observability)과 정보 도메인(Information Domain)이 깊숙이 결합되어 있기 때문이다.31 오케스트레이션 계층을 통과하는 애플리케이션, 데이터, 개별 에이전트 간의 모든 상호작용은 로그(Discrete events), 메트릭(성능 지표), 트레이스(단일 요청의 이동 경로) 형태로 모니터링되고 추적된다.31 다중 에이전트 워크플로우 전반에 걸친 이 포괄적인 분산 추적 데이터는 장애를 진단하는 데 쓰일 뿐만 아니라, 오케스트레이터가 시스템의 현재 상태를 파악하여 가장 최적의 에이전트에게 작업을 라우팅하는 실시간 계획의 근거가 된다.31

여기에 더해, 가장 고도화된 에이전트 아키텍처는 오케스트레이션 엔진 내에 지식 그래프(Knowledge Graphs)를 통합하여 활용한다.33 오케스트레이터는 지식 그래프의 노드와 엣지 관계를 탐색하여 특정 태스크를 실행하기 전에 선행되어야 할 전제조건이 모두 충족되었는지 검증한다. 또한 에이전트가 호출할 수 있는 수많은 API나 데이터베이스 중 주어진 맥락에 가장 부합하는 도구를 추론해 내는 데에도 그래프 탐색 결과를 활용함으로써, 단일 단계의 사고를 넘어 복수의 함축적 단계를 거치는 고차원적 논리 추론(Multi-step reasoning)을 가능하게 한다.33

## **6\. 오케스트레이션의 확장: 상호운용성을 위한 개방형 통신 프로토콜 (MCP & A2A)**

다중 에이전트 시스템의 가능성이 입증됨에 따라, 각기 다른 벤더(Google, Microsoft, IBM 등)나 프레임워크(LangChain, AutoGPT 등)에서 개발된 이질적인 에이전트들이 서로 원활하게 소통하고 협업해야 할 필요성이 대두되었다.34 독점적인 생태계에 갇힌 에이전트들은 조직의 사일로(Silo)를 유발할 뿐이었다. 이에 대응하여 2025년과 2026년 산업계는 Agentic AI Foundation(AAIF)이라는 조직을 Linux Foundation 산하에 출범시켰다.35 AAIF는 거대 테크 기업들의 개별 혁신 속도와 기존 표준화 기구의 느린 대응 사이의 간극을 메우며, 상호운용 가능한 에이전트 통신 프로토콜을 정립하는 중립적 거버넌스의 본산으로 자리 잡았다.36

이러한 개방형 표준화 흐름을 주도하며 오케스트레이션 계층의 신경망을 완성한 양대 핵심 프로토콜이 바로 \*\*MCP(Model Context Protocol)\*\*와 **A2A(Agent-to-Agent) Protocol**이다. 이 두 프로토콜은 상호 경쟁 관계가 아니라, 에이전트 생태계를 완성하는 보완적 관계로 작동한다.34

### **6.1. MCP (Model Context Protocol): 외부 지식과 도구의 연결 표준**

2025년 Anthropic, OpenAI, Block 등에 의해 공동 개발되어 AAIF에 기증된 MCP는 LLM 기반의 AI 에이전트가 외부의 기업 데이터베이스, SaaS 애플리케이션, 그리고 실행 가능한 도구 자원에 안전하고 동적으로 접근할 수 있도록 설계된 개방형 통신 규약이다.37 IBM의 비유에 따르면, 하드웨어 기기들을 범용적으로 연결해 주는 USB-C 포트와 같이, MCP는 다양한 도구와 데이터 소스가 에이전트에게 맥락(Context)과 능력을 제공하는 방식을 완벽히 표준화하였다.5

MCP의 확산 속도는 경이로운 수준이다. 기증 후 1년여 만인 2026년 기준, 10,000개 이상의 활성 공용 MCP 서버가 생태계에 구축되었으며, Claude, ChatGPT, Gemini, Microsoft Copilot은 물론 Visual Studio Code 등 주요 플랫폼에 모두 채택되었다.41 Python과 TypeScript를 기반으로 한 공식 SDK는 월 9,700만 회 이상의 다운로드를 기록하며 사실상의 산업 표준으로 굳어졌다.41 개발자는 더 이상 각 시스템의 API 스펙에 맞춰 커스텀 통합 코드를 짤 필요 없이, MCP라는 통일된 규약을 통해 에이전트에게 지식과 도구를 무한히 장착(Equipping)할 수 있게 되었다.5

### **6.2. A2A (Agent-to-Agent) Protocol: 자율적 협력과 소통의 공용어**

MCP가 에이전트 개인의 능력과 지식을 극대화하는 프로토콜이라면, A2A 프로토콜은 서로 다른 플랫폼에서 개발된 독립적인 에이전트들이 '보편적 번역기(Universal Translator)'를 통해 소통하고 팀으로서 공동의 목표를 향해 협업하도록 돕는 통신 프레임워크이다.34 구글 클라우드와 IBM 주도로 2025년 4월 출범하여 Linux Foundation 산하 프로젝트로 안착한 A2A 프로토콜은 멀티 에이전트 워크플로우를 진정한 엔터프라이즈급 아키텍처로 격상시켰다.42

A2A 프로토콜은 새로운 독점 기술을 강요하는 대신 HTTP/HTTPS, JSON-RPC 2.0, Server-Sent Events(SSE) 등 인터넷 생태계에 이미 널리 통용되는 웹 표준을 재활용하여 구현의 복잡성을 대폭 낮추었다.34 특히 엔터프라이즈 환경에서의 통신 신뢰성을 담보하기 위해 다음과 같은 획기적인 기능들을 사양(Specification) 내에 포함하고 있다.34

1. **Agent Card (에이전트 디지털 신원 보증):** 특정 에이전트의 능력(Capabilities), 정체성, 통신 요구사항을 JSON 매니페스트 형태로 상세히 정의하여, 에이전트 간의 상호 발견(Discovery) 프로세스를 자동화한다 (.well-known/agent.json 규약 활용).  
2. **비동기 통신과 8단계 작업 수명주기 관리:** 텍스트 생성을 넘어 수 시간이 걸릴 수 있는 장기 실행 작업(Long-running tasks)을 관리하기 위해, A2A 프로토콜은 작업 요청부터 진행 중, 추가 정보 대기, 완료에 이르는 8단계의 상태 수명주기(Task Lifecycle)를 공식적으로 지원한다.  
3. **내장형 엔터프라이즈 보안 (Built-in Security):** 에이전트 간 통신의 기밀성과 무결성을 보장하기 위해 OAuth 2.0 기반의 인증과 상호 TLS(mTLS) 암호화를 프로토콜 기본 사양으로 채택하여, 제로 트러스트(Zero Trust) 아키텍처 환경에서도 안전한 상호작용을 보장한다.  
4. **다중 양식(Multi-modal) 지원:** 단순 텍스트 교환에 국한되지 않고, 에이전트들이 오디오, 비디오, 구조화된 이진 데이터 등 전 범위의 데이터를 자유롭게 주고받으며 창의적인 문제 해결을 도모할 수 있다.

이처럼 조직은 MCP를 통해 각 에이전트를 외부 리소스와 정교하게 배선하고, A2A 프로토콜을 오케스트레이션 계층의 신경망으로 활용하여 벤더에 종속되지 않는 진정한 의미의 분산형 지능망을 완성해 내고 있다.34

## **7\. 심층 통찰 (2차 및 3차적 시사점)**

본 보고서에 분석된 자료들을 종합해 보면, 2026년의 에이전트 아키텍처는 개별 용어들의 단순한 집합을 초월하여 극도로 유기적인 엔지니어링 생태계로 진화했음을 확인할 수 있다. 이러한 진화는 기술과 산업 전반에 걸쳐 중대한 함의를 던진다.

**첫째, 경쟁력(Moat)의 원천이 '지능'에서 '인프라'로 완전히 이동했다.** 과거에는 가장 파라미터가 크고 지능적인 파운데이션 모델을 보유한 기업이 시장을 독점할 것이라 예측되었다. 그러나 오픈소스 모델들의 성능이 상향 평준화되고, 아무리 뛰어난 모델이라 할지라도 '환각'과 '망각'이라는 본질적 한계를 지닌다는 사실이 명백해지면서 상황은 역전되었다. LangChain과 Datadog의 사례에서 보듯 4, 진정한 차별적 경쟁 우위는 모델이 아니라, 에이전트의 인지 루프를 정교하게 묶어내는 스캐폴딩 역량, 런타임에서 결정론적 검증을 자동 수행하는 하네스 설계 능력, 그리고 수십 개의 전문 에이전트를 병렬적으로 지휘하는 오케스트레이션 계층의 고도화에 있다. 인프라를 지배하는 자가 AI의 통제권을 쥐게 된 것이다.2

**둘째, '생물학적 메타포(Biological Metaphor)'를 통한 시스템 진화의 완성이다.**

언어 모델이 인간의 단편적 대뇌피질을 흉내 낸 '뇌의 일부'라면, 본 연구에서 다룬 4대 요소는 이 불완전한 뇌가 현실 세계에서 지속 가능하게 기능할 수 있도록 돕는 생물학적 기관들과 같다. 스캐폴딩(Scaffolding)은 인지 구조를 지탱하는 \*\*'골격과 장기 기억소'\*\*이며, 하네스(Harness)는 실시간으로 감각을 수용하고 반사 신경을 통해 오류를 교정하는 \*\*'중추 및 말초 신경계'\*\*다. 더불어 가드레일(Guardrails)은 외부의 악의적 공격(바이러스)이나 내부의 치명적 돌연변이로부터 시스템의 완전성을 지키는 5겹의 **'면역 체계'** 역할을 하며, 오케스트레이션 계층(Orchestration Layer)과 통신 프로토콜(A2A)은 단일 생명체를 넘어 개체 간의 유기적 협업을 관장하는 \*\*'고도화된 사회적 언어와 거버넌스'\*\*로 기능한다.

이러한 인프라의 결합 없이는 AI 시스템이 단순한 실험실의 장난감을 넘어 복잡하고 규제가 엄격한 금융, 의료, 국방, 그리고 대형 제조의 미션 크리티컬(Mission-critical) 환경에 편입되는 것은 불가능하다.11

## **8\. 결론**

2025년부터 2026년에 이르는 격동의 시기 동안, 자율형 AI 에이전트 시스템은 '어떻게 인간처럼 사고할 것인가'라는 철학적 명제에서 벗어나 '어떻게 현실의 시스템과 안전하고 효과적으로 상호작용하며 복잡한 태스크를 완수할 것인가'라는 철저한 엔지니어링의 영역으로 완전히 정착했다.

에이전트는 첫 프롬프트가 주어지기 전 **Scaffolding**을 통해 자신만의 도구 스키마, 컨텍스트 압축 메커니즘, 장기 메모리 구조를 조립하여 확고한 인지적 골격을 형성한다. 본격적인 런타임이 개시되면 **Harness**가 개입하여 에이전트의 불확실한 도구 사용과 코드 생성을 결정론적 시뮬레이션 및 관측성 피드백 루프를 통해 초 단위로 검증하며 오케스트레이션한다. 이 실행의 모든 궤적은 5계층의 심층 방어막을 두른 **Guardrails**에 의해 지속적으로 감시되어, 권한 상승, 데이터 유출, 시스템 훼손의 위험으로부터 조직의 자산을 완벽히 격리한다. 궁극적으로 이 통제된 개별 단위의 전문 에이전트들은 **Orchestration Layer**의 거대한 제어 평면 위에 배치되며, MCP와 A2A라는 강력한 글로벌 개방형 표준 프로토콜을 매개로 서로 역할을 분담하고 협력하여 기하급수적으로 향상된 처리량과 의사 결정 속도를 달성해 낸다.

요컨대, 이 네 가지 핵심 아키텍처 용어는 개별적으로 흩어진 기술 단위가 아니라, 비결정론적이고 자유분방한 확률형 AI 모델을 결정론적이고 감사 가능하며 법적 책임 소재를 명확히 다룰 수 있는 '엔터프라이즈급 자율 노동력(Enterprise-grade autonomous workforce)'으로 승격시키는 하나의 완결된 통합 제어 인프라스트럭처로 귀결된다. 다가오는 미래, 성공적인 AI 전환(AX)을 꿈꾸는 모든 기업은 최신 파운데이션 모델의 도입 여부에 집중하기보다, 자사 고유의 비즈니스 도메인에 부합하는 정교한 스캐폴딩, 강력한 하네스, 빈틈없는 가드레일, 그리고 상호운용 가능한 오케스트레이션 계층을 어떻게 구축하고 내재화할 것인지에 모든 기술 전략의 무게중심을 두어야 할 것이다.

#### **참고 자료**

1. What Is an Agent Harness? The Key to Reliable AI | Salesforce, 3월 13, 2026에 액세스, [https://www.salesforce.com/agentforce/ai-agents/agent-harness/](https://www.salesforce.com/agentforce/ai-agents/agent-harness/)  
2. 2025 Was Agents. 2026 Is Agent Harnesses. Here's Why That Changes Everything., 3월 13, 2026에 액세스, [https://aakashgupta.medium.com/2025-was-agents-2026-is-agent-harnesses-heres-why-that-changes-everything-073e9877655e](https://aakashgupta.medium.com/2025-was-agents-2026-is-agent-harnesses-heres-why-that-changes-everything-073e9877655e)  
3. Chapter 3: Architectures for Building Agentic AI \- arXiv.org, 3월 13, 2026에 액세스, [https://arxiv.org/html/2512.09458v1](https://arxiv.org/html/2512.09458v1)  
4. Closing the verification loop: Observability-driven harnesses for ..., 3월 13, 2026에 액세스, [https://www.datadoghq.com/blog/ai/harness-first-agents/](https://www.datadoghq.com/blog/ai/harness-first-agents/)  
5. What is Model Context Protocol (MCP)? \- IBM, 3월 13, 2026에 액세스, [https://www.ibm.com/think/topics/model-context-protocol](https://www.ibm.com/think/topics/model-context-protocol)  
6. Mastering AI Agents: Your Ultimate Handbook to Agentic AI, 3월 13, 2026에 액세스, [https://www.indium.tech/mastering-agentic-ai/](https://www.indium.tech/mastering-agentic-ai/)  
7. Security & Guardrails in AI Systems (2025): A Complete Engineering Guide | by Dewasheesh Rana | Medium, 3월 13, 2026에 액세스, [https://medium.com/@dewasheesh.rana/%EF%B8%8F-security-guardrails-in-ai-systems-2025-a-complete-engineering-guide-from-layman-pro-f9383336c8ab](https://medium.com/@dewasheesh.rana/%EF%B8%8F-security-guardrails-in-ai-systems-2025-a-complete-engineering-guide-from-layman-pro-f9383336c8ab)  
8. The Missing Layer In AI Agents: The 'Harness' That Makes Them Reliable \- Forbes, 3월 13, 2026에 액세스, [https://www.forbes.com/councils/forbestechcouncil/2026/02/20/the-missing-layer-in-ai-agents-the-harness-that-makes-them-reliable/](https://www.forbes.com/councils/forbestechcouncil/2026/02/20/the-missing-layer-in-ai-agents-the-harness-that-makes-them-reliable/)  
9. What are AI guardrails? Evolving safety beyond foundational model providers \- F5, 3월 13, 2026에 액세스, [https://www.f5.com/company/blog/what-are-ai-guardrails-evolving-safety-beyond-foundational-model-providers](https://www.f5.com/company/blog/what-are-ai-guardrails-evolving-safety-beyond-foundational-model-providers)  
10. AI Guardrails Will Stop Being Optional in 2026 \- StateTech Magazine, 3월 13, 2026에 액세스, [https://statetechmagazine.com/article/2026/01/ai-guardrails-will-stop-being-optional-2026](https://statetechmagazine.com/article/2026/01/ai-guardrails-will-stop-being-optional-2026)  
11. LLM guardrails: Best practices for deploying LLM apps securely \- Datadog, 3월 13, 2026에 액세스, [https://www.datadoghq.com/blog/llm-guardrails-best-practices/](https://www.datadoghq.com/blog/llm-guardrails-best-practices/)  
12. The 2025 AI Agent Index Documenting Technical and Safety Features of Deployed Agentic AI Systems \- arXiv.org, 3월 13, 2026에 액세스, [https://arxiv.org/html/2602.17753v1](https://arxiv.org/html/2602.17753v1)  
13. Building AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned \- arXiv.org, 3월 13, 2026에 액세스, [https://arxiv.org/html/2603.05344v1](https://arxiv.org/html/2603.05344v1)  
14. The Attack and Defense Landscape of Agentic AI: A Comprehensive Survey \- arXiv, 3월 13, 2026에 액세스, [https://arxiv.org/html/2603.11088v1](https://arxiv.org/html/2603.11088v1)  
15. AI Guardrails | Guild.ai, 3월 13, 2026에 액세스, [https://www.guild.ai/glossary/ai-guardrails](https://www.guild.ai/glossary/ai-guardrails)  
16. Agent scaffolding: Architecture, types and enterprise applications \- ZBrain, 3월 13, 2026에 액세스, [https://zbrain.ai/agent-scaffolding/](https://zbrain.ai/agent-scaffolding/)  
17. Design Patterns for Agentic AI and Multi-Agent Systems \- AppsTek Corp, 3월 13, 2026에 액세스, [https://appstekcorp.com/blog/design-patterns-for-agentic-ai-and-multi-agent-systems/](https://appstekcorp.com/blog/design-patterns-for-agentic-ai-and-multi-agent-systems/)  
18. Building AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned | alphaXiv, 3월 13, 2026에 액세스, [https://www.alphaxiv.org/overview/2603.05344](https://www.alphaxiv.org/overview/2603.05344)  
19. LangGraph vs CrewAI vs AutoGen: Top 10 AI Agent Frameworks | Articles \- O-mega.ai, 3월 13, 2026에 액세스, [https://o-mega.ai/articles/langgraph-vs-crewai-vs-autogen-top-10-agent-frameworks-2026](https://o-mega.ai/articles/langgraph-vs-crewai-vs-autogen-top-10-agent-frameworks-2026)  
20. Improving Deep Agents with harness engineering \- LangChain Blog, 3월 13, 2026에 액세스, [https://blog.langchain.com/improving-deep-agents-with-harness-engineering/](https://blog.langchain.com/improving-deep-agents-with-harness-engineering/)  
21. Effective harnesses for long-running agents \- Anthropic, 3월 13, 2026에 액세스, [https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)  
22. Multi-Agent Systems & AI Orchestration Guide 2026 \- Codebridge, 3월 13, 2026에 액세스, [https://www.codebridge.tech/articles/mastering-multi-agent-orchestration-coordination-is-the-new-scale-frontier](https://www.codebridge.tech/articles/mastering-multi-agent-orchestration-coordination-is-the-new-scale-frontier)  
23. Multi-Agent AI System Architecture: Scalable Design Guide \- Codebridge, 3월 13, 2026에 액세스, [https://www.codebridge.tech/articles/multi-agent-ai-system-architecture-how-to-design-scalable-ai-systems-that-dont-collapse-in-production](https://www.codebridge.tech/articles/multi-agent-ai-system-architecture-how-to-design-scalable-ai-systems-that-dont-collapse-in-production)  
24. What is AI Agent Orchestration? Enterprise Leader's Guide (2026) \- OneReach, 3월 13, 2026에 액세스, [https://onereach.ai/blog/what-is-ai-agent-orchestration/](https://onereach.ai/blog/what-is-ai-agent-orchestration/)  
25. The Orchestration of Multi-Agent Systems: Architectures, Protocols, and Enterprise Adoption, 3월 13, 2026에 액세스, [https://arxiv.org/html/2601.13671v1](https://arxiv.org/html/2601.13671v1)  
26. BPA trends 2026: How agentic workflows and multi-agent orchestration are reshaping business process automation | Moxo, 3월 13, 2026에 액세스, [https://www.moxo.com/blog/business-process-automation-trends](https://www.moxo.com/blog/business-process-automation-trends)  
27. 10 agentic AI trends for 2026 \- Moxo, 3월 13, 2026에 액세스, [https://www.moxo.com/blog/agentic-ai-trends](https://www.moxo.com/blog/agentic-ai-trends)  
28. The 5 Best AI Agent Frameworks for Scalable Workflows | Workday US, 3월 13, 2026에 액세스, [https://www.workday.com/en-us/perspectives/ai/2026/01/top-ai-agent-frameworks.html](https://www.workday.com/en-us/perspectives/ai/2026/01/top-ai-agent-frameworks.html)  
29. Multi-Agent Frameworks Explained for Enterprise AI Systems \[2026\], 3월 13, 2026에 액세스, [https://www.adopt.ai/blog/multi-agent-frameworks](https://www.adopt.ai/blog/multi-agent-frameworks)  
30. Multi-Agent AI Systems for Enterprise 2026: Orchestration at Scale \- Swfte AI, 3월 13, 2026에 액세스, [https://www.swfte.com/blog/multi-agent-ai-systems-enterprise](https://www.swfte.com/blog/multi-agent-ai-systems-enterprise)  
31. AI Agent Potential – How Orchestration and Contextual Foundations Can Reshape (Re)Insurance Workflows \- Gen Re, 3월 13, 2026에 액세스, [https://www.genre.com/us/knowledge/publications/2025/december/ai-agent-potential-en](https://www.genre.com/us/knowledge/publications/2025/december/ai-agent-potential-en)  
32. The Agent Harness Is the Architecture (and Your Model Is Not the Bottleneck) \- Medium, 3월 13, 2026에 액세스, [https://medium.com/@epappas/the-agent-harness-is-the-architecture-and-your-model-is-not-the-bottleneck-5ae5fd067bb2](https://medium.com/@epappas/the-agent-harness-is-the-architecture-and-your-model-is-not-the-bottleneck-5ae5fd067bb2)  
33. The Role of Knowledge Graphs in Building Agentic AI Systems \- ZBrain, 3월 13, 2026에 액세스, [https://zbrain.ai/knowledge-graphs-for-agentic-ai/](https://zbrain.ai/knowledge-graphs-for-agentic-ai/)  
34. A2A Protocol Explained: Secure Interoperability for Agentic AI 2026 \- OneReach, 3월 13, 2026에 액세스, [https://onereach.ai/blog/what-is-a2a-agent-to-agent-protocol/](https://onereach.ai/blog/what-is-a2a-agent-to-agent-protocol/)  
35. Agentic AI Foundation: Guide to Open Standards for AI Agents \- IntuitionLabs, 3월 13, 2026에 액세스, [https://intuitionlabs.ai/articles/agentic-ai-foundation-open-standards](https://intuitionlabs.ai/articles/agentic-ai-foundation-open-standards)  
36. FuturumWatch Agentic AI Needs the Agentic AI Foundation, 3월 13, 2026에 액세스, [https://futurumgroup.com/press-release/futurumwatch-agentic-ai-needs-the-agentic-ai-foundation/](https://futurumgroup.com/press-release/futurumwatch-agentic-ai-needs-the-agentic-ai-foundation/)  
37. The February 2026 Agent Stack Decision Guide for Everything That Just Shipped | by Micheal Lanham \- Medium, 3월 13, 2026에 액세스, [https://medium.com/@Micheal-Lanham/the-february-2026-agent-stack-decision-guide-for-everything-that-just-shipped-05585d56c7d8](https://medium.com/@Micheal-Lanham/the-february-2026-agent-stack-decision-guide-for-everything-that-just-shipped-05585d56c7d8)  
38. Agentic AI Foundation \- What Every Developer Must Know, 3월 13, 2026에 액세스, [https://zenvanriel.com/ai-engineer-blog/agentic-ai-foundation-mcp-developer-guide/](https://zenvanriel.com/ai-engineer-blog/agentic-ai-foundation-mcp-developer-guide/)  
39. MCP, ACP, and A2A, Oh My\! The Growing World of Inter-agent Communication | Camunda, 3월 13, 2026에 액세스, [https://camunda.com/blog/2025/05/mcp-acp-a2a-growing-world-inter-agent-communication/](https://camunda.com/blog/2025/05/mcp-acp-a2a-growing-world-inter-agent-communication/)  
40. Disruptive Innovation or Industry Buzz? Understanding Model Context Protocol's Role in Data-Driven Agentic AI | Informatica, 3월 13, 2026에 액세스, [https://www.informatica.com/blogs/disruptive-innovation-or-industry-buzz-understanding-model-context-protocols-role-in-data-driven-agentic-ai.html](https://www.informatica.com/blogs/disruptive-innovation-or-industry-buzz-understanding-model-context-protocols-role-in-data-driven-agentic-ai.html)  
41. Donating the Model Context Protocol and establishing the Agentic AI Foundation \- Anthropic, 3월 13, 2026에 액세스, [https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)  
42. What is A2A protocol (Agent2Agent)? \- IBM, 3월 13, 2026에 액세스, [https://www.ibm.com/think/topics/agent2agent-protocol](https://www.ibm.com/think/topics/agent2agent-protocol)  
43. Linux Foundation Launches the Agent2Agent Protocol Project to Enable Secure, Intelligent Communication Between AI Agents, 3월 13, 2026에 액세스, [https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents)  
44. AI Agent Protocols 2026: The Complete Guide to Standardizing AI Communication, 3월 13, 2026에 액세스, [https://www.ruh.ai/blogs/ai-agent-protocols-2026-complete-guide](https://www.ruh.ai/blogs/ai-agent-protocols-2026-complete-guide)  
45. Multi-Agent Systems: Orchestrating AI Agents with A2A Protocol | by Yusuf Baykaloğlu | Jan, 2026 | Medium, 3월 13, 2026에 액세스, [https://medium.com/@yusufbaykaloglu/multi-agent-systems-orchestrating-ai-agents-with-a2a-protocol-19a27077aed8](https://medium.com/@yusufbaykaloglu/multi-agent-systems-orchestrating-ai-agents-with-a2a-protocol-19a27077aed8)