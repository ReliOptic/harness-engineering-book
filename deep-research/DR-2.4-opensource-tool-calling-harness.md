# **DR-2.4 Ch.2 인공지능 에이전트 오케스트레이션의 기술적 딜레마와 복원력 있는 하네스 아키텍처 연구: 네이티브 툴 호출과 스크래치패드 현상의 심층 분석**

오늘날 인공지능(AI) 엔지니어링 업계는 거대언어모델(LLM)을 단순한 텍스트 생성기를 넘어, 외부 도구와 상호작용하며 실질적인 업무를 수행하는 '에이전트'로 진화시키는 과정에서 심각한 기술적 딜레마에 직면해 있다. 이른바 "합리적인 의심과 피로감"으로 정의되는 이 현상은, 수많은 오픈소스 모델의 등장에도 불구하고 왜 여전히 고비용의 프론티어 모델(OpenAI, Google, Anthropic 등)을 고집할 수밖에 없는지에 대한 근본적인 질문을 던진다.1 본 보고서는 프론티어 모델의 '네이티브 툴 호출(Native Tool Calling)' 기능과 오픈소스 모델에서 나타나는 '스크래치패드(Scratchpad)' 현상의 기술적 격차를 규명하고, 모델의 불확실성 속에서도 시스템의 안정성을 보장하는 '하네스(Harness)' 아키텍처의 필요성과 구축 전략을 심층적으로 논의한다.

## **1\. 함수 호출 훈련의 기술적 격차: 네이티브 툴 호출의 본질**

프론티어 모델과 하위 모델을 가르는 가장 결정적인 잣대는 사용자의 의도를 구조화된 실행 명령으로 변환하는 '함수 호출(Function Calling)'의 정교함에 있다. OpenAI의 GPT-4o나 Google의 Gemini 1.5 Pro와 같은 최상위 모델들은 '네이티브 툴 호출'이라 불리는 메커니즘을 구현하기 위해 수십만 번의 미세조정(Fine-tuning) 과정을 거쳤다.1

네이티브 툴 호출의 핵심은 모델이 시스템으로부터 도구 사용 명령을 받았을 때, 겉으로 드러나는 자연어 응답(content)을 완전히 생략하거나 null로 처리하면서 내부적으로 정확한 JSON 형태의 tool\_calls 속성만을 출력하도록 최적화되었다는 점이다.1 이러한 훈련 방식은 모델이 '생각'과 '행동'을 분리하지 않고, 입력된 맥락에서 즉각적으로 최적의 도구와 매개변수를 도출하게 만든다. 이는 개발자 입장에서 별도의 파싱(parsing)이나 텍스트 필터링 없이도 모델의 출력을 즉시 API 호출에 활용할 수 있음을 의미하며, 결과적으로 전체 시스템의 지연 시간(latency)을 단축하고 오류 발생 가능성을 극도로 낮춘다.1

### **프론티어 모델과 일반 모델의 툴 호출 아키텍처 비교**

| 비교 항목 | 네이티브 툴 호출 (Frontier Models) | 프롬프트 기반 호출 (Small/Open Models) |
| :---- | :---- | :---- |
| **출력 구조** | API 레벨에서 정의된 tool\_calls 필드 사용 1 | 자연어 텍스트 블록 내에 JSON 포함 6 |
| **추론 방식** | 암묵적 매핑 및 직접 구조화 1 | 명시적 추론(Chain-of-Thought) 후 구조화 7 |
| **응답 가독성** | content: null로 깔끔한 데이터 전달 1 | "생각 중..." 등의 혼잣말 포함 가능성 높음 8 |
| **훈련 데이터** | 수십만 건의 전용 툴 사용 데이터셋 적용 1 | 일반적인 지시 이행 및 대화 데이터 중심 9 |
| **신뢰도** | 스키마 준수율 및 매개변수 정확도 매우 높음 5 | 복잡한 스키마에서 구문 오류 발생 빈번 10 |

이러한 기술적 우위는 단순히 모델의 파라미터 크기에서 오는 것이 아니라, 도구 사용이라는 특수한 목적에 부합하도록 설계된 정교한 보상 모델과 강화 학습의 결과물이다.1 따라서 프론티어 모델은 사용자의 말귀를 '한 번에 찰떡같이' 알아듣고 군말 없이 일만 수행하는 전문 비서와 같은 역할을 수행하게 된다.

## **2\. 오픈소스 모델의 한계와 스크래치패드 현상의 필연성**

반면, 파라미터 수가 적거나 툴 사용 훈련이 충분하지 않은 오픈소스 및 무료 모델들은 복잡한 JSON 형식을 단번에 생성하는 능력이 현저히 떨어진다. 이들 모델에서 공통적으로 관찰되는 '스크래치패드(Scratchpad)' 현상은 모델이 행동(함수 호출)을 하기 전, 사람처럼 자신의 생각을 말로 정리(Chain-of-Thought)해야만 비로소 정확한 명령어를 만들어낼 수 있는 특성에서 기인한다.7

