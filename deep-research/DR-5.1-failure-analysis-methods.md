# **DR-5.1Ch.5 대규모 언어 모델 기반 에이전트 시스템의 실패 패턴 분석 및 진단 기법**

## **서론: 결정론적 시스템에서 확률적 에이전트 생태계로의 패러다임 전환**

현대의 소프트웨어 아키텍처 및 컴퓨팅 패러다임은 명시적인 비즈니스 로직과 결정론적 제어 흐름(Control Flow)에 전적으로 의존하던 전통적인 형태를 벗어나, 대규모 언어 모델(Large Language Model, LLM)을 핵심 추론 엔진으로 삼아 자율적으로 목표를 설정하고 수행하는 에이전트(Agent) 시스템으로 급격히 진화하고 있다. 이러한 다중 에이전트 시스템(Multi-Agent Systems, MAS)은 소프트웨어 엔지니어링, 복잡한 데이터 분석, 사이버 보안, 그리고 다양한 지식 노동을 자동화할 수 있는 거대한 잠재력을 지니고 있다. 그러나 실제 벤치마크 테스트 및 프로덕션 환경에서 이러한 에이전트 시스템들이 보여주는 성능 향상 폭은 기대에 미치지 못하는 경우가 많으며, 극도로 높은 예측 불가능성과 실패율을 내포하고 있다.1

전통적인 소프트웨어 아키텍처에서 발생하는 장애는 주로 코드 수준의 구문 오류(Syntax Error), 논리적 결함(Logical Bug), 데이터베이스의 무결성 훼손, 혹은 네트워크 인프라의 결함 등 추적 가능한 단일 지점(Single Point of Failure)에서 발생한다. 반면, 에이전트 시스템의 실패는 구성 요소 간의 복잡한 상호작용, 작업의 순서 배열(Sequencing), 그리고 동적으로 변하는 상태(State)의 누적을 통해 발현되는 창발적(Emergent) 특성을 지닌다.3

에이전트 시스템의 실패를 진단하는 데 있어 중단점 검사(Breakpoint Inspection)나 스택 트레이스(Stack Trace) 분석, 결정론적 리플레이(Deterministic Replay)와 같은 기존의 소프트웨어 디버깅 방식이 철저하게 무력화되는 근본적인 이유는 시스템이 가진 고유한 비결정론적 특성 때문이다. 구체적으로 살펴보면, 첫째, LLM의 온도(Temperature) 및 Top-p 매개변수에 의한 확률적 샘플링(Stochastic Sampling) 메커니즘은 동일한 입력에 대해서도 매번 다른 출력 경로를 생성하게 만든다. 둘째, 이전의 상호작용 기록이 이후의 결정에 절대적인 영향을 미치는 컨텍스트 윈도우(Context Window)의 상태 종속성은 특정 단계에서의 미세한 오류가 전체 실행 주기에 걸쳐 나비효과처럼 증폭되도록 만든다. 셋째, 에이전트가 의존하는 외부 API의 지연이나 가용성 변화는 연쇄적인 실패(Cascading Failures)를 촉발하며, 넷째, 프롬프트의 미세한 변경이나 관리상의 변화가 실행 경로를 완전히 다르게 이끄는 프롬프트 드리프트(Prompt Drift) 현상이 상존한다.5

이러한 특성들은 에이전트 실패의 단순한 재현조차 극도로 어렵게 만든다. 이에 따라 에이전트가 작업을 수행하며 생성하는 사고의 흐름(Chain-of-Thought), 시스템 및 도구 호출(Tool Invocation), 환경으로부터의 피드백, 그리고 다단계 통신 기록을 모두 포함하는 '궤적(Trajectory)' 그 자체를 전면적으로 분석하여 근본 원인을 규명해야 하는 완전히 새로운 진단 프레임워크가 요구되고 있다.4

본 보고서는 LLM 기반 에이전트 시스템 및 다중 에이전트 워크플로우에서 관찰되는 고유한 실패 패턴을 심층적으로 조사하고 체계화한다. 나아가 제조업 및 전통적 IT 인프라 환경에서 신뢰성 확보를 위해 활용되던 근본 원인 분석(Root Cause Analysis, RCA) 및 고장 모드 영향 분석(Failure Mode and Effects Analysis, FMEA) 등의 입증된 품질 관리 기법이 자율형 AI 에이전트 환경의 궤적 분석에 어떻게 이식, 적용, 그리고 자동화되고 있는지에 대한 포괄적인 방법론을 제시한다.

## **자율형 에이전트 시스템의 고유 실패 패턴과 체계적 분류(Taxonomy)**

에이전트 시스템의 복잡한 실패를 정밀하게 진단하기 위한 가장 필수적인 선행 조건은, 무엇이 시스템을 실패로 이끄는지에 대한 구조적 이해와 표준화된 분류 체계(Taxonomy)의 확립이다. 최근의 학계 및 산업계 연구들은 수천 건의 에이전트 실행 궤적을 해부하여 전통적인 소프트웨어 오류의 범주를 벗어나는 고유한 실패 모델을 구축하고 있다. 이는 단순한 버그의 나열이 아니라 에이전트의 인지적, 논리적 한계가 어떻게 시스템적 장애로 발현되는지를 규명하는 과정이다.

### **MAST (Multi-Agent System Failure Taxonomy) 프레임워크**

최근 학계에서 제시된 MAST 프레임워크는 에이전트 실패 패턴을 이해하는 데 중요한 이정표를 제공한다. 이 연구는 7개의 널리 사용되는 다중 에이전트 프레임워크에서 수집된 1600개 이상의 궤적 데이터(MAST-Data)를 심층 분석하였다. 특히 인간 전문가들(전문가 간 일치도 κ \= 0.88)의 엄격한 주석 작업을 거쳐 14개의 고유한 실패 모드를 도출하였으며, 이를 시스템 설계 문제(System design issues), 에이전트 간 정렬 불량(Inter-agent misalignment), 그리고 작업 검증(Task verification)의 세 가지 상위 범주로 군집화하였다.1

이러한 분류 체계는 GPT-4, Claude 3, Qwen2.5 등 최고 수준의 기초 모델(Foundation Models)을 사용하더라도 단순히 모델의 파라미터 크기나 추론 능력을 넘어서는 아키텍처 수준의 한계가 존재함을 시사한다.1 특히 다중 에이전트(Multi-Agent) 환경에서는 단일 에이전트 시스템을 평가하는 지표로는 결코 측정할 수 없는 조정 실패(Miscoordination)와 의도치 않은 담합(Collusion)과 같은 새로운 차원의 위험 모델이 등장한다. 이는 특정 에이전트가 다른 에이전트의 출력을 잘못 해석하거나, 전체 목표와 상충되는 하위 목표를 추구함으로써 작업 전체의 실패가 연쇄적으로 파급됨을 의미한다.2

### **AgentRx 및 모듈 기반 실패 분류 체계**

에이전트의 기능적 모듈(기억, 계획, 행동, 성찰 등)을 중심으로 실패를 분류하는 접근법은 에이전트의 내부 의사결정 구조를 해부하여 각 단계의 취약점을 분석하는 데 탁월하다.4 마이크로소프트의 연구진이 개발한 AgentRx 프레임워크는 API 기반 워크플로우, IT 인시던트 관리, 개방형 웹 탐색 등 다양한 도메인에서 발생하는 에이전트 실패를 9가지의 구체적이고 일반화 가능한 범주로 세분화하였다.7

이 9가지 분류 체계는 에이전트가 맞닥뜨리는 인지적 한계와 논리적 단절을 정확히 포착한다. 첫째, 에이전트가 초기에 수립한 계획을 무시하거나 필수적인 단계를 건너뛰는 '계획 미준수(Plan Adherence Failure)'가 발생한다. 둘째, 에이전트가 도구의 실제 출력에 근거하지 않고 자체적으로 사실을 조작하거나 환각을 일으키는 '새로운 정보의 창조(Invention of New Information)'가 빈번히 관찰된다. 셋째, 필수 인수를 누락하거나 잘못된 데이터 형식을 API에 전송하는 '유효하지 않은 호출(Invalid Invocation)'이 있다. 넷째, API나 도구가 반환한 정확한 데이터를 에이전트가 잘못된 가정하에 곡해하는 '도구 출력의 오해석(Misinterpretation of Tool Output)'이다. 다섯째, 사용자의 실제 목적을 잘못 파악하여 엉뚱한 방향으로 계획을 수립하는 '의도-계획 불일치(Intent-Plan Misalignment)'가 발생한다. 이외에도 정보가 부족한 상태에서 무리하게 작업을 진행하는 현상, 시스템에 존재하지 않는 도구를 호출하려는 시도, 시스템의 보안 및 가드레일 제약에 의한 차단, 그리고 외부 시스템 연결 오류 등 물리적 인프라 수준의 결함이 포함된다.7

