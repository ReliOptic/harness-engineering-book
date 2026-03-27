# **하네스 엔지니어링과 자율적 AI의 진화: 안드레 카파티의 오토리서치와 지속적 학습 에이전트를 위한 구조적 비평**

## **서론: 인공지능 네이티브 소프트웨어 공학의 변곡점**

소프트웨어 공학과 인공지능(AI)의 교차점에서 가장 근본적이고 철학적인 패러다임의 전환이 전개되고 있다. 2025년과 2026년을 기점으로, 대규모 언어 모델(LLM)은 단순한 텍스트 생성 도구나 코드 자동 완성 유틸리티의 역할을 넘어, 독자적인 의사결정 체계와 행동 능력을 갖춘 '에이전트(Agent)'로 진화하였다.1 과거 인간 엔지니어가 명시적인 논리를 코드로 작성하고 기계가 이를 컴파일하여 실행하던 방식에서 벗어나, 이제는 인간이 에이전트의 목표와 환경을 설계하고 에이전트가 자율적으로 코드를 작성, 검증, 배포하는 시대로 진입한 것이다.2

이러한 거대한 전환의 중심에는 전 테슬라(Tesla) AI 디렉터이자 오픈AI(OpenAI)의 창립 멤버인 안드레 카파티(Andrej Karpathy)가 주창한 '소프트웨어 3.0(Software 3.0)'과 '에이전틱 엔지니어링(Agentic Engineering)'이라는 획기적인 개념이 자리 잡고 있다.4 카파티는 인간의 직관에 의존하여 코드를 생성하는 이른바 '바이브 코딩(Vibe Coding)'의 구조적 한계를 지적하며, 에이전트가 신뢰할 수 있는 상용 수준의 소프트웨어를 구축하기 위해서는 엄격한 시스템적 기반이 필요함을 역설했다.6 이와 동시에 오픈AI의 내부 실험과 미첼 하시모토(Mitchell Hashimoto) 등의 산업계 리더들을 통해 구체화된 '하네스 엔지니어링(Harness Engineering)'은 에이전트의 자율성을 통제하고 코드의 품질을 영속적으로 보장하기 위한 환경 설계의 표준으로 자리 잡고 있다.3

본 보고서는 최근 개발자 커뮤니티와 학계의 화두가 되고 있는 하네스 엔지니어링의 구조적 원리를 분석하고, 이를 안드레 카파티의 '오토리서치(Autoresearch)' 루프 및 지속적 학습(Continuous Learning) 철학과 비교 분석한다. 특히, GitHub 생태계에서 '한 명의 개발자가 52일 만에 35만 줄의 코드를 작성한 실험' 등으로 대변되는 커뮤니티 주도의 하네스 프레임워크(ReliOptic 및 AgentsMesh와 같은 구조적 접근법)가 가지는 의의와 한계를 비판적으로 고찰한다.10 나아가, 현재의 통제 중심적 하네스 엔지니어링 패러다임이 안고 있는 인지적, 보안적, 아키텍처적 맹점을 지적하며, 궁극적으로 진정한 의미의 '지속적 학습 에이전트(Continuously Learning Agent)'로 진화하기 위해 요구되는 기술적 초석이 무엇인지 심층적으로 논증한다.

## **소프트웨어 패러다임의 진화와 에이전틱 엔지니어링의 대두**

### **소프트웨어 1.0에서 3.0으로의 다차원적 전환**

안드레 카파티는 컴퓨터 과학의 역사를 관통하는 소프트웨어 개발 방식의 진화를 세 가지 뚜렷한 거시적 단계로 구분한다.4 이 진화 과정은 단순히 도구의 발전을 의미하는 것이 아니라, 계산을 수행하는 주체와 그 계산의 논리를 정의하는 매개체, 그리고 인간 지능과 기계 지능 사이의 권력 이동을 의미한다.

| 패러다임 단계 | 핵심 논리 매개체 | 최적화의 주체 및 대상 | 아키텍처 및 개발자의 역할 |
| :---- | :---- | :---- | :---- |
| **소프트웨어 1.0** | 명시적 소스 코드 (C++, Python 등) | 인간 엔지니어가 작성한 결정론적(Deterministic) 알고리즘과 명령어의 집합.11 | 인간이 모든 엣지 케이스를 예측하고 제어 흐름을 설계함. 기계는 맹목적으로 이를 컴파일하고 실행함.5 |
| **소프트웨어 2.0** | 신경망 아키텍처와 학습된 가중치(Weights) | 데이터와 최적화 알고리즘(역전파 등)이 경험적 오차를 줄이며 스스로 논리를 형성함.11 | 개발자는 코드 대신 데이터를 큐레이션하고 레이블링하며, 목적 함수를 설계하는 기계학습 엔지니어로 변모함.13 |
| **소프트웨어 3.0** | 자연어 프롬프트와 대규모 언어 모델(LLM) | 기계가 자연어를 해석하여 코드를 동적으로 생성하고, 도구를 활용하여 자율적인 추론 궤적을 탐색함.4 | 인간은 의도를 지시(Prompt)하고 시스템의 환경을 설계하는 오케스트레이터(Orchestrator)이자 조율자로 격상됨.14 |

소프트웨어 3.0 환경에서 코드는 더 이상 프로젝트의 궁극적인 목적이 아니라, 자연어로 표현된 인간의 의도가 실행 가능한 형태로 번역되는 과정에서 발생하는 일시적인 부산물(By-product)에 불과해진다.14 카파티의 지적처럼, 이는 1940년대 컴퓨터 과학이 태동한 이래 가장 심오한 지적 패러다임의 전환이며, 자연어인 영어가 사실상 가장 강력한 범용 프로그래밍 언어로 등극했음을 시사한다.4

### **대규모 언어 모델 운영체제 (LLM OS)의 아키텍처적 재정의**

이러한 지적 전환을 구체화하기 위해 카파티는 2023년 말부터 'LLM OS(Large Language Model Operating System)'라는 선구적인 개념적 아키텍처를 도식화하여 제시했다.17 이 아키텍처는 폰 노이만(Von Neumann) 구조에 기반한 고전적인 컴퓨팅 구성 요소들을 언어와 추론, 그리고 학습된 행동 패턴을 중심으로 완전히 재정의한다.

| 고전적 컴퓨팅 요소 | LLM OS의 대응 요소 | 시스템 내 기능적 역할 및 상호작용 특성 |
| :---- | :---- | :---- |
| **중앙처리장치 (CPU)** | **LLM (인지 및 추론 코어)** | 인간이 작성한 프롬프트를 명령어 세트(Instruction Set)로 받아들여, 수십억 개의 학습된 파라미터를 바탕으로 맥락을 평가하고 토큰 단위의 출력을 생성하는 동적 추론 엔진.18 |
| **주기억장치 (RAM)** | **컨텍스트 윈도우 (Context Window)** | 에이전트가 단기적으로 유지하고 참조할 수 있는 작업 기억 공간. 정보의 주입량에 한계가 있어 정교한 메모리 관리가 필수적임.17 |
| **보조기억장치 (Disk)** | **임베딩(Embeddings) 및 벡터 데이터베이스** | 에이전트의 장기 기억 장치. 방대한 도메인 지식과 과거의 실행 궤적을 고차원 벡터 형태로 저장하고, 필요 시 의미론적 유사도에 기반하여 검색(Retrieval)함.17 |
| **주변기기 (Peripherals)** | **터미널, 브라우저, 계산기, 파이썬 인터프리터** | LLM이 외부 세계의 상태를 읽거나 결정론적 논리 연산(Software 1.0 도구)을 수행하기 위해 호출하는 시스템 콜(System Call)의 확장 영역.17 |

