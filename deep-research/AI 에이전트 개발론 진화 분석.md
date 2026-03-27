# **2023-2026 AI 에이전트 개발론의 진화: 프롬프트 엔지니어링에서 하네스 엔지니어링으로의 패러다임 전환과 기술적 고찰**

## **1\. 서론: 인공지능 에이전트 아키텍처의 구조적 변혁**

2023년부터 2026년에 이르는 기간 동안 인공지능(AI) 기반 소프트웨어 개발 및 자동화 방법론은 근본적이고 구조적인 변혁을 겪었다. 초기 대형 언어 모델(LLM)의 폭발적인 성장은 자연어 지시를 통해 코드를 생성하고 텍스트를 처리하는 프롬프트 엔지니어링(Prompt Engineering)의 시대를 열었다. 그러나 모델이 단순한 텍스트 생성기를 넘어 자율적으로 도구를 사용하고 환경과 상호작용하는 '에이전트(Agent)'로 진화함에 따라, 단일 상호작용에 의존하는 프롬프트 기반 접근법은 복잡한 기업용 애플리케이션이나 다단계의 자율적 작업 앞에서 명백한 한계를 드러냈다.1

이러한 한계를 극복하기 위해 산업계는 모델이 참조할 수 있는 정보의 양과 질을 제어하는 컨텍스트 엔지니어링(Context Engineering)으로 무게 중심을 이동시켰다. 수백만 토큰을 처리할 수 있는 초거대 컨텍스트 윈도우의 등장과 검색 증강 생성(RAG) 기술의 고도화는 에이전트에게 방대한 배경 지식을 제공하는 데 기여했다. 그러나 이 역시 동적으로 팽창하는 컨텍스트의 붕괴(Context Rot) 현상과 런타임 제어의 부재라는 구조적 결함을 본질적으로 해결하지는 못했다.4 에이전트는 종종 방대한 정보 속에서 길을 잃거나, 무한 루프에 빠지거나, 스스로 처리할 수 없는 양의 데이터를 호출하여 시스템을 마비시키는 이른바 '문맥 자살(Agent Suicide by Context)' 현상을 겪었다.6

2025년 하반기를 기점으로 글로벌 AI 연구 및 산업계는 단일 모델의 추론 능력 향상이나 정보 주입량의 증가에만 의존하는 대신, 모델을 둘러싼 '환경'과 '시스템' 전체를 설계하는 하네스 엔지니어링(Harness Engineering)이라는 새로운 패러다임에 도달했다.2 하네스(Harness)란 본래 야생마를 제어하고 그 힘을 유용한 노동력으로 전환하기 위한 마구를 의미하는 단어로, AI 공학에서는 예측 불가능한 모델의 출력을 생산적인 방향으로 유도하고, 제약하며, 검증하는 완전한 런타임 오케스트레이션 계층을 뜻한다.1 이 전환은 단순히 개발 도구의 발전을 넘어, 인간 엔지니어의 역할이 '코드 작성자'에서 '에이전트가 활동할 수 있는 환경, 구조, 그리고 피드백 루프의 설계자'로 완전히 이동했음을 의미한다.2

본 연구 보고서는 2023년부터 2026년까지 프롬프트, 컨텍스트, 하네스 엔지니어링으로 이어지는 기술적 진화 과정을 단계별로 심층 추적한다. 나아가 글로벌 AI 연구를 주도하는 OpenAI, Anthropic, Google DeepMind가 각각 '하네스'라는 개념을 어떻게 학술적으로 정의하고 자사의 에이전트 아키텍처에 기술적으로 구현했는지 최신 기술 블로그 포스트와 연구 논문을 근거로 상세히 분석한다.

## **2\. 1단계: 프롬프트 엔지니어링의 한계와 에이전트의 태동 (2023\~2024)**

2023년에서 2024년 사이, AI 개발 생태계의 핵심 규율은 단일 상호작용(Single Interaction)의 품질을 극대화하는 프롬프트 엔지니어링이었다.1 이 시기의 AI 시스템은 본질적으로 상태를 저장하지 않는(Stateless) 함수와 같았으며, 매 호출마다 인간 사용자가 전체 문맥을 다시 제공하고 정확한 지시를 내려야만 유의미한 결과물을 얻을 수 있었다.

### **2.1. 단일 턴 상호작용의 최적화**

프롬프트 엔지니어링의 주된 초점은 템플릿의 체계화, 역할 부여(Role-playing), 엄격한 제약 조건 설정, 퓨샷(Few-shot) 예제 제공, 그리고 연쇄 추론(Chain-of-Thought)과 같은 인지적 유도 기법을 통해 모델의 환각(Hallucination)을 줄이고 출력의 일관성을 높이는 데 맞춰져 있었다.10 개발자들은 복잡한 작업을 수행하기 위해 프롬프트 체이닝(Prompt Chaining)을 고안하여 하나의 모델 출력이 다음 모델의 입력으로 이어지도록 설계했다. 이는 단일 기능 단위나 스크립트 작성, 텍스트 요약 등에서는 탁월한 성능을 발휘했다. 모델은 훌륭한 텍스트 완성기이자 지능적인 자동 완성 도구로 기능했다.

### **2.2. 자율성 부여와 통제력 상실의 딜레마**

그러나 엔터프라이즈 환경에서의 프로덕션 도입이 본격화되고, 인간의 개입 없이 목표를 달성하는 자율적 에이전틱 워크플로우(Agentic Workflow)가 시도되면서 프롬프트 엔지니어링의 구조적 한계가 명확해졌다. 2023년 초에 등장한 AutoGPT나 BabyAGI와 같은 초기 에이전트 실험들은 모델에게 도구 사용 권한과 루프(Loop)를 제공하여 자율성을 부여하려 했다.12 하지만 이러한 초기 시스템들은 대부분 데모 환경을 넘어서지 못하고 실무 적용에 실패했다.

그 이유는 프롬프트가 단일 API 호출의 결과를 개선할 수는 있었으나, 에이전트가 여러 도구를 호출하고, 메모리를 유지하며, 세션을 넘나들어 상태를 관리하거나 예기치 않은 오류를 복구하는 다단계 워크플로우를 시스템적으로 제어할 수는 없었기 때문이다.3 완벽하게 작성된 시스템 프롬프트조차도 모델이 수천 줄의 레거시 코드를 수정하거나 동적인 런타임 에러에 직면했을 때는 무용지물이 되었다. 모델은 지시 사항을 '망각'하거나, 환각에 빠져 존재하지 않는 API를 호출하거나, 목표에서 벗어나 무한한 정보 탐색의 늪에 빠지곤 했다. 이는 단순히 모델의 추론 능력이 부족해서가 아니라, 에이전트가 딛고 설 '물리적 환경'과 지속적인 '배경 지식'이 부재했기 때문에 발생하는 필연적인 현상이었다.

## **3\. 2단계: 컨텍스트 엔지니어링의 부상과 인지적 병목 (2024\~2025)**

프롬프트의 한계를 인지한 연구자들과 엔지니어들은 모델에게 더 많은 정보와 맥락을 제공하는 방향으로 선회했다. 2024년 중반부터 산업계의 초점은 명령(Prompt)의 최적화에서 정보(Context)의 최적화로 이동했다. 컨텍스트 엔지니어링은 모델의 컨텍스트 윈도우(Context Window) 내에 어떤 정보를, 어떤 순서로, 얼마나 효율적으로 주입할 것인지를 체계적으로 설계하는 학문으로 자리 잡았다.13

### **3.1. 무한한 컨텍스트의 환상과 RAG의 한계**

