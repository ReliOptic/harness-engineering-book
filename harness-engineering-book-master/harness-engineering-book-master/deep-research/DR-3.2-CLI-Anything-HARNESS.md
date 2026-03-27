# **DR-3.2Ch.3 HKUDS CLI-Anything 프로젝트의 HARNESS.md 심층 분석 및 에이전트 네이티브 인터페이스 패러다임 연구**

대규모 언어 모델(LLM)을 기반으로 하는 자율형 인공지능 에이전트의 급격한 발전은 컴퓨팅 시스템과의 상호작용 패러다임을 근본적으로 재편하고 있다. 그러나 현대의 컴퓨팅 환경과 대다수의 레거시 애플리케이션은 시각적 인지와 물리적 조작(마우스, 키보드)을 전제로 하는 그래픽 사용자 인터페이스(GUI)를 중심으로 설계되어 왔다. 이러한 인간 중심의 인터페이스는 텍스트를 기반으로 사고하고 명령을 산출하는 AI 에이전트에게 심각한 인지적 오버헤드와 번역의 복잡성을 유발한다. 에이전트가 화면의 픽셀 좌표를 분석하고 DOM(Document Object Model)이나 접근성 트리를 파싱하여 애플리케이션을 제어하려는 기존의 시도들은 본질적으로 높은 지연 시간, 잦은 환각(Hallucination), 그리고 시스템 업데이트 시 쉽게 파손되는 취약성을 드러냈다.

이러한 인간-기계 인터페이스의 근본적인 불일치(Mismatch)를 해소하기 위해 등장한 혁신적인 이니셔티브가 바로 홍콩대학교 데이터 사이언스 연구소(HKUDS)가 주도하는 'CLI-Anything' 프로젝트이다. 이 프로젝트는 "모든 소프트웨어를 에이전트 네이티브(Agent-Native)로 만든다"는 거대한 비전을 표방하며, 세상에 존재하는 복잡한 GUI 소프트웨어들을 에이전트가 직접적으로 이해하고 제어할 수 있는 명령줄 인터페이스(CLI) 형태로 래핑(Wrapping)하는 범용적 프레임워크를 제안한다.1 GIMP, Blender, LibreOffice, Audacity, OBS Studio와 같은 방대하고 복잡한 프로덕션 레벨의 소프트웨어들이 이 프레임워크를 통해 성공적으로 에이전트의 제어 영역 안으로 편입되었다.2

CLI-Anything 아키텍처의 철학과 기술적 근간은 프로젝트 내부에 존재하는 HARNESS.md라는 핵심 방법론 명세서(Methodology Spec)에 고스란히 담겨 있다.2 이 문서는 에이전트가 소프트웨어와 소통하기 위해 생성되는 접점인 '하네스(Harness)'의 구조, 설계 원칙, 구현 절차, 그리고 엄격한 검증 방법론을 규정하는 마스터플랜 역할을 수행한다.2 본 보고서는 HKUDS CLI-Anything 프로젝트의 HARNESS.md에 명시된 Harness의 정의, 아키텍처 구현 원칙, 테스트 및 검증 방법론을 매우 심층적으로 분석한다. 나아가, 이를 관련 문헌 및 지침서(이하 '이 책')에서 정의하는 전통적인 AI 에이전트 하네스 개념과 비교 분석함으로써, 에이전트-환경 상호작용 설계 관점에서 파생되는 2차적, 3차적 파급 효과와 거시적 통찰을 도출한다.

## **대상 중심적(Target-Centric) 패러다임: HARNESS.md의 하네스 정의**

소프트웨어 공학, 테스트 자동화, 그리고 최신 AI 에이전트 생태계에서 'Harness(하네스)'라는 용어는 사용되는 맥락에 따라 그 의미가 매우 다층적으로 변주된다. 그러나 CLI-Anything 프로젝트의 HARNESS.md는 하네스를 '인간과 AI 에이전트 모두를 위한 범용적 인터페이스(Universal interface for both humans and AI agents)'라는 단일하고도 강력한 개념으로 재정의한다.2 이는 하네스를 단순히 에이전트의 코드를 실행하기 위한 샌드박스나 테스트 도구로 보는 시각을 넘어, 복잡한 소프트웨어의 기저 기능을 에이전트가 본질적으로 소화할 수 있는 원자적(Atomic)이고 결정론적인(Deterministic) 언어로 번역하는 '양방향 어댑터 계층(Bi-directional adapter layer)'으로 규정함을 의미한다.4

이러한 철학적 기반 위에서 HARNESS.md는 CLI-Anything 하네스가 반드시 충족해야 할 여섯 가지의 핵심 속성을 명확하게 제시하고 있다.2