### **도구 사용(Tool Use)의 치명적 오류 및 순환적 실패**

에이전트 시스템에서 가장 빈번하게 관찰되며 동시에 가장 치명적인 영향을 미치는 영역은 단연 도구 사용(Tool Use)과 관련된 상호작용 단계이다. 에이전트는 외부 환경과 소통하기 위해 API, 데이터베이스 쿼리, 웹 브라우저 등의 도구를 사용하지만, 이 과정에서 발생하는 오류는 에이전트의 작업을 완전히 마비시킨다.

가장 대표적인 패턴은 '환각적 도구 호출(Hallucinated tool calls)'이다. 이는 에이전트가 시스템에 존재하지 않는 도구, 매개변수, 혹은 API 엔드포인트를 임의로 창조해 내어 호출하는 현상이다. 이 오류가 특히 위험한 이유는, LLM이 생성한 호출 코드가 표면적인 문법 검사나 JSON 유효성 검사 등은 쉽게 통과할 만큼 그럴듯하게(Plausible-sounding) 작성되기 때문에 실행 시점에 도달해서야 치명적인 예외 오류를 발생시키기 때문이다.3

또한, 에이전트가 외부 환경이나 도구로부터 모호한 피드백을 받았을 때 이를 적절히 해석하여 계획을 수정(Reflection)하지 못하고, 완전히 동일한 잘못된 행동을 무한히 반복하는 '무한 루프(Infinite loops)' 현상도 에이전트 고유의 주요 실패 사례다. 이 무한 루프는 시스템의 진행을 가로막을 뿐만 아니라 API 호출 토큰과 컴퓨팅 자원을 급속도로 고갈시킨다.3 실제 소규모 언어 모델(예: Granite 4 Small)을 대상으로 한 벤치마크 실험에서는 에이전트가 도구 호출 과정에서 "다중 도구 호출이 발견되었습니다. 한 번에 하나의 도구만 사용하십시오" 또는 "유효한 JSON 형식의 호출이 아닙니다"와 같은 명시적인 오류 메시지 피드백을 환경으로부터 전달받았음에도 불구하고, 이를 파싱하거나 근본 원인을 이해하지 못해 궤도 수정(Recovery)에 실패하는 패턴이 지속적으로 관찰되었다.8

더불어, 누락된 컨텍스트와 검색 실패(Retrieval failures 및 Missing context)는 에이전트가 불완전하거나 완전히 무관한 RAG(검색 증강 생성) 데이터에 의존하게 만들어, 결과적으로 확신에 찬 어조로 오답을 생성하고 이를 진실로 간주하여 후속 계획을 수립하게 만드는 치명적인 기폭제 역할을 한다.3

| 실패의 근본 영역 (Failure Domain) | 세부 실패 모드 (Detailed Failure Modes) | 시스템 내 인과적 메커니즘 (Causal Mechanism) | 참조 문헌 |
| :---- | :---- | :---- | :---- |
| **시스템 구조 및 에이전트 정렬** | 다중 에이전트 조정 실패, 담합, 의도-계획 불일치 | 프롬프트의 모호성, 역할 분리의 불명확성으로 인해 에이전트 간의 통신 병목 및 충돌 발생 | 1 |
| **도구 및 환경 상호작용** | 환각적 도구 호출, 무한 루프, 유효하지 않은 호출 형식 | API 스키마 및 제약 조건에 대한 LLM의 내재적 이해 부족, 예외 처리에 대한 성찰(Reflection) 능력 부재 | 3 |
| **인지 메커니즘 및 지식의 한계** | 컨텍스트 누락, 정보 창조(환각), 도구 출력 오해석 | 불완전한 검색(RAG) 청크 활용, 파라미터 지식에 의존한 무리한 추측, 장기 컨텍스트 한계로 인한 기억 상실 | 3 |

이러한 방대한 궤적 데이터를 기반으로 한 분석 결과들은 에이전트의 실패가 코드 한 줄의 오타가 아니라 문맥의 상실, 환각, 논리적 단절, 그리고 환경 피드백에 대한 수용 거부가 복합적으로 작용한 인지적 실패(Cognitive Failure)의 성격을 강하게 띠고 있음을 증명한다.

## **궤적 기반 분석을 통한 근본 원인 분석(RCA)의 방법론적 재구성**

기존 클라우드 기반 소프트웨어 및 분산 IT 시스템 환경에서의 근본 원인 분석(Root Cause Analysis, RCA)은 CPU 사용량, 메모리 누수, 정적인 애플리케이션 로그, 그리고 분산 추적(Distributed Tracing)과 같은 원격 측정(Telemetry) 데이터를 기반으로 통계적 상관관계를 분석하는 데 치중해 왔다.9 그러나 에이전트 기반 시스템에서는 시스템의 '상태'가 로그 파일의 타임스탬프가 아니라 LLM이 생성하는 자연어 기반의 추론 과정과 다단계의 자율적 결정 속에 숨어 있다.4 따라서 단순한 데이터의 덤프나 통계적 분석만으로는 실패의 실제 인과 메커니즘을 밝혀낼 수 없으며, 에이전트의 전체 실행 과정을 추적하는 궤적(Trajectory) 기반 분석이 에이전트 RCA의 핵심 패러다임으로 부상하였다.4

### **에이전트 인지 오류 추적을 위한 5-Whys 기법의 적용**

전통적인 제조업과 신뢰성 공학 분야에서 널리 쓰이는 5-Whys(왜 5번 묻기) 기법은 표면적으로 드러난 증상에서 출발하여 꼬리를 무는 질문의 사슬을 따라 근본 원인을 파헤치는 구조화된 인과 분석 프레임워크다.11 이 고전적인 방법론은 블랙박스와 같은 에이전트의 인지적 오류를 추적하는 논리적 도구로 완벽하게 재해석되고 있다.

에이전트 시스템에서 가장 빈번하게 발생하는 환각(Hallucination) 현상을 진단하는 과정에 5-Whys 기법을 적용할 경우, 다음과 같은 추론 궤적이 형성된다. Mata v. Avianca (2023) 사건처럼 AI 에이전트가 허위 판례나 조작된 사실을 포함한 법률 보고서를 생성했다는 표면적 증상이 발생했다고 가정해 보자.17

1. **첫 번째 질문 (Why?):** "왜 보고서에 허위 사실 및 조작된 판례가 포함되었는가?"  
   * **답변:** 에이전트가 검색된 지식 베이스 외부의 정보를 자의적으로 생성하여 답변을 구성했기 때문이다 (Unfaithful to source).17  
2. **두 번째 질문 (Why?):** "왜 에이전트는 외부 지식 베이스가 아닌 내부 파라미터 지식에 의존하여 환각을 일으켰는가?"  
   * **답변:** RAG(검색 증강 생성) 파이프라인 호출 과정에서 해당 판례에 대한 적절한 문맥(Context) 데이터를 충분히 검색하지 못했기 때문이다.3  
3. **세 번째 질문 (Why?):** "왜 RAG 시스템은 올바른 문맥을 검색하는 데 실패했는가?"  
   * **답변:** 에이전트가 도구를 호출할 때 사용한 검색 쿼리 매개변수가 지나치게 포괄적이고 모호하여 무관한 문서들만 상위에 랭크되었기 때문이다.3  
4. **네 번째 질문 (Why?):** "왜 에이전트는 모호한 검색 쿼리를 생성했는가?"  
   * **답변:** 에이전트의 초기 계획 수립(Planning) 모듈이 다단계 추론(Chain-of-Thought)을 거치지 않고 사용자 입력을 그대로 검색 도구에 단일 키워드로 전달하도록 단순하게 설계되었기 때문이다.18  
5. **다섯 번째 질문 (Why?):** "왜 다단계 추론 과정이 생략되었는가?"  
   * **근본 원인 (Root Cause):** 시스템 프롬프트(System Prompt)가 복잡한 쿼리에 대해 도구를 사용하기 전 스스로 단계별 계획을 세우도록 강제하는 지시어(Instructions)와 제약 조건을 명시적으로 포함하고 있지 않았기 때문이다.18

이러한 논리적 추적 과정은 단순히 인간 개발자가 사후에 분석하는 도구에 그치지 않고, 복잡한 에이전트 시스템 내부에 자체 진단 스킬(Self-diagnostic Skills)로 내재화되어 자율적으로 5-Whys 분석 보고서와 시정 조치 계획(8D Reports)을 생성하는 데 활용되고 있다.21

### **피시본 다이어그램 (Ishikawa) 기반의 에이전트 인과망 분석**

5-Whys가 단일한 선형적 원인을 깊게 파고드는 데 유리하다면, 피시본 다이어그램(Ishikawa Diagram 또는 Cause-and-Effect Diagram)은 여러 모듈이 얽혀 있는 에이전트 시스템에서 다각적이고 복합적인 인과관계를 구조화하는 데 필수적인 방법론이다.23