초기 컨텍스트 엔지니어링은 검색 증강 생성(Retrieval-Augmented Generation, RAG) 기술을 중심으로 발전했다. 기업의 내부 문서나 코드베이스를 벡터 데이터베이스에 저장하고, 사용자의 질문과 의미론적으로 유사한 청크(Chunk)를 추출하여 프롬프트에 동적으로 삽입하는 방식이었다. 이와 동시에 모델 제공업체들은 하드웨어와 알고리즘의 발전을 바탕으로 수십만에서 수백만 토큰에 이르는 거대한 컨텍스트 윈도우를 경쟁적으로 발표했다. Google의 Gemini 모델은 200만 토큰을, Anthropic의 Claude 모델은 20만 토큰을 처리할 수 있게 되면서, 검색(Retrieval) 과정 자체를 생략하고 모든 문서를 컨텍스트 윈도우에 밀어 넣으면 된다는 주장이 제기되기도 했다.4

그러나 프로덕션 환경에서의 실제 측정 결과는 이러한 '무한한 컨텍스트'의 환상을 깨뜨렸다. LLM의 기반이 되는 트랜스포머(Transformer) 아키텍처는 본질적으로 모든 토큰이 다른 모든 토큰에 주의(Attention)를 기울이는 구조를 갖는다. 입력 토큰 수가 ![][image1]일 때, 연산 복잡도는 $\\mathcal{O}(n^2)$으로 증가하며, 모델의 인지적 자원(Attention Budget)은 분산된다.13 연구 기관 Chroma의 보고서에 따르면, 모델들이 통제된 벤치마크(예: Needle in a Haystack)에서는 수백만 토큰 속에서도 특정 정보를 완벽하게 찾아내지만, 실제 복잡한 프로덕션 작업에서는 입력이 약 6만 토큰을 초과할 경우 정보 검색과 장기 추론 능력이 급격히 저하되는 '컨텍스트 부패(Context Rot)' 현상이 관찰되었다.4 컨텍스트의 크기가 커질수록 모델은 지시 사항의 우선순위를 잃고, 최신 정보나 시작 부분의 정보에만 편향되는 경향을 보였다.

### **3.2. 에이전트의 문맥 자살 (Agent Suicide by Context)**

에이전트가 도구를 자율적으로 사용하게 되면서 컨텍스트 관리는 더욱 치명적인 문제로 부상했다. 정적인 문서를 사전에 주입하는 초기 RAG와 달리, 에이전틱 워크플로우에서는 에이전트가 런타임 중에 도구를 호출하며 컨텍스트가 동적으로 누적된다.6 에이전트가 특정 코드를 이해하기 위해 grep이나 파일 읽기 도구를 호출할 때, 반환되는 데이터의 크기를 예측하기 어렵다.

이로 인해 발생하는 가장 심각한 실패 모드가 '문맥 자살'이다. 예를 들어, 에이전트가 시스템 아키텍처를 이해하기 위해 문서 데이터베이스를 조회하는 도구를 호출했다고 가정해 보자. 만약 해당 문서가 수백 개의 하위 페이지나 방대한 내장 데이터를 포함하고 있어 도구의 반환값이 15만 토큰에 달한다면, 이 결과값이 에이전트의 컨텍스트 윈도우로 쏟아져 들어오게 된다.6 모델의 최대 컨텍스트 한도를 초과하는 순간 프로세스는 즉각적으로 강제 종료되며, 에이전트는 자신이 왜 죽었는지조차 파악하지 못한 채 실행을 멈춘다. LLM과의 상호작용은 본질적으로 단일 스레드(Single-threaded)로 이루어지므로, 네이티브 상태에서는 위험한 연산을 격리하거나 컨텍스트 오버플로우를 복구할 수 있는 아키텍처적 장치가 전무했다.6

Anthropic은 이러한 문제를 해결하기 위해 에이전트가 적시에 필요한 정보만 동적으로 가져오는 적시(Just-in-Time) 컨텍스트 검색 전략과, 세션이 길어질 때 이전 대화를 요약하여 컨텍스트 윈도우를 초기화하는 '압축(Compaction)' 기법을 도입하여 컨텍스트 엔지니어링을 고도화했다.13 하지만, 모델이 '무엇을 아는가'를 제어하는 것만으로는 모델이 '무엇을 할 수 있는가'와 '어떻게 복구하는가'를 통제할 수 없다는 한계가 명백해졌다. 이는 모델 외부에서 실행을 통제하는 물리적인 프레임워크의 필요성을 대두시켰다.

## **4\. 3단계: 하네스 엔지니어링의 도래 (2025\~2026)**

2025년 말부터 2026년 초에 이르러, 소프트웨어 자동화 및 AI 에이전트 개발 커뮤니티는 '하네스 엔지니어링(Harness Engineering)'이라는 새로운 개념으로 빠르게 수렴했다.2 Mitchell Hashimoto의 선구적인 블로그 포스트를 시작으로, OpenAI의 내부 프로젝트 보고서, Anthropic의 장기 실행 에이전트 가이드라인이 연이어 발표되며 이 용어는 산업 표준으로 자리 잡았다.3

### **4.1. 하네스의 정의와 기술적 범위**

하네스(Harness)란 AI 모델(엔진)이 유용하고 신뢰할 수 있는 작업(자동차)을 수행할 수 있도록 감싸는 런타임 오케스트레이션 및 인프라스트럭처 시스템을 의미한다.1 가장 뛰어난 언어 모델이라 할지라도 조향 장치, 브레이크, 서스펜션이 없으면 위험하고 쓸모없는 엔진에 불과하다. 하네스는 프롬프트 엔지니어링(단일 지시어)과 컨텍스트 엔지니어링(정보의 주입)을 모두 포괄하면서도, 그 너머에 있는 **상태 유지, 도구 실행, 안전 경계 설정, 세션 관리 및 오류 복구 메커니즘을 시스템 수준에서 구현**하는 것을 목표로 한다.1

분석에 따르면, 완성된 형태의 하네스 시스템은 다음 네 가지의 핵심적인 기술적 기능을 반드시 수행해야 한다.1

| 핵심 기능 | 세부 목적 | 구현 및 적용 기술 스택 (예시) |
| :---- | :---- | :---- |
| **제약 (Constrain)** | 에이전트의 물리적 행동 범위와 논리적 권한을 엄격하게 통제하여 파괴적 결과를 방지 | 샌드박스 기반의 파일 접근 제어, 읽기 전용 모드 적용, 커스텀 린터(Linter), 시스템 아키텍처의 의존성 경계 설정 |
| **정보 제공 (Inform)** | 에이전트가 작업의 목적과 제약 사항을 정확히 이해할 수 있도록 구조화된 컨텍스트를 주입 | 리포지토리 내의 정적 문서(AGENTS.md), 동적 텔레메트리 시스템(LogQL, PromQL 연동), E2E 브라우저 내비게이션 데이터 |
| **검증 (Verify)** | 에이전트의 코드 변경 사항이나 작업 결과물이 사전에 정의된 품질 및 논리 기준을 충족하는지 기계적으로 평가 | 구조적 유닛 테스트, CI/CD 파이프라인의 자동 컴파일, 결함 주입 및 E2E 브라우저 자동화 테스트 |
| **교정 (Correct)** | 검증 단계에서 에러가 발생했을 때, 에이전트가 스스로 원인을 분석하고 상태를 복구할 수 있도록 견고한 피드백 루프 제공 | 서브 에이전트 격리 기술, 폴백(Fallback) 및 재시도 로직, 린터의 상세 에러 메시지를 컨텍스트로 재주입 |