첫째, 구조화 및 결합성(Structured & Composable)이다. 텍스트 기반의 명령어는 대규모 언어 모델의 자연어 생성 및 추론 형식과 완벽하게 일치한다.2 에이전트는 복잡한 GUI 메뉴 트리를 탐색할 필요 없이, 여러 개의 단일 텍스트 명령어를 유닉스 파이프라인(Unix Pipeline)처럼 결합하여 복잡한 다단계 워크플로우를 구성할 수 있다. 이는 에이전트의 사고 과정(Chain of Thought)을 실행 가능한 코드 체인으로 직접 치환할 수 있음을 의미하며, 실행 계획의 수립과 적용 사이의 인지적 마찰을 최소화한다.

둘째, 경량성 및 범용성(Lightweight & Universal)이다. CLI 하네스는 무거운 시각적 렌더링 엔진이나 복잡한 의존성 라이브러리를 요구하지 않으며, 운영체제의 터미널 셸 위에서 최소한의 오버헤드로 작동하도록 설계되었다.2 하네스는 디렉토리 구조상 /root/cli-anything/\<software\>/agent-harness와 같이 대상 소프트웨어별로 철저히 독립된 모듈로 생성된다.3 이는 대상 소프트웨어의 핵심 비즈니스 로직이나 바이너리를 훼손하지 않고 외부에서 API 호출이나 서브프로세스 형태로 기능을 안전하게 주입 및 제어하는 비침투적(Non-invasive) 래퍼 구조를 보장한다.

셋째, 자기 서술적(Self-Describing) 특성이다. 하네스로 래핑된 모든 명령어는 \--help 플래그를 통해 대상 기능의 설명, 사용 가능한 인자(Arguments), 제약 사항 등을 포함한 자동화된 문서를 반환한다.2 이 특성은 에이전트 생태계에서 매우 결정적인 역할을 한다. 에이전트는 사전 학습(Pre-training)이나 컨텍스트 창(Context Window) 내에 도구의 모든 사용법을 하드코딩받을 필요 없이, 런타임에 스스로 \--help를 호출하여 낯선 도구의 사용법을 발견하고 학습할 수 있다.2 이는 모델의 한정된 토큰 리소스를 절약하면서도, 소프트웨어 업데이트로 인한 명령어 변경에 유연하게 대처할 수 있는 자가 치유적(Self-healing) 상호작용의 기반이 된다.

넷째, 입증된 성공 사례(Proven Success)와 범용적 호환성이다. CLI 기반의 텍스트 프로토콜은 이미 컴퓨터 과학의 역사에서 가장 안정적인 인터페이스로 검증되었다. Claude Code와 같은 최상위 코드 에이전트들은 매일 수천 건의 실제 워크플로우를 CLI를 통해 성공적으로 처리하고 있으며, 이러한 통계적 신뢰성은 CLI-Anything 하네스가 환상이나 실험실 수준의 아이디어가 아닌 프로덕션 레벨의 해답임을 증명한다.2

다섯째, 에이전트 최우선 설계(Agent-First Design) 원칙에 입각한 엄격한 JSON 출력 통제이다. 인간을 위한 CLI는 종종 가독성을 위해 색상 코드, 포맷팅된 표, 진행률 표시줄(Progress bar) 등 다양한 비구조적 텍스트를 출력한다. 그러나 이러한 자유 형식의 텍스트는 에이전트가 결과를 파싱하고 상태를 추적할 때 정규표현식 오류나 의미론적 모호성(Ambiguity)을 유발한다. CLI-Anything 하네스는 실행 결과를 기계 판독이 가능한 완벽하게 구조화된 JSON 형식으로만 반환하도록 강제함으로써, 에이전트가 파싱 논리에 토큰을 낭비하지 않고 즉각적으로 다음 추론 단계로 넘어갈 수 있도록 돕는다.2

여섯째, 결정론적이며 신뢰할 수 있는 작동(Deterministic & Reliable)이다. 동일한 상태에서 동일한 명령을 내렸을 때 시스템은 반드시 동일한 JSON 결과를 반환해야 한다.2 대규모 언어 모델은 본질적으로 확률적(Probabilistic) 텍스트 생성기이기 때문에 자체적인 환각 현상에 취약하다. 이를 보완하기 위해 시스템의 제어 계층인 하네스만큼은 극도로 결정론적이어야 하며, 이 견고한 기반 위에서 에이전트는 변수 없는 예측 가능한 계획을 수립할 수 있다.

이러한 핵심 속성들은 CLI-Anything이 지향하는 '에이전트 네이티브'의 철학적 정의를 명확히 보여준다. 아래 표는 CLI-Anything의 하네스 정의와 그로부터 파생되는 에이전트 시스템 레벨의 2차적 파급 효과를 구조화한 것이다.

