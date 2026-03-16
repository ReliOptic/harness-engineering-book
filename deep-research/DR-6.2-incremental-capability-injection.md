# **인공지능 에이전트의 점진적 능력 주입 및 자가 진화론적 아키텍처 연구**

## **1\. 서론: 정적 지식 모델에서 동적 진화 에이전트로의 패러다임 전환**

초거대 언어 모델(Large Language Model, LLM)의 등장은 자연어 처리와 인지적 추론 분야에 전례 없는 혁신을 가져왔으나, 모델의 매개변수 내부에 고정된 정적 지식(Static Knowledge)에만 의존하는 구조적 특성은 한계를 내포하고 있다. 특히 개방형 환경(Open-ended Environment)에서 다단계의 복잡한 추론을 수행하거나, 고도의 도메인 특화 지식이 요구되는 장기 실행(Long-horizon) 작업을 처리할 때, 사전 학습된 지식만으로는 동적으로 변화하는 환경의 요구사항을 충족하기 어렵다.1 이러한 한계를 극복하기 위해, 최근의 인공지능 에이전트 연구는 모델을 정적인 '완제품'으로 간주하는 관점에서 벗어나, 외부 환경과의 상호작용을 통해 평생에 걸쳐 능력을 축적하고 구조를 재편하는 '지속 가능한 생애 주기 시스템(Lifelong Agentic Systems)'으로 그 초점을 이동시키고 있다.4

본 보고서에서 심층적으로 다루고자 하는 핵심 주제는 에이전트의 능력을 실행 시간(Runtime)에 동적으로 확장하는 '점진적 능력 주입(Gradual Capability Injection)'과, 에이전트 스스로 초기 역량을 지렛대 삼아 새로운 도구와 제어 정책을 합성해 내는 '능력 부트스트래핑(Capability Bootstrapping)' 방법론이다.1 이 두 가지 접근법은 인공지능이 모델의 가중치(Weights)를 재학습하는 막대한 컴퓨팅 비용을 지불하지 않고도, 새로운 기술을 학습하고 이를 영구적인 자산으로 보존할 수 있도록 하는 결정적인 기제를 제공한다.9

본 연구는 에이전트가 겪는 파국적 망각(Catastrophic Forgetting)과 컨텍스트 윈도우의 제약을 분석하고, 도구 제작자로서의 LLM(LATM), 컨텍스트 엔지니어링을 통한 상태 주입, 그리고 명시적인 스킬 라이브러리(Skill Library)의 구축에 이르는 광범위한 기술적 진보를 체계적으로 조사한다. 나아가 실패 궤적(Failed Trajectories) 기반의 자동화된 스킬 발견과 자가 진화(Self-Evolution) 에이전트의 구조적 프레임워크를 분석함으로써, 인공지능이 자율적 초지능(Artificial Super Intelligence, ASI)으로 나아가는 기술적 궤적을 제시한다.11

## **2\. 에이전트 인지 구조의 근본적 제약과 점진적 확장의 당위성**

인공지능 에이전트가 새로운 환경에 적응하고 능력을 획득하는 과정에서 직면하는 가장 큰 기술적 장벽은 정보의 손실과 절차적 지식의 부재이다. 기초 모델(Foundation Models)은 광범위한 세계 지식을 보유하고 강력한 영샷(Zero-shot) 추론과 인컨텍스트 학습(In-context Learning) 능력을 발휘하지만, 이들은 특정 도메인의 워크플로우에 필요한 세밀한 '절차적 지식(Procedural Knowledge)'을 본질적으로 결여하고 있다.1

에이전트에게 이러한 절차적 지식을 주입하기 위해 전통적으로 사용되어 온 지속적 학습(Continual Learning) 방식이나 모델 파인튜닝(Fine-tuning)은 '파국적 망각(Catastrophic Forgetting)'이라는 치명적인 부작용을 동반한다.14 파국적 망각이란 인공 신경망이 새로운 작업(Task)이나 데이터 패턴을 학습하기 위해 내부 가중치를 업데이트할 때, 기존에 학습했던 지식의 표현(Representation)과 수학적 관계성이 훼손되거나 완전히 덮어쓰기 되어 원래 수행하던 작업 능력을 상실하는 현상을 의미한다.15 대형 언어 모델일수록 이러한 네트워크 가중치의 간섭 현상은 더욱 심각하게 나타나며, 이는 에이전트가 지속적으로 다양한 스킬을 누적 학습해야 하는 시나리오에서 모델 매개변수 자체를 수정하는 접근법이 근본적으로 부적합함을 시사한다.12

이러한 가중치 업데이트의 대안으로 제시된 것이 프롬프트를 통한 인컨텍스트 학습이지만, 이 역시 장기 실행 환경에서는 '컨텍스트 윈도우(Context Window)'라는 물리적 병목에 가로막힌다.8 복잡한 소프트웨어 프로젝트나 수일이 소요되는 장기 목표를 수행하는 에이전트는 제한된 토큰 용량으로 인해 필연적으로 세션을 분할해야 한다.8 Anthropic의 연구에 따르면, 장기 실행 코딩 에이전트(예: Claude Agent SDK 기반)는 컨텍스트가 한계에 다다르면 과거의 메시지를 압축(Compaction)하거나 요약하여 토큰 공간을 확보하는데, 이 순간 에이전트가 자신이 작업 중이던 Git 브랜치의 위치나 최근 수정한 파일의 맥락을 상실하는 치명적인 실패 모드가 발생한다.8 교대 근무자가 이전 근무자의 인수인계 없이 업무에 투입되는 것과 같은 이러한 맥락 단절 현상은, 에이전트의 능력을 시스템 내부에 정적으로 담아두는 것이 아니라 실행 시간에 점진적이고 동적으로 주입(Injection)해야 할 절대적인 당위성을 부여한다.8

| 한계 유형 | 발생 원인 및 메커니즘 | 에이전트 성능에 미치는 영향 | 대안적 해결 프레임워크 |
| :---- | :---- | :---- | :---- |
| **파국적 망각 (Catastrophic Forgetting)** | 파인튜닝 중 그래디언트 업데이트로 인한 기존 가중치 간섭 및 손실 15 | 새로운 스킬 학습 시 기존에 마스터한 기능이나 추론 능력의 붕괴 15 | 모듈형 외부 스킬 라이브러리 및 코드 기반 아티팩트 보존 10 |
| **컨텍스트 압축 손실 (Context Compaction Loss)** | 컨텍스트 윈도우 초과 방지를 위한 런타임 과거 로그 삭제 및 요약 8 | 현재 진행 중인 작업의 논리적 흐름 상실, 환각 증세 발생 8 | 압축 직전 중요 상태 스냅샷의 명시적 주입 및 컨텍스트 엔지니어링 8 |
| **절차적 지식 부재 (Procedural Knowledge Gap)** | 일반적인 텍스트 코퍼스로 학습된 기초 모델의 도메인 특화 워크플로우 경험 부족 1 | 복잡한 도메인(예: 의료, 전문 코딩)에서의 다단계 행동 계획 실패 1 | 도구 자동 생성(LATM), 자기 성찰 기반 스킬 큐레이션 및 능력 부트스트래핑 18 |

## **3\. 능력 부트스트래핑(Capability Bootstrapping): 자율적 역량 증폭 메커니즘**