이 구조적 모델은 LLM이 단순히 챗봇의 백엔드에 머무는 것이 아니라, 운영체제의 핵심 커널로서 다양한 서브 시스템을 제어하고 다중 에이전트 시스템을 조율하는 모듈식 아키텍처의 심장부로 기능할 수 있음을 수학적이고 구조적으로 증명한다.19

### **바이브 코딩에서 에이전틱 엔지니어링으로의 성숙**

2025년 초기, 소프트웨어 개발 커뮤니티는 프롬프트를 입력하고 결과물을 확인하는 직관적이고 캐주얼한 개발 방식인 '바이브 코딩(Vibe Coding)'에 열광했다.6 이는 코드가 존재한다는 사실조차 잊은 채 아이디어를 빠르게 프로토타이핑할 수 있는 자유를 제공했으나, 곧바로 구조적 취약성을 노출했다.22 바이브 코딩은 검증되지 않은 코드의 양산, 아키텍처 원칙의 부재, 그리고 보안 취약점의 기하급수적 증가라는 치명적인 부작용을 낳았다.6

이에 따라 2026년에 이르러 카파티는 진화된 개념인 '에이전틱 엔지니어링(Agentic Engineering)'을 제창하였다.4 에이전틱 엔지니어링은 단순히 AI의 조력을 받는 것을 넘어, 에이전트가 기획, 코드 작성, 테스트, 배포에 이르는 전체 생명 주기를 수행하는 시스템을 체계적으로 설계하는 공학 방법론이다.4 이는 인간의 역할을 단순한 프롬프터에서 "아키텍처를 소유하고 구현의 세부 사항을 위임하는" 오케스트레이터로 전환시킴으로써, 대규모 기업용 소프트웨어 개발에 필요한 신뢰성과 재현성을 담보한다.4

## **하네스 엔지니어링: 에이전트를 위한 통제와 토양의 설계**

에이전틱 엔지니어링의 철학을 실제 프로덕션 환경에 적용하기 위해 산업계가 도달한 실천적 프레임워크가 바로 '하네스 엔지니어링(Harness Engineering)'이다.9 하시코프(HashiCorp)의 공동 창립자 미첼 하시모토와 오픈AI의 라이언 로포폴로(Ryan Lopopolo) 연구팀에 의해 체계화된 이 개념은, 에이전트가 예측 불가능한 환각(Hallucination)에 빠지지 않고 신뢰성 있게 작동할 수 있도록 제약 조건과 피드백 루프를 시스템 레벨에서 설계하는 과정을 의미한다.3

### **프롬프트, 컨텍스트, 하네스의 계층적 확장**

에이전트를 제어하는 기술적 층위는 모델과의 상호작용 거리에 따라 세 가지 확연한 계층으로 구분된다.6

| 엔지니어링 계층 | 핵심 질문 (Core Question) | 설계 및 최적화의 대상 (Design Target) | 한계점 |
| :---- | :---- | :---- | :---- |
| **프롬프트 엔지니어링** | "모델에게 무엇을 질문할 것인가?" | LLM에 전달되는 텍스트 지시문의 구조와 논리적 배열.6 | 단일 상호작용에 국한되며, 복잡한 프로젝트 전반의 일관성을 유지할 수 없음.6 |
| **컨텍스트 엔지니어링** | "모델에게 무엇을 보여줄 것인가?" | 모델이 추론 시점에 활용할 수 있는 외부 지식, 시스템 로그, 코드 조각 등 메모리와 정보의 범위.6 | 에이전트가 오답을 생성하거나 아키텍처를 위반하는 행동 자체를 선제적으로 차단하지 못함.9 |
| **하네스 엔지니어링** | "모델을 어떻게 제약하고 복구할 것인가?" | 에이전트를 둘러싼 인프라, 린터, 강제적 아키텍처 규칙, 도구 접근 권한 및 자동화된 피드백 루프.6 | 초기 구축에 막대한 비용(수개월의 시간)이 소요되며, 동적인 환경 변화에 유연하게 대처하기 어려움.3 |

에이전트가 팀의 코딩 컨벤션을 무시하거나, 객체 지향 설계의 의존성 역전 원칙을 위반하며 코드를 생성하는 문제는 프롬프트의 미사여구나 컨텍스트의 추가만으로는 결코 해결되지 않는다.9 1주일에 1,000개의 풀 리퀘스트(PR)를 자율적으로 생성하는 에이전트 무리가 초래할 폭발적인 엔트로피(기술 부채)를 통제하기 위해서는, 물리적인 성벽과도 같은 하네스 엔지니어링이 필수적이다.3

### **오픈AI의 하네스 실험: 100만 줄의 코드와 3대 원칙**

오픈AI 팀은 코덱스(Codex) 에이전트만을 활용하여 인간의 직접적인 코드 타이핑 없이 5개월 동안 100만 줄에 달하는 프로덕션 소프트웨어를 구축하는 대규모 실험을 성공적으로 수행했다.1 이 성과는 모델 자체의 추론 능력이 비약적으로 향상되었기 때문이 아니라, 에이전트를 둘러싼 하네스의 품질이 압도적이었기 때문에 가능했다. 이 실험에서 도출된 하네스 엔지니어링의 핵심 원칙은 커뮤니티의 모범 사례로 자리 잡았다.

#### **1\) 기록의 시스템으로서의 코드베이스 (Repository as System of Record)**

에이전트에게 1,000페이지 분량의 방대한 지침서를 프롬프트로 주입하는 것은 필연적인 실패를 부른다. 컨텍스트 윈도우는 희소한 인지적 자원이기 때문이다.3 만약 모든 것이 "중요하다"고 강조된다면, 에이전트의 어텐션 메커니즘은 결국 아무것도 중요하게 처리하지 못한다.9 이에 따라 오픈AI는 AGENTS.md 파일을 모든 지식이 담긴 백과사전(Encyclopedia)이 아니라, 지식의 위치를 안내하는 목차(Table of Contents)로 활용했다.1 약 100줄로 구성된 이 지시사항은 코드베이스 내부의 구조화된 docs/ 디렉터리(설계 문서, 아키텍처 지도, 실행 계획 등)를 포인터처럼 가리키며, 에이전트가 작업의 맥락에 따라 필요한 문서를 스스로 검색하여 읽도록 유도한다.1 인간의 머릿속이나 슬랙(Slack)의 휘발성 스레드에 존재하는 지식은 에이전트에게 존재하지 않는 것과 동일하다.25

#### **2\) 기계적 강제(Mechanical Enforcement)와 자율적 가비지 컬렉션**

에이전트가 생성한 코드가 애플리케이션의 아키텍처를 위반하지 않도록 방어하기 위해, 하네스는 커스텀 린터(Linter)와 ArchUnit 같은 구조적 테스트 프레임워크를 통해 결정론적(Deterministic) 제약을 가한다.3 나아가 에이전트가 남긴 파편화된 문서나 미세하게 누적되는 기술 부채를 통제하기 위해, '가비지 컬렉션(Garbage Collection)' 역할을 수행하는 배경 에이전트가 주기적으로 코드베이스를 스캔하여 일관성을 복원하는 리팩토링 PR을 자동으로 생성한다.1