| 하네스 핵심 속성 (HARNESS.md 기준) | 기술적 구현 메커니즘 | 에이전트 생태계에 미치는 2차적 파급 효과 (Implications) |
| :---- | :---- | :---- |
| **구조화 및 결합성** | 단위 명령어의 모듈화 및 파이프라인 연계 지원 | 복잡한 GUI 워크플로우를 선형적인 텍스트 추론(Chain of Thought) 과정으로 치환 가능 |
| **경량성 및 범용성** | 비침투적 CLI 래퍼, 시스템 표준 입출력(Stdio) 활용 | 특정 프레임워크나 에이전트 플랫폼에 종속되지 않는 범용적 도구 생태계 구축 |
| **자기 서술성 (--help)** | 런타임 도움말 동적 생성 및 반환 메커니즘 | 사전 훈련 없는 제로샷(Zero-shot) 도구 발견 및 자율 학습 가능, 프롬프트 토큰 절약 |
| **에이전트 최우선 설계** | 모든 실행 결과를 엄격한 구조의 JSON 형식으로 출력 | 로그 파싱 과정의 모호성 제거, 정규표현식 오류 및 텍스트 환각 원천 차단 |
| **결정론적 신뢰성** | 상태 모델 기반의 예측 가능한 명령어 실행 보장 | 확률적 언어 모델의 한계를 보완하여, 다단계 계획 수립 시 누적되는 오류 확률 극소화 |

## **아키텍처 및 구현 원칙: 7단계 자율 생성 파이프라인과 비파괴적 진화**

CLI-Anything 프로젝트의 HARNESS.md는 기존 소프트웨어를 에이전트 네이티브 CLI로 변환하는 과정을 단순히 스크립트를 작성하는 수작업이 아니라, 에이전트 스스로가 주도하여 도구를 생성해 내는 자동화된 7단계 아키텍처 파이프라인으로 규정하고 있다.2 이는 소프트웨어 분석부터 배포에 이르는 전체 소프트웨어 생명주기(SDLC)를 단일한 /cli-anything 명령어 호출로 압축하는 놀라운 공학적 성취를 보여준다.2 이 파이프라인은 Claude Code, OpenCode, Codex, Qodercli 등 다양한 플랫폼 위에서 동작하며, 에이전트의 자율적 도구 생성 능력을 극대화한다.2

가장 초기 단계인 **분석(Analyze)** 단계에서는 에이전트가 대상 소프트웨어(예: 깃허브 리포지토리 또는 로컬 설치 경로)의 소스 코드와 API 문서를 스캔하여, 기존 GUI에서 인간이 마우스 클릭이나 단축키로 수행하던 작업들을 내부적인 기반 API 호출로 매핑(Mapping)하는 심층적인 구조 분석을 수행한다.2 이 과정은 타겟 애플리케이션의 메모리 구조와 이벤트 루프를 에이전트가 이해할 수 있는 논리적 인터페이스로 추상화하는 역공학(Reverse Engineering)의 성격을 지닌다.

이어지는 **설계(Design)** 단계는 분석된 API들을 바탕으로 논리적인 명령어 그룹(Command Groups)을 아키텍처링하는 과정이다.2 여기서 가장 중요한 아키텍처 원칙은 '상태 모델(State Model)'의 구축이다. 멀티미디어 편집기인 GIMP나 3D 렌더링 도구인 Blender와 같은 소프트웨어는 단순한 1회성 명령어(예: ls, grep)와 달리, 내부에 복잡한 프로젝트 상태(레이어, 렌더링 그래프, 타임라인 등)를 유지하는 거대한 상태 기계(State Machine)이다.3 따라서 하네스는 에이전트가 애플리케이션의 현재 상태를 조회하고 연속적으로 작업을 이어갈 수 있도록 추상화된 상태 추적 모델과 그에 맞는 JSON 출력 포맷을 설계해야 한다.2

**구현(Implement)** 단계에서는 설계된 아키텍처를 실제 코드로 전환한다. CLI-Anything은 Python 3.10 이상의 환경을 기반으로 하며, CLI 프레임워크인 Click을 활용하여 계층적이고 체계적인 명령어 트리를 빌드한다.2 이 단계의 핵심 구현 원칙 중 하나는 상호작용형 REPL(Read-Eval-Print Loop) 모드의 통합이다.2 REPL은 에이전트가 애플리케이션을 시작한 후 종료하지 않은 상태에서 연속적으로 다수의 명령을 내리고 결과를 피드백받을 수 있는 세션을 제공한다. 더욱 중요한 것은 실행 취소 및 재실행(Undo/Redo) 로직을 하네스 레벨에서 강제한다는 점이다.2 자율형 에이전트는 필연적으로 잘못된 명령을 실행하거나 예상치 못한 결과에 직면하게 되는데, Undo 메커니즘의 존재는 에이전트가 시스템을 영구적으로 파손하지 않고 스스로 상태를 롤백하여 오류를 복구할 수 있는 '회복 탄력성(Resilience)'을 부여한다.