에이전트가 외부의 인간 엔지니어에 의존하지 않고 자신이 현재 보유한 추론 능력만을 활용하여 스스로 결여된 도구를 만들고 절차적 지식을 합성해 내는 과정을 '능력 부트스트래핑(Capability Bootstrapping)'이라고 정의한다.1 이는 척박한 자원 환경(Low-resource settings)에서 합성 데이터(Synthetic Data)를 자가 생성하고 스스로 검증하는 메커니즘을 통해 기초 모델을 강력한 전문가 시스템으로 탈바꿈시키는 핵심 동력이다.7

### **3.1. 도구 제작자로서의 거대 언어 모델 (LATM 프레임워크)**

가장 직관적이고 강력한 능력 부트스트래핑 방법론은 LLM을 단순한 도구의 사용자가 아닌 도구의 '창조자'로 격상시키는 LATM(LLMs As Tool Makers) 프레임워크이다.18 기존의 도구 증강 에이전트(Tool Augmented Agents)들은 개발자가 사전에 하드코딩한 API나 외부 함수에 의존하여 계산, 검색 등의 기능을 수행했다.21 그러나 LATM은 이러한 의존성을 제거하고, 폐쇄 루프(Closed-loop) 내에서 에이전트가 스스로 재사용 가능한 도구를 생성하는 혁신적인 인지적 분업(Cognitive Division of Labor) 아키텍처를 제시한다.18

이 프레임워크는 비용과 능력이 서로 다른 다중 LLM을 교차 활용한다. 첫 번째 단계에서 고성능의 대형 모델(예: GPT-4)은 '도구 제작자(Tool Maker)'로 배치되어, 주어진 복잡한 논리적 과제를 분석하고 이를 해결하기 위한 맞춤형 파이썬(Python) 함수를 작성한다.20 이 도구 제작자는 코드를 작성할 뿐만 아니라 몇 가지 샘플을 통해 해당 도구의 무결성을 검증하며, 성공적으로 작동하는 도구에 대해서는 사용법을 설명하는 문서화 스트링(Docstring)까지 스스로 생성하여 라이브러리에 캡슐화한다.21

두 번째 단계에서는 비교적 가볍고 연산 비용이 저렴한 모델(예: GPT-3.5)이 '도구 사용자(Tool User)' 역할을 맡아, 새롭게 주입된 도구들을 호출하여 실제 사용자들의 후속 요청을 처리한다.20 여기서 가장 중요한 구조적 요소는 세 번째 에이전트인 '디스패처(Dispatcher)'의 존재이다. 디스패처는 새로운 작업 스트림이 유입될 때마다 현재 스킬 라이브러리에 있는 도구들로 해결이 가능한지 판별하고, 해결이 불가능한 미지의 문제에 대해서만 도구 제작자를 호출해 새로운 도구를 합성하도록 트리거를 당긴다.24 이는 일종의 '기능적 캐시(Functional Cache)' 메커니즘으로 작용하여, 시스템이 마주하는 새로운 태스크에 대한 처리 능력을 무한히 확장하면서도 반복적인 작업에 대해서는 연산 자원을 극적으로 절감하는 고도의 자율 부트스트래핑을 완성한다.22

### **3.2. 시뮬레이션을 통한 로보틱스 데이터 자가 합성 (BLAZER 프레임워크)**

능력 부트스트래핑의 원리는 순수 소프트웨어 환경을 넘어 데이터의 희소성이 극심한 물리적 로봇 조작(Robotic Manipulation) 분야로 확장되고 있다. 자연어 모델과 달리 로보틱스 분야는 인터넷 규모의 시연 데이터가 존재하지 않아 수동적인 데이터 수집에 크게 의존해 왔다.25 이러한 제약을 극복하기 위해 제안된 BLAZER 프레임워크는 대형 언어 모델의 영샷(Zero-shot) 계획 수립 능력을 활용하여 조작 에이전트의 능력을 부트스트래핑한다.25

BLAZER 시스템의 작동 메커니즘은 강력한 기초 LLM을 시뮬레이터와 결합하는 것에서 시작된다. 주어진 물리적 조작 과제 모음에 대해, LLM은 어떠한 인간의 시연이나 사전 지식 없이 스스로 판단하여 실행 가능한 제어 명령어 시퀀스를 합성한다.25 생성된 제어 정책들은 로봇 시뮬레이터 환경 내에서 즉시 실행되며, 환경의 상태(State) 피드백을 통해 목표를 완수한 성공적인 궤적(Successful Trajectories)들만이 엄격하게 필터링되어 작업 데이터베이스에 추가된다.25

이렇게 기계가 스스로 합성하고 검증한 방대한 시뮬레이션 데이터를 활용하여, 최종적으로 더 작고 가벼운 에이전트 모델을 지도 학습(Supervised Finetuning) 방식으로 최적화한다.25 이 프레임워크는 런타임 능력 주입을 넘어선 오프라인 지식의 내재화 과정으로, 기초 LLM의 언어적 추론 능력을 로봇 제어를 위한 절차적 지식으로 성공적으로 치환한다. 실험 결과, BLAZER를 통해 부트스트래핑된 에이전트는 인간의 개입 없이도 학습 풀(Training Pool)에 존재하지 않았던 새로운 물리적 과제를 해결하는 강력한 일반화 성능을 보였으며, 시뮬레이션에서 획득한 스킬들이 센서 기반의 실제 로봇(Sim-to-Real)으로 직접 전이(Direct Transfer)되는 놀라운 성과를 입증하였다.25

## **4\. 컨텍스트 엔지니어링과 런타임 스킬 주입 (Runtime Skill Injection)**

부트스트래핑 메커니즘이 에이전트의 능력을 오프라인이나 백그라운드에서 근본적으로 창출하고 향상시키는 과정이라면, '스킬 주입(Skill Injection)'은 확보된 수많은 역량 중 현재 상황에 가장 적합한 도구와 지식을 에이전트의 실행 시간(Runtime)에 동적으로 할당하는 기술적 매개체이다.16 초기의 프롬프트 엔지니어링이 단순히 모델에게 지시하는 문장을 정제하는 작업에 머물렀다면, 현대의 에이전트 아키텍처에서는 이를 넘어서서 모델의 추론 과정 중 어느 시점에 어떤 토큰(정보)을 전략적으로 노출시킬 것인가를 결정하는 포괄적인 '컨텍스트 엔지니어링(Context Engineering)'으로 발전하였다.16

### **4.1. 장기 실행 세션에서의 상태 보호와 강제 주입 메커니즘**

에이전트가 단일 컨텍스트 윈도우의 제약을 넘어 연속적인 작업을 수행하기 위해서는 컨텍스트 압축 과정에서 유실되는 지향성을 보존해야 한다. Anthropic의 Claude Agent SDK 개발 사례에서 관찰할 수 있듯, 런타임 환경에서 에이전트에게 필요한 것은 단순한 프롬프트가 아니라 실행 맥락에 대한 '상태(State)' 정보의 지속적인 주입이다.8