기술적인 관점에서 볼 때, 이는 모델의 추론 능력이 특정 토큰 수 안에 압축되지 못하고 문맥 윈도우(context window)라는 연산 공간을 빌려 '생각의 흐름'을 펼쳐야만 문제 해결이 가능함을 시사한다.7 만약 엔지니어가 시스템 프롬프트를 통해 이러한 혼잣말을 억지로 금지하면, 모델은 논리적 단계를 생략하게 되어 엉뚱한 매개변수를 생성하거나 JSON 문법을 어기는 등 소위 '멍청해지는' 현상이 발생한다.7

### **스크래치패드 전략에 따른 정확도 변화 (GPT-4o 및 하위 모델 테스트)**

| 시나리오 | 추론 단계(Reasoning Steps) 위치 | 실행 정확도 (%) | 비고 |
| :---- | :---- | :---- | :---- |
| **Case A** | 추론 단계 없음 | 0% | 복잡한 계산 및 툴 선택 실패 7 |
| **Case B** | 마지막 매개변수로 추론 단계 배치 | 20% 이하 | 결론을 먼저 내린 후 추론하여 오류 수정 불가 7 |
| **Case C** | 첫 번째 매개변수로 추론 단계 배치 | 100% 가깝게 도달 | 충분한 연산 공간 확보 후 최종 값 도출 7 |

이러한 특성 때문에 오픈소스 모델을 실무에 투입하려면 시스템이 모델의 혼잣말을 실시간으로 감지하고, 실제 API로 전달되는 데이터에서 이를 분리해내는 필터링 엔지니어링이 필수적으로 수반되어야 한다.12 이는 개발 생산성을 저해하고 인프라 비용 외의 '엔지니어링 공수'를 기하급수적으로 늘리는 원인이 된다.

## **3\. 모델의 비결정론을 극복하는 '하네스(Harness)' 아키텍처**

모델이 에러를 내거나 예기치 못한 응답을 뱉더라도 전체 시스템, 특히 기억력(Memory)과 봇의 실행 상태가 유지되도록 만드는 '하네스'의 구축은 에이전트 엔지니어링의 핵심 과제이다.14 하네스는 모델을 감싸는 보호막이자 오케스트레이션 계층으로서, 모델의 실패가 서비스 전체의 셧다운으로 이어지지 않도록 방어한다.

### **3.1. 내구성이 있는 실행(Durable Execution)과 상태 관리**

하네스 설계의 가장 중요한 원칙은 '에이전트의 실행 상태'를 모델의 추론 과정과 완전히 분리하는 것이다. 이를 위해 Temporal, Inngest, 혹은 DBOS와 같은 프레임워크가 제안하는 '내구성이 있는 실행' 패턴이 활용된다.16 이 아키텍처 하에서 에이전트의 모든 활동은 '체크포인트(Checkpoint)'를 통해 외부 데이터베이스에 기록된다.

* **의미적 체크포인팅(Semantic Checkpointing):** 각 단계의 LLM 호출 결과, 도구 사용 기록, 결정 사항 등을 스냅샷 형태로 저장한다.18  
* **오류 복구 메커니즘:** 모델이 잘못된 JSON을 반환하거나 API 속도 제한(Rate Limit)에 걸려 죽더라도, 하네스는 마지막 성공 지점부터 다시 시작할 수 있게 한다.17  
* **비결정론의 통제:** LLM의 응답은 매번 바뀔 수 있지만, 이미 수행된 도구 호출(예: 결제 완료, 메일 발송)은 재실행되지 않도록 멱등성(Idempotency)을 보장한다.16

### **3.2. JSON 수리 및 스키마 검증 시스템**

오픈소스 모델의 불안정한 출력을 보완하기 위해 하네스 내부에는 강력한 출력 필터와 수리(Repair) 로직이 내장되어야 한다. json\_repair와 같은 라이브러리는 모델이 누락한 괄호나 잘못된 따옴표를 수정하여 파싱 에러를 방지한다.10 또한 Pydantic이나 Instructor와 같은 도구를 사용하여 모델의 출력이 사전에 정의된 데이터 형식을 엄격히 준수하는지 검증하고, 실패 시 자동으로 재질의(Re-asking)를 수행한다.21

## **4\. 성능 벤치마크 분석: BFCL과 실전 모델 평가**

거대언어모델의 함수 호출 능력을 객관적으로 평가하는 기준점으로 '버클리 함수 호출 리더보드(Berkeley Function Calling Leaderboard, BFCL)'가 널리 사용된다.2 2025년 말 업데이트된 최신 데이터에 따르면, 프론티어 모델과 오픈소스 모델 간의 격차는 특정 영역에서 좁혀지고 있으나 여전히 복합적인 시나리오에서는 유의미한 차이가 존재한다.