### **4.2. '비터 레슨(The Bitter Lesson)'과 하네스의 철학적 조화**

하네스 엔지니어링의 발전 과정에서는 AI 연구계의 오랜 논쟁거리인 '비터 레슨(The Bitter Lesson)'이 중요한 철학적 배경으로 작용했다.16 Rich Sutton이 주창한 이 원칙은 연구자가 인간의 도메인 지식을 인공지능에 하드코딩(Hard-coding)하여 주입하려는 시도는 결국 컴퓨팅 파워를 활용한 일반적인 학습 방법론론에 패배한다는 것을 의미한다.

초기 에이전트 프레임워크 설계자들은 모델의 결함을 메우기 위해 계획 모듈, 출력 파서, 엄격한 검증 계층 등 수많은 추상화(Abstraction)를 손수 작성했다.16 하지만 모델의 지능이 급격히 향상됨에 따라, 이러한 인간의 개입과 래퍼(Wrapper) 코드는 오히려 모델의 범용적인 문제 해결 능력을 제약하는 병목으로 작용했다. 즉, 프레임워크가 모델이 스스로 추론할 수 있는 행동 공간을 차단해버린 것이다.16

하네스 엔지니어링은 이 딜레마를 우회한다. 하네스는 모델 내부의 추론 과정을 지시하거나 인지적 편향을 하드코딩하지 않는다. 대신 모델에게 최대한의 자유를 부여하되, 모델이 상호작용하는 **외부 환경의 물리적, 논리적 제약을 강화**하는 데 집중한다.16 즉, "어떻게 코드를 작성할 것인가"를 가르치는 대신, "작성된 코드가 컴파일되지 않으면 어떻게 실패 로그를 반환할 것인가"에 집중하는 시스템 공학적 접근이다.

## **5\. OpenAI의 하네스 엔지니어링: 환경의 명료성과 아키텍처의 기계적 강제**

OpenAI는 하네스 엔지니어링을 "에이전트가 안정적으로 작업할 수 있도록 둘러싼 스캐폴딩, 제약 조건, 그리고 피드백 루프의 전체 환경"으로 명확히 정의하며, 이를 실제 프로덕션 환경에서 대규모로 입증했다.2

2026년 2월, OpenAI의 기술 스태프 Ryan Lopopolo가 발표한 *"Harness engineering: leveraging Codex in an agent-first world"* 기술 보고서는 산업계에 큰 반향을 일으켰다.9 OpenAI 내부의 3명에서 7명으로 구성된 소규모 엔지니어링 팀은 약 5개월 동안 자사의 AI 모델인 Codex 에이전트만을 사용하여 완전히 새로운 사내 베타 제품을 구축하고 출시했다. 이 프로젝트에서 인간이 직접 손으로 작성한 코드는 **단 0줄**이었으며, 애플리케이션 로직, 단위 테스트, CI 구성, 내부 문서, 심지어 모니터링 대시보드 설정에 이르는 약 100만 줄의 소스 코드가 순수하게 에이전트에 의해 생성되었다.9 이 과정에서 1,500개 이상의 Pull Request(PR)가 병합되었으며, 엔지니어당 하루 평균 3.5개의 PR을 처리하는 놀라운 생산성을 기록했다.2

이러한 극단적인 제약(인간의 코드 작성 금지)은 엔지니어링 팀이 '에이전트 중심 세계'에서 살아남기 위해 필수적인 인프라, 즉 하네스를 개발하도록 강제하는 원동력이 되었다. 프로젝트 초기에는 환경 설정의 부재와 열악한 도구 통합, 취약한 오류 복구 로직으로 인해 생산성이 매우 낮았으나, 하네스 시스템이 단계적으로 개선됨에 따라 생산성은 수직 상승했다.2

### **5.1. 환경의 명료성 (Environmental Legibility)과 관측성 스택**

OpenAI가 직면한 첫 번째 과제는 모델이 시스템을 쉽게 이해하고 디버깅할 수 있도록 시스템을 '투명하게' 만드는 것이었다. 기존의 레거시 코드는 인간 엔지니어의 직관에 의존하는 경향이 있었으나, 에이전트에게는 기계적으로 읽을 수 있는 명료한 환경이 필요했다.

OpenAI의 하네스는 에이전트가 새로운 태스크를 할당받을 때마다 **완전히 격리된 일회성(Ephemeral) 작업 환경**을 동적으로 부팅시킨다.9 이 샌드박스 환경에는 크롬 개발자 도구 프로토콜(Chrome DevTools Protocol)이 연결되어 있어 에이전트가 직접 웹 브라우저를 띄워 DOM을 검사하고, UI 요소를 클릭하며, 스크린샷을 찍어 시각적으로 결과를 확인할 수 있다.19

더욱 놀라운 점은 텔레메트리(Telemetry)의 통합이다. 일회성 환경에는 로그, 메트릭, 분산 트레이싱을 수집하는 로컬 관측성 스택이 포함되어 있다. 에이전트는 LogQL을 사용하여 시스템 로그를 직접 쿼리하고, PromQL을 통해 메모리 사용량이나 응답 시간 메트릭을 수집한다.9 이 완벽한 런타임 하네스 덕분에 개발자는 모델에게 코드를 짜라고 지시하는 대신, "서비스 시작이 800ms 이내에 완료되도록 보장하라"거나 "이 핵심 사용자 여정에서 2초를 초과하는 트랜잭션 스팬이 없도록 수정하라"와 같은 고차원적이고 추상적인 목표를 부여할 수 있게 되었다.9 에이전트는 인간이 잠든 새벽 시간에도 최대 6시간 이상 로그를 쿼리하고 코드를 수정하며 컴파일을 반복하는 폐쇄 루프(Closed loop) 내에서 자율적으로 작동했다.9

### **5.2. 아키텍처 강제와 기계적 피드백 루프**

대규모 코드베이스에서 수많은 에이전트가 동시에 코드를 생성할 때 가장 큰 위험은 시스템 아키텍처의 일관성이 무너지는 것이다. 프롬프트 창에 아무리 "의존성 방향을 지켜라"라고 명시해도 모델은 종종 편의를 위해 아키텍처 원칙을 위반하곤 한다.2

OpenAI의 하네스는 이를 프롬프트 튜닝이 아닌, **기계적 린터(Linter)와 구조적 테스트의 물리적 강제**를 통해 해결했다.2 하네스는 코드 병합 전 엄격한 구조적 검증을 수행한다. 중요한 것은 이 린터가 단순히 '실패'라는 결과만을 반환하는 것이 아니라, 오류가 발생한 지점과 원인을 상세히 분석하여 **교정 지시어(Correction Instructions)의 형태로 에이전트의 컨텍스트 윈도우에 역으로 주입**하도록 설계되었다는 점이다.2 예를 들어, 하네스에 Types \-\> Config \-\> Repo \-\> Service \-\> Runtime의 엄격한 계층적 의존성 규칙이 설정되어 있을 때, 에이전트가 이를 위반하면 하네스가 즉시 개입하여 에러를 주입하고 올바른 아키텍처 패턴으로 코드를 재작성하도록 강제한다.2

### **5.3. 단일 진실 공급원으로서의 저장소와 가비지 컬렉션**

에이전트는 텍스트 파일과 코드에 기반하여 추론한다. 슬랙 대화, 이메일 스레드, 혹은 엔지니어의 머릿속에 존재하는 비공식적인 도메인 지식은 에이전트에게 존재하지 않는 정보나 다름없다.1 따라서 하네스 환경 내에서는 리포지토리 자체가 모든 지식의 유일한 진실 공급원(Single source of truth)이 되어야 한다.