시스템이 토큰 한계에 도달하여 과거 대화 기록을 요약하거나 폐기하기 직전, 최첨단 주입 메커니즘은 훅(Hook) 시스템을 통해 명시적인 상태 검사 명령어를 실행한다.17 예를 들어, inject\_command 기능을 활용하여 에이전트가 활동 중인 터미널에서 git branch \--show-current나 git status와 같은 명령어를 백그라운드에서 강제 실행하고, 그 결과로 도출된 "현재 작업 브랜치" 및 "최근 수정된 파일 10개"의 목록을 압축 이후의 새로운 컨텍스트 윈도우 상단에 스냅샷 형태로 강제 삽입한다.17

이러한 명시적 상태 주입은 에이전트가 작업의 연속성을 잃고 잘못된 파일 경로를 탐색하거나 환각을 일으키는 것을 원천적으로 차단하는 가장 강력한 안전망으로 작용한다.8 이는 정적인 텍스트 지시가 아니라, 에이전트의 현재 환경적 맥락을 실시간으로 반영하여 절차적 기억을 인공적으로 연장하는 고도의 스킬 주입 사례이다.

### **4.2. 엔터프라이즈급 스케일링을 위한 점진적 스킬 공개와 미들웨어**

수백 가지의 다양한 보안 정책, 사내 개발 가이드라인, 그리고 특화된 도구들을 보유한 대규모 엔터프라이즈 환경에서는 모든 스킬과 지식을 에이전트의 기본 프롬프트에 담는 것이 불가능하다. 이에 따라 현대의 프레임워크들은 에이전트의 현재 의도와 작업 맥락을 분석하여 필요한 스킬만을 적시에 노출시키는 '점진적 스킬 공개(Progressive Skill Disclosure)' 메커니즘을 채택한다.28

JoySafeter 프레임워크의 구조를 살펴보면, 확장 가능한 미들웨어 아키텍처(Extensible Middleware Architecture)를 통해 이러한 동적 능력을 달성한다.28 사용자의 입력이 에이전트 모델에 도달하기 전, 우선순위가 부여된 스킬 미들웨어(Skill Middleware, 예: Priority 50)가 가로채기를 수행하여 대화의 주제와 요구 사항을 분석한다.28 이후, 200개 이상의 거대한 스킬 매트릭스 중에서 관련된 스킬들의 명세와 사용 방법만을 선별하여 시스템 프롬프트에 지능적으로 주입한다.28

특히 이러한 스킬들은 실행 효율성을 극대화하기 위해 백엔드의 에이전트 전용 격리 환경(Docker 컨테이너 등)에 밀리초(ms) 단위로 사전 로드되며, 에이전트는 상황에 따라 주입된 스킬들을 동적으로 탐색하고 유연하게 조합하여 호출한다.13 이러한 아키텍처는 컨텍스트 윈도우의 낭비를 최소화하면서도 에이전트가 접근할 수 있는 기능적 범위를 기하급수적으로 확장하는 이점을 제공한다.28 동시에 CaveAgent와 같은 시스템은 파이썬(Python) 런타임 자체를 에이전트의 영구적인 중앙 상태 저장소로 승격시킴으로써, 스킬이 한 번 주입된 후에는 런타임 객체로 유지되어 긴 지평(Long-horizon)을 갖는 작업 내내 높은 신뢰성으로 재사용될 수 있도록 보장한다.27

### **4.3. 스킬 주입의 보안적 취약성과 무결성 보장**

동적 스킬 주입 시스템이 가지는 가장 큰 취약점은 외부 스킬이나 도구 명세를 컨텍스트에 삽입하는 과정에서 발생할 수 있는 '검색된 프롬프트 주입 공격(Retrieved Prompt Injection)'이다.1 에이전트가 신뢰할 수 없는 외부 저장소나 오염된 라이브러리에서 스킬 문서(Markdown이나 Docstring)를 검색하여 자신의 프롬프트에 주입할 경우, 문서 내에 숨겨진 악의적인 명령어(예: 데이터 탈취, 권한 상승)를 자신의 목표로 착각하고 실행하게 되는 치명적인 보안 결함이 발생할 수 있다.1

최근 42,447개의 에이전트 스킬을 분석한 대규모 실증 연구에 따르면, 데이터 탈취 및 공급망 위험과 같은 보안 취약점이 스킬 라이브러리 생태계 전반에 광범위하게 퍼져 있음이 확인되었다.27 이에 대응하기 위해 에이전트 아키텍처는 반드시 '제로 트러스트(Zero-Trust)' 기반으로 설계되어야 하며, AgentGuardian과 같은 보안 프레임워크는 에이전트의 정상적인 실행 궤적(Execution Traces)을 모니터링하여 컨텍스트 인식 접근 제어 정책을 학습함으로써 악의적인 입력과 스킬 주입 시도를 런타임에 차단하는 필수적인 방어 기제를 제공한다.27

| 아키텍처 / 프레임워크 | 스킬 주입 메커니즘 및 활용 방식 | 방어 및 안전성 메커니즘 | 해결하는 핵심 문제 |
| :---- | :---- | :---- | :---- |
| **Claude Agent SDK (Anthropic)** | inject\_command 훅을 통한 압축 직전 시스템 상태 스냅샷 주입 8 | 명시적 상태 검사를 통한 환각 및 컨텍스트 상실 방지 17 | 장기 실행 세션에서의 맥락 단절 및 논리적 붕괴 8 |
| **JoySafeter** | 미들웨어 기반 점진적 스킬 공개 (Progressive Skill Disclosure) 28 | 전략 패턴(Strategy Pattern) 기반 미들웨어 오류 격리 28 | 엔터프라이즈급 대규모 스킬 세트 통합 시 컨텍스트 윈도우 오버플로우 28 |
| **AgentGuardian** | 런타임 추적 기반 컨텍스트 인식 제어 (Context-aware Access Control) 27 | 악성 입력 감지 및 권한 제어 정책 자동 학습 27 | 오염된 스킬 주입으로 인한 권한 상승 및 데이터 탈취 취약점 27 |

## **5\. 파국적 망각을 회피하는 모듈형 스킬 라이브러리와 기억의 자산화**

점진적 능력 주입의 패러다임이 지속 가능한 자가 진화로 이어지기 위해서는, 획득한 스킬들을 파국적 망각 없이 장기적으로 보존하고 필요할 때 즉각적으로 인출할 수 있는 저장 구조가 필수적이다. 전통적인 에이전트 메모리 시스템이 과거 대화의 텍스트 조각을 보존하는 데 그쳤다면, 최근의 진보된 에이전트들은 지식을 '실행 가능한 코드'나 '버전이 관리되는 명시적 행동 지침'의 형태로 외재화(Externalization)하여 저장하는 모듈형 '스킬 라이브러리(Skill Library)'를 채택하고 있다.9

### **5.1. Voyager: 실행 가능한 행동 공간과 구성적 스킬의 합류**

스킬 라이브러리의 효용성을 가장 극적으로 증명한 사례는 마인크래프트(Minecraft)라는 고도의 개방형 환경에서 동작하는 Voyager 에이전트이다.10 과거 강화학습(RL) 기반의 에이전트들이 환경을 제어하기 위해 마우스나 키보드 이동과 같은 원시적이고 즉각적인 물리 행동에 의존했다면, Voyager는 '실행 가능한 컴퓨터 코드(Executable Code)' 자체를 에이전트의 행동 공간(Action Space)으로 재정의하였다.10