이후의 과정은 소프트웨어의 무결성을 입증하는 **테스트 계획(Plan Tests)** 및 **테스트 작성(Write Tests)**, 그리고 결과를 명세화하는 **문서화(Document)**, 마지막으로 생성된 하네스를 시스템 경로(PATH)에 설치하여 즉시 사용할 수 있도록 패키징하는 **배포(Publish)** 단계로 이어진다.2 이 일련의 과정은 setup.py의 생성까지 포함하여 에이전트가 즉각적으로 새로운 도구를 장착하게 만든다.

초기 파이프라인의 완료 이후, 아키텍처는 정체되지 않고 \*\*선택적 정제(Refine and Improve)\*\*라는 강력한 진화 메커니즘을 지원한다.2 /cli-anything:refine 명령어는 소프트웨어가 본래 지닌 전체 역량(Full capabilities)과 현재 생성된 CLI 하네스가 커버하는 기능(Current CLI coverage) 사이의 간극(Gap analysis)을 정밀하게 분석한다.2 에이전트는 분석 결과 식별된 누락 기능들을 보완하기 위해 새로운 명령어, 단위 테스트, 그리고 문서를 스스로 추가 구현한다.2 이 정제 과정은 기존 코드를 파괴하지 않는 점진적이고 비파괴적인(Incremental and non-destructive) 방식으로 수행되며, 반복적인 실행을 통해 하네스의 커버리지를 100%에 가깝게 지속적으로 확장할 수 있다.2 사용자는 필요에 따라 /cli-anything:refine./gimp "이미지 일괄 처리와 필터 기능에 대한 CLI를 더 추가해줘"와 같이 특정 도메인을 타겟팅하는 집중 정제(Focused refinement) 지시를 내릴 수도 있다.2 이는 에이전트가 도구를 한 번 만들고 끝나는 것이 아니라, 피드백과 요구사항에 따라 도구를 스스로 유지보수하고 성장시키는 '메타 도구화(Meta-tooling)'의 실현을 보여준다.

| 파이프라인 단계 | 핵심 활동 및 수행 메커니즘 | 아키텍처 설계 원칙 및 목적 |
| :---- | :---- | :---- |
| **1\. Analyze** | 소스 코드 스캔, GUI 액션 및 이벤트 루프를 내부 API 호출 로직으로 맵핑 | 블랙박스화된 소프트웨어의 내부 로직을 에이전트가 조작 가능한 추상화 계층으로 전환 |
| **2\. Design** | 명령어 그룹 계층화, 상태 모델(State Model) 설계, 통일된 JSON 출력 포맷 정의 | 복잡한 런타임 상태(프로젝트, 레이어 등)를 에이전트가 추적할 수 있도록 시각화 제거 및 의미론적 재구성 |
| **3\. Implement** | Python Click 기반 CLI 빌드, REPL 모드 활성화, Undo/Redo 로직 강제 적용 | 연속적 세션 지원 및 에이전트의 치명적 오류에 대한 자가 복구 능력(Resilience) 보장 |
| **4\. Plan Tests** | TEST.md 생성, 기능별 단위 테스트 및 복합 E2E 테스트 계획 수립 | 명세 우선(Specification-first) 검증 접근을 통한 구조적 신뢰성 확보 및 목표 설정 |
| **5\. Write Tests** | 포괄적 테스트 스위트 코드 구현 및 실행 검증 | 엣지 케이스 및 예외 상황에 대한 에이전트의 방어적 코드 작성 강제 |
| **6\. Document** | 테스트 결과 및 명령어 커버리지를 TEST.md 및 마크다운 리포트에 지속 반영 | 에이전트 간, 혹은 에이전트-인간 간 컨텍스트 공유 및 영구적 지식 베이스(Source of truth) 구축 |
| **7\. Publish** | setup.py 자동 생성, 의존성 해결 및 시스템 전역(PATH) 설치 | 생성된 하네스를 에이전트의 즉각적인 실행 환경으로 매끄럽게 통합 |
| **\+ Refine (옵션)** | 전체 기능과 CLI 커버리지 간의 갭 분석 후 점진적, 비파괴적 코드 병합 | 지속 가능한 소프트웨어 유지보수 철학 적용, 에이전트의 도구 확장 자율성 부여 |

## **검증 체계와 컨텍스트 엔트로피 제어를 위한 테스트 방법론**

인간 개발자의 개입 없이 코드가 생성되고 실행되는 에이전트 기반 생태계에서 가장 큰 위협은 '환각에 의한 오류의 연쇄 증폭'이다. 잘못된 명령어가 생성되거나 출력 포맷이 어긋나면, 후속 에이전트 워크플로우 전체가 붕괴되는 치명적인 결과가 발생한다. 이러한 위험을 사전에 차단하기 위해 HARNESS.md는 하네스 생성 파이프라인의 절반에 가까운 공수를 테스트와 검증에 할당하는 테스트 주도 개발(Test-Driven Development, TDD) 철학을 극단적으로 채택하고 있다.2