### **ReliOptic과 커뮤니티 주도의 하네스 원칙: 고립, 분해, 조율**

오픈AI와 같은 거대 기업의 인프라뿐만 아니라, 1인의 개발자가 오픈소스 도구를 활용하여 하네스 엔지니어링을 구현한 사례(예: 52일 만에 35만 줄의 코드를 작성한 실험 및 AgentsMesh 프레임워크)는 이 패러다임이 어떻게 보편화될 수 있는지 보여준다.10 원본 ReliOptic 저장소의 문서화된 세부 지침이 현재 접근 불가능한 상태라 하더라도, 이와 관련된 커뮤니티의 기술적 논의를 통해 하네스의 본질적 원리를 세 가지 프리미티브(Primitives)로 재구성할 수 있다.10

1. **고립 (Isolation):** 병렬로 동작하는 다수의 에이전트 무리가 서로의 파일 시스템을 침범하여 충돌하는 것을 방지하기 위해, 모든 에이전트는 개별적인 Git 작업 트리(Worktree)와 샌드박스 환경을 독립적으로 할당받아야 한다.10  
2. **분해 (Decomposition):** 에이전트는 "이 레거시 코드베이스를 개선하라"는 식의 모호하고 광범위한 목표 앞에서는 마비된다. 따라서 모든 작업은 명확한 인수 조건(Acceptance Criteria)과 완료의 정의(Definition of Done)를 갖춘 세밀한 티켓(Ticket) 단위로 쪼개어져야 한다.10  
3. **조율 (Coordination):** 에이전트는 전통적인 역할(프론트엔드, 백엔드)에 얽매이지 않는 제너럴리스트이므로, 채널과 권한 바인딩(Bindings)을 통해 에이전트 간의 관찰과 직접 실행 권한을 유동적으로 통제하는 통신 레이어가 필요하다.10

### **오차 기반의 반복과 4단계 피드백 루프**

미첼 하시모토가 정의한 하네스 엔지니어링의 정수는 "에이전트가 실수를 저질렀을 때, 단순히 프롬프트를 수정하여 당장의 오류를 덮는 것이 아니라, 시스템적으로 다시는 같은 실수를 반복하지 않도록 도구와 검증 환경 자체를 재설계하는 것"이다.3 이는 하네스가 에이전트를 위해 제공하는 다음과 같은 다층적 피드백 루프를 통해 구현된다.10

1. **컴파일 및 핫 리로드 (Compilation/Hot-reload):** 언어 단위의 문법 및 타입 검사를 통해 런타임 오류를 컴파일 타임 오류로 전환하여 에이전트에게 즉각적인 텍스트 피드백을 제공한다.10  
2. **단위 테스트 (Unit Tests):** 멀티테넌트 격리와 같은 복잡한 비즈니스 논리의 경계 조건에서 에이전트가 발생시키는 회귀(Regression) 오류를 수 분 이내에 감지한다.27  
3. **엔드투엔드 (E2E) 테스트:** 단위 테스트가 미치지 못하는 모듈 간의 통합 이슈를 검증한다. 특히 크롬 개발자 도구 프로토콜(CDP)을 에이전트 런타임에 직접 연결하여, UI의 시각적 결함까지 에이전트가 자율적으로 추적하고 수정할 수 있게 한다.25  
4. **연속 통합 파이프라인 (CI Pipeline):** 병합 전 최후의 안전망으로서, 클린 룸 환경에서 린팅과 빌드 가능성을 검증한다.27

이러한 고도의 하네스 환경에서 인간 엔지니어의 핵심 역량은 알고리즘의 작성에서 벗어나, 에이전트가 번성할 수 있는 인프라의 토양(Engineering Soil)을 윤택하게 가꾸고 피드백 파이프라인을 설계하는 '엄격성의 재배치(Relocating Rigor)'로 이동하게 된다.1

## **오토리서치(Autoresearch): 진화와 자율적 발견의 역학**

하네스 엔지니어링이 에이전트의 파괴적 행동을 제약하고 프로덕션 환경에서의 신뢰성을 담보하는 '안전망'이자 '보수적 규제자'라면, 안드레 카파티가 2026년 3월에 공개한 '오토리서치(Autoresearch)' 프레임워크는 에이전트가 주어진 컴퓨팅 자원 내에서 모델의 성능을 극대화하고 새로운 지식을 스스로 발굴해 내는 능동적 '탐색(Exploration)'의 메커니즘을 제시한다.28

### **오토리서치 루프의 미니멀리즘 아키텍처**

오토리서치는 단일 GPU 환경에서 AI 에이전트가 인간의 수면 시간 동안 수십, 수백 번의 기계학습 아키텍처 실험을 자율적으로 수행하게 하는 오픈소스 프레임워크다.28 카파티는 이 시스템을 의도적으로 극도로 작게 유지하여 단 3개의 핵심 파일로 캡슐화했다.29

1. prepare.py (고정된 진실의 닻): 데이터 다운로드, BPE 토크나이저 훈련, 그리고 모델의 평가 함수를 포함한다. 시스템은 에이전트가 이 파일을 절대로 수정할 수 없도록 강제한다. 이는 에이전트가 평가 지표 자체를 조작하여 성능이 향상된 것처럼 속이는 행위를 원천적으로 차단하여 평가의 객관성을 유지한다.29  
2. train.py (변이의 대상): 에이전트가 유일하게 수정 권한을 가지는 단일 파일이다. GPT 모델의 층위적 아키텍처, 옵티마이저(Muon \+ AdamW의 조합), 학습률 스케줄, 배치 크기 등 신경망의 심장부에 해당하는 모든 변수가 실험과 조작의 대상이 된다.29  
3. program.md (인간의 의도): 인간 연구자가 에이전트에게 실험의 방향성, 제약 조건, 엣지 케이스 처리 방법을 평문(English)으로 지시하는 가이드라인 파일이다. 인간은 더 이상 파이썬 코드를 만지지 않고, 오직 이 마크다운 파일을 통해 연구 조직 전체를 '프로그래밍'한다.29

### **자율적 최적화의 수학적 정형화 (MDP)와 타임박싱**

오토리서치의 진정한 혁신은 인간의 개입을 배제한 무한 최적화 루프를 마르코프 결정 과정(MDP, Markov Decision Process)으로 정형화했다는 데 있다.32

![][image1]

이 공식화에서 상태 $\\mathcal{S}$는 현재의 train.py 코드베이스이며, 행동 $\\mathcal{A}$는 아키텍처 깊이나 하이퍼파라미터의 구문론적 수정이다. 시스템의 보상 $\\mathcal{R}$은 모델의 검증 손실(Validation Loss) 지표인 ![][image2](validation bits per byte)가 이전 세대에 비해 얼마나 개선되었는지의 여부다.30 이 지표는 어휘 크기(Vocab-size)에 독립적이므로 에이전트가 토크나이저를 변경하더라도 공정한 비교가 가능하다.29

루프의 역학은 다음과 같다.29