OpenAI는 시스템의 구조, 설계 결정 기록, 네이밍 규칙 등을 명시한 AGENTS.md 파일을 통해 에이전트에게 지침을 제공했다. 그러나 프로젝트 초기, 모든 규칙을 거대한 하나의 AGENTS.md 파일에 때려 넣는 방식은 실패로 돌아갔다.2 제한된 컨텍스트 윈도우 안에서 수많은 규칙이 경쟁하게 되면, 에이전트는 가장 중요한 제약 조건을 무시하고 대략적인 패턴 매칭에 의존하게 되기 때문이다.2 이에 대응하여 OpenAI는 지침 파일을 아키텍처 설계도, 실행 계획, 레퍼런스 등으로 잘게 쪼개어 디렉토리 구조에 분산 배치하고, 에이전트가 현재 작업 중인 디렉토리의 컨텍스트에 맞는 지침만을 동적으로 로드하도록 하네스를 재설계했다.2

더불어, 코드와 문서 간의 불일치로 인한 엔트로피 증가를 막기 위해 백그라운드에서 주기적으로 **가비지 컬렉션(Garbage Collection) 에이전트**를 실행시켰다.18 이 에이전트는 코드베이스를 순회하며 오래된 주석, 사용되지 않는 함수, 문서화되지 않은 엣지 케이스 등 '쓰레기'를 찾아내어 청소함으로써 리포지토리의 무결성을 유지하는 데 핵심적인 역할을 수행했다.18

### **5.4. 코덱스 앱 서버와 에이전트 루프의 추상화**

이러한 하네스를 시스템화하기 위해 OpenAI는 내부적으로 **Codex App Server**를 구축했다.21 이는 에이전트 루프의 핵심 로직을 캡슐화한 클라이언트 친화적인 양방향 JSON-RPC API로, 하네스의 핵심 구성 요소다.21 App Server는 사용자의 입력을 받아 시스템 프롬프트를 구성하고, 모델을 추론하며, 반환된 도구 호출을 로컬 샌드박스 환경에서 실행한 뒤 그 결과를 다시 모델에 주입하는 순환적인 '에이전트 루프(Agent Loop)'를 완벽하게 통제한다.22

특히 멀티턴 대화에서 발생하는 컨텍스트 한계 문제를 해결하기 위해 App Server는 자동 압축(Auto-compaction) 기능을 제공한다. 대화 기록이 일정 한도를 초과하면, 이전 대화의 핵심적인 '잠재적 이해(Latent understanding)'만을 암호화된 불투명 객체 형태로 보존하면서 윈도우를 확보하여 에이전트가 장시간 일관성을 잃지 않도록 보장한다.22

## **6\. Anthropic의 하네스 엔지니어링: 장기 실행 에이전트와 자원 효율의 극대화**

OpenAI가 아키텍처의 기계적 강제성과 피드백 루프에 집중했다면, Anthropic의 하네스 철학은 장기 복합 태스크를 수행하는 에이전트가 겪는 **기억 상실(Amnesia) 문제의 극복과 도구 호출(Tool use) 과정에서의 토큰 연산 효율성 극대화**에 초점이 맞춰져 있다.23

2025년 11월, Anthropic의 엔지니어들은 \*"Effective harnesses for long-running agents"\*라는 블로그 포스트를 통해 장기 실행 에이전트의 근본적인 실패 모드와 이를 해결하기 위한 Claude Agent SDK 기반의 혁신적인 하네스 아키텍처를 공개했다.23

### **6.1. 이산적 세션의 한계와 인간 공학자의 교대 근무 모델**

Anthropic의 연구진은 최상위 플래그십 모델(Claude 3.5 Opus 등)조차도 복잡한 엔터프라이즈 애플리케이션을 단 한 번의 프롬프트만으로 구축하려 할 때(One-shot) 심각한 실패를 겪는다는 사실을 발견했다.23 이는 LLM의 제한된 컨텍스트 윈도우로 인해 에이전트가 수 시간에 걸친 프로젝트를 단일 세션에서 완료할 수 없기 때문이다. 따라서 에이전트는 필연적으로 여러 개의 이산적인(Discrete) 세션으로 나뉘어 작업을 수행해야 하는데, 각각의 새로운 세션은 이전 세션에서 어떤 논의가 있었고 무슨 코드가 작성되었는지에 대한 기억이 전혀 없는 백지 상태에서 시작된다.23

이는 마치 소프트웨어 프로젝트에 투입된 교대 근무 엔지니어가 출근할 때마다 이전 근무자의 작업 내용을 전혀 기억하지 못하는 것과 같은 재앙적인 상황이다.23 이를 해결하기 위해 Anthropic은 단일 모델을 두 가지 역할로 엄격하게 분리하여 작업의 연속성을 보장하는 **투 트랙(Two-fold) 에이전트 하네스**를 고안했다.23

#### **초기화 에이전트 (Initializer Agent): 환경과 목표의 스캐폴딩**

사용자가 프로젝트 생성을 요청하면, 하네스는 가장 먼저 단 한 번만 실행되는 '초기화 에이전트' 세션을 부팅한다.23 이 에이전트는 코드를 짜는 것이 아니라, 후속 에이전트들이 헤매지 않고 작업할 수 있는 물리적, 논리적 인프라를 구축한다.

1. **환경 세팅:** 런타임 개발 서버를 띄우고 테스트 환경을 구성하는 init.sh 스크립트를 작성한다.23  
2. **형상 관리 및 로깅:** 빈 깃(Git) 리포지토리를 초기화하고, 앞으로 에이전트들의 작업 이력을 기록할 claude-progress.txt 파일을 생성한다.23  
3. **마스터 요구사항 명세서 작성:** 사용자의 초기 프롬프트를 분석하여 구현해야 할 모든 기능(Feature)을 상세하게 쪼갠 방대한 리스트를 생성한다.23 수백 개의 기능이 담긴 이 리스트는 구조화된 JSON 포맷(feature\_list.json)으로 작성되며, 모든 기능은 초기 상태인 "failing(실패)"으로 마킹된다.23 Anthropic의 실험 결과, 일반적인 마크다운(Markdown) 문서를 사용할 경우 모델이 텍스트를 임의로 편집하거나 훼손할 확률이 높았으나, JSON 객체 형식을 강제하고 오직 "passes" 불리언(Boolean) 필드만 수정하도록 엄격히 제한하자 이탈률이 획기적으로 감소했다.23

#### **코딩 에이전트 (Coding Agent): 점진적 실행과 맹목적 승리 방지**

초기화가 완료되면 하네스는 프로젝트가 끝날 때까지 수십, 수백 번의 '코딩 에이전트' 세션을 반복 호출한다.23 이 에이전트는 다음과 같은 엄격한 행동 강령을 기계적으로 따르도록 하네스에 의해 제어된다.

1. **지형지물 파악:** 세션이 시작되면 무작정 코드를 생성하는 대신 pwd로 작업 디렉토리를 확인하고, git 커밋 로그와 claude-progress.txt를 읽어 이전 근무자가 어디까지 작업했는지 컨텍스트를 동기화한다.23  
2. **단일 기능 집중:** JSON 피처 리스트를 확인하여 가장 우선순위가 높은 미구현 기능 단 하나만을 선택해 작업한다. 이는 에이전트가 의욕을 앞세워 너무 많은 기능을 한 번에 건드리다 컨텍스트를 소진해버리는 실패 모드를 원천 차단한다.23  
3. **E2E 자가 검증:** 코딩이 끝나면 에이전트는 성급하게 작업을 완료했다고 선언하는 대신, init.sh를 실행해 서버를 구동한다.23 이후 Puppeteer MCP 서버와 같은 브라우저 자동화 도구를 직접 활용하여 인간 사용자처럼 버튼을 클릭하고 화면을 검증하는 E2E(End-to-End) 테스트를 수행해야만 해당 기능의 "passes" 값을 true로 바꿀 수 있다.23  
4. **클린 스테이트 종료:** 작업이 검증되면 변경 사항을 Git에 커밋하고 진행 로그 파일을 업데이트한 뒤 세션을 종료하여, 다음 에이전트 세션에게 버그가 없는 깨끗한 상태(Clean state)를 인계한다.23