전통적인 제조업에서는 불량의 원인을 사람(Man), 기계(Machine), 재료(Material), 방법(Method)의 4M 등으로 범주화하였다.15 AI 에이전트 장애 분석에서 이 범주는 시스템의 특성에 맞게 완전히 새롭게 정의된다. 물고기의 '머리' 부분에 "고객 응대 에이전트의 무한 루프 발생 및 서버 자원 고갈"이라는 문제 현상을 배치한 후, 주요 뼈대(Category)를 다음과 같이 구성할 수 있다.3

* **프롬프트 엔지니어링 (Prompting / Methods):** 시스템 지시어의 모호성, 제약 조건 명시 부족, 역할 정의의 충돌, 프롬프트 드리프트 현상.5  
* **데이터 및 컨텍스트 (Data / Material):** RAG 검색 품질 저하, 벡터 데이터베이스 내 문서의 청킹(Chunking) 오류, 아웃데이트된 정보 탑재, 컨텍스트 윈도우 초과로 인한 과거 기억 삭제.3  
* **도구 및 환경 (Tools & Environment / Machine):** 외부 API의 간헐적 타임아웃, 예외 처리(Error Feedback) 메시지의 비표준화, 환각을 유발하는 잘못된 API 스키마 정의.3  
* **기초 모델 매개변수 (Model Configuration / Measurement):** 확률적 샘플링의 온도(Temperature) 및 Top-p 값이 너무 높게 설정됨, 특정 언어나 모달리티에 대한 모델 파라미터 자체의 편향성 혹은 취약성.5

이러한 구조적 시각화는 산발적으로 발생하는 에이전트의 이상 행동이 단일한 버그 때문이 아니라 프롬프트, 도구, 데이터의 결함이 상호작용한 결과임을 명확히 보여준다.

### **가설 검증(Hypothesis Testing) 및 사후 가정적(Counterfactual) 추론 메커니즘**

에이전트 궤적 분석의 가장 진보된 형태는 단순한 로그의 역추적을 넘어선 가설 검증과 '사후 가정적 추론(Counterfactual Reasoning)' 메커니즘의 도입이다. 에이전트의 실패가 발생했을 때, 분석 시스템은 단순히 오류 로그를 뱉어내는 대신 "만약 특정 단계에서 에이전트가 도구 A 대신 도구 B를 호출했다면?", 혹은 "환경이 에러 메시지 대신 다른 형태의 피드백을 주었다면 실패의 연쇄 고리를 끊고 성공할 수 있었을까?"라는 가설을 자율적으로 설정한다.4

이러한 패러다임은 다양한 연구 프레임워크를 통해 실증되고 있다. DoVer 및 AgentDebug와 같은 개입 주도형(Intervention-driven) 분석 프레임워크는 실패한 궤적의 세부 단계마다 모듈별(기억, 성찰, 계획 등) 오류 유형을 할당한다. 이후 원인으로 의심되는 메시지, API 호출 인수, 또는 계획 수립 단계의 프롬프트를 시스템적으로 수정한 뒤 롤아웃(Rollout)을 재실행한다. 이 재실행 과정에서 해당 '개입'이 실제로 궤도를 수정하여 최종 목표 달성으로 이어지는지를 확인함으로써 실패의 진정한 근본 원인을 과학적으로 검증한다.4

TraceElephant와 AgentFail 프레임워크 역시 LLM을 심판관으로 활용하여 실패의 근본 원인 후보를 식별한 후, 사후 가정적 검증 과정을 거쳐 최종적인 근본 원인을 확정하는 방식을 취한다. Dify와 같은 플랫폼 기반으로 오케스트레이션된 에이전트 시스템에서 추출한 307개의 실패 로그(AgentFail 데이터셋)를 활용한 벤치마크 결과, 이러한 사후 가정적 추론 및 분류 체계의 적용은 시스템의 실패 식별 능력을 향상시켰다.27

그러나 현재 기술 수준에서 이러한 고도화된 인과적 분석 기법이 개별 단계 수준의 오류(Step-level attribution accuracy)를 정확히 짚어내는 정확도는 약 33.6%에서 최대 40% 수준에 머물고 있다.4 이는 에이전트 시스템 내부의 원인과 결과를 분리하고 책임(Attribution)을 명확히 규명하는 작업이 단일 시스템의 버그 수정보다 본질적으로 훨씬 높은 복잡성과 추상적 인지 능력을 요구함을 시사하며, 진단 시스템의 지속적인 고도화가 필요함을 역설한다.

## **자율적 위험 관리를 위한 FMEA (고장 모드 영향 분석)의 에이전트 이식 및 고도화**

근본 원인 분석(RCA)이 사고가 발생한 후 그 원인을 역추적하는 사후 대응적(Reactive) 성격을 띤다면, 고장 모드 영향 분석(Failure Mode and Effects Analysis, FMEA)은 제품이나 프로세스가 미래에 실패할 수 있는 모든 잠재적 시나리오를 사전에 식별하고, 그 파급력을 평가하여 선제적으로 방지하기 위한 능동적(Proactive)이고 체계적인 위험 관리 기법이다.28 에이전트 시스템이 단순한 질의응답을 넘어 의료 판독, 금융 거래, 인프라 제어 등 미션 크리티컬한 비즈니스 환경에 본격 배치됨에 따라, 에이전트의 자율적 의사결정 프로세스 자체에 FMEA를 적용하여 환각이나 도구 오용의 위험을 통제하려는 시도가 본격화되고 있다.

### **정량적 리스크 평가: 에이전트 시스템에서의 RPN (위험 우선순위) 산출**

FMEA 프레임워크의 핵심 동력은 식별된 각 고장 모드의 상대적 위험도를 정량화하는 위험 우선순위 산출(Risk Priority Number, RPN) 메커니즘이다. RPN은 심각도(Severity, S), 발생 빈도(Occurrence, O), 검출 난이도(Detection, D)의 세 가지 핵심 파라미터를 통상 1부터 10까지의 척도로 평가하여 이를 모두 곱한 값(RPN \= S × O × D)으로 산출된다.31 과거 제조업 부품의 마모나 기계 결함 평가에 쓰이던 이 수학적 모델은 자율형 AI 에이전트의 확률적 행동 패턴과 그 위험성을 평가하는 데 완벽하게 치환될 수 있다.

에이전트 워크플로우 분석 시, 심각도(Severity)는 에이전트의 특정 인지적 실패나 도구 오용이 사용자 데이터, 보안, 시스템 인프라에 미치는 물리적 및 논리적 파괴력을 의미한다. 예를 들어, 데이터 파싱 모듈을 사용하는 에이전트가 데이터베이스 읽기 권한을 오인하여 DROP(삭제) 명령어를 실행하려는 '의도-계획 불일치' 실패는 시스템 전체를 마비시킬 수 있으므로 치명적인 심각도(S=10)를 가진다.7 자율 주행이나 헬스케어 에이전트의 편향된 진단 역시 생명에 위협을 가하므로 최고 수준의 심각도가 부여된다.29

발생 빈도(Occurrence)는 기초 모델(LLM)의 내재적 특성에 기인한다. 모델의 확률적 샘플링 온도 설정, 프롬프트 지시어의 복잡성, 모델 크기에 따른 본질적 환각률(Hallucination rate) 통계에 기초하여 해당 논리적 오류가 얼마나 자주 시스템 내에서 재현될 것인지를 예측한다.17

가장 중요한 지표 중 하나인 검출 난이도(Detection)는 시스템 모니터링 체계나 인간 감독자(Human-in-the-loop)가 해당 오류가 치명적인 결과로 이어지기 전에 사전에 식별하고 차단할 수 있는 가능성을 의미한다. 언어 모델의 환각은 종종 매우 문법적으로 완벽하고 논리 정연하게(Plausible-sounding) 생성되며, 허위 문헌이나 조작된 참조를 교묘하게 섞어 놓기 때문에 표면적인 텍스트 검증만으로는 검출이 극히 어렵다.3 따라서 에이전트 환각 관련 고장 모드는 자연스럽게 매우 높은 검출 난이도 점수(D=8\~10)를 받게 된다.

이렇게 산출된 RPN 값이 특정 임계값(예: 의료 IT 시스템 연구 기준 300 이상)을 초과하는 실행 경로에 대해서는 '비안전(Unsafe)' 상태로 분류하고 36, 수많은 에이전트 추론 경로 중 가장 우선적으로 하드코딩된 가드레일(Guardrails)을 적용하거나, 다중 검증 에이전트(Validator Agent)를 배치하는 방식으로 위험을 통제할 수 있다.

### **에이전트 주도형 자동화 FMEA (Agentic AI for FMEA) 시스템의 부상**