1. **가설 생성 및 변이:** 에이전트는 기존의 코드 상태를 분석하고, 어텐션 메커니즘을 수정하거나 새로운 학습률을 적용하는 가설을 세운다.30  
2. **타임박싱된 실행 (Fixed Budget):** 에이전트는 수정한 코드를 바탕으로 정확히 5분(Wall clock time) 동안만 모델을 훈련시킨다.29 이 엄격한 시간 제약은 두 가지 목적을 가진다. 첫째, 복잡한 아키텍처 변경으로 인해 연산량이 증가하더라도 시간 단위 당 성능이라는 절대적 기준으로 공정하게 평가할 수 있다. 둘째, 시간당 약 12회의 실험을 보장하여 하룻밤 사이에 유의미한 수의 표본을 확보한다.29  
3. **검증 및 정책 갱신:** 훈련이 종료되면 ![][image2]를 측정한다. 손실이 낮아져 성능 개선이 입증되면 해당 코드 변경을 Git 커밋으로 영구히 저장(Keep)하고, 성과가 저하되면 즉시 이전 상태로 롤백(Revert)하여 새로운 탐색을 시작한다.30

카파티의 실제 구동 사례에서 에이전트는 단 하룻밤 만에 126회의 독립적인 실험을 자율적으로 완수하여 손실을 0.9979에서 0.9697로 크게 낮추었다. 더 놀라운 것은, 인간 전문가가 20년 이상의 경력 동안 간과했던 정규화(Regularization)와 어텐션 스케일링의 미세한 결함을 에이전트 스스로 찾아내어 수정함으로써, GPT-2 수준의 성능에 도달하는 훈련 시간을 11%나 단축시켰다는 점이다.30

### **RLVR: 검증 가능한 보상을 통한 강화학습의 승리**

오토리서치의 아키텍처는 2025년과 2026년 AI 기초 연구를 지배한 RLVR(Reinforcement Learning from Verifiable Rewards) 패러다임의 완벽한 축소판이다.38 과거 인간 피드백 기반 강화학습(RLHF) 모델들이 인간의 주관적인 선호도에 얽매여 비싼 레이블링 비용과 편향의 한계에 직면했던 반면, RLVR은 코드의 컴파일 통과 여부나 수학 문제의 정답 도출, 그리고 ![][image2]와 같은 자동화되고 객관적인 지표를 최적화 목표로 삼는다.38

이를 통해 에이전트는 인간이 제시하지 않은, 혹은 인간조차 이해하기 어려운 기상천외하고 복잡한 최적의 '추론 궤적(Reasoning Traces)'을 수많은 시행착오 속에서 스스로 조각해 낸다.38 오토리서치는 단순히 코드를 고치는 스크립트가 아니라, 에이전트가 과학적 방법론(Scientific Method) 자체를 기계화하여 수행하는 지적 탐구의 자동화 과정인 것이다.30

## **하네스 엔지니어링 패러다임에 대한 건설적 비평 (Constructive Criticism)**

오픈AI, 미첼 하시모토, 그리고 AgentsMesh와 같은 커뮤니티 실험을 통해 정립된 하네스 엔지니어링은 AI 모델을 무질서한 프로덕션 환경에 성공적으로 연착륙시키기 위한 필수 불가결한 통제 시스템이다. 그러나 이 패러다임을 AI가 스스로의 한계를 극복하고 세계를 이해하는 '지속적으로 학습하는 에이전트(Continuously Learning Agent)'로 진화하기 위한 궁극적인 토대로 삼기에는 몇 가지 구조적, 인지적, 그리고 보안적 측면에서 중대한 맹점이 존재한다.

안드레 카파티의 오토리서치가 보여준 동적인 진화의 역학과 리차드 서튼(Richard Sutton) 등의 인지과학적 통찰을 바탕으로, 하네스 엔지니어링이 극복해야 할 한계를 다음 네 가지 측면에서 건설적으로 비판한다.

### **비판 1: 정적 검증의 병목과 행동적 의미론의 부재 (The Verification Bottleneck)**

하네스 엔지니어링의 방어기제는 철저히 린터, 정적 타입 체커, E2E 스크립트 등 기계적 강제력(Mechanical Enforcement)에 의존한다.3 이 접근법은 코드의 구문(Syntax) 오류를 잡거나 패키지 간의 아키텍처 의존성 역전을 방지하는 등 '구조적 품질'을 유지하는 데는 눈부신 성과를 보이지만, 마틴 파울러(Martin Fowler)의 지적처럼 소프트웨어가 고객의 실제 비즈니스 요구에 맞게 유용하게 동작하는지를 판단하는 '기능적, 행동적 검증(Behavioral Verification)'의 층위에서는 구조적인 무력함을 노출한다.3

카파티의 오토리서치가 극단적으로 성공할 수 있었던 본질적 이유는, ![][image2]라는 속일 수 없는 절대적이고 단일한 성능 지표(Scalar Metric)가 존재했기 때문이다.34 에이전트는 자신의 코드가 세계를 더 낫게 만들었는지 수학적으로 즉시 증명할 수 있었다. 반면, 일반적인 엔터프라이즈 하네스 환경에서 개발되는 상용 애플리케이션은 "이 UI 컴포넌트가 사용자의 구매 전환율에 긍정적인 감성을 유발하는가?" 혹은 "이 데이터베이스 마이그레이션 전략이 향후 확장성에 유리한가?"와 같은 극도로 퍼지(Fuzzy)하고 정성적인 다차원적 목표를 다룬다.39

객관적인 피드백이 지연되거나 모호한 영역에서 하네스 엔지니어링의 기계적 검증은 멈춰 선다.39 따라서 정적인 하네스만으로는 에이전트가 구문론적으로 무결한 코드를 공장처럼 찍어내는 수준을 넘어, 사용자의 요구를 능동적으로 파악하고 가치를 창출하는 방향으로 학습을 심화하도록 유도하기 어렵다.

### **비판 2: 소세계 가정의 오류와 물리적 세계와의 충돌 부재**

강화학습의 선구자인 리차드 서튼은 최근 인터뷰에서 현재의 LLM 중심적 접근이 필연적인 '막다른 골목(Dead End)'에 봉착할 것이라고 경고했다.40 현재의 하네스 엔지니어링 철학은 철저히 '소세계 가정(Small-World Assumption)'에 매몰되어 있다. 이는 "충분히 거대한 파라미터를 가진 모델에, 완벽하게 구조화된 AGENTS.md와 지식 데이터베이스만 제공하면 모델이 세상의 모든 문제를 추론하고 해결할 수 있다"는 오만이다.40

그러나 진정한 지능과 지속적인 학습은 폐쇄된 텍스트 공간이 아니라 동적인 환경과의 끊임없는 상호작용 속에서만 발생한다.40 하네스에 갇힌 에이전트는 코드베이스라는 철저히 정제되고 격리된 샌드박스 내부에서만 행동한다. 현재 에이전트 구동에 주로 사용되는 PPO나 GRPO 기반의 모델 프리(Model-free) 강화학습 방법론들은 오직 하네스가 허용하는 희소한 보상(Sparse Rewards)에만 반응할 뿐, 현실 세계가 제공하는 무한히 풍부하고 복잡한 피드백을 수용하지 못한다.40

인지과학자 장 피아제(Jean Piaget)나 레프 비고츠키(Lev Vygotsky)의 이론이 시사하듯, 지능의 발달은 체화된(Embodied) 상호작용의 산물이다.41 닫힌 시스템(하네스) 안에서 주어진 문서만을 반복해서 읽고 린터의 경고에 순응하는 닫힌 루프만으로는, 배치 후 자가 개선(Self-improvement after deployment)이라는 진정한 의미의 평생 학습(Life-long learning)에 도달할 수 없다.41 에이전트는 하네스의 안전망을 찢고 나가 미지의 데이터를 탐색하고, 복잡한 웹 환경과 충돌하며 깨달음을 얻어야 한다.