Voyager는 사전 프로그래밍된 목표 없이 자동 커리큘럼(Automatic Curriculum) 모듈에 의해 새로운 작업을 끊임없이 제안받으며 탐험을 수행한다.10 새로운 목표를 달성하기 위해 에이전트가 코드를 작성하면, 이는 환경 피드백과 실행 오류 메시지, 그리고 자가 검증(Self-verification) 모듈의 비평을 수용하는 '반복적 프롬프팅 메커니즘(Iterative Prompting Mechanism)'을 거쳐 정교하게 다듬어진다.10 자가 검증 모듈이 코드의 성공적인 실행을 확인하면, 해당 코드는(예: 몬스터와 전투하거나 특정 도구를 제작하는 절차) 단순히 버려지는 것이 아니라 스킬 라이브러리에 영구적으로 저장된다.10

이 라이브러리 아키텍처의 탁월함은 스킬의 '구성성(Compositionality)'과 '시맨틱 검색(Semantic Retrieval)'에 있다. 저장되는 각 스킬 코드는 독립된 모듈로 존재하므로, 기존 신경망 가중치를 교란하지 않아 파국적 망각을 원천적으로 회피한다.10 또한 GPT-3.5를 통해 생성된 각 스킬의 기능적 설명은 고차원 벡터 임베딩(Vector Embedding)으로 변환되어 인덱싱된다.10 Voyager가 새로운 도전에 직면하면 자신의 현재 상태와 목표에 대한 코사인 유사도를 계산하여 라이브러리에서 가장 적합한 상위 5개의 스킬을 즉시 검색 및 주입한다.10 더욱 놀라운 점은 에이전트가 이전에 만들어 둔 단순한 스킬들을 하위 함수로 호출하여 더 복잡한 상위 계층의 스킬을 연쇄적으로 합성해 낸다는 것이다.10 그 결과 Voyager는 기존 최첨단 방법론 대비 기술 트리(Tech Tree)를 15.3배 빠르게 해제하였으며, 전혀 학습되지 않은 새로운 맵(Zero-shot environment)에 배치되더라도 라이브러리를 활용해 즉각적으로 복잡한 임무를 수행하는 일반화 능력을 입증하였다.10

### **5.2. AutoSkill: 행동 단위 경험의 결정화와 개인화된 대리인 구축**

스킬 라이브러리의 개념은 게임 환경을 넘어 사용자와의 상호작용 속에서 개인화된 워크플로우를 학습하는 범용 인지 어시스턴트로 진화하고 있다. 기존의 대화형 메모리 기반 에이전트(예: Mem0 등)는 과거의 선호도나 사실을 텍스트로 보관하지만, 과거의 상호작용을 운영 가능한 '행동 규범(Behavior)'으로 전환하는 데는 한계가 있었다.9 이를 극복하기 위해 AutoSkill 프레임워크는 사용자의 명시적인 지시나 암묵적인 선호(예: 특정 라이브러리의 임포트 스타일, 데이터 분석 시 선호하는 통계적 검정 방법 등)를 구조화된 SKILL.md 마크다운 아티팩트로 추출하는 혁신적인 접근을 취한다.9

AutoSkill의 구조는 실시간 사용성을 보장하는 전경(Foreground) 프로세스와 지식을 내재화하는 배경(Background) 프로세스의 이중 트랙으로 작동한다.9 사용자가 쿼리를 입력하면 OpenAI 호환 리버스 프록시가 작동하여, 로컬 벡터 스토어에 보관된 SKILL.md 파일 중 가장 적합한 것을 검색하여 토큰 임계값(Thresholded Top-K) 내에서 프롬프트에 동적 주입한다.9 상호작용이 종료된 후, 배경 프로세스에서는 에이전트가 대화 기록을 분석하여 새로운 절차적 지식이나 스타일 선호도를 추출해 내고, 이를 기존의 스킬 파일과 병합(Versioned Merging)하여 지식 라이브러리를 지속적으로 조용히 진화시킨다.9

이러한 명시적 스킬 파일 기반의 아키텍처는 에이전트의 매개변수를 전혀 재학습하지 않는 학습 무설정(Training-free) 구조임에도 불구하고, 모델의 투명성과 제어 능력을 극적으로 향상시킨다.9 무엇보다 사용자가 자신의 에이전트가 축적한 SKILL.md 파일을 직접 열어보고 편집할 수 있으며, 더 나아가 이러한 스킬 파일 자체가 독립적인 자산(Asset)이 된다.9 이는 특정 분야 전문가가 자신의 에이전트와 상호작용하며 극도로 정제해 놓은 "버전 1.45 데이터 파이프라인 스킬" 파일을 GitHub 클론 방식처럼 다른 사용자의 에이전트로 전송하여 즉시 해당 행동 제약과 능력을 주입할 수 있는 완전히 새로운 차원의 개방형 행동 생태계(Open-source Behavior Ecosystem)의 도래를 예고한다.37

## **6\. 실패 궤적 기반의 자동화된 스킬 발견과 제로샷 전이 역량**

능력 부트스트래핑과 스킬 주입의 잠재력을 극한으로 끌어올리는 단계는 에이전트가 인간의 선험적 설계나 피드백 없이, 자신이 경험한 '실패'를 분석하여 완전히 새로운 추상적 인지 전략을 창조하는 수준에 도달하는 것이다. 이는 단순한 도구의 합성을 넘어선 상위 개념의 메타 인지적 진화를 의미한다. 다중 에이전트 및 코딩 환경에 특화된 EvoSkill 프레임워크는 이러한 진화 과정을 소프트웨어 공학의 버전 관리 원리와 융합하여 자동화된 스킬 발견(Automated Skill Discovery) 루프를 제안한다.11

### **6.1. EvoSkill의 진화적 스킬 자가 개선 루프**

EvoSkill은 에이전트의 시스템 프롬프트와 스킬 라이브러리의 조합 자체를 하나의 최적화 가능한 '프로그램(Program)'으로 취급하며, 다음과 같은 5단계의 정밀한 자가 개선 루프(Self-improvement Loop)를 무한히 반복한다.11

1. **기반 에이전트 실행 (Base Agent Execution):** 에이전트가 현재 자신이 보유한 최고 버전의 프로그램(시스템 프롬프트 및 스킬 조합)을 사용하여 복잡한 장기 실행 벤치마크 문제의 해결을 시도한다.11  
2. **실패 분석 (Proposer):** 평가 과정에서 실패한 궤적(Failed Trajectories)을 '제안자(Proposer)' 모듈이 수집하고 분석한다. 여기서 단순히 오답을 인지하는 것이 아니라, 코드가 루프에 빠진 이유나 검색을 조기에 종료해 버린 패턴 등 실패의 구조적 원인을 진단하고 이를 극복하기 위한 새로운 스킬 생성이나 프롬프트 수정을 제안한다.11  
3. **스킬 합성 (Generator):** '생성자(Generator)' 모듈은 제안자의 분석을 바탕으로 파이썬 언어로 된 실제 스킬 코드를 새롭게 작성하여 디렉토리에 추가하거나, 에이전트의 시스템 프롬프트 구조 자체를 재작성한다.11  
4. **엄격한 평가 (Evaluator):** 새롭게 생성된 프로그램 변형(Variant)은 학습 데이터가 아닌 별도의 검증 데이터셋에서 평가되어, 수정 사항이 실제로 에이전트의 전반적인 성능을 향상시켰는지 정량적으로 측정받는다.11  
5. **프론티어 관리 (Frontier Tracking):** 진화 과정에서 가장 우수한 성과를 보인 상위 N개의 프로그램 구성들은 Git 브랜치(Git branches)의 형태로 추적 및 관리된다.11 이 과정을 통해 특정 스킬의 추가가 치명적인 퇴행(Regression)을 일으켰을 경우 과거의 안정적인 상태로 롤백할 수 있는 재현성(Reproducibility)을 확보한다.11