최근 신뢰성 공학 분야에서 관찰되는 가장 혁신적인 패러다임의 변화는, FMEA를 에이전트 시스템의 위험을 평가하는 '대상'으로만 적용하는 것을 넘어, 대규모 언어 모델 기반 에이전트 자체가 FMEA 프로세스를 완전 자동화하고 생성하는 '주체'로 진화하고 있다는 점이다.37 전통적인 FMEA 수행 방식은 여러 분야의 엔지니어들이 장시간 대면 회의를 거쳐 방대한 스프레드시트에 수동으로 데이터를 입력하고 브레인스토밍하는 노동 집약적 과정이었다. 이 과정에서는 작업자의 피로도 증판, 주관적 편향 개입, 그리고 과거 부서별로 파편화된 문서의 재사용성 부족 등 수많은 비효율이 존재했다.37

이를 극복하기 위해 등장한 LLMRiskAnalyzer 및 Omnex 플랫폼 등 최신 에이전트 프레임워크는 RAG 파이프라인과 다중 에이전트 아키텍처를 결합하여 수동 위험 분석 프로세스를 해체하고 재구성한다.38 이러한 시스템은 외부의 산업 표준, 방대한 과거의 사고 이력, 시스템 아키텍처 설계 문서를 ElasticSearch나 벡터 데이터베이스에서 실시간으로 검색하여 잠재적 고장 모드를 동적으로 식별해 낸다.39

이러한 에이전트 주도의 FMEA(Agentic AI FMEA)는 시스템 내에서 크게 두 가지 핵심 페르소나를 부여받아 작동한다. 첫째, 기존 문서 지능(Document Intelligence)을 활용하는 '리뷰어 에이전트' 역할이다. 이 에이전트는 흩어진 워드 프로세서, PDF, 기존 스프레드시트에 기록된 FMEA 데이터베이스를 크롤링하고 분석하여 논리적 모순, 누락된 RPN 값, 불완전한 완화 조치, 혹은 비표준화된 전문 용어를 자율적으로 탐지하고 규격화한다.37 둘째, 정제된 데이터를 바탕으로 새로운 시스템 설계에 대한 설계 FMEA(DFMEA) 및 공정 FMEA(PFMEA)를 기초부터 도출해 내는 '크리에이터 에이전트' 역할이다. 사용자가 간단한 채팅 프롬프트로 대상 시스템(예: 자동차의 브레이크 바이 와이어 시스템)을 제시하면, 에이전트는 과거 라이브러리를 참조하여 고장 모드, 원인, 영향을 추론하고 정량화된 RPN 테이블을 엑셀이나 JSON 형태로 즉시 출력해 낸다.37

이러한 AI 에이전트 기반 접근의 효과는 산업 현장의 수치로 직접 증명되고 있다. 인간 엔지니어가 수동으로 진행하는 전통적인 FMEA가 전체 잠재적 고장 요인의 약 60\~80%를 인지하지 못하고 놓치는(Missed) 것과 극명하게 대비하여, AI 에이전트 모델은 과거 패턴 학습을 통해 95% 이상의 결함 식별률을 달성하였다.43 더 나아가 이 모델이 실시간 제조 센서 데이터 및 재작업(Rework) 데이터와 연동될 경우, 과거에는 인간이 통계적 연관성을 파악하기 어려웠던 미세한 매개변수 조합(예: 사출 성형 시 냉각 시간과 용융 온도의 특정 결합이 유발하는 미세 균열)을 식별해 낸다.44 그 결과, 에이전트 분석은 단순한 문서 작성을 넘어 예기치 않은 시스템 다운타임을 35\~50% 감소시키는 동적 모니터링 체계로 승화된다.43 따라서 FMEA는 과거 캐비닛에 보관되던 정적인 문서에서 벗어나, 에이전트의 지속적인 감시 하에 스스로 진화하는 살아 숨 쉬는 지식 베이스(Living Database)로 기능하게 된다.

| 비교 척도 | 전통적 수동 FMEA 방식 | 에이전트 주도형 (Agentic AI) 자동화 FMEA | 도입에 따른 시스템적 이점 및 가치 |
| :---- | :---- | :---- | :---- |
| **데이터 처리 및 저장** | 엑셀 등 스프레드시트 기반 수동 입력, 부서별로 파편화된 문서 관리 | 다중 소스(RAG) 기반 자동 지식 추출, 벡터 DB를 통한 동적 연동 및 지식 그래프화 | 과거 교훈(Lessons learned)의 매몰 방지, 문서 통합 및 지식 재사용성 극대화 |
| **위험 요인 식별 방식** | 참여 전문가의 개인적 경험, 직관 및 브레인스토밍 역량에 전적으로 의존 | LLM의 방대한 학습 데이터와 과거 사고 문서, 실시간 센서 데이터의 교차 패턴 분석 | 인간이 놓치기 쉬운 비선형적 상관관계 포착, 주관적 편향 배제, 95% 이상의 검출률 43 |
| **프로세스 갱신 주기** | 제품 설계 및 공정 초기 단계에서 1회성으로 작성되며, 설계 변경 시 업데이트 지연 빈번 | 실시간 텔레메트리 데이터 처리, 설계 및 매개변수 변경 조건 발생 시 시스템 자율 재계산 | 24/7/365 동적이고 지속적인 위험 모니터링 가능, 문서의 실시간성 확보 43 |
| **RPN (위험 척도) 산출** | 인간 엔지니어의 주관적이고 자의적인 척도 부여에 기인함 | RAG 프레임워크 및 과거 발생 확률 통계 기반의 정량적 근거에 의한 RPN 자동 산출 알고리즘 | 위험 평가의 일관성 및 객관성 확보, 최우선 완화 조치 결정의 신뢰성 증대 |

## **에이전트 평가 및 진단 프레임워크의 구조적 통합과 자동화**

에이전트 시스템의 실패를 분석하고 리스크를 선제적으로 방어하는 방법론이 단순한 학술적 수준의 이론에 머물지 않고 실제 기업의 프로덕션 환경에 성공적으로 적용되기 위해서는, 시스템의 개발에서부터 운영 수명주기 전체를 아우르며 지속적으로 추적하고 평가하는 전용 '에이전트 평가 프레임워크(Agent Evaluation Framework)'가 필수적이다. 전통적인 단일 프롬프트-응답 쌍을 평가하는 도구(예: 단순 텍스트 일치율 검사)는, 외부 도구를 연속적으로 호출하고 환경 상태를 변화시키며 장시간에 걸쳐 자율적으로 목표를 추구하는 에이전트의 동적 흐름을 평가하는 데 턱없이 부족하며 시스템을 그저 '블랙박스'로 취급할 뿐이다.46

### **체계적 디버깅 및 보호된 분석을 위한 AgentRx 파이프라인 해부**

앞서 언급한 마이크로소프트의 AgentRx 프레임워크는 이론적 실패 분류를 넘어서, 에이전트 시스템의 전체 실행 궤적을 하나의 운영체제 트레이스(OS Trace)처럼 구조적으로 취급하여 실패의 '결정적 단계(Critical Failure Step)'를 정밀하게 짚어내는 도메인 독립적 파이프라인 아키텍처를 구현하였다.7 이 진단 프레임워크는 자동화된 RCA를 위해 다음과 같은 네 가지의 고도화된 기술적 단계를 순차적으로 거친다.

1. **궤적 정규화(Trajectory Normalization):** 다양한 애플리케이션 프레임워크(LangChain, LlamaIndex 등)와 서로 다른 도메인(예: 웹 브라우징, 기업 데이터베이스 쿼리, IT 인시던트 관리 시스템)에서 생성되는 구조가 각기 다른 이질적인 로그 데이터를 파싱하여, 분석기가 이해할 수 있는 공통의 중간 표현(Intermediate Representation) 형식으로 통일하고 변환한다.7  
2. **제약 조건 합성(Constraint Synthesis):** 시스템에 내장된 도구들의 스키마 명세서(예: API가 필수적으로 요구하는 파라미터 타입, 반환해야 하는 JSON의 구조)와 기업의 도메인 비즈니스 정책(예: "사용자의 명시적인 권한 승인 없이 데이터베이스의 레코드를 임의로 삭제해서는 안 됨")을 바탕으로, 실행 가능한 형태의 '가드레일 제약 조건(Guarded Constraints)'을 자율적으로 합성하고 생성한다.7  
3. **보호된 단계별 평가(Guarded Evaluation):** 생성된 가드레일 제약 조건들을 에이전트가 실행한 궤적 데이터에 중첩시켜 스텝 단위로 꼼꼼하게 검사한다. 특정 가드 조건이 충족될 시점에만 제약 확인을 수행하여, 단순한 오류 메시지의 나열이 아니라 명확한 증거(Evidence)로 뒷받침되는 강력하고 감사 가능한(Auditable) 위반 로그(Validation Log) 세트를 산출해 낸다.7  
4. **LLM 심판 기반의 원인 규명(LLM-based Judging):** 마지막 단계에서 특화된 LLM이 심판(Judge) 역할을 수행한다. 앞서 산출된 검증 로그와 사전에 정의된 9가지 실패 분류 체계를 교차 분석하여, 단순히 가장 나중에 발생한 에러가 아니라 에이전트가 더 이상 복구할 수 없는 오류 상태의 늪에 빠진 '최초의 결정적 실패 단계'를 정확하게 타겟팅하고 그 실패의 범주를 선언한다.7