테스트 계획(Plan Tests) 단계에서는 구현된 명령어 아키텍처의 무결성을 입증하기 위해 TEST.md라는 마스터 검증 문서를 자동 생성한다.2 이 문서 내에는 개별 기능과 단일 명령어의 정확성, 인자 처리의 유효성, JSON 출력의 스키마 준수 여부를 검증하는 세밀한 단위 테스트(Unit test) 계획이 기록된다. 나아가, 개별 명령어들이 조합되어 유의미한 작업을 수행할 때 상태 전이가 올바르게 일어나는지를 확인하는 단대단(End-to-End, E2E) 테스트 계획이 포괄적으로 포함된다.2 에이전트는 이 계획에 기반하여 테스트 코드를 직접 작성(Write Tests)하고, 대상 애플리케이션에 대한 자동화된 검증 스위트를 실행한다.2

이러한 엄격한 테스트 방법론이 거둔 성과는 압도적이다. 공개된 프로젝트 이슈 추적 데이터에 따르면, CLI-Anything은 GIMP, Blender, Inkscape, Audacity, LibreOffice, OBS Studio, Kdenlive, Shotcut과 같은 고도의 복잡성을 지닌 8개의 상용 애플리케이션을 대상으로 생성된 하네스에서 무려 1,298개의 테스트를 성공적으로 통과(Passing tests)시켰다.3 이는 생성형 AI가 단순한 스크립트를 짜는 수준을 넘어, 수백만 줄의 코드로 이루어진 프로덕션 레벨의 데스크톱 소프트웨어를 완벽하고 정밀하게 조작할 수 있는 강건한 인터페이스를 구축했음을 입증하는 강력한 지표이다.

더욱 중요한 것은 이러한 테스트 방법론이 에이전트 시스템 특유의 '컨텍스트 엔트로피(Context Entropy)'와 '구조적 표류(Architectural Drift)' 문제를 제어하는 기계적 장치로 작동한다는 점이다. 장시간 실행되는 에이전트는 컨텍스트 창이 길어짐에 따라 초기 설계 원칙을 망각하고 비효율적이거나 일관성 없는 코드를 생성하는 이른바 'AI 슬롭(AI Slop)' 현상에 빠지기 쉽다.6 OpenAI의 Codex 팀 사례에서도 볼 수 있듯, 코드베이스에 '황금 원칙(Golden principles)'을 기계적인 규칙과 강제된 테스트 형태로 인코딩하지 않으면 시스템은 점진적으로 부패한다.6 CLI-Anything의 HARNESS.md는 테스트 결과를 다시 TEST.md 문서에 꼼꼼하게 업데이트하고(Document 단계), 성공한 테스트 명세만을 진실의 원천(Source of truth)으로 삼게 함으로써 에이전트가 환각에 의해 임의로 인터페이스 규격을 변경하는 것을 원천적으로 억제한다.2

특히, 상태가 지속적으로 변하는 소프트웨어 환경에서 문서화된 테스트 마크다운(TEST.md)은 에이전트의 영구적인 기억 장치 역할을 한다. 에이전트가 여러 세션에 걸쳐 작업을 중단하고 재개하더라도, 마크다운 형식으로 텍스트화된 테스트 통과 이력과 상태 정의는 컨텍스트 손실 없이 즉각적으로 시스템의 현재 상태를 재동기화하는 강력한 닻(Anchor)이 된다.7 이는 단순한 품질 보증(QA) 절차를 넘어, AI 에이전트가 복잡한 소프트웨어 환경에서 자율성을 상실하지 않고 목표를 향해 나아가도록 돕는 핵심 항법 장치인 셈이다.

## **패러다임의 충돌: '이 책'의 기존 하네스 정의와 CLI-Anything의 비교 분석**

CLI-Anything의 HARNESS.md가 제시하는 비전의 진정한 혁신성은 기존 관련 문헌이나 개발 지침서(통칭 '이 책' 또는 기존 에이전트 생태계 가이드)에서 통용되던 'Harness'의 개념을 근본적으로 뒤집은 패러다임 전환에 있다. AI 시스템 공학에서 전통적으로 사용되어 온 하네스의 개념과 CLI-Anything이 재정의한 하네스의 철학을 심층적으로 비교하면, 에이전트 아키텍처의 설계 중심축이 어디로 이동하고 있는지 명확하게 파악할 수 있다.