### **비판 3: 데이터 주권의 상실과 가속화되는 엔트로피의 모순**

하네스 엔지니어링의 인프라적 측면에서 가장 심각하게 간과되는 맹점은 보안(Security)과 데이터 주권(Data Sovereignty)의 문제다.26 오픈AI의 선언적인 플레이북은 시스템의 아키텍처 결정 과정, 데이터 스키마의 근본, 내부 기밀 스펙, এমনকি 팀의 구두 논의나 기술 부채 내역까지 모든 정보를 마크다운 파일로 명시화하여 저장소에 기록할 것을 강요한다.1 에이전트가 문서를 완전히 읽을 수 있어야(Legible) 업무를 수행할 수 있기 때문이다.

그러나 마이클 하네케(Michael Hannecke)를 비롯한 보안 전문가들의 시각에서 볼 때, 특히 유럽(EU)의 데이터 보안 규정과 엔터프라이즈 환경을 고려하면 이는 재앙에 가깝다. 기업의 핵심 지적 자산인 '왕관의 보석(Crown Jewels)'이 통째로 미국 기반의 외부 데이터 센터에서 구동되는 상업용 모델의 컨텍스트 윈도우로 쉴 새 없이 스트리밍되어야 하기 때문이다.26 진정한 엔터프라이즈 지속적 학습 에이전트라면 외부 API 의존도를 탈피하여 내부 네트워크에서 구동되는 강력한 프라이빗 LLM을 기반으로 자신만의 하네스를 독립적으로 직조해야 하지만, 극도로 높은 메모리 대역폭과 하드웨어 유지 비용이 이를 현실적으로 가로막고 있다.42

더불어, 하네스 환경 내의 에이전트는 인간보다 압도적으로 빠른 속도로 코드를 양산하기 때문에, 만약 아키텍처의 사소한 타협점이나 잘못된 설계 패턴을 한 번이라도 정당한 선례로 학습하게 되면, 이를 수만 줄의 코드에 기하급수적으로 복제하여 기술 부채(Entropy)를 폭발적으로 증폭시킨다.10 가비지 컬렉터 에이전트가 이를 백그라운드에서 청소한다고는 하나, 본질적으로 결함 있는 모델이 남긴 결함 있는 패턴을 동일한 수준의 다른 언어 모델이 교정한다는 것은 구조적인 모순에 불과하다.

### **비판 4: 혁신의 억압 – '적응(Adaptation)'과 '진화(Evolution)'의 혼동**

하네스 엔지니어링의 근본적인 한계는 에이전트가 기존 시스템이 정해놓은 질서와 규칙을 단 한 치도 벗어나지 못하도록 옥죄는 강력한 통제에 있다. 에이전트는 린터의 문법 검사와 계층형 아키텍처(DDD) 테스트가 허용하는 비좁은 울타리 내에서만 코드를 짜깁기할 수 있다.3 이는 프로덕션 시스템의 단기적인 붕괴를 막는 데는 효과적이지만, 카파티가 오토리서치에서 보여주었던 경이로운 '진화'의 가능성을 원천적으로 억압한다.

오토리서치 루프 속의 에이전트는 모델의 성능이 개선되지 않을 경우 옵티마이저를 통째로 교체하거나 어텐션 구조를 근본적으로 해체하는 혁신적인 파괴를 스스로 감행할 수 있었다.31 그러나 강한 타입 검사와 엄격한 파일 명명 규칙이 군대처럼 강제되는 닫힌 하네스 내에서는 창조적인 파괴가 용납되지 않는다.10 지속적 학습이란 단순히 기존의 낡은 코드베이스에 새로운 API 엔드포인트를 기계적으로 덧붙이는 행위가 아니라, 소프트웨어 시스템의 메타 구조 자체를 뒤엎고 재설계하는 행위여야 한다. 따라서 현재의 하네스 엔지니어링은 에이전트의 혁신을 안전하게 억누르는 '디지털 감옥(Playpen)'으로 전락할 위험을 다분히 내포하고 있다.

## **지속적 학습 에이전트로 진화하기 위한 구조적 초석 (Foundation for Evolution)**

정적인 통제를 지향하는 하네스 엔지니어링의 맹점을 극복하고, 동적인 탐색을 지향하는 오토리서치의 잠재력을 보편적 소프트웨어 공학에 결합할 때 비로소 진정한 '지속적으로 학습하는 에이전트(Continuously Learning Agent)'의 초석을 다질 수 있다. 이를 위해서는 AI 개발 패러다임 전반에 걸쳐 다음의 세 가지 근본적인 아키텍처 전환이 선행되어야 한다.

### **1\) 시스템 A, B, M을 융합한 인지 아키텍처의 구축**

단일한 프롬프트 주입이나 단순한 린터 기반의 하네스를 넘어, 생물학적 인지 모델과 진화의 역사에서 영감을 받은 다중 시스템 아키텍처(Multi-System Architecture)가 구현되어야 한다.41

* **System A (관찰과 모방을 통한 학습):** 기존의 하네스 엔지니어링이 담당하던 영역이다. 에이전트는 저장소의 AGENTS.md를 읽고, 기존 개발자들의 PR 리뷰 역사와 코드베이스의 구조를 흡수하여 현재 시스템의 규칙과 컨벤션을 체화한다.25  
* **System B (능동적 행동과 시행착오를 통한 학습):** 오토리서치가 증명한 탐색의 영역이다. 에이전트가 단순히 코드를 작성하는 것을 넘어, 안전하게 격리된 병렬 샌드박스(Pods) 내에서 독자적인 가설을 세우고, 코드를 파괴적으로 변이(Mutation)시키며 실험을 거듭하여 기존 시스템이 상상하지 못한 새로운 최적의 알고리즘 경로를 발굴한다.10  
* **System M (메타 제어 및 통제 신호):** 에이전트가 단순한 실행기를 넘어 지능체로 거듭나기 위한 핵심이다. 에이전트 스스로 하네스의 특정 린터 규칙이나 아키텍처 제약이 개발 속도를 저해하는 구시대적 유물이라고 판단될 경우, 무조건적으로 복종하는 대신 그 제약 조건을 해제하거나 수정하기 위한 메타-PR을 인간에게 능동적으로 제안할 수 있는 상위 통제 및 비판 기능이다.41

이러한 삼위일체의 구조 속에서 에이전트는 규칙을 따르는 동시에 규칙을 파괴하며 학습을 지속할 수 있다.

### **2\) 무상태(Stateless) 실행에서 세대 간 전승(Generational Memory)으로의 전환**

현재의 하네스 프레임워크는 에이전트가 실행될 때마다 비어있는 컨텍스트 윈도우에 지식을 새롭게 욱여넣는 철저한 무상태(Stateless) 방식에 머물러 있다. 에이전트가 한계를 돌파하기 위해서는 컨텍스트에 의존하는 '소프트웨어 3.0'을 넘어, 스스로 훈련 데이터를 생산하여 내재화하는 '소프트웨어²(Software²)' 패러다임으로의 진입이 요구된다.45