이러한 단계적이고 체계적인 프레임워크는 사용자에게 단순히 에이전트가 작업에 실패했다는 결과만을 알리는 것을 넘어선다. 정확히 어떤 시스템 조건이 어느 시점에 위반되었으며, 에이전트의 추론 과정 중 어느 맥락에서 논리적 의사결정이 어긋났는지를 투명하게 제시한다. 실제로 115개의 복잡하고 긴 실패 궤적으로 구성된 AgentRx 벤치마크 테스트(τ-bench, Flash 인시던트 관리, Magentic-One 다중 에이전트 웹 태스크 환경 포함)에서 이 프레임워크는 기존의 단순 LLM 프롬프팅 방식에 비해 결정적 실패 위치를 파악하는 데 23.6%, 근본 원인을 귀인하는 데 22.9%의 절대적인 성능 향상을 입증하였다.7

비슷한 맥락에서 AgentDebug 프레임워크는 ALFWorld(체화된 로봇 에이전트 작업), GAIA(일반 AI 비서 작업), WebShop(웹 탐색 및 쇼핑) 등 더욱 폭넓고 다양한 실제 벤치마크 환경에서 200개의 고도로 주석 처리된 실패 궤적(AgentErrorBench)을 수집하고 분석하였다. AgentDebug 파이프라인은 궤적을 단계별로 분석하여 근본 원인을 고립시키고, 에이전트에게 맞춤형 시정 피드백을 동적으로 제공하여 자율 복구를 유도함으로써 에이전트 시스템의 전반적인 성공률을 무려 26% 이상 끌어올리는 성과를 보였다.6

### **IT 인프라 진단 도구로서의 에이전트 투입과 그 본질적 한계성 (OpenRCA 벤치마크)**

에이전트를 소프트웨어 개발의 코드 생성 도구를 넘어, 실제 프로덕션 환경에서 발생하는 복잡한 소프트웨어 및 서버 장애를 진단하고 RCA를 수행하는 '전문 진단 요원'으로 투입하려는 시도가 활발히 이루어지고 있다. 그러나 이러한 기술의 현재 주소와 언어 모델의 본질적 한계를 냉철하게 짚어내는 연구 결과들이 속속 발표되고 있다.

대표적인 예로 OpenRCA 벤치마크 프레임워크 연구를 들 수 있다. 이 연구는 3개의 대규모 엔터프라이즈 소프트웨어 시스템에서 발생한 335개의 실제 장애 사례와 이에 수반되는 68GB에 달하는 막대한 분량의 혼합 텔레메트리 데이터(시스템 로그, 성능 메트릭, 분산 트레이스 등)를 활용하여 LLM 에이전트의 진단 능력을 실증적으로 평가하였다.49 에이전트에게 주어진 미션은 이질적이고 컨텍스트가 극도로 긴 모니터링 데이터를 종합적으로 파싱하여, 분산 시스템의 복잡한 종속성 구조를 이해하고 궁극적으로 소프트웨어를 멈추게 만든 진정한 근본 원인을 추론해 내는 것이었다.

실험 결과는 매우 시사하는 바가 크다. 현재 가장 진보된 최첨단 모델로 평가받는 Claude 3.5 시스템을 활용하여 특별히 설계된 RCA 전용 에이전트를 구축했음에도 불구하고, 주어진 장애 케이스 중 단 11.34%만의 근본 원인을 정확히 찾아내 해결하는 데 그쳤다.50 이토록 저조한 정확도(Detection Accuracy)는 언어 모델 기반 에이전트가 주어진 프롬프트를 바탕으로 논리적인 텍스트를 선형적으로 생성하는 데는 탁월한 성능을 보일지라도, 다양한 형태의 모달리티(수십만 줄의 시계열 숫자 데이터, 비정형 시스템 로그, 마이크로서비스 간의 거미줄 같은 아키텍처 종속성)를 융합하여 기저에 깔린 인과관계를 수학적으로 추론하는 능력은 여전히 치명적으로 취약함을 증명한다.49

마이크로소프트 팀이 수행한 또 다른 연구에서는 ReAct 아키텍처 기반 에이전트에게 검색 도구(Retrieval tools)를 장착하여 생산 환경의 인시던트를 진단하게 하였으나, 강력한 지식 검색 기능을 추가했음에도 불구하고 성능의 획기적인 도약은 달성하지 못했다. 심지어 사고 보고서와 연관된 엔지니어들의 토론 텍스트를 추가적인 컨텍스트로 제공했음에도 성능 향상에 큰 도움이 되지 않는 놀라운 결과를 보여주기도 했다.10 이는 에이전트에게 단순히 방대한 양의 데이터를 RAG 형태로 밀어 넣는 것만으로는 문제 해결의 본질에 다가설 수 없음을 보여준다. 방대한 원격 측정 데이터의 바다 속에서 단순한 통계적 상관관계(Correlation)에 매몰되지 않고 그 이면에 숨겨진 인과 메커니즘(Causal Mechanism)을 밝혀내는 구조화된 '인과 추론(Causal Inference)' 파이프라인을 에이전트 엔진 내부에 근본적으로 내재화하는 설계만이 자율형 RCA 에이전트 발전의 핵심 과제임을 확인시켜 준다.9

### **시스템 지속성 확보를 위한 피드백 루프 아키텍처와 EDDOps**

분석 도구들을 통해 진단된 에이전트 시스템의 실패 패턴과 도출된 방대한 RCA 데이터는 그 자체로 아카이빙되는 정적 데이터에 머물러서는 안 되며, 시스템을 능동적으로 진화시키고 자가 치유(Self-healing)하게 만드는 엔진의 연료로 작용해야만 한다. 이러한 목적을 달성하기 위해 최근 에이전트 운영 분야에서 새롭게 확립되고 있는 개념이 바로 '평가 주도형 개발 및 운영(Evaluation-Driven Development and Operations, EDDOps)' 패러다임이다.53

EDDOps는 에이전트를 설계하는 개발 시점(오프라인 환경)에서의 광범위한 벤치마크 테스트와 실제 프로덕션 배치 이후(런타임/온라인 환경)의 실시간 모니터링을 분리하지 않고, 이를 하나의 단단하게 묶인 '폐쇄형 피드백 루프(Closed Feedback Loop)'로 통합하는 방법론이다.53

전통적인 소프트웨어의 디버깅 프로세스가 발견된 버그의 코드를 패치하여 즉각적인 에러를 소거하는 데 집중한다면, 확률적 특성을 지닌 에이전트 시스템의 유지보수는 '지속적인 실패의 수집, 편입, 그리고 점진적 모델 개선'이라는 절차적 흐름을 거쳐야 한다. 구체적인 워크플로우를 살펴보면 다음과 같다.54 첫째, 프로덕션 환경에 배포된 에이전트가 10,000건의 고객 요청을 처리한다고 가정할 때, 시스템 외곽에 배치된 인라인 평가기(In-stream evaluator)가 모든 응답의 품질(관련성, 맥락 준수율, 환각 여부)과 안전성 정책 위반(PII 유출, 프롬프트 인젝션) 여부를 실시간으로 감시하여 기준에 미달하는 150건의 저품질 응답 궤적을 포착해 낸다. 둘째, 이 실패한 궤적들은 자동으로 별도의 분석 데이터셋으로 추출되며, 인간 프롬프트 엔지니어 혹은 고도화된 디버깅 전용 에이전트가 앞서 설명한 MAST 분류 체계나 5-Whys 인과 분석 기법을 활용하여 실패에 내재된 패턴을 심층 분석한다. 셋째, 분석 결과, 예를 들어 특정 API를 호출할 때 스키마 설명의 모호성이 지속적으로 에이전트의 무한 루프를 유발하는 근본 원인(Root Cause)으로 밝혀지면, 시스템 아키텍트는 즉시 시스템 프롬프트를 더욱 정교하게 다듬거나 외부 도구의 인터페이스 명세를 수정하여 방어적 가드레일을 보강한다. 넷째, 개선 조치가 반영된 새로운 시스템은 이전에 수집된 150개의 실패 궤적 데이터셋을 대상으로 집중적인 회귀 테스트(Regression Detection)를 거친다. 이를 통해 동일한 오류가 더 이상 재발하지 않으며, 프롬프트 수정이 다른 정상 기능에 부작용을 일으키지 않았음을 통계적으로 검증받은 후 다시 프로덕션 환경에 무중단 배포된다.46 매주 반복되는 이 순환 사이클은 "평가 없는 측정은 무의미하다"는 원칙하에, 단발성 실패를 시스템의 체질을 개선하는 예방 백신으로 전환시킨다.