이러한 Anthropic의 하네스는 복잡한 프로젝트를 끝까지 완수해 내는 에이전트의 지구력이 단일 모델의 지능 상승이 아닌, 올바른 스캐폴딩과 기록 시스템의 설계에서 비롯됨을 증명했다.24

### **6.2. MCP와 코드 실행(Code Execution)을 통한 토큰 경제학 혁신**

하네스 환경 내에서 에이전트는 외부 데이터를 읽거나 데이터베이스를 쿼리하기 위해 도구를 사용해야 한다. Anthropic은 이를 표준화하기 위해 \*\*모델 컨텍스트 프로토콜(Model Context Protocol, MCP)\*\*을 도입했다.25 MCP는 클라이언트-서버 아키텍처를 기반으로 에이전트가 로컬 파일, 외부 API, 기업 데이터베이스 등에 통합된 방식으로 접근할 수 있게 해주는 혁신적인 표준이다.27

하지만 MCP 도입 초기, 연동된 도구의 수가 수십에서 수백 개로 늘어나자 새로운 문제가 발생했다. 기존의 에이전트 클라이언트들은 모든 도구의 이름, 설명, 매개변수 스키마를 모델의 프롬프트 내에 '도구 정의(Tool definitions)' 형태로 전부 로드했다.25 130개가 넘는 도구를 사용할 경우, 도구 정의를 나열하는 데에만 모델 컨텍스트 윈도우의 26% 이상이 소모되는 엄청난 비효율이 발생했다.29 더불어 도구를 호출할 때마다 방대한 중간 결과값이 컨텍스트로 들어오면서 비용과 지연 시간이 폭증했다.25

이를 해결하기 위해 Anthropic은 하네스 아키텍처를 재설계하여, 에이전트가 직접 도구를 호출하는 대신 **'코드 실행(Code execution)'을 통해 도구를 제어**하도록 만들었다.25 즉, 에이전트는 자신이 사용할 도구를 자바스크립트나 파이썬 스크립트 형태의 논리 구조(Loops, Conditionals)로 작성하여 런타임 환경에서 실행시킨다.25 이 방식은 다음과 같은 압도적인 효율성을 가져왔다.

* **토큰 절약:** 직접 도구를 호출할 때 15만 토큰을 소모하던 워크플로우가 코드 실행을 통할 경우 단 2천 토큰으로 줄어들어 무려 98.7%의 컨텍스트 비용 절감 효과를 달성했다.29  
* **개인정보 보호 및 보안:** 수만 개의 데이터베이스 행을 검색할 때, 결과값이 모델의 컨텍스트 윈도우로 들어오지 않고 런타임 환경 내에서만 처리되므로 민감한 데이터의 유출을 원천적으로 방지할 수 있다.25 에이전트는 최종적으로 연산된 결과(예: 필터링된 5개의 행)만을 열람하게 된다.25

Anthropic의 MCP 기반 하네스 최적화는 "더 많고 좁은 도구보다, 더 적고 스마트한 도구가 낫다"는 원칙을 증명하며, 에이전트가 수만 개의 기업용 API 생태계 속에서도 길을 잃지 않고 효율적으로 작동할 수 있는 기반을 마련했다.29

## **7\. Google DeepMind의 하네스 엔지니어링: 자율 코드 합성(AutoHarness)과 위임 아키텍처**

OpenAI와 Anthropic이 인간 엔지니어의 정교한 아키텍처 설계와 시스템적 제약을 통해 하네스를 구축했다면, 기초 AI 연구의 산실인 Google DeepMind는 여기서 한 걸음 더 나아가 **"모델이 스스로 자신의 하네스를 코딩하도록 만드는"** 혁신적이고 수학적인 접근을 취했다.30 더불어, 코딩 도구를 넘어선 에이전트 중심의 완전한 IDE 'Antigravity'를 통해 인간-에이전트 간의 위임(Delegation) 프로세스를 재정의했다.

### **7.1. AutoHarness: 환각을 차단하는 자율 합성 제어기**

2026년 3월, Google DeepMind의 연구진은 \*"AutoHarness: improving LLM agents by automatically synthesizing a code harness"\*라는 기념비적인 논문을 발표했다.30 이 논문은 LLM이 추론 과정에서 겪는 치명적인 약점, 즉 외부 환경의 명시적인 규칙을 어기는 '불법적 행동(Illegal actions)' 문제를 짚어낸다.

실제로 Kaggle GameArena의 체스 대회에 출전한 Gemini 2.5 Flash 모델의 패배 원인을 분석한 결과, 전략적인 오판 때문이 아니라 체스판의 물리적 규칙을 어기는 불가능한 수를 시도했기 때문에 패배한 비율이 무려 78%에 달했다.30 모델 내부의 가상 세계(World model) 시뮬레이션은 매우 불안정하여 종종 환각(Hallucination)에 빠지기 때문이다. 기존의 방식은 인간이 게임의 규칙을 파이썬 코드로 일일이 하드코딩하여 모델을 감싸거나, 수만 건의 데이터를 수집해 모델의 가중치를 미세 조정(Fine-tuning)하는 것이었으나, 두 방법 모두 확장성이 떨어지고 비용이 막대했다.30

DeepMind가 제안한 AutoHarness 프레임워크는 이 패러다임을 뒤집었다. 모델의 내부 추론을 고치는 대신, 모델 스스로 외부 규칙을 검증하는 파이썬 코드를 작성하게 한 것이다. AutoHarness는 LLM을 \*\*'돌연변이 연산자(Mutation operator)'\*\*로 활용하는 탐색 및 정제(Search and Refine) 알고리즘을 사용한다.30

1. **가설 생성 및 검증:** LLM이 is\_legal\_action()이라는 검증 함수의 초기 코드를 작성한다. 에이전트가 이 코드를 통해 행동을 제안했을 때 게임 환경(Critic)이 이를 불법으로 판정하여 에러 메시지를 반환하면, LLM은 이 에러 피드백을 바탕으로 코드를 지속적으로 디버깅하고 진화시킨다.30  
2. **톰슨 샘플링 (Thompson Sampling):** 코드 가설들은 트리(Tree) 구조로 관리된다. 시스템은 톰슨 샘플링 알고리즘을 사용하여 어떤 코드 가설을 더 다듬을지(Exploitation) 아니면 아예 새로운 코드를 시도할지(Exploration)를 수학적으로 결정하여 최적의 하네스를 탐색한다.30

#### **하네스의 진화: 필터에서 정책(Policy)으로**

논문은 코드로 합성된 하네스가 어떻게 모델의 성능을 비약적으로 끌어올리는지 세 가지 단계로 나누어 증명했다.30