이는 에이전트가 수행한 수만 번의 E2E 테스트 실패 기록, 막다른 골목에 다다랐던 디버깅 세션, 그리고 린터 위반 사례의 역사를 단순히 로그로 폐기하는 것이 아니라, 구조화된 메타데이터로 영구히 축적하는 것을 의미한다.45 에이전트는 수면 시간이나 유휴 컴퓨팅 자원을 활용하여 이 실패의 궤적들을 자체 학습 데이터로 변환하고, 자신의 내부 신경망 가중치(Weights)를 직접 파인튜닝(Fine-tuning)함으로써 다음 세대에는 동일한 추론 과정을 거치지 않고도 직관적으로 정답에 도달해야 한다. 카파티의 오토리서치 역시 단일 세대의 실험에 그치지 않고, 수천 세대에 걸쳐 누적된 실험 궤적을 바탕으로 PPO 기반의 메타 정책을 학습시켜 에이전트가 '문제 해결을 위한 연구 전략' 자체를 진화시키도록 유도하는 비전을 내포하고 있다.33

### **3\) 검증 가능성(Verifiability)의 무한한 확장과 자기 참조적 하네스**

하네스가 단순히 구문론적 오류나 코딩 컨벤션을 강제하는 옹졸한 수문장에 머물지 않으려면, 현실 세계의 비즈니스 로직과 사용자 경험에서 뿜어져 나오는 동적인 피드백을 수용할 수 있도록 검증 가능성의 경계를 획기적으로 확장해야 한다.

선구적인 마케팅 AI 시스템이 수만 번의 A/B 테스트 랜딩 페이지를 자율적으로 생성하고, 고객의 긍정적인 답장 비율(Positive Reply Rate)이라는 외부 지표를 보상 함수로 삼아 스스로를 진화시키듯 30, 지속적 학습을 추구하는 소프트웨어 에이전트 역시 코드의 정적 정합성을 넘어 배포 이후의 성능 지표(APM 로그, 사용자 체류 시간, 인프라 비용 증감 등)를 RLVR의 새로운 보상 함수(Reward Function)로 파이프라인에 통합해야 한다. 궁극적으로 에이전트는 인간이 최초에 구축한 하네스 자체를 비판적으로 평가하고, "더 빠르고 정확한 에이전트 실행을 위해 현재의 하네스를 어떻게 리팩토링해야 하는가"에 대한 자기 참조적(Self-referential) 개선안을 끊임없이 도출하는 안티-프래질(Anti-fragile) 시스템으로 거듭나야 한다.44

## **결론: 엔지니어링 엄격성의 재배치 (Relocating Rigor)**

안드레 카파티의 오토리서치 프레임워크와 하네스 엔지니어링의 동시다발적인 대두는, 인간이 컴퓨터와 소프트웨어를 대하는 근본적인 철학의 종말과 새로운 시작을 선언한다. 우리는 모니터 앞에서 한 줄 한 줄 코드를 타이핑하며 밤을 지새우던 시대(Software 1.0)를 지나, 거대한 GPU 클러스터 앞에서 모델의 가중치를 최적화하던 시대(Software 2.0)마저 뛰어넘어, 이제는 지능형 에이전트가 독자적으로 사유하고 코드를 생산하며 물리적, 가상적 세계와 상호작용할 수 있는 생태계적 환경을 조각하는 시대(Software 3.0 및 Agentic Engineering)의 심장부에 서 있다.4

하네스 엔지니어링은 폭주하는 에이전트가 아키텍처의 궤도를 이탈하여 치명적인 기술 부채를 양산하지 않도록 지탱해 주는 훌륭하고도 견고한 닻(Anchor)이다. 인간의 통제력을 유지하고 상용 시스템의 안정성을 보장하기 위해 이는 반드시 거쳐야 할 공학적 관문이다. 그러나 오토리서치의 단순하고도 아름다운 루프가 잔인하리만치 명백하게 증명했듯, 기계 지능의 진정한 진보와 혁신적인 발견은 안전망 속의 안주가 아니라, 끊임없는 가설의 생성, 무자비한 실험과 파괴, 그리고 객관적이고 가혹한 지표를 통한 최적화 루프 속에서만 폭발적으로 피어난다.

따라서 에이전트가 인간의 대리인을 넘어 진정한 의미의 '지속적 학습' 능력을 획득하기 위한 초석은, 에이전트를 답답한 린터와 마크다운 지시서의 감옥 속에 억압하는 단단하고 경직된 하네스가 아니다. 오히려 하네스 그 자체가 에이전트의 실험 결과와 외부 세계의 피드백에 반응하여 유기적으로 확장되고 세포 분열하듯 재조정될 수 있는 '살아 숨 쉬는 토양(Engineering Soil)'으로 기능해야만 한다.

소프트웨어 공학의 엄격함(Rigor)은 사라진 것이 아니라 그 위치를 이동했을 뿐이다. 코드를 완벽하게 작성하는 데 집중되었던 인간의 지적 에너지는 이제, 에이전트가 무한한 탐색과 파괴적 혁신을 지속하면서도 시스템의 완전성을 잃지 않을 수 있도록 다차원적인 피드백 루프와 진화론적 평가 환경을 정교하게 세공하는 위대한 조물주의 영역으로 승화하고 있다.3

이러한 정적인 제약(Harness)과 동적인 진화(Autoresearch)의 완벽한 융합 체계를 구축하는 것만이, 거세게 밀려오는 자율형 AI 시대의 압도적인 복잡성과 엔트로피를 통제하고, 끝없이 학습하며 팽창하는 외계의 지능을 인류의 소프트웨어 공학이라는 문명의 틀 안에 안전하게 정착시키는 유일하고도 영원한 초석이 될 것이다.

#### **참고 자료**