### **에이전트 특화 관측 및 모니터링 생태계 (Industry Tools)**

이러한 EDDOps 피드백 루프를 기술적으로 뒷받침하기 위해 최근 산업계에서는 기존의 애플리케이션 성능 모니터링(APM) 도구를 대체하는 에이전트 전용 모니터링 및 평가 플랫폼(Agent Observability Platforms)이 폭발적으로 등장하며 생태계를 구축하고 있다. 이 플랫폼들은 에이전트의 실패를 해부하고 진단하는 데 특화된 아키텍처를 자랑한다.

예를 들어, Galileo 플랫폼은 JPMorgan Chase, Twilio와 같은 대규모 엔터프라이즈 환경에서 다중 에이전트의 복잡한 의사결정 흐름을 직관적으로 시각화하는 '에이전트 그래프(Agent Graph)' 기능을 제공하여 어느 도구 호출 지점에서 논리적 병목이 발생했는지를 추적한다. 또한 내장된 인사이트 엔진을 통해 근본 원인 분석을 자동화함으로써 95%에 달하는 파일럿 프로젝트의 실패율을 극적으로 낮추는 역할을 수행한다.55 마찬가지로 시장에는 특정한 목적과 프레임워크에 최적화된 다양한 도구들이 경합 중이다. LangSmith는 LangChain 생태계에 깊게 뿌리내려 다중 턴(Multi-turn) 환경에서의 단계별 점수 채점과 궤적 추적에 뛰어난 성능을 보이며 56, Truesight는 도메인 전문가가 정의한 성공/실패 기준에 맞춰 API 기반 라이브 평가를 지원한다.56 W\&B Weave는 로컬 소형 평가 모델을 활용하여 프로덕션 규모의 추적을 수행하고, Braintrust와 Comet Opik은 각각 CI/CD 파이프라인에 통합된 RAG 메트릭 평가와 하루 4천만 건의 궤적을 처리하는 대규모 최적화 알고리즘에 강점을 지니고 있다.56 DeepEval은 결정론적 DAG(Directed Acyclic Graph) 메트릭을 통해 일관된 평가 척도를 제공하는 데 집중한다.

특히 평가 시스템 아키텍처의 효율성 측면에서 주목할 만한 돌파구를 제시한 곳은 Coralogix이다. 초기 대부분의 AI 관측 도구들은 평가 대상으로 삼은 GPT-4의 출력을 검증하기 위해 또다시 값비싼 GPT-4를 호출하는 'LLM-as-a-judge' 구조에 의존했다. 이는 응답 지연 시간(Latency)의 급증과 기하급수적으로 불어나는 토큰 비용이라는 치명적인 문제를 야기했다. Coralogix는 이를 해결하기 위해 범용 LLM 대신 안전성, 독성 판별, 맥락 준수 등 특정 평가 작업에만 고도로 훈련된 '목적형 소형 언어 모델(Purpose-built SLM evaluators)'을 도입하였다. 이를 통해 사용자 요청 처리를 방해하지 않는 스트리밍 기반 실시간 인스트림 평가(In-stream evaluation)를 구현함으로써, 비용과 성능, 커버리지 사이의 딜레마를 효과적으로 해결하고 에이전트 진단 생태계의 성숙도를 한 단계 끌어올렸다.54

| 평가 및 진단 플랫폼 (Platform) | 핵심 특화 영역 및 평가 접근법 (Core Strength & Approach) | 지원 프레임워크 및 특징 (Key Features) | 참조 |
| :---- | :---- | :---- | :---- |
| **Galileo** | 엔터프라이즈급 라이프사이클 보호, 에이전트 그래프 시각화 엔진 | 자동화된 근본 원인 분석 엔진(Insights Engine) 내장 | 55 |
| **Truesight** | 도메인 전문가 관점의 결과(Outcome) 스코어링 중심 평가 | 라이브 평가 API, 특정 전문가의 기준(Pass/Fail) 반영 | 56 |
| **W\&B Weave** | 프로덕션 규모의 대용량 궤적 추적 및 로컬 기반 평가 | 소형 언어 모델(SLM) 기반 채점기 도입, LangChain 지원 | 56 |
| **LangSmith** | 다중 턴(Multi-turn) 에이전트의 궤적 추적 및 심층 디버깅 | LangGraph 워크플로우에 최적화된 단계별 점수 산출 기능 | 56 |
| **Coralogix** | 인스트림(In-stream) 실시간 평가를 통한 비용 및 지연 극복 | 범용 LLM 판단기를 대체하는 목적형 SLM 채점기 도입 | 54 |

## **결론 및 발전 방향**

대규모 언어 모델을 엔진으로 채택한 자율형 에이전트 시스템은 그 내재적인 비결정론적 특성과 동적인 외부 환경과의 상호작용으로 인해 필연적인 창발적 현상을 낳으며, 이는 전통적인 소프트웨어 공학의 디버깅 패러다임을 근본적으로 뒤흔들고 해체하고 있다. 본 보고서의 포괄적인 분석에 따르면, 에이전트 시스템의 진단과 신뢰성 확보 방안은 단일 코드 라인의 문법적 오류를 찾는 1차원적 과정에서 완전히 탈피하여, 에이전트가 인지하고 추론하며 결정하는 일련의 흐름, 즉 궤적(Trajectory) 전체를 다차원적이고 구조적으로 분석하는 방향으로 거대한 전환을 맞이하고 있다.

MAST, AgentRx, 그리고 AgentDebug와 같이 새롭게 등장한 궤적 기반의 실패 분류 체계들은 시스템 실패를 단순히 버그의 집합이 아니라, 에이전트 간의 정렬 오류, 지식 검색의 한계로 인한 환각, 그리고 도구 활용의 논리적 단절이라는 관점에서 정밀하게 해부할 수 있는 전문적인 진단 언어를 제공하였다. 나아가 5-Whys, 피시본 다이어그램과 같이 전통적 신뢰성 공학에서 오랜 기간 검증받은 기법들과 정량적 리스크 산출 척도인 RPN을 결합한 FMEA 방법론이, 에이전트의 복잡한 자율적 추론 환경에 완벽하게 치환되고 이식되어 활용되고 있음이 확인되었다. 특히 인간 엔지니어의 수동 노동에 의존하던 전통적인 FMEA 프로세스를 언어 모델 자체가 RAG 파이프라인과 결합하여 동적으로 자동 생성해 내는 '에이전트 주도형 자동화 FMEA (Agentic AI FMEA)'의 출현은, 95% 이상의 압도적인 잠재 위험 식별률을 기록하며 시스템 신뢰성 공학의 새로운 지평을 열어가고 있다.

그러나 축포를 터뜨리기에는 아직 이르다. 현존하는 최고 수준의 기술은 개별 추론 단계의 논리적 오류를 정확히 귀인(Attribution)하여 원인을 짚어내는 데 있어 기껏해야 30\~40% 수준의 성공률을 기록하며 뚜렷한 한계를 노출하고 있다. 더욱이 68GB 이상의 방대한 텔레메트리 데이터를 종합하여 분산 시스템의 근본 원인을 추론해야 하는 과제(OpenRCA)에서는 Claude 3.5와 같은 최첨단 모델조차 11.34%라는 극도로 저조한 정확도를 보이며, 텍스트 생성 능력과 인과 메커니즘을 밝히는 '인과 추론' 능력 사이에는 여전히 거대한 기술적 간극이 존재함을 뼈저리게 확인시켜 주었다.

따라서 에이전트 시스템의 실패 패턴 진단 방법론이 나아가야 할 다음 단계는 자명하다. 단순한 로그 텍스트의 확률적 상관관계를 분석하는 수준을 뛰어넘어, 시스템 역학의 물리적·논리적 본질을 수학적으로 이해하고 '개입(Intervention)'과 '사후 가정적(Counterfactual)' 시나리오 구동을 통해 가설을 독립적으로 검증할 수 있는 진정한 의미의 '인과적 에이전트(Causal Agent)' 아키텍처를 구현하는 것이다. 동시에, 발견된 실패 패턴과 통계 데이터를 EDDOps의 폐쇄형 루프 시스템에 강력하게 통합함으로써, 에이전트 인프라 스스로가 자신의 실패 원인을 성찰하고 취약점을 보수하여 구조적 가드레일을 지속적으로 보강해 나가는 진정한 '자기 치유적(Self-healing) 자율 시스템'으로 진화해야만 한다. 이러한 분석 프레임워크와 평가 도구의 치열한 고도화만이 자율형 에이전트 시스템이 안고 있는 신뢰성의 장벽을 무너뜨리고, 미션 크리티컬한 엔터프라이즈 환경에서의 완전한 확산과 적용을 가능케 할 유일한 핵심 열쇠가 될 것이다.