### **주요 모델별 BFCL v4 성능 지표 요약**

| 순위 | 모델명 | 전체 정확도 (%) | AST 정확도 (%) | 실행 정확도 (%) | 특이사항 |
| :---- | :---- | :---- | :---- | :---- | :---- |
| 1 | Claude 4 Opus 4.1 | 70.36 | 85.50 | 89.25 | 복잡한 스키마 이해력 최상 2 |
| 2 | Claude 4 Sonnet 4.5 | 70.29 | 82.50 | 88.65 | 속도와 정확도의 최적 밸런스 2 |
| 3 | GPT-5 Medium | 59.22 | 89.27 | 90.07 | 높은 비용 효율성 및 멀티모달 지원 2 |
| 4 | ToolACE-8B (Open Source) | 59.22 | 89.27 | 90.07 | 8B 파라미터로 GPT-4급 성능 달성 9 |
| 5 | Granite-20B-FC | 84.71 | 84.11 | 86.50 | 오픈 라이선스 모델 중 가장 안정적 24 |

리더보드 분석을 통해 도출된 핵심 통찰은 다음과 같다. 첫째, 파라미터 크기가 절대적인 성능을 보장하지 않는다. ToolACE-8B와 같이 툴 호출 전용 데이터셋으로 훈련된 소형 모델이 훨씬 거대한 범용 모델보다 높은 AST(Abstract Syntax Tree) 정확도를 보일 수 있다.9 둘째, '무관함 감지(Irrelevance Detection)' 능력이 모델의 완성도를 좌우한다. 사용자 질문에 답하기 위해 도구가 필요 없는 상황에서 억지로 도구를 쓰려 하지 않는 능력은 고도의 미세조정이 필요하며, 이 부분에서 프론티어 모델의 우위가 두드러진다.23 셋째, 멀티턴(Multi-turn) 대화 상황에서의 성능 저하가 공통적인 약점이다. 대화가 길어질수록 과거의 도구 호출 결과와 현재의 목표를 일치시키는 능력이 급격히 떨어지며, 이는 하네스의 기억 시스템이 왜 중요한지를 다시 한번 증명한다.23

## **5\. 경제성 평가: API 비용과 자체 호스팅의 총소유비용(TCO)**

프론티어 모델의 높은 비용에도 불구하고 이를 선택하는 이유는 단순히 성능 때문만이 아니라, 자체 호스팅 모델이 수반하는 '숨겨진 비용'에 기인한다.27 2026년 기준, 하루 5천만 토큰 이상을 처리하는 고용량 Tier에서의 비용 분석은 다음과 같은 시사점을 준다.

### **2026년 기준 LLM 배포 방식별 TCO 비교 (연간 기준)**

| 항목 | GPT-5.2 API (프론티어) | Llama 3.3 70B (관리형 API) | Llama 3.3 70B (자체 호스팅) |
| :---- | :---- | :---- | :---- |
| **토큰 비용** | 약 $432,000 29 | 약 $120,000 29 | $0 (인프라 비용 별도) |
| **인프라 비용** | $0 | $0 | 약 $54,000 (H100 2개) 29 |
| **운영 인건비** | 낮음 (API 관리 수준) | 중간 (MLOps 필요) | 높음 (24/7 모니터링) 27 |
| **총계 (추정)** | **$450,000+** | **$150,000+** | **$120,000+ (인건비 포함 시)** |

데이터에 따르면, 토큰 사용량이 월 1천만 건 이하인 소규모 프로젝트에서는 프론티어 API를 쓰는 것이 압도적으로 경제적이다.29 그러나 서비스 규모가 커질수록 자체 호스팅의 이점이 커지는데, 이때 앞서 언급한 '하네스'가 잘 구축되어 있다면 엔지니어는 인프라 비용 0원에 수렴하는 오픈소스 모델로 즉시 전환할 수 있는 전략적 유연성을 얻게 된다.14

자체 호스팅의 가장 큰 리스크는 GPU 장비의 유휴 시간(Idle time)과 운영 복잡성이다. 에이전트가 24시간 내내 풀가동되지 않는다면, 사용한 만큼만 지불하는 프론티어 API가 실제로는 더 저렴할 수 있다.30 하지만 금융이나 의료와 같이 데이터 보안과 낮은 지연 시간이 생명인 산업군에서는 비용과 관계없이 에어갭(Air-gap) 환경을 구축할 수 있는 자체 호스팅 모델이 유일한 선택지가 된다.31

## **6\. 강화된 에이전트 훈련: ToolACE와 xLAM의 부상**