1. Harness engineering: leveraging Codex in an agent-first world | OpenAI, 3월 19, 2026에 액세스, [https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)  
2. Embracing the agentic engineering era at Speak, 3월 19, 2026에 액세스, [https://www.speak.com/blog/agentic-engineering](https://www.speak.com/blog/agentic-engineering)  
3. Harness Engineering \- Martin Fowler, 3월 19, 2026에 액세스, [https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)  
4. What Is Agentic Engineering? Complete History: From Turing to Karpathy, AutoGPT to Autoresearch & Beyond (2026) \- Taskade, 3월 19, 2026에 액세스, [https://www.taskade.com/blog/what-is-agentic-engineering](https://www.taskade.com/blog/what-is-agentic-engineering)  
5. Andrej Karpathy's “Software 3.0” Vision: The Definitive Blueprint for AI-Native Application Modernisation, 3월 19, 2026에 액세스, [https://ainativefoundation.org/andrej-karpathys-software-3-0-vision-the-definitive-blueprint-for-ai-native-application-modernization/](https://ainativefoundation.org/andrej-karpathys-software-3-0-vision-the-definitive-blueprint-for-ai-native-application-modernization/)  
6. Agentic Engineering: The Complete Guide to AI-First Software Development Beyond Vibe Coding (2026) | NxCode, 3월 19, 2026에 액세스, [https://www.nxcode.io/resources/news/agentic-engineering-complete-guide-vibe-coding-ai-agents-2026](https://www.nxcode.io/resources/news/agentic-engineering-complete-guide-vibe-coding-ai-agents-2026)  
7. What is Agentic Engineering? | IBM, 3월 19, 2026에 액세스, [https://www.ibm.com/think/topics/agentic-engineering](https://www.ibm.com/think/topics/agentic-engineering)  
8. My AI Adoption Journey \- Mitchell Hashimoto, 3월 19, 2026에 액세스, [https://mitchellh.com/writing/my-ai-adoption-journey](https://mitchellh.com/writing/my-ai-adoption-journey)  
9. Beyond Prompts and Context: Harness Engineering for AI Agents ..., 3월 19, 2026에 액세스, [https://madplay.github.io/en/post/harness-engineering](https://madplay.github.io/en/post/harness-engineering)  
10. 52 Days of Harness Engineering by One Person : r/SideProject \- Reddit, 3월 19, 2026에 액세스, [https://www.reddit.com/r/SideProject/comments/1rt7kyv/52\_days\_of\_harness\_engineering\_by\_one\_person/](https://www.reddit.com/r/SideProject/comments/1rt7kyv/52_days_of_harness_engineering_by_one_person/)  
11. Software 2.0 \- Andrej Karpathy – Medium, 3월 19, 2026에 액세스, [https://karpathy.medium.com/software-2-0-a64152b37c35](https://karpathy.medium.com/software-2-0-a64152b37c35)  
12. \#72: Software 2.0 in the Enterprise – Celebrating the learning and curious mindset, 3월 19, 2026에 액세스, [https://thinklikesocrates.com/2022/11/27/software-2-0-in-the-enterprise/](https://thinklikesocrates.com/2022/11/27/software-2-0-in-the-enterprise/)  
13. Lessons from Andrej Kaparthy \- Antoine Buteau, 3월 19, 2026에 액세스, [https://www.antoinebuteau.com/lessons-from-andrej-kaparthy/](https://www.antoinebuteau.com/lessons-from-andrej-kaparthy/)  
14. Software 3.0: Redefining the Foundations of Programming | by Christos Theodoropoulos | Data Science Collective | Medium, 3월 19, 2026에 액세스, [https://medium.com/data-science-collective/software-3-0-redefining-the-foundations-of-programming-409cf24e6c96](https://medium.com/data-science-collective/software-3-0-redefining-the-foundations-of-programming-409cf24e6c96)  
15. AI Trends 2025: What Karpathy's Talk Didn't Tell You (But You Need to Know) \- Software 3.0, 3월 19, 2026에 액세스, [https://www.phenx.io/post/ai-trends-2025-software-30](https://www.phenx.io/post/ai-trends-2025-software-30)  
16. The Future of Software: Insights from Andrej Karpathy \- Frank's World of Data Science & AI, 3월 19, 2026에 액세스, [https://www.franksworld.com/2025/06/19/the-future-of-software-insights-from-andrej-karpathy/](https://www.franksworld.com/2025/06/19/the-future-of-software-insights-from-andrej-karpathy/)  
17. A Story of Computer-Use: Where We Started, Where We're Headed \- Hugging Face, 3월 19, 2026에 액세스, [https://huggingface.co/blog/cua-ai/clawdbot-computer-use-history](https://huggingface.co/blog/cua-ai/clawdbot-computer-use-history)  
18. Inside the LLM OS: Understanding the Architecture | by Shaunak J \- Medium, 3월 19, 2026에 액세스, [https://medium.com/@shaunakpython/inside-the-llm-os-understanding-the-architecture-a00b7be1da53](https://medium.com/@shaunakpython/inside-the-llm-os-understanding-the-architecture-a00b7be1da53)  
19. What would an LLM OS look like? \- Cam Pedersen, 3월 19, 2026에 액세스, [https://campedersen.com/llm-os](https://campedersen.com/llm-os)  
20. Build the LLM OS | Autonomous LLMs as the new Operating System \- YouTube, 3월 19, 2026에 액세스, [https://www.youtube.com/watch?v=YMZm7LdGQp8](https://www.youtube.com/watch?v=YMZm7LdGQp8)  
21. Agent Harness. The harness enforces control at scale… | by Bijit Ghosh \- Medium, 3월 19, 2026에 액세스, [https://medium.com/@bijit211987/agent-harness-b1f6d5a7a1d1](https://medium.com/@bijit211987/agent-harness-b1f6d5a7a1d1)  
22. What is agentic engineering? \- Simon Willison's Weblog, 3월 19, 2026에 액세스, [https://simonwillison.net/guides/agentic-engineering-patterns/what-is-agentic-engineering/](https://simonwillison.net/guides/agentic-engineering-patterns/what-is-agentic-engineering/)  
23. From vibes to engineering: How AI agents outgrew their own terminology \- The New Stack, 3월 19, 2026에 액세스, [https://thenewstack.io/vibe-coding-agentic-engineering/](https://thenewstack.io/vibe-coding-agentic-engineering/)  
24. OpenAI Introduces Harness Engineering: Codex Agents Power Large‑Scale Software Development \- InfoQ, 3월 19, 2026에 액세스, [https://www.infoq.com/news/2026/02/openai-harness-engineering-codex/](https://www.infoq.com/news/2026/02/openai-harness-engineering-codex/)  
25. Harness Engineering: What It Means for QA \- Test Collab, 3월 19, 2026에 액세스, [https://testcollab.com/blog/harness-engineering](https://testcollab.com/blog/harness-engineering)  
26. The Agent-First Engineering Playbook Has a Blind Spot the Size of the Atlantic \- Medium, 3월 19, 2026에 액세스, [https://medium.com/@michael.hannecke/the-agent-first-engineering-playbook-has-a-blind-spot-the-size-of-the-atlantic-6d9e18af5fae](https://medium.com/@michael.hannecke/the-agent-first-engineering-playbook-has-a-blind-spot-the-size-of-the-atlantic-6d9e18af5fae)  
27. What I Learned Building a 350K-Line Codebase Solo in 52 Days Using AI Agents (Harness Engineering Lessons) : r/ClaudeAI \- Reddit, 3월 19, 2026에 액세스, [https://www.reddit.com/r/ClaudeAI/comments/1rt81de/what\_i\_learned\_building\_a\_350kline\_codebase\_solo/](https://www.reddit.com/r/ClaudeAI/comments/1rt81de/what_i_learned_building_a_350kline_codebase_solo/)  
28. Andrej Karpathy Just Released Autonomous AI Agents That Run Research Overnight – Here's What It Means for Enterprise AI \- LeapLytics, 3월 19, 2026에 액세스, [https://www.leaplytics.de/cs/andrej-karpathy-just-released-autonomous-ai-agents-that-run-research-overnight-heres-what-it-means-for-enterprise-ai/](https://www.leaplytics.de/cs/andrej-karpathy-just-released-autonomous-ai-agents-that-run-research-overnight-heres-what-it-means-for-enterprise-ai/)  
29. karpathy/autoresearch: AI agents running research on ... \- GitHub, 3월 19, 2026에 액세스, [https://github.com/karpathy/autoresearch](https://github.com/karpathy/autoresearch)  
30. Andrej Karpathy's new open source 'autoresearch' lets you run hundreds of AI experiments a night — with revolutionary implications | VentureBeat, 3월 19, 2026에 액세스, [https://venturebeat.com/technology/andrej-karpathys-new-open-source-autoresearch-lets-you-run-hundreds-of-ai](https://venturebeat.com/technology/andrej-karpathys-new-open-source-autoresearch-lets-you-run-hundreds-of-ai)  
31. Karpathy Autoresearch Explained: 100 Experiments Overnight \- Data Science Dojo, 3월 19, 2026에 액세스, [https://datasciencedojo.com/blog/karpathy-autoresearch-explained/](https://datasciencedojo.com/blog/karpathy-autoresearch-explained/)  
32. What Is the AutoResearch Loop? How to Apply Karpathy's Pattern to Business Optimization, 3월 19, 2026에 액세스, [https://www.mindstudio.ai/blog/what-is-autoresearch-loop-karpathy-business-optimization](https://www.mindstudio.ai/blog/what-is-autoresearch-loop-karpathy-business-optimization)  
33. AutoResearch-RL: Perpetual Self-Evaluating Reinforcement Learning Agents for Autonomous Neural Architecture Discovery \- arXiv, 3월 19, 2026에 액세스, [https://arxiv.org/pdf/2603.07300](https://arxiv.org/pdf/2603.07300)  
34. Andrej Karpathy's 630-line Python script ran 50 experiments overnight without any human input \- The New Stack, 3월 19, 2026에 액세스, [https://thenewstack.io/karpathy-autonomous-experiment-loop/](https://thenewstack.io/karpathy-autonomous-experiment-loop/)  
35. autoresearch: Karpathy's Blueprint for Agents That Improve Themselves \- mager.co, 3월 19, 2026에 액세스, [https://www.mager.co/blog/2026-03-14-autoresearch-pattern/](https://www.mager.co/blog/2026-03-14-autoresearch-pattern/)  
36. Andrew Karpathy's “autoresearch”: An autonomous loop where AI edits PyTorch, runs 5-min training experiments, and continuously lowers its own val\_bpb. "Who knew early singularity could be this fun? \- Reddit, 3월 19, 2026에 액세스, [https://www.reddit.com/r/singularity/comments/1roo6v0/andrew\_karpathys\_autoresearch\_an\_autonomous\_loop/](https://www.reddit.com/r/singularity/comments/1roo6v0/andrew_karpathys_autoresearch_an_autonomous_loop/)  
37. Karpathy Agent Portends AI 'Final Boss Battle' \- Techstrong.ai, 3월 19, 2026에 액세스, [https://techstrong.ai/features/karpathy-agent-portends-ai-final-boss-battle/](https://techstrong.ai/features/karpathy-agent-portends-ai-final-boss-battle/)  
38. 2025 LLM Year in Review | karpathy, 3월 19, 2026에 액세스, [https://karpathy.bearblog.dev/year-in-review-2025/](https://karpathy.bearblog.dev/year-in-review-2025/)  
39. Harness Engineering: Why the Frame Matters More Than the Model \- Infralovers, 3월 19, 2026에 액세스, [https://www.infralovers.com/blog/2026-03-13-harness-engineering-rahmen-wichtiger-als-modell/](https://www.infralovers.com/blog/2026-03-13-harness-engineering-rahmen-wichtiger-als-modell/)  
40. The Dilemma of Continuous Learning for Agents: Why a Reasoner Is Not a True Agent, 3월 19, 2026에 액세스, [https://01.me/en/2025/10/agent-continual-learning/](https://01.me/en/2025/10/agent-continual-learning/)  
41. Why AI systems don't learn and what to do about it Lessons on autonomous learning from cognitive science \- arXiv, 3월 19, 2026에 액세스, [https://arxiv.org/html/2603.15381v1](https://arxiv.org/html/2603.15381v1)  
42. reflections, and the state of LLMs in 2025 | ( ・\_・)ノ Ritchot's Corner, 3월 19, 2026에 액세스, [https://ritchot.me/reflections-and-the-state-of-llms-in-2025/](https://ritchot.me/reflections-and-the-state-of-llms-in-2025/)  
43. Mitchell Hashimoto's New Way of Writing Code \- TeamDay.ai, 3월 19, 2026에 액세스, [https://www.teamday.ai/ai/hashimoto-new-way-of-writing-code](https://www.teamday.ai/ai/hashimoto-new-way-of-writing-code)  
44. Humans and Agents in Software Engineering Loops \- Martin Fowler, 3월 19, 2026에 액세스, [https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html](https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html)  
45. Software²: A new generation of AIs that become increasingly general by producing their own training data \- The Gradient, 3월 19, 2026에 액세스, [https://thegradient.pub/software2-a-new-generation-of-ais-that-become-increasingly-general-by-producing-their-own-training-data/](https://thegradient.pub/software2-a-new-generation-of-ais-that-become-increasingly-general-by-producing-their-own-training-data/)  
46. Andrej Karpathy — AGI is still a decade away \- Dwarkesh Podcast, 3월 19, 2026에 액세스, [https://www.dwarkesh.com/p/andrej-karpathy](https://www.dwarkesh.com/p/andrej-karpathy)

[image1]: <data:image/png;base64,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>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD8AAAAYCAYAAABN9iVRAAADk0lEQVR4Xu2XS6iNURTHlzwi78gj5NGdmJA8SokUopAYUMpEKCYiFAa3pBATj5TkNcRMXiWuKMpMpEguiQxQikIe/5/1rXP2993rdM59uAPnX//O9+21v70ee6219zGro4466qijQzBIHCJ2KwqqQHdxmNivKKgRvcXhYs+ioLMwV/wk/hIvmxtQLXqJp8Qf5t+vzourRoP4yHyNt+KEvLhzgTKU7iwKqsQG8bM4tSioAQSd4DdZ+zOoJswTv2W/tYIyOS0+EAcXZLVglNgs7i2MdzpQ2NZ0Gyo+Ng9AW/pFgMBTPkuLghQ0F9JrtpUbA0oni2NjUgLmTLP8/BSRbrXWewBbSPk12fMScUAi53mROCZ77ysuMJ+LL4Ed5hswKZPPKsj/GH9I3Cbez54BjtO0bpgvHpgjPhS3ipvEe+JHc2MCUe9tTTfq/af4TNxibtsL84D3EY+Z95I34j7xonlj5PeEuU+xAV/FW5n8rHhVHGgZ5ou7zWsL55kAUHLG8s1ihvhOXJm9AxwsNqaOqHcCij6A/qZsHHt3iRPF9+JJc1vBdPPv0Bv1zuaFs9jIhpbKYJ35QjPFL+KqEJinyZHsOQwgQKXImSunPqnTQHvqnU2g0aX1HrohWUFQcIB6TgOMvd/Ns4Vndj2t9ygnyiGHRvG1OD4ZW26uDKCEVExTuTVDO6reQy+IMkpLEDuazXc4wDec69iNg2QGGxsg9ZETnBLCCWqmRzaGM41W/pjFcD6NdPSF1gxta73T3MhAUjgQgW/M3gkAgUjt5Zf3cJjyvSP2z+TgsHk2kOUljBRfWj4dyICDVl4cGY7icIBIhqH0gRWWr3ea49rS7OqA89iCTYBNOGre3BqysQhw0V4y97i5zTgf/QtwxX0inrfCCYXguZVvYwj3i1NKM8wWih+s3Ng4Ap+aG8qRQ28g4qQUhmHoAStEuQowny4f/YL6Zj0CG6COSd/G7J0A7TG/zsbRjCwyA/l2c+dbHN0IN5p38nPiNXFZboYHhEy4ax7RS+YGvRKviJvN1yEABOS6+bHZ2j2gEiLwpCy2EODFlr/sUFJ0dZrvBfG2uaMjkjmjxZvZOPY1ieMSeQvQoEi3So2q+E+Nuel7jPGPLC4UfMN5zBlcieldgQ6frpGON5k3VI44dMdRXAQ2IUd/lyH+nhLYSvybEylaq/f/AgRnvXm9c/Xt0h391+DkSMskvZDVUQt+Awx+wdM7Q//uAAAAAElFTkSuQmCC>