* **액션 필터/검증기 (Action-Filter & Verifier):** LLM이 추론을 통해 다음 행동을 제안하면, 합성된 파이썬 코드가 물리적 규칙을 검사한다. 불가능한 수일 경우 코드는 즉시 에러를 반환하고 LLM에게 "불법적인 행동임"이라는 경고와 함께 다시 생각하도록 강제한다.30  
* **정책으로서의 하네스 (Harness-as-Policy):** DeepMind는 여기서 멈추지 않고, 모델의 전략적 사고방식 자체를 완벽한 파이썬 및 Numpy 코드로 컴파일해 내는 데 성공했다.30 이렇게 되면 런타임 게임 플레이 중에는 LLM을 API로 호출할 필요조차 없게 된다. 코드가 곧 완벽한 에이전트(Policy)가 되기 때문이다.30

실험 결과는 압도적이었다. TextArena의 145개 복잡한 텍스트 기반 게임(체스, 스도쿠 등) 테스트에서, AutoHarness를 장착한 경량 모델 **Gemini 2.5 Flash**는 스스로 합성한 코드를 무기로 불법적인 행동을 0%로 차단했다. 2인용 게임 대결에서 이 경량 모델은 무거운 플래그십 모델인 **Gemini 2.5 Pro**를 상대로 56.3%의 높은 승률을 기록했으며(Pro의 승률은 38.2%), 1인용 게임에서는 심지어 타사의 최고급 모델인 GPT-5.2-High보다도 높은 평균 보상을 획득했다.30 이는 에이전트의 능력을 결정짓는 요소가 단일 모델의 매개변수 크기(Size)가 아니라, 환각을 기계적으로 차단하는 '코드 하네스의 유무'임을 과학적으로 입증한 결정적 사례다.30

### **7.2. Antigravity: 에이전트 우선(Agent-first) 통합 개발 환경**

기초 연구 성과를 실무에 적용하기 위해 DeepMind는 AI 코딩 스타트업 Windsurf 팀을 인수합병하고, 완전히 새로운 에이전트 중심 IDE인 **Google Antigravity**를 2025년 11월에 출시했다.34

기존의 Cursor나 GitHub Copilot과 같은 도구들이 기존 텍스트 편집기에 AI 챗봇을 결합한 래퍼(Wrapper) 수준에 머물렀다면, Antigravity는 아키텍처 자체가 다수의 자율 에이전트를 오케스트레이션하기 위해 설계되었다.34 가장 큰 특징은 코드를 직접 수정하는 뷰 외에, 비동기적으로 작동하는 여러 에이전트의 작업 흐름을 지휘하는 '매니저 뷰(Manager View)'를 전면에 내세운 점이다.34 하나의 에이전트가 백그라운드에서 레거시 모듈을 리팩토링하는 동안, 다른 에이전트는 E2E 테스트 코드를 작성하고 브라우저를 띄워 UI를 확인한다.34

여기서 핵심적인 하네스 역할은 \*\*아티팩트 시스템(Artifacts System)\*\*이 담당한다. 에이전트는 코드를 소스 파일에 무작정 덮어쓰기 전에 반드시 아키텍처 구조도, 변경 예정 파일 목록, 검증 시나리오 등 인간이 직관적으로 검토할 수 있는 청사진(Plan) 아티팩트를 먼저 생성해야 한다.34 개발자는 이 아티팩트를 승인하거나 거절함으로써, 수천 줄의 엉망진창인 코드가 생성되기 전에 값싸고 안전하게 에이전트의 방향을 교정할 수 있다.36 DeepMind는 위임(Delegation)을 단순한 태스크 분할이 아니라 권한과 신뢰의 구조적 통제 과정으로 정의했으며, Antigravity의 아티팩트 하네스는 이 철학을 시각적으로 구현한 결과물이다.37

## **8\. 3대 AI 연구소의 하네스 아키텍처 비교 분석**

앞서 분석한 OpenAI, Anthropic, Google DeepMind의 하네스 시스템은 모델 외부에서 런타임 제어와 검증을 수행한다는 공통된 목적을 지니고 있다. 그러나 각 조직이 마주한 문제 의식과 기술적 철학에 따라 구현 방식은 뚜렷하게 구별된다.

다음은 세 기업의 하네스 아키텍처를 핵심 구성 요소별로 비교한 결과이다.

| 구분 | OpenAI (Codex / App Server) | Anthropic (Claude Agent SDK / MCP) | Google DeepMind (AutoHarness / Antigravity) |
| :---- | :---- | :---- | :---- |
| **핵심 철학** | 아키텍처 원칙의 기계적 강제와 지속적 피드백 루프 구축 9 | 장기 실행 세션의 상태 유지와 도구 호출의 컴퓨팅 효율성 극대화 23 | 모델 환각의 수학적/코드적 차단 및 자율적 정책(Policy) 컴파일 30 |
| **상태 관리 및 환경** | 일회성(Ephemeral) 샌드박스와 런타임 텔레메트리 (LogQL/PromQL) 기반 관측 9 | feature\_list.json 및 claude-progress.txt를 통한 영구적(Persistent) 상태 및 진척도 관리 23 | 톰슨 샘플링을 통한 탐색 트리(Tree) 내 다중 코드 가설 유지 30 |
| **오류 복구 기법** | 커스텀 린터(Linter)의 실패 로그를 역으로 프롬프트에 주입하여 의존성 규칙 교정 2 | 도구를 활용한 로컬 서버 구동 및 E2E 브라우저 테스트(Puppeteer)를 통한 성급한 성공 선언 방지 23 | 환경의 피드백을 통해 모델이 직접 작성한 검증 함수(Action-Verifier) 코드를 자율적으로 디버깅 및 정제 30 |
| **엔트로피 제어 (부패 방지)** | 백그라운드 가비지 컬렉터를 가동하여 정적 문서(AGENTS.md)와 코드 간의 동기화 강제 18 | 수백 개의 도구 정의 로드를 생략하고 런타임에서 자바스크립트 등 코드 실행을 통해 MCP 도구 동적 제어 25 | 전략적 의사결정 과정 자체를 파이썬 코드로 컴파일(Harness-as-Policy)하여 추론 런타임의 비결정성 원천 차단 30 |

OpenAI는 시스템의 가시성을 높이고 기계적인 린터를 활용해 코드의 품질을 높이는 인프라적 제어에 강점을 보인다. 반면 Anthropic은 JSON과 마크다운을 넘나들며 에이전트의 인지적 혼란을 막고 세션을 영속적으로 이어가는 워크플로우 제어에 집중했다. Google DeepMind는 여기서 한 차원 높은 추상화를 이루어, 모델 스스로 자신을 제약하는 코드를 짜게 만드는 재귀적 향상(Recursive self-improvement)의 가능성을 보여주었다.30

## **9\. 산업적 파급 효과와 생산성 역설 (The Productivity Paradox)**

하네스 엔지니어링의 필요성은 단지 선도적인 AI 연구소들의 실험실 내부에서만 증명된 것이 아니다. 프로덕션 환경의 실증적 데이터는 하네스가 결여된 AI 도입이 오히려 조직의 생산성을 심각하게 훼손할 수 있음을 경고하고 있다.38

### **9.1. 활동량은 늘고 진행은 멈추는 역설**

산업 연구 기관인 METR(Measuring the Impact of Early-2025 AI)의 2025년 연구에 따르면, 16명의 숙련된 오픈소스 개발자들이 실제 프로젝트 246개를 수행할 때 일반적인 챗봇 형태의 AI 어시스턴트(Claude 3.5 등)를 사용하자 작업 완료 시간이 **평균 19% 더 오래 소요**되었다.38 더욱 흥미로운 점은, 개발자들 스스로는 AI가 자신을 20% 더 빠르게 만들어주었다고 '착각'했다는 것이다. DORA 2024의 대규모 조직 지표 조사 역시 유사한 패턴을 보여준다. 조직 차원의 AI 도입률이 25% 포인트 증가할 때, 실제 소프트웨어 딜리버리 처리량(Throughput)은 1.5% 감소했고 안정성은 7.2% 떨어졌다.38 Faros AI의 1만 명 규모 개발자 조사에서는 에이전트 도입 후 Pull Request의 병합 횟수는 98% 폭증했지만, 이를 인간이 리뷰하는 시간은 91%나 증가하여 병목 현상이 극심해진 것으로 나타났다.38