기존 문헌과 생태계, 특히 'Everything Claude Code (ECC)', 'OpenClaw', 'Codex CLI' 등으로 대변되는 주류 에이전트 프레임워크에서 하네스는 철저히 \*\*'에이전트를 감싸는 실행 및 성능 최적화 런타임(Agent harness performance optimization system)'\*\*으로 정의된다.5 예를 들어 ECC v1.8.0 릴리스 노트나 관련 가이드를 살펴보면, 하네스 시스템은 에이전트 내부의 스킬(Skills) 관리, 사전 정의된 본능(Instincts)의 주입, 세션 간 메모리 영속성(Memory persistence) 보장, 보안 검증(AgentShield), 서브에이전트 오케스트레이션, 그리고 평가 루프(Verification loops) 등을 통제하는 거대한 운영체제로 작동한다.5 즉, 기존의 에이전트 하네스는 \*\*'어떻게 하면 에이전트(뇌)의 인지 능력을 강화하고, 컨텍스트 한계를 보완하여, 복잡한 현실 세계의 과제를 잘 풀도록 훈련시키고 지원할 것인가'\*\*에 초점을 맞추었다. 이 과정에서 AGENTS.md, CLAUDE.md, RELAY.MD와 같은 마크다운 파일들은 에이전트가 컨텍스트 붕괴(Context rot)에 빠지지 않도록 작업 내역을 메모리 훅(Hook)을 통해 지속적으로 주입하고 에이전트 간의 통신을 중계하는 역할을 수행한다.9 모델 평가 프레임워크인 'Claw-Eval' 역시 하네스를 언어 모델 자체의 문제 해결 능력을 벤치마킹하고 평가하기 위한 도구로 정의한다.12 더 나아가 DevOps 환경(예: Harness CD)에서는 하네스를 단순한 소프트웨어 빌드 및 컨테이너 배포 파이프라인 플랫폼으로 규정하고 있다.13

이와 대조적으로 CLI-Anything의 HARNESS.md는 아키텍처의 중심축을 에이전트에서 '대상 소프트웨어 환경(Target Environment)'으로 완전히 이동시킨다. CLI-Anything에서 하네스는 에이전트를 감싸는 운영체제가 아니라, \*\*'레거시 소프트웨어를 감싸 에이전트의 언어에 맞게 형태를 변환하는 외부 어댑터 인터페이스(Environment-facing adapter)'\*\*로 재정의된다.2

기존 패러다임이 인간을 위해 설계된 복잡한 GUI나 파편화된 API 환경을 에이전트가 '애써서' 학습하고 극복하게 만들려 했다면(즉, 모델의 추론 능력 향상에 집착했다면), CLI-Anything은 그 접근법 자체가 비효율적이라고 주장한다. 대신 "복잡한 세상을 에이전트가 날것으로 파싱하게 하지 말고, 세상(소프트웨어)의 형태를 에이전트가 숨쉬듯 자연스럽게 소화할 수 있는 CLI와 정제된 JSON 출력으로 깎아내어 제공하자"는 것이 CLI-Anything 하네스의 본질이다.2

이러한 설계 철학의 차이는 시스템의 안정성과 오버헤드 측면에서 극적인 차이를 낳는다. 기존 에이전트 중심 하네스는 에이전트가 복잡한 환경 상태를 모두 기억해야 하므로 막대한 토큰 비용을 소모하며 컨텍스트 로트(Context Rot)와 환각 현상의 위험에 상시 노출된다.7 이를 막기 위해 지속적인 요약, 체크포인트 생성, 모델 라우팅 등 복잡한 기교가 동원된다.5 반면, CLI-Anything 환경에서는 소프트웨어의 상태 관리를 래핑된 하네스 내부의 객체 지향 상태 모델이 전담한다.2 에이전트는 하네스에 텍스트 명령을 던지고, 성공 여부와 현재 상태가 깔끔하게 요약된 JSON 결과만을 수신한다. 언제든 \--help를 통해 도구의 사용법을 다시 물어볼 수 있으므로 단기 기억에 의존할 필요가 대폭 감소한다.2 이는 모델의 지능적 수준(예: GPT-5.4 vs GPT-5.3 Codex)에 크게 구애받지 않고, 상대적으로 가벼운 추론 모델만으로도 복잡한 시스템 통합 워크플로우를 신뢰성 있게 완수할 수 있는 길을 열어준다.11

| 비교 속성 | 기존 에이전트 하네스 (예: Everything Claude Code, OpenClaw, Codex CLI) | CLI-Anything 대상 중심 하네스 (HARNESS.md 기준) |
| :---- | :---- | :---- |
| **개념적 본질** | 에이전트(두뇌)의 실행 능력을 극대화하기 위한 운영체제 및 런타임 환경 | 대상 소프트웨어(환경)의 복잡성을 에이전트의 인지 구조에 맞게 단절하는 어댑터 인터페이스 |
| **적용 타겟** | AI 언어 모델 및 에이전트 (Claude, GPT, Cursor 등) | 물리적 시스템 및 개별 애플리케이션 (GIMP, Blender, OBS, LibreOffice 등) |
| **해결하고자 하는 핵심 문제** | 에이전트의 기억 상실(Context Rot), 스킬 부재, 평가 루프 구성, 에이전트 간 오케스트레이션 한계 | 기존 GUI 소프트웨어의 시각적 파싱 불가능성, 비구조적 로그의 정규식 처리 모호성, 시스템 비결정성 |
| **상태 관리 및 메모리 영속성 주체** | 에이전트 시스템 내부 (메모리 Hook, 지속적인 마크다운 요약, RAG 기반 히스토리 주입) | 대상 소프트웨어를 래핑한 하네스 인스턴스 (상태 기계 추상화 및 REPL 세션 내 유지) |
| **성능 확장 및 유지보수 방식** | 에이전트의 컨텍스트 프롬프트 최적화, 스킬(Skill) 스크립트 핫로드 추가 | refine 명령을 통한 대상 소프트웨어 API 기반의 점진적, 비파괴적 CLI 커버리지 확장 |
| **명령어 및 데이터 파이프라인 형태** | 자연어 지시 → 에이전트 프레임워크 해석 → 범용 터미널 실행 → 자유 형식 텍스트 로그 분석 | 구조화된 파이프라인 명령어 체인 조합 → 타겟 하네스 전달 → 엄격한 규격의 **JSON 출력** 반환 |