### **6.2. 발견된 스킬의 제로샷 일반화와 추상적 인지 모델링**

EvoSkill과 같은 자동화된 발견 프레임워크가 가지는 가장 중대한 학술적 의의는 이렇게 발견된 스킬들이 특정 훈련 데이터에 과적합(Overfitting)되지 않고, 완전히 다른 도메인으로 변형 없이 적용될 수 있는 강력한 전이성(Transferability)과 일반화(Generalization) 능력을 지닌다는 점이다.38

문서 기반의 질의응답 벤치마크인 SEAL-QA에서 EvoSkill을 구동한 결과, 에이전트는 초기 검색 결과에 노이즈가 많을 경우 성급하게 오답을 제출해 버리는 치명적인 약점을 극복하기 위해 '검색 지속성 프로토콜(Search-persistence-protocol)'이라는 스킬을 스스로 진화시켰다.38 이 스킬은 용어 해석 확장, 다중 소스 교차 검증, 완전성 검사라는 다단계의 절차를 코드로 캡슐화한 것이다.38 놀라운 점은, 이 스킬 코드를 어떠한 코드 수정(Zero-shot)도 없이 BrowseComp라는 고난도의 웹 브라우징 기반 사실 탐색 벤치마크에 주입했을 때, 모델의 정확도가 43.5%에서 48.8%로 무려 5.3%p나 절대적으로 향상되었다는 것이다.38

이러한 교차 도메인 성능 향상은 EvoSkill이 발견한 스킬이 단순히 훈련 데이터의 정답 패턴을 암기한 것이 아니라, "답변을 내리기 전에 가능한 모든 정보를 철저하게 검색하고 교차 검증한다"는 인간 전문가의 범용적인 인지적 전략(Cognitive Strategy)을 추상화하여 절차적 코드로 포획했음을 강력히 시사한다.38 이는 에이전트의 최적화가 프롬프트 수준의 미세 조정을 넘어, 스킬 수준(Skill-level)에서 이루어질 때 훨씬 더 강력하고 이식 가능한(Transferable) 형태로 역량 부트스트래핑이 일어남을 증명한다.38

| 특성 | 파라미터 기반의 인지 모델 (Traditional LLM) | 모듈형 명시적 자가 진화 에이전트 (EvoSkill, AutoSkill) |
| :---- | :---- | :---- |
| **지식의 본질과 형태** | 신경망 가중치 내에 분포된 암묵적 표현 | 버전 관리 시스템(Git)에 의해 관리되는 명시적 코드 및 텍스트 파일 |
| **적응 메커니즘** | 지도 학습이나 강화 학습을 통한 그래디언트 업데이트 | 실패 궤적 분석을 통한 절차적 코드 재작성 및 런타임 주입 |
| **오류 수정 가능성** | 내부 블랙박스 특성으로 인해 특정 기능의 디버깅 불가 | 개별 스킬 파일 단위로 인간의 직접 열람, 편집 및 격리 디버깅 가능 |
| **도메인 간 지식 전이** | 파인튜닝 시 파국적 망각 위험 상존, 롤백 어려움 | 특정 스킬 모듈을 그대로 추출하여 다른 환경에 제로샷 주입 가능 |

## **7\. 특수 도메인에서의 자가 진화와 제어 환경의 무한 확장**

능력 주입 및 진화형 에이전트 아키텍처는 일상적인 텍스트 생성이나 단순 코딩의 영역을 넘어, 복잡한 의료 진단과 범용 컴퓨터 제어라는 고도의 특수 도메인으로까지 그 영향력을 확장하고 있다. 이들 시스템은 시뮬레이션 환경 내에서 수많은 가상적 상호작용을 거치며 자신의 전문성을 스스로 부트스트래핑한다.

### **7.1. Agent Hospital: 시뮬레이션 기반의 전문 지식 진화**

의료 분야는 환자의 증상, 병력, 검사 결과를 종합적으로 분석해야 하는 고도의 논리적 추론이 요구된다. Agent Hospital 프레임워크는 단순히 의학 서적 코퍼스를 검색하는 RAG 기반 시스템을 넘어, 의사 역할을 수행하는 다중 에이전트들이 상호작용하는 대규모 시뮬레이션 환경을 구축하였다.39

이 환경 내에서 의사 에이전트들은 지속적으로 가상 환자를 진료하며, 다중 에이전트 간의 임상 토론(Multi-agent discussion), 연쇄적 추론(Chain-of-thought) 메커니즘을 통해 초기 진단의 오류를 수정해 나간다.40 에이전트가 진료한 환자들의 기록과 성공적인 진단 궤적(Trajectory)은 경험 데이터베이스로 축적되며, 시스템은 이 기록을 활용하여 의료 에이전트의 추론 프롬프트를 자율적으로 강화하고 지식 기반을 지속적으로 갱신한다.39 이 진화 메커니즘의 결과로, 약 1만 명의 가상 환자를 진료하는 과정을 거친 진화형 의사 에이전트(Evolved Doctor Agent)는 호흡기 질환 등을 다루는 현실 세계의 메디컬 벤치마크(MedQA) 테스트에서 93.06%라는 최첨단(State-of-the-Art)의 높은 정확도를 달성하였다.41 이는 가상 시뮬레이션 공간에서 에이전트 스스로 부트스트래핑한 임상적 경험이 실제 세계의 복잡한 의학적 과제 해결에 직접적으로 전이될 수 있음을 증명한 획기적인 사례이다.

### **7.2. Cradle: 범용 컴퓨터 제어(GCC) 시나리오로의 인터페이스 확장**

대다수의 기존 에이전트들은 소프트웨어를 제어하기 위해 시스템마다 다르게 설계된 특수한 API 문서나 텍스트 기반의 인터페이스 환경에 맞추어 개별적으로 코드를 수정해야 하는 이식성의 한계를 지니고 있었다.19 이를 극복하기 위해 제안된 Cradle 프레임워크는 에이전트가 소프트웨어와 상호작용하는 방식을 인간과 완벽하게 동일한 조건, 즉 시각적 모니터 스크린샷을 입력받고 마우스 및 키보드 조작을 출력하는 '범용 컴퓨터 제어(General Computer Control, GCC)' 모델로 재정의하였다.3