이러한 지표의 역설은 명백한 사실을 시사한다. 하네스 없는 모델은 엄청난 양의 코드를 쏟아내며 개발자 개인의 로컬 활동량(Activity)은 극대화하지만, 그 코드가 아키텍처 규칙을 위반하거나 눈에 보이지 않는 엣지 케이스를 포함하기 때문에 최종적인 시스템 반영(Progress)은 오히려 늦어진다는 것이다.38 올바른 조직적 구조와 작업 분해(Decomposition), 그리고 초 단위의 짧은 피드백 루프를 제공하는 오케스트레이션 층위, 즉 '하네스'가 없다면 에이전트는 결코 프로덕션 레벨의 딜리버리 성과를 낼 수 없다.38

## **10\. 결론: 판단력 제조(Judgment Manufacturing)의 시대로**

2023년에서 2026년까지 이어지는 AI 개발 방법론의 궤적은 기계와 상호작용하는 인류의 방식이 본질적으로 진화했음을 증명한다. 지시어의 수사학에 의존했던 프롬프트 엔지니어링에서, 데이터와 정보의 주입량을 제어하는 컨텍스트 엔지니어링을 거쳐, 마침내 물리적이고 논리적인 시스템 인프라를 구축하는 하네스 엔지니어링으로 패러다임이 성숙했다.

프롬프트와 컨텍스트 엔지니어링이 단일 턴에서의 출력 정확도를 높이기 위한 '언어적 제어'였다면, 하네스 엔지니어링은 다단계 자율 작업 중 발생하는 필연적인 실패를 시스템 수준에서 안전하게 차단하고 복구하는 '구조적 제어'다. DeepMind의 AutoHarness 연구와 OpenAI의 100만 줄 코드 생성 실험은 공통적으로 거대 모델의 스케일업(Scale-up)만이 능사가 아님을 강력히 시사한다. 엄격하게 최적화된 하네스 내에서 작동하는 소형 모델이, 아무런 제약 없이 방목된 초대형 플래그십 모델을 압도하는 결과를 증명했기 때문이다. 이는 향후 AI 플랫폼의 궁극적인 해자(Moat)가 기반 모델의 매개변수 크기가 아니라, 그 모델을 얼마나 일관되고 파괴적이지 않게 구동시킬 수 있는지 결정하는 하네스 아키텍처 역량에 의해 형성될 것임을 뜻한다.14

이러한 패러다임의 전환은 소프트웨어 엔지니어링이라는 직업의 본질을 영구적으로 재편하고 있다. 미래의 엔지니어링 병목은 소스 코드를 타이핑하여 구현하는 데 있지 않다. 대신, 에이전트가 쉽게 파악할 수 있는 명료한 아키텍처(Environmental legibility)를 설계하고, 이들이 무한정 생성해 내는 결과물을 기계적으로 검증하며 통제할 수 있는 단단한 가드레일을 구축하는 데 모든 자원이 집중될 것이다.

궁극적으로 인간의 역할은 '하네스 엔지니어링'을 통한 안전판의 구축과 더불어, 기계가 쏟아내는 수많은 아티팩트의 논리적 결함을 찾아내고 방향성을 조율하는 '판단력 제조(Judgment manufacturing)'로 이행하고 있다.40 기업과 조직은 에이전트의 코드 생산 속도를 자랑하는 단계를 넘어, 이 거대한 코드 생성기를 안전하게 품어낼 수 있는 통제 시스템 설계에 전사적 역량을 기울여야 할 시점이다.

#### **참고 자료**