## **구현상의 과제와 생태계 확장성**

이러한 혁신적인 설계에도 불구하고, CLI-Anything 프로젝트의 하네스 생태계가 다양한 플랫폼으로 확장되는 과정에서 몇 가지 기술적, 운용상의 과제들이 식별되고 있다.

가장 대표적인 것은 이식성(Portability) 및 경로 종속성 문제이다. 깃허브 리포지토리의 이슈 트래커를 분석한 결과, HARNESS.md, README.md, QUICKSTART.md 등 프로젝트의 주요 문서 곳곳에 /root/cli-anything/과 같은 절대 경로가 하드코딩되어 있는 것이 발견되었다.3 예를 들어, cp \-r /root/cli-anything/cli-anything-plugin \~/.claude/plugins/cli-anything와 같은 설치 명령이나 cd /root/cli-anything/\<software\>/agent-harness와 같은 실행 예제는 특정 리눅스 루트 권한 환경이나 도커(Docker) 컨테이너 내부 환경을 강하게 암시한다.3 이는 다양한 운영체제(macOS, Windows 등) 환경을 구축하고 깃허브 액션(GitHub Actions) 등을 통해 크로스 플랫폼 CI/CD 파이프라인을 구성하려는 일반 사용자나 다른 시스템 통합 시 심각한 호환성 마찰을 일으키는 요인으로 작용한다.16 현재 개발 커뮤니티에서는 이러한 하드코딩된 절대 경로를 시스템 독립적인 상대 경로 및 환경 변수 기반으로 수정하여 하네스의 휴대성을 높이는 작업이 요구되고 있다.3

또한, 플러그인 생태계의 분화에 따른 설정 통합의 과제도 존재한다. CLI-Anything은 Claude Code의 공식 마켓플레이스를 통한 설치(/plugin marketplace add HKUDS/CLI-Anything)를 권장함과 동시에, 실험적으로 OpenCode 환경 지원을 제공하고 있다.2 그러나 OpenCode 환경의 경우 .config/opencode/commands/ 경로로 마크다운 명령어 명세와 HARNESS.md를 직접 복사해야 하는 등, 에이전트 프레임워크마다 상이한 설정 방식과 디렉토리 구조(commands 폴더 유무 등)로 인해 사용자의 수동 개입이 불가피한 엣지 케이스들이 보고되고 있다.2 이러한 설치 파편화는 향후 하네스 생태계가 AnyGen OpenAPI 등 더 넓은 범위로 확장됨에 따라 통합된 패키지 매니저나 표준화된 인스톨러 구성을 통해 해결되어야 할 중요한 아키텍처적 과제이다.2

## **결론 및 거시적 시사점**

종합적으로, HKUDS CLI-Anything 프로젝트의 HARNESS.md는 AI 에이전트 시대에 걸맞은 소프트웨어 상호작용의 새로운 표준 프로토콜을 성공적으로 정립하였다. 인간의 시각과 물리적 상호작용을 위해 설계된 레거시 GUI의 본질적 복잡성을 폐기하고, 소프트웨어를 에이전트의 인지 모델과 완벽하게 일치하는 구조화된 언어(CLI \+ JSON)로 번역해 내는 대상 중심(Target-centric) 하네스 아키텍처는 에이전트 공학의 거대한 패러다임 전환을 의미한다.

자동화된 분석, 상태 모델 기반의 설계, 상호작용형 REPL과 복구 탄력성을 갖춘 구현, TDD 기반의 엄격한 테스트 및 비파괴적 정제 과정을 포함하는 7단계 파이프라인은 복잡한 도구를 에이전트가 자율적으로 생성하고 관리할 수 있음을 입증하였다. 특히 기존 에이전트 하네스 시스템들이 모델의 지능을 보조하기 위한 무거운 런타임 환경 구축에 몰두했던 것과 달리, 환경 자체의 조작 인터페이스를 경량화하고 결정론적으로 개조함으로써 에이전트의 컨텍스트 과부하와 환각 현상을 원천적으로 억제하는 실용적 접근은 시사하는 바가 크다.