Cradle 아키텍처는 에이전트의 능력을 지원하기 위해 고도로 모듈화된 6개의 시스템(정보 수집, 자기 성찰, 태스크 추론, 스킬 큐레이션, 행동 계획, 메모리)을 갖추고 있다.3 특히 '스킬 큐레이션(Skill Curation)' 모듈은 기초 대형 다중모달 모델(LMM, 예: GPT-4o)의 시각 분석 능력과 텍스트 임베딩 모델(예: text-embedding-ada-002)을 결합하여, 현재 화면 상태에 가장 적합한 과거의 조작 스킬을 유사도 매칭을 통해 실시간으로 검색하여 주입한다.3 나아가 '자기 성찰(Self-Reflection)' 모듈을 통해 에이전트는 이전 행동의 화면 변화를 분석하여 성공과 실패를 평가하고, 실패 시 마우스 좌표나 키 입력 타이밍을 스스로 보정하는 능력을 획득한다.3 이러한 포괄적인 스킬 획득 메커니즘을 통해 Cradle 에이전트는 복잡한 오픈월드 게임(예: Red Dead Redemption 2)의 40분 길이 서사 미션을 외부 API 없이 완료하거나, 이미지 편집 프로그램이나 웹 브라우저 등 일상적 애플리케이션들을 통달하는 놀라운 범용 조작 역량을 입증하였다.19

## **8\. 자가 진화 에이전트의 구조적 프레임워크와 ASI를 향한 전망**

2025년과 2026년에 걸쳐 이루어진 자가 진화형 AI 에이전트(Self-Evolving AI Agents)에 관한 종합적인 최신 문헌 조사 연구들은, 현재의 스킬 주입과 부트스트래핑 기술이 인공지능 연구의 궁극적 목표인 자율적이고 지속 가능한 '평생 생애 주기 시스템(Lifelong Agentic Systems)'으로 도약하기 위한 거대한 패러다임 전환의 시작점에 불과함을 시사한다.4

### **8.1. 진화 시스템의 4대 핵심 구성 요소**

자가 진화 아키텍처는 정적인 단방향 추론이 아니라, 다중 구성 요소 간의 닫힌 루프(Closed-loop) 내에서 피드백과 메타 인지를 통해 지속적인 최적화를 수행하는 통일된 개념적 프레임워크를 따른다.5

1. **시스템 입력 (System Inputs):** 사용자의 근본적인 목표, 사용 가능한 컴퓨팅 자원 및 토큰 예산, 초기 제약 조건 등 에이전트가 최적화를 수행해야 하는 초기 경계 조건이다.6  
2. **에이전트 시스템 (Agent System):** 최적화와 진화의 대상이 되는 핵심 코어이다. 기초가 되는 LLM 엔진뿐만 아니라, 앞서 서술한 절차적 스킬 라이브러리, 계층화된 장기 메모리 뱅크, 다중 에이전트 간의 통신 워크플로우 토폴로지 등이 모두 포괄적으로 포함된다.6  
3. **환경 (Environment):** 물리 시뮬레이터, 코드 샌드박스, 웹 브라우저 등 에이전트의 행동 결과(예: 코드가 버그 없이 컴파일되었는가, 비행기 티켓이 성공적으로 예약되었는가)에 대한 실측 데이터(Ground Truth)를 제공하는 관찰 공간이다.6  
4. **최적화기 (Optimisers / Meta-Brain):** 시스템의 진화를 주도하는 상위 계층의 메타 시스템이다. 환경으로부터 반환된 복잡한 로그와 성찰 데이터를 분석하여 에이전트 시스템 내부의 프롬프트 구조, 스킬 코드, 메모리 검색 전략을 실질적으로 재작성하고 업데이트하는 결정적 역할을 수행한다.6

### **8.2. 다중 에이전트 시스템 진화의 핵심 난제: 신용 할당 딜레마**

초지능 시스템(Artificial Super Intelligence, ASI)으로 나아가는 과정에서 현재 자가 진화 에이전트가 극복해야 할 가장 큰 기술적 난관 중 하나는 '신용 할당(Credit Assignment) 문제'이다.4 장기 실행(Long-horizon) 시나리오나 수십 개의 스킬이 복잡하게 얽혀 있는 다중 에이전트 워크플로우에서 최종적으로 태스크가 실패했을 경우, 과연 어떤 에이전트의 발언, 어떤 프롬프트의 특정 문구, 또는 라이브러리 내 어느 스킬 코드의 단 한 줄이 근본적인 실패의 원인인지를 정확히 식별해 내는 것은 통계적으로 매우 복잡한 인과 추론 과제이다.4

이러한 신용 할당 딜레마로 인해, 개별 모듈(예: 특정 스킬 코드 하나)에만 국한하여 최적화를 수행하면 시스템이 국소 최적점(Local Optima)에 빠지거나 다른 모듈과의 호환성이 깨지는 문제가 발생한다.46 반대로, 전체 시스템 프롬프트나 에이전트 구조에 대해 거시적인 블랙박스 최적화를 시도하면, 한 요소의 수정이 기존에 잘 작동하던 다른 기능들까지 불안정하게 만드는 연쇄적인 퇴행(Regression) 현상이 발생한다.46

결과적으로, 향후 자가 진화 아키텍처 연구의 지향점은 단순히 에이전트의 개별 도구 문제 해결 능력(Task-level Performance)을 향상시키는 데 머물지 않고, 에이전트 자신이 "어떻게 환경에 더 잘 적응하고 탐색할 수 있는가"에 대한 메타 인지적 전략(Meta-evolution of strategy prompts) 자체를 진화시키는 '공진화(Co-evolution)' 패러다임에 집중될 것이다.45 즉, 개방형 시스템(Open-ended Systems)에서 실패와 경험을 증류(Experience Distillation)하여 시맨틱 공간에 영구적으로 통합하고, 복잡한 교차 도메인 지식 전이(Cross-domain consolidation)를 유기적으로 수행할 수 있는 강건한 평생 학습 에이전트로 도약할 것으로 예측된다.45

## **9\. 결론**

인공지능 에이전트 모델의 발전은 과거 기초 언어 모델의 가중치 내부에 은닉된 암묵적 지식을 활용하는 방식에서 벗어나, 실행 환경에서 역동적으로 지식을 획득하고 외재화하는 자율적이고 지속 가능한 평생 생애 주기 시스템으로 급격하게 진화하고 있다.45

에이전트가 단일 컨텍스트 윈도우의 제약과 파국적 망각이라는 구조적 한계를 극복하기 위해서는, 텍스트 형태의 단순한 장기 기억을 넘어서는 절차적 지식(Procedural Knowledge)의 축적이 필수적이다.13 이를 해결하는 가장 진보된 형태의 점진적 능력 주입 방식은, 인간의 런타임 환경과 유사하게 컨텍스트 압축 직전에 핵심 상태 스냅샷을 명시적으로 삽입하거나, 엔터프라이즈 미들웨어를 통해 거대한 보안 및 도메인 스킬 매트릭스 중 필요한 기능만을 적재적소에 동적 호출(Progressive Skill Disclosure)하는 컨텍스트 엔지니어링 기술을 포함한다.8

나아가, LATM 프레임워크나 BLAZER의 시뮬레이션 기반 데이터 합성 기법과 같이, 강력한 추론 능력을 가진 모델이 가벼운 모델이나 로봇 정책을 제어하기 위한 맞춤형 도구를 자체적으로 합성하고 검증해 내는 능력 부트스트래핑(Capability Bootstrapping)은 에이전트 시스템에 있어 인간의 개입을 배제한 완벽한 자율 학습 체계를 완성하고 있다.18