오픈소스 진영에서도 네이티브 툴 호출 능력을 확보하기 위한 노력이 이어지고 있으며, 그 선두에는 ToolACE와 xLAM 데이터셋이 있다.9 이들은 기존의 수동 라벨링 방식에서 벗어나 AI가 AI를 가르치는 '자기 진화 합성(Self-evolution synthesis)' 기법을 도입했다.

* **ToolACE (Salesforce 등):** 26,507개의 고유 API를 포함하는 방대한 풀을 구축하고, 390개 도메인에 걸친 다양한 시나리오를 자동 생성한다. 특히 단순 호출을 넘어 병렬(Parallel), 의존(Dependent), 중첩(Nested) 호출 등 실제 복잡한 워크플로우를 학습시킨다.9  
* **xLAM (Salesforce):** 미스트랄(Mistral)이나 라마(Llama) 기반 모델을 툴 호출 전용으로 미세조정하기 위한 고품질 데이터셋을 제공한다. 이를 통해 7B 수준의 소형 모델에서도 프론티어 모델에 육박하는 툴 호출 정확도를 이끌어낸다.11  
* **GRPO 강화학습:** DeepSeek-R1 등에서 사용된 Group Relative Policy Optimization(GRPO) 기법은 모델이 툴 호출 시 자신의 오류를 스스로 수정하고 최적의 경로를 찾는 '추론형 툴 사용' 능력을 배양한다.35

이러한 특수 목적 모델들은 프론티어 모델의 범용적인 지능은 부족할지 몰라도, 특정 도메인의 툴 호출 업무에서는 "군말 없이 일만 잘하는" 수준에 도달하고 있다.31

## **7\. 환각 방지와 안정성 제어 기법**

에이전트가 존재하지 않는 API 매개변수를 꾸며내거나 성공하지 않았는데 성공했다고 거짓말하는 '환각(Hallucination)' 현상은 운영 환경에서 치명적이다.36 하네스는 이러한 환각을 방지하기 위해 다층적인 방어 기법을 적용해야 한다.

### **환각 제어를 위한 4대 핵심 기술**

1. **그래프-RAG(Graph-RAG):** 단순 텍스트 검색을 넘어 지식 그래프를 통해 정형화되고 검증된 데이터만을 모델에 제공함으로써, 존재하지 않는 정보를 지어내는 행위를 원천 차단한다.36  
2. **신경 기호 가드레일(Neurosymbolic Guardrails):** 비즈니스 규칙을 자연어 프롬프트가 아닌 실제 코드로 강제한다. 예를 들어, 결제 모듈 호출 전 사용자 인증 확인 여부를 하네스가 물리적으로 검증하는 방식이다.36  
3. **멀티 에이전트 검증(Multi-agent Validation):** 실행 에이전트(Executor)와 검증 에이전트(Validator)를 분리하여, 실행 에이전트가 제안한 도구 호출 계획을 검증 에이전트가 비판적으로 검토한 뒤 승인한다.36  
4. **출력 구조 강제(Structured Output Enforcement):** 모델이 자유로운 텍스트를 생성하지 못하도록 문법적 제약(CFG)을 가하거나, 유효한 토큰만을 생성하도록 필터링하여 문법 오류를 원천 배제한다.37

에이전트의 신뢰도는 개별 모델의 지능보다 시스템이 설계한 '검증 루프'의 촘촘함에 의해 결정된다.37 "프롬프트에 기도하는(Prompt & Pray)" 방식에서 벗어나 결정론적인 비즈니스 로직과 확률론적인 LLM을 적절히 격리하는 것이 엔지니어링의 정수이다.40

## **8\. 미래 전망: MCP와 에이전트 오케스트레이션의 표준화**

2025년 말 Anthropic이 발표한 '모델 컨텍스트 프로토콜(Model Context Protocol, MCP)'은 에이전트와 도구 간의 연결 방식을 혁신하고 있다.1 기존에는 각 도구마다 커스텀 통합 코드를 작성해야 했지만, MCP는 이를 범용적인 클라이언트-서버 구조로 표준화한다.

* **상호운용성:** 한 번 구축한 MCP 서버는 GPT, Claude, Llama 등 어떤 모델과도 즉시 연결될 수 있어 벤더 락인(Vendor Lock-in)을 방지한다.41  
* **보안 격리:** 에이전트가 직접 데이터베이스나 로컬 파일에 접근하는 대신, MCP 서버라는 통제된 게이트웨이를 통하게 함으로써 보안 위협을 최소화한다.41  
* **인프라로서의 하네스:** MCP의 보급은 개별 엔지니어가 구축한 '하네스'가 단순한 코드 뭉치를 넘어 하나의 독립적인 마이크로서비스로 기능하게 됨을 의미한다.15

## **9\. 결론 및 제언**