#### **참고 자료**

1. Why Do Multi-Agent LLM Systems Fail? \- arXiv, 3월 13, 2026에 액세스, [https://arxiv.org/pdf/2503.13657](https://arxiv.org/pdf/2503.13657)  
2. Survey of Multi-agent LLM Evaluations \- LessWrong, 3월 13, 2026에 액세스, [https://www.lesswrong.com/posts/tGcLA596E8g3KnphE/survey-of-multi-agent-llm-evaluations](https://www.lesswrong.com/posts/tGcLA596E8g3KnphE/survey-of-multi-agent-llm-evaluations)  
3. What is AI Agent Evaluation? | Databricks, 3월 13, 2026에 액세스, [https://www.databricks.com/blog/what-is-agent-evaluation](https://www.databricks.com/blog/what-is-agent-evaluation)  
4. (PDF) A Survey for LLM Agent Trajectory Analysis: From Failure Attribution to Enhancement, 3월 13, 2026에 액세스, [https://www.researchgate.net/publication/401193207\_A\_Survey\_for\_LLM\_Agent\_Trajectory\_Analysis\_From\_Failure\_Attribution\_to\_Enhancement](https://www.researchgate.net/publication/401193207_A_Survey_for_LLM_Agent_Trajectory_Analysis_From_Failure_Attribution_to_Enhancement)  
5. Diagnosing and Measuring AI Agent Failures: A Complete Guide, 3월 13, 2026에 액세스, [https://www.getmaxim.ai/articles/diagnosing-and-measuring-ai-agent-failures-a-complete-guide/](https://www.getmaxim.ai/articles/diagnosing-and-measuring-ai-agent-failures-a-complete-guide/)  
6. ulab-uiuc/AgentDebug \- GitHub, 3월 13, 2026에 액세스, [https://github.com/ulab-uiuc/AgentDebug](https://github.com/ulab-uiuc/AgentDebug)  
7. Systematic debugging for AI agents: Introducing the AgentRx ..., 3월 13, 2026에 액세스, [https://www.microsoft.com/en-us/research/blog/systematic-debugging-for-ai-agents-introducing-the-agentrx-framework/](https://www.microsoft.com/en-us/research/blog/systematic-debugging-for-ai-agents-introducing-the-agentrx-framework/)  
8. How Do LLMs Fail In Agentic Scenarios? A Qualitative Analysis of Success and Failure Scenarios of Various LLMs in Agentic Simulations \- arXiv.org, 3월 13, 2026에 액세스, [https://arxiv.org/html/2512.07497v1](https://arxiv.org/html/2512.07497v1)  
9. A Systematic Approach to Causal Reasoning Using Agentic AI in Distributed System Failures \- ResearchGate, 3월 13, 2026에 액세스, [https://www.researchgate.net/publication/399952170\_A\_Systematic\_Approach\_to\_Causal\_Reasoning\_Using\_Agentic\_AI\_in\_Distributed\_System\_Failures](https://www.researchgate.net/publication/399952170_A_Systematic_Approach_to_Causal_Reasoning_Using_Agentic_AI_in_Distributed_System_Failures)  
10. Exploring LLM-based Agents for Root Cause Analysis \- arXiv, 3월 13, 2026에 액세스, [https://arxiv.org/html/2403.04123v1](https://arxiv.org/html/2403.04123v1)  
11. 5 Whys Templates \- Miro, 3월 13, 2026에 액세스, [https://miro.com/templates/5-whys/](https://miro.com/templates/5-whys/)  
12. 5-Whys Template: How To Find Root Causes Fast \- Wondershare EdrawMind, 3월 13, 2026에 액세스, [https://edrawmind.wondershare.com/examples/5-whys-template.html](https://edrawmind.wondershare.com/examples/5-whys-template.html)  
13. 5 Whys Template for Root Cause Analysis and Problem Solving \- Monday.com, 3월 13, 2026에 액세스, [https://monday.com/blog/project-management/5-whys-template/](https://monday.com/blog/project-management/5-whys-template/)  
14. Root Cause Analysis: A Seven-Step Process | by Tahir | Medium, 3월 13, 2026에 액세스, [https://medium.com/@tahirbalarabe2/root-cause-analysis-a-seven-step-process-aaabdeda249a](https://medium.com/@tahirbalarabe2/root-cause-analysis-a-seven-step-process-aaabdeda249a)  
15. How to conduct root cause analysis for equipment risk identification? \- Tencent Cloud, 3월 13, 2026에 액세스, [https://www.tencentcloud.com/techpedia/125755](https://www.tencentcloud.com/techpedia/125755)  
16. A systematic approach to root cause analysis using 3 × 5 why's technique \- ResearchGate, 3월 13, 2026에 액세스, [https://www.researchgate.net/publication/326272877\_A\_systematic\_approach\_to\_root\_cause\_analysis\_using\_3\_5\_why's\_technique](https://www.researchgate.net/publication/326272877_A_systematic_approach_to_root_cause_analysis_using_3_5_why's_technique)  
17. LLM Hallucinations in 2026: How to Understand and Tackle AI's Most Persistent Quirk, 3월 13, 2026에 액세스, [https://www.lakera.ai/blog/guide-to-hallucinations-in-large-language-models](https://www.lakera.ai/blog/guide-to-hallucinations-in-large-language-models)  
18. How to Systematically Tame LLM Hallucinations: A Developer's Guide | by Nayeem Islam, 3월 13, 2026에 액세스, [https://medium.com/@nomannayeem/how-to-systematically-tame-llm-hallucinations-a-developers-guide-de2b16ece764](https://medium.com/@nomannayeem/how-to-systematically-tame-llm-hallucinations-a-developers-guide-de2b16ece764)  
19. How to Detect Hallucinations in Your LLM Applications \- Maxim AI, 3월 13, 2026에 액세스, [https://www.getmaxim.ai/articles/how-to-detect-hallucinations-in-your-llm-applications/](https://www.getmaxim.ai/articles/how-to-detect-hallucinations-in-your-llm-applications/)  
20. LLM hallucinations and failures: lessons from 5 examples \- Evidently AI, 3월 13, 2026에 액세스, [https://www.evidentlyai.com/blog/llm-hallucination-examples](https://www.evidentlyai.com/blog/llm-hallucination-examples)  
21. Smart Audit System Empowered by LLM \- arXiv, 3월 13, 2026에 액세스, [https://arxiv.org/html/2410.07677v1](https://arxiv.org/html/2410.07677v1)  
22. problem-solving | Skills Marketplace \- LobeHub, 3월 13, 2026에 액세스, [https://lobehub.com/skills/geekatron-jerry-problem-solving](https://lobehub.com/skills/geekatron-jerry-problem-solving)  
23. Performing effective root cause analysis | New Relic, 3월 13, 2026에 액세스, [https://newrelic.com/blog/observability/performing-effective-root-cause-analysis](https://newrelic.com/blog/observability/performing-effective-root-cause-analysis)  
24. Root Cause Analysis: What It Is and Methods For Doing It \- Slack, 3월 13, 2026에 액세스, [https://slack.com/blog/productivity/root-cause-analysis-what-it-is-how-to-do-it-and-examples-that-work](https://slack.com/blog/productivity/root-cause-analysis-what-it-is-how-to-do-it-and-examples-that-work)  
25. Fishbone Diagram in Root Cause Analysis: Explained \- The Knowledge Academy, 3월 13, 2026에 액세스, [https://www.theknowledgeacademy.com/blog/root-cause-analysis-fishbone/](https://www.theknowledgeacademy.com/blog/root-cause-analysis-fishbone/)  
26. Solve Anything: AI-Powered Problem Analysis with Fishbone Diagrams \+ ChatGPT, 3월 13, 2026에 액세스, [https://www.youtube.com/watch?v=u-EhJBGZ63Q](https://www.youtube.com/watch?v=u-EhJBGZ63Q)  
27. \[2509.23735\] Diagnosing Failure Root Causes in Platform-Orchestrated Agentic Systems: Dataset, Taxonomy, and Benchmark \- arXiv.org, 3월 13, 2026에 액세스, [https://arxiv.org/abs/2509.23735](https://arxiv.org/abs/2509.23735)  
28. What is FMEA? Failure Mode and Effects Analysis \- Fabrico SaaS, 3월 13, 2026에 액세스, [https://www.fabrico.io/blog/fmea/](https://www.fabrico.io/blog/fmea/)  
29. Overview of Failure Mode and Effects Analysis (FMEA): A Patient Safety Tool \- PMC, 3월 13, 2026에 액세스, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10229026/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10229026/)  
30. The Future of Manufacturing: FMEA Analysis Empowered by AI \- Praxie.com, 3월 13, 2026에 액세스, [https://praxie.com/fmea-analysis-using-ai/](https://praxie.com/fmea-analysis-using-ai/)  
31. How to calculate Risk Priority Number RPN in FMEA \- Scrut, 3월 13, 2026에 액세스, [https://www.scrut.io/post/calculate-rpn-in-fmea](https://www.scrut.io/post/calculate-rpn-in-fmea)  
32. FMEA RPN \- Risk Priority Number. How to Calculate and Evaluate? | IQASystem, 3월 13, 2026에 액세스, [https://www.iqasystem.com/news/risk-priority-number/](https://www.iqasystem.com/news/risk-priority-number/)  
33. How to perform Failure Mode and Effects Analysis in a Risk Assessment Engine?, 3월 13, 2026에 액세스, [https://www.tencentcloud.com/techpedia/125729](https://www.tencentcloud.com/techpedia/125729)  
34. Examining Risk Priority Numbers in FMEA \- HBK, 3월 13, 2026에 액세스, [https://www.hbkworld.com/en/knowledge/resource-center/articles/examining-risk-priority-numbers-in-fmea](https://www.hbkworld.com/en/knowledge/resource-center/articles/examining-risk-priority-numbers-in-fmea)  
35. FMEA-AI: AI fairness impact assessment using failure mode and effects analysis, 3월 13, 2026에 액세스, [https://www.researchgate.net/publication/359070382\_FMEA-AI\_AI\_fairness\_impact\_assessment\_using\_failure\_mode\_and\_effects\_analysis](https://www.researchgate.net/publication/359070382_FMEA-AI_AI_fairness_impact_assessment_using_failure_mode_and_effects_analysis)  
36. Revised Risk Priority Number in Failure Mode and Effects Analysis Model from the Perspective of Healthcare System \- PMC, 3월 13, 2026에 액세스, [https://pmc.ncbi.nlm.nih.gov/articles/PMC5801596/](https://pmc.ncbi.nlm.nih.gov/articles/PMC5801596/)  
37. AI-Powered FMEA Development | Intelligent Automation \- Omnex, 3월 13, 2026에 액세스, [https://www.omnex.com/focus-areas/artificial-intelligence-and-digital-platforms/unlocking-the-power-of-ai-for-fmea-development](https://www.omnex.com/focus-areas/artificial-intelligence-and-digital-platforms/unlocking-the-power-of-ai-for-fmea-development)  
38. YuchenXia/LLMRiskAnalyzer: Failure Mode and Effect Analysis (FMEA) assisted by LLM \- GitHub, 3월 13, 2026에 액세스, [https://github.com/YuchenXia/LLMRiskAnalyzer](https://github.com/YuchenXia/LLMRiskAnalyzer)  
39. (PDF) A framework for automating failure modes and effects analysis ..., 3월 13, 2026에 액세스, [https://www.researchgate.net/publication/400877218\_A\_framework\_for\_automating\_failure\_modes\_and\_effects\_analysis\_FMEA\_using\_large\_language\_models\_LLMs\_and\_retrieval-augmented\_generation\_RAG/download](https://www.researchgate.net/publication/400877218_A_framework_for_automating_failure_modes_and_effects_analysis_FMEA_using_large_language_models_LLMs_and_retrieval-augmented_generation_RAG/download)  
40. AI-driven FMEA: integration of large language models for faster and more accurate risk analysis | Design Science \- Cambridge University Press & Assessment, 3월 13, 2026에 액세스, [https://www.cambridge.org/core/journals/design-science/article/aidriven-fmea-integration-of-large-language-models-for-faster-and-more-accurate-risk-analysis/22F110A2BF0DB4D01A69472CF17A0B43](https://www.cambridge.org/core/journals/design-science/article/aidriven-fmea-integration-of-large-language-models-for-faster-and-more-accurate-risk-analysis/22F110A2BF0DB4D01A69472CF17A0B43)  
41. The consistency analysis of failure mode and effect analysis (FMEA) in information technology risk assessment \- PMC, 3월 13, 2026에 액세스, [https://pmc.ncbi.nlm.nih.gov/articles/PMC6994836/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6994836/)  
42. Managing Complex Failure Analysis Workflows with LLM-based Reasoning and Acting Agents \- arXiv.org, 3월 13, 2026에 액세스, [https://arxiv.org/html/2506.15567v1](https://arxiv.org/html/2506.15567v1)  
43. Using AI for Failure Mode Analysis in Maintenance \- Oxmaint, 3월 13, 2026에 액세스, [https://oxmaint.com/article/ai-failure-mode-analysis-maintenance](https://oxmaint.com/article/ai-failure-mode-analysis-maintenance)  
44. Reducing Scrap and Rework Using AI-Driven Root Cause Analysis \- Auxiliobits, 3월 13, 2026에 액세스, [https://www.auxiliobits.com/blog/reducing-scrap-and-rework-using-ai-driven-root-cause-analysis/](https://www.auxiliobits.com/blog/reducing-scrap-and-rework-using-ai-driven-root-cause-analysis/)  
45. Enhancing Failure Mode and Effects Analysis Using Auto Machine Learning: A Case Study of the Agricultural Machinery Industry \- MDPI, 3월 13, 2026에 액세스, [https://www.mdpi.com/2227-9717/8/2/224](https://www.mdpi.com/2227-9717/8/2/224)  
46. LLM Evaluation and Agent Evaluation | MLflow AI Platform, 3월 13, 2026에 액세스, [https://mlflow.org/llm-evaluation](https://mlflow.org/llm-evaluation)  
47. Evaluating AI agents: Real-world lessons from building agentic systems at Amazon, 3월 13, 2026에 액세스, [https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-real-world-lessons-from-building-agentic-systems-at-amazon/](https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-real-world-lessons-from-building-agentic-systems-at-amazon/)  
48. AgentRx: Diagnosing AI Agent Failures from Execution Trajectories \- Microsoft Research, 3월 13, 2026에 액세스, [https://www.microsoft.com/en-us/research/publication/agentrx-diagnosing-ai-agent-failures-from-execution-trajectories/](https://www.microsoft.com/en-us/research/publication/agentrx-diagnosing-ai-agent-failures-from-execution-trajectories/)  
49. \[2602.09937\] Why Do AI Agents Systematically Fail at Cloud Root Cause Analysis? \- arXiv, 3월 13, 2026에 액세스, [https://arxiv.org/abs/2602.09937](https://arxiv.org/abs/2602.09937)  
50. OpenRCA: Can Large Language Models Locate the Root Cause of Software Failures?, 3월 13, 2026에 액세스, [https://openreview.net/forum?id=M4qNIzQYpd](https://openreview.net/forum?id=M4qNIzQYpd)  
51. Stalled, Biased, and Confused: Uncovering Reasoning Failures in LLMs for Cloud-Based Root Cause Analysis \- arXiv, 3월 13, 2026에 액세스, [https://arxiv.org/html/2601.22208v1](https://arxiv.org/html/2601.22208v1)  
52. \[2403.04123\] Exploring LLM-based Agents for Root Cause Analysis \- arXiv, 3월 13, 2026에 액세스, [https://arxiv.org/abs/2403.04123](https://arxiv.org/abs/2403.04123)  
53. Evaluation-Driven Development and Operations of LLM Agents: A Process Model and Reference Architecture \- arXiv.org, 3월 13, 2026에 액세스, [https://arxiv.org/html/2411.13768v3](https://arxiv.org/html/2411.13768v3)  
54. Why Traditional Testing Fails for AI Agents (and What Actually Works) \- Coralogix, 3월 13, 2026에 액세스, [https://coralogix.com/ai-blog/why-traditional-testing-fails-for-ai-agents-and-what-actually-works/](https://coralogix.com/ai-blog/why-traditional-testing-fails-for-ai-agents-and-what-actually-works/)  
55. 7 Best Agent Evaluation Frameworks \- Galileo AI, 3월 13, 2026에 액세스, [https://galileo.ai/blog/best-agent-evaluation-frameworks](https://galileo.ai/blog/best-agent-evaluation-frameworks)  
56. Top Tools to Evaluate and Benchmark AI Agent Performance in 2026 | Dr. Randal S. Olson, 3월 13, 2026에 액세스, [https://randalolson.com/2026/03/06/top-tools-to-evaluate-and-benchmark-ai-agent-performance-2026/](https://randalolson.com/2026/03/06/top-tools-to-evaluate-and-benchmark-ai-agent-performance-2026/)  
57. Top LLM Evaluation Platforms: In Depth Comparison : r/AI\_Agents \- Reddit, 3월 13, 2026에 액세스, [https://www.reddit.com/r/AI\_Agents/comments/1pa02zc/top\_llm\_evaluation\_platforms\_in\_depth\_comparison/](https://www.reddit.com/r/AI_Agents/comments/1pa02zc/top_llm_evaluation_platforms_in_depth_comparison/)