비록 경로 종속성이나 생태계 파편화와 같은 초기 구축 과정의 기술적 부채가 일부 관찰되지만, CLI-Anything이 1,298개의 엄격한 E2E 테스트를 거쳐 방대한 프로덕션 애플리케이션들을 에이전트 제어 하에 두었다는 사실은 변함없는 공학적 성과이다. 이러한 하네스 프레임워크가 보편화될 미래의 컴퓨팅 환경에서는, 모든 소프트웨어가 출시와 동시에 에이전트 네이티브 인터페이스를 내장하게 될 것이며, 이는 복수의 특화 에이전트들이 인간의 개입 없이 다양한 데스크톱 애플리케이션과 클라우드 서비스를 거미줄처럼 엮어내며 복합적인 지식 노동을 자율적으로 완수하는 진정한 의미의 초자동화(Hyperautomation) 시대를 가속화할 것이다.

#### **참고 자료**

1. Releases · HKUDS/CLI-Anything \- GitHub, 3월 13, 2026에 액세스, [https://github.com/HKUDS/CLI-Anything/releases](https://github.com/HKUDS/CLI-Anything/releases)  
2. CLI-Anything: Making ALL Software Agent-Native \- GitHub, 3월 13, 2026에 액세스, [https://github.com/HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything)  
3. Docs: Replace hardcoded /root/ paths with portable examples · Issue \#3 · HKUDS/CLI-Anything \- GitHub, 3월 13, 2026에 액세스, [https://github.com/HKUDS/CLI-Anything/issues/3](https://github.com/HKUDS/CLI-Anything/issues/3)  
4. Excellent project ！！some questions · Issue \#44 · HKUDS/CLI-Anything \- GitHub, 3월 13, 2026에 액세스, [https://github.com/HKUDS/CLI-Anything/issues/44](https://github.com/HKUDS/CLI-Anything/issues/44)  
5. GitHub \- affaan-m/everything-claude-code: The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond., 3월 13, 2026에 액세스, [https://github.com/affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code)  
6. Harness engineering: leveraging Codex in an agent-first world | OpenAI, 3월 13, 2026에 액세스, [https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)  
7. Show HN: VS Code Agent Kanban: Task Management for the AI-Assisted Developer, 3월 13, 2026에 액세스, [https://news.ycombinator.com/item?id=47307169](https://news.ycombinator.com/item?id=47307169)  
8. fire17/awesome-stars: Curated List of all my starred repos on github, 3월 13, 2026에 액세스, [https://github.com/fire17/awesome-stars](https://github.com/fire17/awesome-stars)  
9. How to Use Claude Code: A Guide to Slash Commands, Agents, Skills, and Plug-ins, 3월 13, 2026에 액세스, [https://www.producttalk.org/how-to-use-claude-code-features/](https://www.producttalk.org/how-to-use-claude-code-features/)  
10. Hybrid Claude Code / Codex : r/ClaudeCode \- Reddit, 3월 13, 2026에 액세스, [https://www.reddit.com/r/ClaudeCode/comments/1rrp17j/hybrid\_claude\_code\_codex/](https://www.reddit.com/r/ClaudeCode/comments/1rrp17j/hybrid_claude_code_codex/)  
11. Does anyone get why people prefer codex? : r/ClaudeCode \- Reddit, 3월 13, 2026에 액세스, [https://www.reddit.com/r/ClaudeCode/comments/1rm9mpn/does\_anyone\_get\_why\_people\_prefer\_codex/](https://www.reddit.com/r/ClaudeCode/comments/1rm9mpn/does_anyone_get_why_people_prefer_codex/)  
12. Hype \- ML/AI News, 3월 13, 2026에 액세스, [https://hype.replicate.dev/](https://hype.replicate.dev/)  
13. Harness Blog: DevOps, CI/CD Insights, 3월 13, 2026에 액세스, [https://www.harness.io/blog](https://www.harness.io/blog)  
14. Nanobot: Ultra-Lightweight Alternative to OpenClaw | Hacker News, 3월 13, 2026에 액세스, [https://news.ycombinator.com/item?id=46897737](https://news.ycombinator.com/item?id=46897737)  
15. Codex Prompting Guide \- OpenAI for developers, 3월 13, 2026에 액세스, [https://developers.openai.com/cookbook/examples/gpt-5/codex\_prompting\_guide/](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide/)  
16. Actions · HKUDS/CLI-Anything \- GitHub, 3월 13, 2026에 액세스, [https://github.com/HKUDS/CLI-Anything/actions](https://github.com/HKUDS/CLI-Anything/actions)  
17. opencode安装命令有错误· Issue \#35 · HKUDS/CLI-Anything \- GitHub, 3월 13, 2026에 액세스, [https://github.com/HKUDS/CLI-Anything/issues/35](https://github.com/HKUDS/CLI-Anything/issues/35)