1. Harness Engineering: The Complete Guide to Building Systems That Make AI Agents Actually Work (2026) | NxCode, 3월 21, 2026에 액세스, [https://www.nxcode.io/resources/news/harness-engineering-complete-guide-ai-agent-codex-2026](https://www.nxcode.io/resources/news/harness-engineering-complete-guide-ai-agent-codex-2026)  
2. Beyond Prompts and Context: Harness Engineering for AI Agents | MadPlay, 3월 21, 2026에 액세스, [https://madplay.github.io/en/post/harness-engineering](https://madplay.github.io/en/post/harness-engineering)  
3. What Is an Agent Harness? The Infrastructure That Makes AI Agents Actually Work, 3월 21, 2026에 액세스, [https://www.firecrawl.dev/blog/what-is-an-agent-harness](https://www.firecrawl.dev/blog/what-is-an-agent-harness)  
4. Context Engineering: The Evolution Beyond RAG in Modern AI Architecture | by Tao An, 3월 21, 2026에 액세스, [https://tao-hpu.medium.com/context-engineering-the-evolution-beyond-rag-in-modern-ai-architecture-4219d5a49c46](https://tao-hpu.medium.com/context-engineering-the-evolution-beyond-rag-in-modern-ai-architecture-4219d5a49c46)  
5. Context Rot: How Increasing Input Tokens Impacts LLM Performance | Chroma Research, 3월 21, 2026에 액세스, [https://research.trychroma.com/context-rot](https://research.trychroma.com/context-rot)  
6. Agent Suicide by Context | StackOne, 3월 21, 2026에 액세스, [https://www.stackone.com/blog/agent-suicide-by-context](https://www.stackone.com/blog/agent-suicide-by-context)  
7. What Is Agentic Engineering? Complete History: From Turing to Karpathy, AutoGPT to Autoresearch & Beyond (2026) \- Taskade, 3월 21, 2026에 액세스, [https://www.taskade.com/blog/what-is-agentic-engineering](https://www.taskade.com/blog/what-is-agentic-engineering)  
8. The importance of Agent Harness in 2026 \- Philschmid, 3월 21, 2026에 액세스, [https://www.philschmid.de/agent-harness-2026](https://www.philschmid.de/agent-harness-2026)  
9. Harness engineering: leveraging Codex in an agent-first world | OpenAI, 3월 21, 2026에 액세스, [https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)  
10. Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing | Request PDF \- ResearchGate, 3월 21, 2026에 액세스, [https://www.researchgate.net/publication/363563506\_Pre-train\_Prompt\_and\_Predict\_A\_Systematic\_Survey\_of\_Prompting\_Methods\_in\_Natural\_Language\_Processing](https://www.researchgate.net/publication/363563506_Pre-train_Prompt_and_Predict_A_Systematic_Survey_of_Prompting_Methods_in_Natural_Language_Processing)  
11. AI/ML Resources \- DZone, 3월 21, 2026에 액세스, [https://dzone.com/ai-ml](https://dzone.com/ai-ml)  
12. LangChain's CEO argues that better models alone won't get your AI agent to production, 3월 21, 2026에 액세스, [https://venturebeat.com/orchestration/langchains-ceo-argues-that-better-models-alone-wont-get-your-ai-agent-to](https://venturebeat.com/orchestration/langchains-ceo-argues-that-better-models-alone-wont-get-your-ai-agent-to)  
13. Effective context engineering for AI agents \- Anthropic, 3월 21, 2026에 액세스, [https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)  
14. 2025 Was Agents. 2026 Is Agent Harnesses. Here's Why That Changes Everything., 3월 21, 2026에 액세스, [https://aakashgupta.medium.com/2025-was-agents-2026-is-agent-harnesses-heres-why-that-changes-everything-073e9877655e](https://aakashgupta.medium.com/2025-was-agents-2026-is-agent-harnesses-heres-why-that-changes-everything-073e9877655e)  
15. Building AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned \- arXiv, 3월 21, 2026에 액세스, [https://arxiv.org/html/2603.05344v1](https://arxiv.org/html/2603.05344v1)  
16. The Bitter Lesson of Agent Frameworks \- Browser Use, 3월 21, 2026에 액세스, [https://browser-use.com/posts/bitter-lesson-agent-frameworks](https://browser-use.com/posts/bitter-lesson-agent-frameworks)  
17. The Bitter Lesson \- Rich Sutton, 3월 21, 2026에 액세스, [http://www.incompleteideas.net/IncIdeas/BitterLesson.html](http://www.incompleteideas.net/IncIdeas/BitterLesson.html)  
18. Harness Engineering \- Martin Fowler, 3월 21, 2026에 액세스, [https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)  
19. Harness Engineering: What It Means for QA \- Test Collab, 3월 21, 2026에 액세스, [https://testcollab.com/blog/harness-engineering](https://testcollab.com/blog/harness-engineering)  
20. OpenAI Introduces Harness Engineering: Codex Agents Power Large‑Scale Software Development \- InfoQ, 3월 21, 2026에 액세스, [https://www.infoq.com/news/2026/02/openai-harness-engineering-codex/](https://www.infoq.com/news/2026/02/openai-harness-engineering-codex/)  
21. Unlocking the Codex harness: how we built the App Server \- OpenAI, 3월 21, 2026에 액세스, [https://openai.com/index/unlocking-the-codex-harness/](https://openai.com/index/unlocking-the-codex-harness/)  
22. Unrolling the Codex agent loop | OpenAI, 3월 21, 2026에 액세스, [https://openai.com/index/unrolling-the-codex-agent-loop/](https://openai.com/index/unrolling-the-codex-agent-loop/)  
23. Effective harnesses for long-running agents \- Anthropic, 3월 21, 2026에 액세스, [https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)  
24. Anthropic just showed how to make AI agents work on long projects without falling apart, 3월 21, 2026에 액세스, [https://www.reddit.com/r/LocalLLaMA/comments/1p7siuu/anthropic\_just\_showed\_how\_to\_make\_ai\_agents\_work/](https://www.reddit.com/r/LocalLLaMA/comments/1p7siuu/anthropic_just_showed_how_to_make_ai_agents_work/)  
25. Code execution with MCP: building more efficient AI agents \- Anthropic, 3월 21, 2026에 액세스, [https://www.anthropic.com/engineering/code-execution-with-mcp](https://www.anthropic.com/engineering/code-execution-with-mcp)  
26. Introducing the Model Context Protocol \- Anthropic, 3월 21, 2026에 액세스, [https://www.anthropic.com/news/model-context-protocol](https://www.anthropic.com/news/model-context-protocol)  
27. Model Context Protocol, 3월 21, 2026에 액세스, [https://modelcontextprotocol.io/docs/getting-started/intro](https://modelcontextprotocol.io/docs/getting-started/intro)  
28. A Survey of the Model Context Protocol (MCP): Standardizing Context to Enhance Large Language Models (LLMs) \- Preprints.org, 3월 21, 2026에 액세스, [https://www.preprints.org/manuscript/202504.0245](https://www.preprints.org/manuscript/202504.0245)  
29. Designing MCP for the Age of AI Agents \- Harness, 3월 21, 2026에 액세스, [https://www.harness.io/blog/harness-mcp-server-redesign](https://www.harness.io/blog/harness-mcp-server-redesign)  
30. AutoHarness: improving LLM agents by automatically synthesizing a code harness \- arXiv, 3월 21, 2026에 액세스, [https://arxiv.org/abs/2603.03329](https://arxiv.org/abs/2603.03329)  
31. AutoHarness: improving LLM agents by automatically synthesizing a code harness \- arXiv, 3월 21, 2026에 액세스, [https://arxiv.org/pdf/2603.03329](https://arxiv.org/pdf/2603.03329)  
32. Auto-Harness Synthesis \- Just Understanding Data \- James Phoenix, 3월 21, 2026에 액세스, [https://understandingdata.com/posts/auto-harness-synthesis/](https://understandingdata.com/posts/auto-harness-synthesis/)  
33. The Google tool helping small AI models outperform the giants, 3월 21, 2026에 액세스, [https://www.aiacceleratorinstitute.com/the-google-tool-helping-small-ai-models-outperform-the-giants/](https://www.aiacceleratorinstitute.com/the-google-tool-helping-small-ai-models-outperform-the-giants/)  
34. Google Antigravity: First Impressions of the Agent-First IDE \- PromptLayer Blog, 3월 21, 2026에 액세스, [https://blog.promptlayer.com/google-antigravity-first-impressions-of-the-agent-first-ide/](https://blog.promptlayer.com/google-antigravity-first-impressions-of-the-agent-first-ide/)  
35. Google Antigravity: The Agent-First IDE That's Redefining Software Development \- Medium, 3월 21, 2026에 액세스, [https://medium.com/@hamipirzada/google-antigravity-the-agent-first-ide-thats-redefining-software-development-bc595fb2de0e](https://medium.com/@hamipirzada/google-antigravity-the-agent-first-ide-thats-redefining-software-development-bc595fb2de0e)  
36. Google Antigravity Review: DeepMind's Agent-First Bet on Faster, Safer Software Development | Scalable Path, 3월 21, 2026에 액세스, [https://www.scalablepath.com/ai/google-antigravity-review](https://www.scalablepath.com/ai/google-antigravity-review)  
37. Blog | Alex Lavaee, 3월 21, 2026에 액세스, [https://alexlavaee.me/blog/](https://alexlavaee.me/blog/)  
38. Harness Engineering: Why the Frame Matters More Than the Model \- Infralovers, 3월 21, 2026에 액세스, [https://www.infralovers.com/blog/2026-03-13-harness-engineering-rahmen-wichtiger-als-modell/](https://www.infralovers.com/blog/2026-03-13-harness-engineering-rahmen-wichtiger-als-modell/)  
39. The Agent Harness Is the Architecture (and Your Model Is Not the Bottleneck) \- Medium, 3월 21, 2026에 액세스, [https://medium.com/@epappas/the-agent-harness-is-the-architecture-and-your-model-is-not-the-bottleneck-5ae5fd067bb2](https://medium.com/@epappas/the-agent-harness-is-the-architecture-and-your-model-is-not-the-bottleneck-5ae5fd067bb2)  
40. FOD\#141: What Happens to Software Engineering When Anyone Can Build? \- Turing Post, 3월 21, 2026에 액세스, [https://www.turingpost.com/p/fod141](https://www.turingpost.com/p/fod141)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAXCAYAAAA/ZK6/AAAAwUlEQVR4XmNgGAUjC/ABsScQy0L5rEBsAsS+QCwOUwQDPEA8E4gbgfgJEMcC8WYgTgPiaiD+CMQucNVAkArEmkAcBMS/gdgRSQ4k/haIi5DE4GASEF8FYhEksQgg/gnENkhiYMALxIeBeA0Qs0DFQPRyID4BxPxQMTjAZrUiA8RPDUDMCcTtQCwMk4S5H9lqUAh9A2JTIHYF4iokObApFxmQTAACJSC+A8TbgXgZA5qzOBggwYsOQPEBCgRmdImhDADRNRteI2vVTAAAAABJRU5ErkJggg==>