현재 AI 엔지니어링 업계가 겪고 있는 피로감은 거대 모델의 압도적인 편리함과 오픈소스 모델의 복잡한 핸들링 사이의 간극에서 발생한다. 프론티어 모델은 네이티브 툴 호출 훈련을 통해 엔지니어의 부담을 최소화해주지만, 그 대가로 높은 비용과 통제권의 상실을 요구한다.1 반면 오픈소스 모델은 스크래치패드 현상이라는 내재적 한계를 가지고 있으나, 이를 보완할 수 있는 강력한 하네스 아키텍처가 뒷받침된다면 진정한 인프라 독립과 비용 최적화를 달성할 수 있다.14

에이전트 시스템을 성공적으로 구축했다는 것은 단순히 '똑똑한 모델'을 선택했다는 뜻이 아니라, 모델이 실패하더라도 기억과 상태를 유지하며 자가 치유를 시도하는 '복원력 있는 하네스'를 완성했음을 의미한다.14 이러한 기반 위에서 엔지니어는 모델의 발전에 따라 가장 효율적인 지능을 선택적으로 갈아 끼울 수 있는 '모델 불가지론적(Model-agnostic)'인 경쟁력을 갖추게 될 것이다. 결국 승자는 모델의 성능에 의존하는 자가 아니라, 모델의 비결정론을 시스템적으로 통제하는 하네스 설계자가 될 것이다.

수학적으로 에이전트의 성공 확률 $P\_{agent}$는 다음과 같은 수식으로 표현될 수 있다.

![][image1]  
여기서 $P\_{model}$은 모델의 툴 호출 정확도이며, $P\_{harness}$는 오류 감지 및 복구 성공 확률이다. 모델의 지능이 70% 수준이라 하더라도 하네스의 복구 능력이 90%를 상회한다면, 전체 시스템은 97% 이상의 높은 신뢰도를 유지할 수 있다. 이것이 바로 우리가 비싼 프론티어 모델의 대안으로 하네스 엔지니어링에 집중해야 하는 이유이다.

#### **참고 자료**