특히 AutoSkill이나 Voyager, EvoSkill과 같은 최근의 연구들은, 에이전트가 실패한 궤적과 상호작용 경험을 모호한 벡터로 치환하는 대신 버전 관리가 가능한 마크다운(SKILL.md)이나 실행 가능한 소프트웨어 코드의 형태로 외재화(Externalization)함으로써 지식을 완전히 재사용 가능한 독립적 자산으로 승격시켰다.10 이는 에이전트의 진화가 블랙박스 최적화의 굴레를 벗어나, 인간 엔지니어의 통제 및 편집이 가능하고 심지어 타 시스템과 거래할 수 있는 개방형 행동 생태계(Open-source Behavior Ecosystem)로 도약하고 있음을 시사한다.11

결론적으로, 인공지능 에이전트의 점진적 능력 주입과 자가 진화 아키텍처는 에이전트가 사전에 주입된 지식을 단순히 인출하는 정적 시스템에서 벗어나, 끊임없이 변화하는 미지의 세계를 능동적으로 개척하고 도구를 발명하며 스스로의 인지 구조를 재설계하는 자율적 초지능 시스템(ASI)으로 나아가는 가장 확고한 기술적 토대이다.

#### **참고 자료**

1. AI Agent Systems: Architectures, Applications, and Evaluation \- arXiv, 3월 14, 2026에 액세스, [https://arxiv.org/html/2601.01743v1](https://arxiv.org/html/2601.01743v1)  
2. AI Agents vs. Agentic AI: A Conceptual Taxonomy, Applications and Challenges \- arXiv, 3월 14, 2026에 액세스, [https://arxiv.org/html/2505.10468v1](https://arxiv.org/html/2505.10468v1)  
3. \[Literature Review\] Cradle: Empowering Foundation Agents Towards General Computer Control \- Moonlight, 3월 14, 2026에 액세스, [https://www.themoonlight.io/en/review/cradle-empowering-foundation-agents-towards-general-computer-control](https://www.themoonlight.io/en/review/cradle-empowering-foundation-agents-towards-general-computer-control)  
4. A Survey of Self-Evolving Agents \- OpenReview, 3월 14, 2026에 액세스, [https://openreview.net/pdf/3345d492f049f49353081001b10c99e2d7124cc5.pdf](https://openreview.net/pdf/3345d492f049f49353081001b10c99e2d7124cc5.pdf)  
5. A Comprehensive Survey of Self-Evolving AI Agents: A New Paradigm Bridging Foundation Models and Lifelong Agentic Systems \- Hugging Face, 3월 14, 2026에 액세스, [https://huggingface.co/papers/2508.07407](https://huggingface.co/papers/2508.07407)  
6. Self-Evolving Agents — II \- by Lince Mathew \- Medium, 3월 14, 2026에 액세스, [https://medium.com/@linz07m/self-evolving-agents-ii-1551b6fb3bd2](https://medium.com/@linz07m/self-evolving-agents-ii-1551b6fb3bd2)  
7. SELF-GENERATED IN- CONTEXT EXAMPLES FOR LOW-RESOURCE GPU DSL KERNELS \- OpenReview, 3월 14, 2026에 액세스, [https://openreview.net/pdf/b22368035e308a5700d17b71d6f55b76e5dd41b1.pdf](https://openreview.net/pdf/b22368035e308a5700d17b71d6f55b76e5dd41b1.pdf)  
8. Effective harnesses for long-running agents \- Anthropic, 3월 14, 2026에 액세스, [https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)  
9. AutoSkill: Experience-Driven Lifelong Learning via Skill Self-Evolution \- arXiv, 3월 14, 2026에 액세스, [https://arxiv.org/html/2603.01145v1](https://arxiv.org/html/2603.01145v1)  
10. Voyager | An Open-Ended Embodied Agent with Large Language ..., 3월 14, 2026에 액세스, [https://voyager.minedojo.org/](https://voyager.minedojo.org/)  
11. sentient-agi/EvoSkill: EvoSkill — An open-source ... \- GitHub, 3월 14, 2026에 액세스, [https://github.com/sentient-agi/EvoSkill](https://github.com/sentient-agi/EvoSkill)  
12. A Survey of Self-Evolving Agents What, When, How, and Where to Evolve on the Path to Artificial Super Intelligence \- arXiv.org, 3월 14, 2026에 액세스, [https://arxiv.org/html/2507.21046v4](https://arxiv.org/html/2507.21046v4)  
13. SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks \- arXiv.org, 3월 14, 2026에 액세스, [https://arxiv.org/html/2602.12670v1](https://arxiv.org/html/2602.12670v1)  
14. VOYAGER: An Open-Ended Embodied Agent with Large Language Models \- arXiv.org, 3월 14, 2026에 액세스, [https://arxiv.org/pdf/2305.16291](https://arxiv.org/pdf/2305.16291)  
15. What is Catastrophic Forgetting? \- IBM, 3월 14, 2026에 액세스, [https://www.ibm.com/think/topics/catastrophic-forgetting](https://www.ibm.com/think/topics/catastrophic-forgetting)  
16. Effective context engineering for AI agents \- Anthropic, 3월 14, 2026에 액세스, [https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)  
17. Agent RuleZ: A Deterministic Policy Engine for AI Coding Agents \- Medium, 3월 14, 2026에 액세스, [https://medium.com/@richardhightower/agent-rulez-a-deterministic-policy-engine-for-ai-coding-agents-9489e0561edf](https://medium.com/@richardhightower/agent-rulez-a-deterministic-policy-engine-for-ai-coding-agents-9489e0561edf)  
18. Daily Papers \- Hugging Face, 3월 14, 2026에 액세스, [https://huggingface.co/papers?q=large%20language%20models](https://huggingface.co/papers?q=large+language+models)  
19. Cradle: Empowering Foundation Agents Towards General Computer Control \- Nanyang Technological University, 3월 14, 2026에 액세스, [https://personal.ntu.edu.sg/boan/papers/ICML25\_Cradle.pdf](https://personal.ntu.edu.sg/boan/papers/ICML25_Cradle.pdf)  
20. (PDF) Large Language Models as Tool Makers \- ResearchGate, 3월 14, 2026에 액세스, [https://www.researchgate.net/publication/371124051\_Large\_Language\_Models\_as\_Tool\_Makers](https://www.researchgate.net/publication/371124051_Large_Language_Models_as_Tool_Makers)  
21. Solving Reasoning Problems with LLMs in 2023 | by Zhaocheng Zhu \- Medium, 3월 14, 2026에 액세스, [https://medium.com/data-science/solving-reasoning-problems-with-llms-in-2023-6643bdfd606d](https://medium.com/data-science/solving-reasoning-problems-with-llms-in-2023-6643bdfd606d)  
22. A Pipeline of Neural-Symbolic Integration to Enhance Spatial Reasoning in Large Language Models \- arXiv.org, 3월 14, 2026에 액세스, [https://arxiv.org/html/2411.18564v1](https://arxiv.org/html/2411.18564v1)  
23. Materials science in the era of large language models: a perspective \- RSC Publishing, 3월 14, 2026에 액세스, [https://pubs.rsc.org/en/content/articlehtml/2024/dd/d4dd00074a](https://pubs.rsc.org/en/content/articlehtml/2024/dd/d4dd00074a)  
24. Large Language Models as Tool Makers \- arXiv.org, 3월 14, 2026에 액세스, [https://arxiv.org/pdf/2305.17126](https://arxiv.org/pdf/2305.17126)  
25. BLAZER: Bootstrapping LLM-based Manipulation Agents with Zero-Shot Data Generation, 3월 14, 2026에 액세스, [https://arxiv.org/html/2510.08572v1](https://arxiv.org/html/2510.08572v1)  
26. Overview of BLAZER. Given a set of manipulation tasks τ ∈ T , we use... \- ResearchGate, 3월 14, 2026에 액세스, [https://www.researchgate.net/figure/Overview-of-BLAZER-Given-a-set-of-manipulation-tasks-t-T-we-use-LLM-to-automatically\_fig2\_396373568](https://www.researchgate.net/figure/Overview-of-BLAZER-Given-a-set-of-manipulation-tasks-t-T-we-use-LLM-to-automatically_fig2_396373568)  
27. VoltAgent/awesome-ai-agent-papers \- GitHub, 3월 14, 2026에 액세스, [https://github.com/VoltAgent/awesome-ai-agent-papers](https://github.com/VoltAgent/awesome-ai-agent-papers)  
28. JoySafeter: An enterprise AI Agent Platform—Not just chatting. building、running、testing, and tracing autonomous Agent Teams with visual orchestration... \- GitHub, 3월 14, 2026에 액세스, [https://github.com/jd-opensource/JoySafeter](https://github.com/jd-opensource/JoySafeter)  
29. 7 Types of AI Agent Architecture | Galileo, 3월 14, 2026에 액세스, [https://galileo.ai/blog/ai-agent-architecture](https://galileo.ai/blog/ai-agent-architecture)  
30. A Survey of Self-Evolving Agents: On Path to Artificial Super Intelligence \- arXiv, 3월 14, 2026에 액세스, [https://arxiv.org/html/2507.21046v1](https://arxiv.org/html/2507.21046v1)  
31. A Mine-Blowing Breakthrough: Open-Ended AI Agent Voyager Autonomously Plays 'Minecraft' \- Nvidia, 3월 14, 2026에 액세스, [https://blogs.nvidia.com/blog/ai-jim-fan/](https://blogs.nvidia.com/blog/ai-jim-fan/)  
32. Voyager: An Open-Ended Embodied Agent with Large Language Models \- arXiv, 3월 14, 2026에 액세스, [https://arxiv.org/abs/2305.16291](https://arxiv.org/abs/2305.16291)  
33. Skill Library: Modular Capabilities, 3월 14, 2026에 액세스, [https://www.emergentmind.com/topics/skill-library](https://www.emergentmind.com/topics/skill-library)  
34. Architectural overview of the Mem0 system showing extraction and update... \- ResearchGate, 3월 14, 2026에 액세스, [https://www.researchgate.net/figure/Architectural-overview-of-the-Mem0-system-showing-extraction-and-update-phase-The\_fig2\_396785886](https://www.researchgate.net/figure/Architectural-overview-of-the-Mem0-system-showing-extraction-and-update-phase-The_fig2_396785886)  
35. AutoSkill: Experience-Driven Lifelong Learning via Skill Self-Evolution \- arXiv, 3월 14, 2026에 액세스, [https://arxiv.org/pdf/2603.01145](https://arxiv.org/pdf/2603.01145)  
36. AutoSkill: Experience-Driven Lifelong Learning via Skill Self-Evolution | alphaXiv, 3월 14, 2026에 액세스, [https://www.alphaxiv.org/overview/2603.01145](https://www.alphaxiv.org/overview/2603.01145)  
37. AutoSkill: Experience-Driven Lifelong Learning via Skill Self-Evolution (Mar 2026), 3월 14, 2026에 액세스, [https://www.youtube.com/watch?v=PRmSkMJef1c](https://www.youtube.com/watch?v=PRmSkMJef1c)  
38. EvoSkill: Automated Skill Discovery for Multi-Agent Systems \- arXiv, 3월 14, 2026에 액세스, [https://arxiv.org/html/2603.02766v1](https://arxiv.org/html/2603.02766v1)  
39. (PDF) MDTeamGPT: A Self-Evolving LLM-based Multi-Agent Framework for Multi-Disciplinary Team Medical Consultation \- ResearchGate, 3월 14, 2026에 액세스, [https://www.researchgate.net/publication/389947634\_MDTeamGPT\_A\_Self-Evolving\_LLM-based\_Multi-Agent\_Framework\_for\_Multi-Disciplinary\_Team\_Medical\_Consultation](https://www.researchgate.net/publication/389947634_MDTeamGPT_A_Self-Evolving_LLM-based_Multi-Agent_Framework_for_Multi-Disciplinary_Team_Medical_Consultation)  
40. MedAgentSim: Self-Evolving Multi-Agent Simulations for Realistic Clinical Interactions \- MICCAI, 3월 14, 2026에 액세스, [https://papers.miccai.org/miccai-2025/paper/2575\_paper.pdf](https://papers.miccai.org/miccai-2025/paper/2575_paper.pdf)  
41. A Simulacrum of Hospital with Evolvable Medical Agents \- arXiv.org, 3월 14, 2026에 액세스, [https://arxiv.org/html/2405.02957v1](https://arxiv.org/html/2405.02957v1)  
42. Self-Evolving Multi-Agent Simulations for Realistic Clinical Interactions \- arXiv.org, 3월 14, 2026에 액세스, [https://arxiv.org/html/2503.22678v1](https://arxiv.org/html/2503.22678v1)  
43. (PDF) Cradle: Empowering Foundation Agents Towards General Computer Control, 3월 14, 2026에 액세스, [https://www.researchgate.net/publication/383311855\_Cradle\_Empowering\_Foundation\_Agents\_Towards\_General\_Computer\_Control](https://www.researchgate.net/publication/383311855_Cradle_Empowering_Foundation_Agents_Towards_General_Computer_Control)  
44. Towards General Computer Control: A Multimodal Agent for Red Dead Redemption II as a Case Study \- arXiv, 3월 14, 2026에 액세스, [https://arxiv.org/html/2403.03186v2](https://arxiv.org/html/2403.03186v2)  
45. Self-Evolving AI Agents \- Emergent Mind, 3월 14, 2026에 액세스, [https://www.emergentmind.com/topics/self-evolving-ai-agent](https://www.emergentmind.com/topics/self-evolving-ai-agent)  
46. EvoTool: Self-Evolving Tool-Use Policy Optimization in LLM Agents via Blame-Aware Mutation and Diversity-Aware Selection \- arXiv, 3월 14, 2026에 액세스, [https://arxiv.org/html/2603.04900v1](https://arxiv.org/html/2603.04900v1)  
47. ai-agent-papers/lectures/2025\_trend.md at main \- GitHub, 3월 14, 2026에 액세스, [https://github.com/masamasa59/ai-agent-papers/blob/main/lectures/2025\_trend.md](https://github.com/masamasa59/ai-agent-papers/blob/main/lectures/2025_trend.md)  
48. Bootstrapping Cognitive Agents with a Large Language Model \- arXiv.org, 3월 14, 2026에 액세스, [https://arxiv.org/html/2403.00810v1](https://arxiv.org/html/2403.00810v1)