1. Function Calling: How LLMs Execute Real-World Actions | ZIVIS Security Research, 3월 10, 2026에 액세스, [https://www.zivis.ai/publications?article=function-calling-guide](https://www.zivis.ai/publications?article=function-calling-guide)  
2. Function Calling and Agentic AI in 2025: What the Latest Benchmarks Tell Us About Model Performance \- Klavis AI, 3월 10, 2026에 액세스, [https://www.klavis.ai/blog/function-calling-and-agentic-ai-in-2025-what-the-latest-benchmarks-tell-us-about-model-performance](https://www.klavis.ai/blog/function-calling-and-agentic-ai-in-2025-what-the-latest-benchmarks-tell-us-about-model-performance)  
3. Function Calling with LLMs \- Prompt Engineering Guide, 3월 10, 2026에 액세스, [https://www.promptingguide.ai/applications/function\_calling](https://www.promptingguide.ai/applications/function_calling)  
4. Function Calling vs Tool Calling — A Complete Guide (With OpenAI Example) | by Faria Khan | Medium, 3월 10, 2026에 액세스, [https://medium.com/@zainabmustaqeem123/function-calling-vs-tool-calling-a-complete-guide-with-openai-example-a46e496934ce](https://medium.com/@zainabmustaqeem123/function-calling-vs-tool-calling-a-complete-guide-with-openai-example-a46e496934ce)  
5. Question: Regarding Structured Output Strategy \- How does it compare to other libraries? \#660, 3월 10, 2026에 액세스, [https://github.com/pydantic/pydantic-ai/issues/660](https://github.com/pydantic/pydantic-ai/issues/660)  
6. Tool Calling Is Not a Solved Problem \- by Jae Li \- Substack, 3월 10, 2026에 액세스, [https://substack.com/home/post/p-167344254](https://substack.com/home/post/p-167344254)  
7. Chain of Thought with Tool Calling and Structured Output | by Clint ..., 3월 10, 2026에 액세스, [https://clintgoodman27.medium.com/chain-of-thought-with-tool-calling-and-structured-output-5afdfc984870](https://clintgoodman27.medium.com/chain-of-thought-with-tool-calling-and-structured-output-5afdfc984870)  
8. Chain-of-Thought Prompting Guide: Master CoT for LLM Super-Reasoning, 3월 10, 2026에 액세스, [https://idealinspiration.blog/chain-of-thought-prompting-guide/](https://idealinspiration.blog/chain-of-thought-prompting-guide/)  
9. ToolACE: Winning the Points of LLM Function Calling \- arXiv, 3월 10, 2026에 액세스, [https://arxiv.org/html/2409.00920v2](https://arxiv.org/html/2409.00920v2)  
10. Tutorial on Using json\_repair in Python: Easily Fix Invalid JSON Returned by LLM \- Medium, 3월 10, 2026에 액세스, [https://medium.com/@yanxingyang/tutorial-on-using-json-repair-in-python-easily-fix-invalid-json-returned-by-llm-8e43e6c01fa0](https://medium.com/@yanxingyang/tutorial-on-using-json-repair-in-python-easily-fix-invalid-json-returned-by-llm-8e43e6c01fa0)  
11. Tool Zero: Training Tool-Augmented LLMs via Pure RL from Scratch \- ACL Anthology, 3월 10, 2026에 액세스, [https://aclanthology.org/2025.findings-emnlp.485.pdf](https://aclanthology.org/2025.findings-emnlp.485.pdf)  
12. AI Agent Architecture Patterns for Developers: A Practical Guide | Breyta Blog, 3월 10, 2026에 액세스, [https://breyta.ai/blog/ai-agent-architecture-patterns](https://breyta.ai/blog/ai-agent-architecture-patterns)  
13. \[R\] Plain English outperforms JSON for LLM tool calling: \+18pp accuracy, \-70% variance, 3월 10, 2026에 액세스, [https://www.reddit.com/r/MachineLearning/comments/1o8szk0/r\_plain\_english\_outperforms\_json\_for\_llm\_tool/](https://www.reddit.com/r/MachineLearning/comments/1o8szk0/r_plain_english_outperforms_json_for_llm_tool/)  
14. The Agent Harness Is the Architecture (and Your Model Is Not the Bottleneck) \- Medium, 3월 10, 2026에 액세스, [https://medium.com/@epappas/the-agent-harness-is-the-architecture-and-your-model-is-not-the-bottleneck-5ae5fd067bb2](https://medium.com/@epappas/the-agent-harness-is-the-architecture-and-your-model-is-not-the-bottleneck-5ae5fd067bb2)  
15. Agent Frameworks vs Runtime vs Harnesses: What They Are and When to Use Which, 3월 10, 2026에 액세스, [https://www.analyticsvidhya.com/blog/2025/12/agent-frameworks-vs-runtimes-vs-harnesses/](https://www.analyticsvidhya.com/blog/2025/12/agent-frameworks-vs-runtimes-vs-harnesses/)  
16. Durable Workflow Platforms for AI Agents and LLM Workloads \- Render, 3월 10, 2026에 액세스, [https://render.com/articles/durable-workflow-platforms-ai-agents-llm-workloads](https://render.com/articles/durable-workflow-platforms-ai-agents-llm-workloads)  
17. Durable AI Loops: Fault Tolerance across Frameworks and without Handcuffs \- Restate, 3월 10, 2026에 액세스, [https://www.restate.dev/blog/durable-ai-loops-fault-tolerance-across-frameworks-and-without-handcuffs](https://www.restate.dev/blog/durable-ai-loops-fault-tolerance-across-frameworks-and-without-handcuffs)  
18. (PDF) Cost-Performance Trade-offs in Checkpoint-Based LLM Agent Architectures, 3월 10, 2026에 액세스, [https://www.researchgate.net/publication/399575870\_Cost-Performance\_Trade-offs\_in\_Checkpoint-Based\_LLM\_Agent\_Architectures](https://www.researchgate.net/publication/399575870_Cost-Performance_Trade-offs_in_Checkpoint-Based_LLM_Agent_Architectures)  
19. Durable Execution for AI Agents | blog \- inference.sh, 3월 10, 2026에 액세스, [https://inference.sh/blog/agent-runtime/durable-execution](https://inference.sh/blog/agent-runtime/durable-execution)  
20. DyfanJones/llmjson: Fast JSON repair for LLM outputs using Rust-powered string correction \- GitHub, 3월 10, 2026에 액세스, [https://github.com/DyfanJones/llmjson](https://github.com/DyfanJones/llmjson)  
21. Instructor \- Multi-Language Library for Structured LLM Outputs | Python, TypeScript, Go, Ruby \- Instructor, 3월 10, 2026에 액세스, [https://python.useinstructor.com/](https://python.useinstructor.com/)  
22. Leverage LiteLLM in Guardrails to Validate Any LLM's Output \- My Framer Site, 3월 10, 2026에 액세스, [https://guardrailsai.com/blog/guardrails-litellm-validate-llm-output](https://guardrailsai.com/blog/guardrails-litellm-validate-llm-output)  
23. The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models \- ICML 2026, 3월 10, 2026에 액세스, [https://icml.cc/virtual/2025/poster/46593](https://icml.cc/virtual/2025/poster/46593)  
24. Berkeley Function Calling Leaderboard v4 \- Emergent Mind, 3월 10, 2026에 액세스, [https://www.emergentmind.com/topics/berkeley-function-calling-leaderboard-v4-bfclv4](https://www.emergentmind.com/topics/berkeley-function-calling-leaderboard-v4-bfclv4)  
25. ToolACE: Winning the Points of LLM Function Calling \- OpenReview, 3월 10, 2026에 액세스, [https://openreview.net/forum?id=8EB8k6DdCU](https://openreview.net/forum?id=8EB8k6DdCU)  
26. The True Cost of Enterprise AI Agents: A Complete TCO Framework \- Medium, 3월 10, 2026에 액세스, [https://medium.com/@yugank.aman/the-true-cost-of-enterprise-ai-agents-a-complete-tco-framework-e3b6228857e7](https://medium.com/@yugank.aman/the-true-cost-of-enterprise-ai-agents-a-complete-tco-framework-e3b6228857e7)  
27. Local LLMs vs Cloud APIs: 2026 Total Cost of Ownership Analysis | SitePoint, 3월 10, 2026에 액세스, [https://www.sitepoint.com/local-llms-vs-cloud-api-cost-analysis-2026/](https://www.sitepoint.com/local-llms-vs-cloud-api-cost-analysis-2026/)  
28. The Cost of Running Open Source LLMs: A TCO Analysis | Cloudatler, 3월 10, 2026에 액세스, [https://cloudatler.com/blog/the-true-cost-of-running-open-source-llms-a-tco-analysis](https://cloudatler.com/blog/the-true-cost-of-running-open-source-llms-a-tco-analysis)  
29. Open Source vs Closed LLMs: Choosing the Right Model in 2026 \- Let's Data Science, 3월 10, 2026에 액세스, [https://www.letsdatascience.com/blog/open-source-vs-closed-llms-choosing-the-right-model-in-2026](https://www.letsdatascience.com/blog/open-source-vs-closed-llms-choosing-the-right-model-in-2026)  
30. Cost Comparison: API vs Self-Hosting for Open-Weight LLMs \- DETECTX, 3월 10, 2026에 액세스, [https://www.detectx.com.au/cost-comparison-api-vs-self-hosting-for-open-weight-llms/](https://www.detectx.com.au/cost-comparison-api-vs-self-hosting-for-open-weight-llms/)  
31. Self-Hosting AI Guide 2026: Local LLMs vs Cloud APIs | ValueStreamAI Blog, 3월 10, 2026에 액세스, [https://valuestreamai.com/blog/self-hosted-ai-llms-vs-cloud-apis-guide-2026](https://valuestreamai.com/blog/self-hosted-ai-llms-vs-cloud-apis-guide-2026)  
32. Fine-tuning LLMs for Function Calling with xLAM Dataset \- Hugging Face Open-Source AI Cookbook, 3월 10, 2026에 액세스, [https://huggingface.co/learn/cookbook/en/function\_calling\_fine\_tuning\_llms\_on\_xlam](https://huggingface.co/learn/cookbook/en/function_calling_fine_tuning_llms_on_xlam)  
33. \[Literature Review\] ToolACE: Winning the Points of LLM Function Calling \- Moonlight, 3월 10, 2026에 액세스, [https://www.themoonlight.io/en/review/toolace-winning-the-points-of-llm-function-calling](https://www.themoonlight.io/en/review/toolace-winning-the-points-of-llm-function-calling)  
34. ToolACE: Winning the Points of LLM Function Calling \- arXiv.org, 3월 10, 2026에 액세스, [https://arxiv.org/html/2409.00920v1](https://arxiv.org/html/2409.00920v1)  
35. Tool Zero: Training Tool-Augmented LLMs via Pure RL from Scratch \- arXiv, 3월 10, 2026에 액세스, [https://arxiv.org/html/2511.01934v1](https://arxiv.org/html/2511.01934v1)  
36. Stop AI Agent Hallucinations: 4 Essential Techniques \- DEV Community, 3월 10, 2026에 액세스, [https://dev.to/aws/stop-ai-agent-hallucinations-4-essential-techniques-2i94](https://dev.to/aws/stop-ai-agent-hallucinations-4-essential-techniques-2i94)  
37. Prevent AI Agent Hallucinations in Production Environments \- StackAI, 3월 10, 2026에 액세스, [https://www.stack-ai.com/insights/prevent-ai-agent-hallucinations-in-production-environments](https://www.stack-ai.com/insights/prevent-ai-agent-hallucinations-in-production-environments)  
38. Architecting Resilient LLM Agents: A Guide to Secure Plan-then-Execute Implementations \- arXiv, 3월 10, 2026에 액세스, [https://arxiv.org/pdf/2509.08646?](https://arxiv.org/pdf/2509.08646)  
39. instruct/SCRATCHPAD.md at development \- GitHub, 3월 10, 2026에 액세스, [https://github.com/instruct-rb/instruct/blob/development/SCRATCHPAD.md](https://github.com/instruct-rb/instruct/blob/development/SCRATCHPAD.md)  
40. Managing AI Hallucinations: The Power of Tools & Parameters \- Cognigy, 3월 10, 2026에 액세스, [https://www.cognigy.com/product-updates/managing-ai-hallucinations-the-power-of-tools-parameters](https://www.cognigy.com/product-updates/managing-ai-hallucinations-the-power-of-tools-parameters)  
41. MCP vs. Function Calling: How They Differ and Which to Use \- Descope, 3월 10, 2026에 액세스, [https://www.descope.com/blog/post/mcp-vs-function-calling](https://www.descope.com/blog/post/mcp-vs-function-calling)  
42. When to use OpenAI vs. open source LLMs in production \- LogRocket Blog, 3월 10, 2026에 액세스, [https://blog.logrocket.com/openai-vs-open-source-llm/](https://blog.logrocket.com/openai-vs-open-source-llm/)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAAApCAYAAACIn3XTAAAFMklEQVR4Xu3dW6itUxTA8SGX3O/3a4gSJfeEB5Fb8YBO5MFBucUDQhGpkzfk8iaFB4lcHtwvsV2KopTkTeGBIrwpFMbf/OZZc82z9toezt7r7HX+vxrt9c011zrf+NbDGo05v3UiJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJG2G/sm4vzneOeO3jOOasdXmiYzTm+PjM37KeLsZW23I6a8Yz6vmtGMzJkmS5hAF2/kTxh7txlaLnTI+ytinGaOgWcj4uxlbbcjpmxjPayFKTmc3Y5Ikac5sm/FjxmHdeN91W02OyvglY6tmbLeMz6J0qGbloIyt+8G0Q8Ye/eAE5PRCjOdVc2q7bpIkac7QmWkLsy0y7si4bXi8GtEZ7AuzdzN+zjixG19JXM+bYrxoeznj5OZ4mr4w2yVmn5MkSVoBd0bZA/X4EF9kfB6zK9a+XyLezNh9/ezJFjL+iFFOT2c8mXFgM2dWuK6PRSna9o3/X6yxpEtOz8Qopx9i08hJkiQtI5ZDX8s4I2O/IXYdm7HxbdkPLAOWDt+JUU7ExnBDxu/94ODYKHvM2D+3FLpsz2e80j8xBcu85HRIjHLi88P+GR/GhsvakiRpDrAcupKb8Clq9uwHO22RNSn2jqWLvuXahE8369N+cMC+siv6wUXQJTwlY21M3tM2Ccu803KiUypJkubQXVFuLlgMBcqDGedmHDCM8ZMfd2e8GKXrgwsynhpir4xHMm6O8jMULOHRCbo9ytIrz7H5fjGXLhHczbrd+tkbosP1bYzOt0VRdW3GEVFyPyfj1IznoixPVvdmvBplHx/4917KeCDjjWGM4pHrcGWUZU4K0Xo9puGa1mXQdnl0mnrX66ScwPWlW1evd10m5byvy7g444SMC6N09k7LWDc8f2iU68rYw1H2xaHmx3Woy+PcHPF6jApTju8Zjme1hC5J0tzijsQ/oxRrBF/y24/NiHg2ytIdPonRT0nUuxS565IN8HR9ro+yXEjBQDF0XpTijC9x9o6B+e8Nj5cDy7rfxSinX8ef/g/duSOjFC+geCEX4qLhL3lXdK2uiVKk1KKIgpFlZF57WcbVUfKkMFoKxU1/gwCvpWBa041XfU6cT4/PoL3enAvnxnlTlNXzPnh4TK4UZuTL58VreC3vwXuRa83voeG5unx+S5Ql2Hr81XAsSZJm4MuMk4bHtbCho1ILE7pJdJUoavoOEWPceUqRtzCMMf/9OmGGKNYoHlGXEekyEXSVvh7GyJfilM39dOPqcij7xJhz5jAPde6stNebvWzHxOi8QXeO86ZDVx9XFGO1Y/ZBlM+U69DmVx0e5Yd66brWYzqm9ViSJK2whShf3Hyh35pxVZQvfJbVsDZKodJ2lmrXhgKPLg7BY7pHFAV08m4c5s1KXb7jrsu6J4wxlin5S0GDo6MUMBQ+5EzXkOXQszI+jlGXjnncCEAxOqn7tdza68058jMhdPHqeaOeN/nymMK7onituVD0MY/X1TFQxPG+FIYsr97XHINjSZI0I3yx0z3jL0VOxZ6qt5pjlljrHYvMawuCdqm1HZ+Vej5tPmhvZOjvlK0dxG2ax+RL3lXfZVwpk653zaV+dvW82/Ov2rzbz7nm116n/r+/4rgfkyRJM0YHiYLgkiib0SVJkrSJYcP+uozLY/qdmpIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZIkSZu9fwED+cSTfXgG1wAAAABJRU5ErkJggg==>