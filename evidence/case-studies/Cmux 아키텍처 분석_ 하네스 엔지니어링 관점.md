# **manaflow-ai/cmux 심층 분석: 다중 AI 에이전트 오케스트레이션을 위한 하네스 엔지니어링 아키텍처 및 구현 메커니즘**

## **1\. 서론: AI 에이전트 패러다임의 전환과 하네스 엔지니어링의 대두**

소프트웨어 개발의 근본적인 패러다임이 인간 중심의 수동 코딩에서 대규모 언어 모델(LLM) 기반의 자율형 AI 코딩 에이전트(Autonomous AI Coding Agents)를 활용하는 방향으로 급격히 전환되고 있다. 초기 AI 보조 도구들이 단순히 코드 조각을 자동 완성하거나 단일 프롬프트에 대한 응답을 생성하는 데 그쳤다면, 최근의 AI 에이전트(예: Claude Code, Codex, Amp, Gemini CLI, Cursor Agent 등)는 복잡한 디렉토리 구조를 탐색하고, 다수의 파일을 수정하며, 터미널 명령어를 직접 실행하는 등 자율적인 워크플로우를 수행할 수 있는 수준에 이르렀다.1 그러나 이러한 에이전트의 지능적 능력 향상은 역설적으로 새로운 엔지니어링 위기를 초래했다. 모델의 추론 속도와 코드 생성량은 기하급수적으로 증가한 반면, 인간 개발자가 여러 에이전트의 작업 상태를 동시에 추적하고, 검증하며, 제어할 수 있는 인프라는 그 발전 속도를 따라가지 못했기 때문이다.1

이러한 맥락에서 새롭게 부상한 학문적, 실무적 규율이 바로 '하네스 엔지니어링(Harness Engineering)'이다. 하네스 엔지니어링은 AI 에이전트가 작동하는 환경 전체를 통제하고 관리하는 시스템을 설계하는 것을 의미한다.6 이는 단순히 더 나은 질문을 던지는 프롬프트 엔지니어링(Prompt Engineering)이나 모델이 참조할 데이터를 최적화하는 컨텍스트 엔지니어링(Context Engineering)과는 명확히 구분된다. 하네스 엔지니어링은 에이전트의 행동 반경을 아키텍처 수준에서 제한(Constrain)하고, 필요한 작업 컨텍스트를 시각적, 프로그래밍적으로 제공(Inform)하며, 에이전트의 산출물을 지속적 통합(CI) 도구 등을 통해 검증(Verify)하고, 오류 발생 시 인간의 개입이나 자동화된 피드백 루프를 통해 이를 수정(Correct)하는 거시적인 시스템 생명주기 관리에 초점을 맞춘다.7

특히 2026년을 기점으로 다수의 에이전트를 병렬로 실행하는 '팩토리 모드(Factory Mode)' 기반의 개발 방법론이 각광받으면서, 개발자는 코드를 직접 작성하는 생산자에서, 다수의 AI 워커(Worker)를 지휘하고 산출물을 검토하는 감독관(Supervisor)으로 역할이 변화하고 있다.8 이러한 환경에서는 생성 속도보다 AI가 생성한 코드를 효과적으로 반박(Refute)하고 검증할 수 있는 통제력이 훨씬 중요해진다.6 통제력이 결여된 고속 코드 생성은 단지 치명적인 오류를 대규모로 확산시키는 결과만을 낳기 때문이다.6

이러한 시대적 요구에 부응하여 등장한 오픈소스 프로젝트가 바로 manaflow-ai/cmux이다.1 cmux는 단순히 탭을 나누어주는 터미널 멀티플렉서(Terminal Multiplexer)를 넘어, 다수의 코딩 에이전트를 병렬로 관리할 수 있도록 설계된 'Ghostty 기반의 macOS 네이티브 AI 에이전트 하네스 터미널'이다.1 본 보고서는 하네스 엔지니어링의 네 가지 핵심 원칙(제한, 제공, 검증, 수정)을 렌즈로 삼아, cmux의 핵심 설계 철학, UI/UX 렌더링 파이프라인, IPC 기반의 소켓 제어 평면(Control Plane), 그리고 에이전트 특화 브라우저 통합 프로토콜(ABP)에 이르는 아키텍처 전반을 심층적으로 해부하고 분석한다.

## **2\. 'Zen of cmux'와 네이티브 하네스 아키텍처의 철학적 기반**

AI 에이전트 생태계가 팽창하면서 다양한 오케스트레이션 도구들이 시장에 등장했다. 그러나 이들 대다수는 특정한 워크플로우를 강제하는 무거운 GUI 기반의 통합 개발 환경(IDE)이거나, Electron 및 Tauri와 같은 웹 기반 프레임워크를 사용하여 성능적 한계를 지닌 경우가 많았다.1 복수의 Claude Code나 Codex 세션이 초당 수천 개의 토큰을 터미널 표준 출력(stdout)으로 쏟아내는 환경에서, 웹 기반 기술 스택은 심각한 메모리 오버헤드와 렌더링 지연(Lag)을 유발하여 오히려 개발자의 인지적 흐름을 방해하는 병목 현상을 초래했다.4

### **2.1 솔루션이 아닌 프리미티브(Primitive)로서의 도구**

cmux 프로젝트를 관통하는 핵심 설계 철학은 'The Zen of cmux'라는 명제로 요약된다. 이는 cmux가 특정한 문제를 해결하기 위한 '의견이 강한(Opinionated) 솔루션'을 자처하기보다는, 개발자가 자신의 필요에 맞게 조립하고 구성할 수 있는 '원초적 도구(Primitive)'를 지향한다는 것을 의미한다.1 AI 모델의 발전 속도는 하네스 시스템의 업데이트 속도를 압도하며, 통제 흐름(Control flow)을 지나치게 복잡하게 엔지니어링할 경우 다음 세대의 모델 업데이트 시 시스템 전체가 붕괴할 위험이 존재한다.7

따라서 cmux는 에이전트의 내부 로직이나 라우팅을 직접 관리하지 않는다. 대신 터미널 화면, 인앱 브라우저, 세션 알림 시스템, 수직 및 수평 화면 분할, 워크스페이스 탭 관리, 그리고 이 모든 것을 외부에서 스크립트로 제어할 수 있는 CLI(Command Line Interface)와 소켓 API라는 독립적인 컴포넌트들만을 제공한다.1 에이전트 프레임워크가 Python 기반이든, Rust 기반이든, TypeScript 기반이든 상관없이, 유효한 JSON 페이로드와 소켓 경로만 있다면 cmux의 인프라를 자유롭게 차용할 수 있다.10 이러한 고도의 디커플링(Decoupling) 아키텍처는 개발자가 가장 자신에게 익숙한 코드베이스와 워크플로우 내에서 에이전트를 유연하게 통제할 수 있는 기반을 마련한다.1

### **2.2 Swift와 AppKit을 활용한 네이티브 성능 극대화**

성능적 한계를 극복하기 위해 cmux는 철저한 네이티브 운영체제 통합을 선택했다. 애플의 Swift 언어와 AppKit 프레임워크를 기반으로 순수 macOS 네이티브 애플리케이션으로 컴파일되며, 메모리 누수를 최소화하고 극도로 빠른 초기 구동(Startup) 속도를 보장한다.1 터미널 렌더링의 핵심 엔진으로는 단일 스레드 병목을 제거하고 GPU 하드웨어 가속을 완벽히 지원하는 libghostty를 채택하였다.1

여기서 주목할 점은 cmux가 인기 있는 오픈소스 터미널인 Ghostty의 단순한 하드 포크(Hard Fork)가 아니라는 점이다.2 마치 데스크톱 애플리케이션들이 웹 뷰를 임베딩하기 위해 WebKit 엔진을 라이브러리로 차용하듯, cmux는 터미널 에뮬레이션이라는 핵심 렌더링 영역만을 libghostty에 위임하고, 그 외곽의 사이드바, 탭 관리, 브라우저 분할 등 GUI 요소들은 독자적인 AppKit 계층에서 구현했다.2 이 영리한 아키텍처 분리를 통해 cmux는 Ghostty 프로젝트의 업스트림 업데이트(예: v1.3.0 업데이트 수용 1)를 손쉽게 추적하면서도, 사용자의 로컬 환경에 이미 존재하는 \~/.config/ghostty/config 구성 파일(테마, 글꼴, 색상 팔레트, 커스텀 키바인딩 등)을 100% 호환하여 읽어 들일 수 있는 무결성을 확보했다.1

## **3\. 에이전트 상태의 시각적 투영: 인지 부하 감소를 위한 메타데이터 아키텍처**

병렬 하네스 엔지니어링 환경에서 개발자가 겪는 가장 큰 고통은 극심한 컨텍스트 스위칭(Context Switching)이다.5 전통적인 tmux 환경에서 5\~6개의 분할된 패널을 열어두고 작업을 진행할 때, 각각의 윈도우에 직접 이름을 지정하더라도 특정 에이전트가 어떤 저장소의 무슨 작업을 진행 중인지, 혹은 어느 에이전트가 사용자 입력을 기다리며 유휴 상태에 빠져 있는지 즉각적으로 파악하기란 불가능에 가깝다.5 cmux는 하네스 엔지니어링의 두 번째 원칙인 '제공(Inform)'을 아키텍처적으로 극대화하여 이 문제를 해결한다.

### **3.1 컨텍스트 메타데이터와 수직 탭(Vertical Tabs)의 실시간 파싱**

cmux의 좌측면을 구성하는 사이드바는 단순한 화면 전환 도구를 넘어선, 강력한 실시간 메타데이터 대시보드 역할을 수행한다. 이 수직 탭 시스템은 각 워크스페이스 내에서 실행 중인 터미널 세션의 내부 상태를 지속적으로 파싱하여 핵심적인 개발 컨텍스트를 시각화한다.1 사이드바는 현재 작업 중인 Git 브랜치 이름, 해당 브랜치와 연결된 원격 Pull Request(PR)의 상태 및 번호, 활성화된 로컬 작업 디렉토리(Working Directory), 백그라운드 서버가 점유하고 있는 리스닝 포트(Listening Ports) 정보를 별도의 쿼리 명령어 없이 실시간으로 추출하여 표시한다.1 디렉토리별로 브랜치 컨텍스트 항목을 중복 제거(Deduplicate)하여 사이드바의 가독성을 높이는 알고리즘(v0.61.0 업데이트 사항)도 포함되어 있다.13 사용자는 Cmd \+ B 단축키를 통해 언제든 사이드바를 토글하여 화면을 넓게 사용할 수 있으며, 필요에 따라 Cmd \+ 1\~8 단축키로 특정 워크스페이스로 즉시 점프하거나 Cmd \+ N으로 완전히 격리된 새 워크스페이스를 생성할 수 있다.1

### **3.2 알림 링(Notification Rings)과 상태 추적 시스템**

여러 코딩 에이전트가 병렬로 작동할 때, 에이전트가 오류에 직면하여 디버깅을 요청하거나, 코드를 커밋하기 전 인간의 승인을 대기하는 등 '블로킹 상태'에 돌입하는 시점을 포착하는 것은 매우 중요하다.4 Claude Code와 같은 도구는 자체적으로 운영체제 데스크톱 알림을 발송하지만, 수많은 탭이 열려 있는 상태에서 "Claude is waiting for your input"이라는 텍스트 하나만으로는 어느 워크스페이스의 어느 패널이 호출을 보냈는지 역추적하는 데 엄청난 시간이 소모된다.4

cmux는 에이전트 프로세스가 주의를 요하는 상태에 진입할 때 이를 즉각적으로 시각화하는 '알림 링(Notification Rings)' 아키텍처를 도입했다.1

1. **시각적 강조:** 특정 에이전트가 대기 상태에 들어가면 해당 터미널 패널의 경계선(Border) 주변이 파란색 링으로 점등되며, 사이드바의 해당 워크스페이스 탭 전체가 밝게 빛난다.1 이 색상은 v0.62.2 업데이트 이후 워크스페이스 커스텀 색상 테마를 동적으로 상속받도록 최적화되었다.14  
2. **알림 중앙 집중화:** Cmd \+ I 단축키를 입력하면 사이드바 위에 전용 알림 패널이 팝오버(Popover) 형태로 나타나, 모든 워크스페이스에서 대기 중인 최근 알림의 실제 텍스트 내용을 한곳에서 열람할 수 있다.1  
3. **즉시 이동 루틴(Jump to Unread):** 사용자가 Cmd \+ Shift \+ U 단축키를 누르면, cmux는 내부 트리 구조를 순회하여 가장 최근에 발생한 '읽지 않은 알림'을 소유한 패널을 찾아 즉시 포커스를 전환한다.1 이는 수십 개의 화면 분할 속에서도 길을 잃지 않게 해주는 하네스 오케스트레이션의 백미라 할 수 있다.

이러한 알림은 복잡한 별도의 API 통합 없이도, 터미널 표준 규격인 OSC 9, OSC 99, OSC 777 이스케이프 시퀀스(Escape Sequences)를 터미널로 출력하는 것만으로 자동으로 트리거된다.1 에이전트가 printf "\\033\]9;Message\\007"과 같은 표준 출력을 발생시키면, Ghostty 렌더링 엔진 계층이 이를 가로채어 cmux의 AppKit UI 상태 머신으로 이벤트를 전달하는 우아한 디커플링 구조를 취하고 있다.2

## **4\. 렌더링 파이프라인 심층 분석: 스플릿 트리 변이와 포커스 제어 알고리즘**

cmux의 고성능을 담보하는 핵심 중 하나는 bonsplit이라는 커스텀 탭 바 및 레이아웃 분할 라이브러리다.16 이 라이브러리는 SwiftUI 기반으로 작성되어 120fps의 부드러운 애니메이션과 드래그 앤 드롭 재정렬을 지원한다.17 그러나 다수의 AI 에이전트가 실시간으로 텍스트를 출력하는 상황에서 터미널 화면을 수평(Cmd \+ Shift \+ D), 수직(Cmd \+ D)으로 분할하거나 닫는(Ctrl \+ D) 행위는 GUI 프레임워크에 막대한 연산 부하를 일으키며 치명적인 렌더링 버그를 유발할 수 있다.16 하네스 엔지니어링 관점에서 UI의 안정성은 에이전트 통제의 필수 전제 조건이므로, cmux 개발진이 이를 해결한 아키텍처적 접근을 살펴볼 필요가 있다.

### **4.1 포털(Portal) 계층 구조와 뷰포트의 비동기 지오메트리 동기화**

사용자가 새로운 터미널 패널을 분할할 때, 기존 터미널 화면이 일시적으로 깜빡이거나 1프레임 동안 완전히 검은 화면(Blackout)이 나타나는 블링크(Blink) 현상은 네이티브 UI 렌더링에서 흔히 마주하는 난제다.16 이는 bonsplit이 화면 분할 트리(Split Tree)를 변형(Mutation)할 때, SwiftUI가 전체 뷰의 바디(Body)를 재평가하면서 발생한다. 이 과정에서 기존 터미널의 NSViewRepresentable인 GhosttyTerminalView가 일시적으로 분해(Dismantle)되었다가 재조립될 수 있다.16

cmux 아키텍처는 이를 방어하기 위해 TerminalWindowPortal.swift라는 중간 포털 계층을 도입했다. 이 계층의 synchronizeHostedView() 메서드는 터미널 뷰의 호스트 경계(Host Bounds)가 유효한지, 조상 뷰가 숨김 처리되었는지, 최소 크기 임계값을 충족하는지 등을 엄격히 검사한다.16 레이아웃이 완전히 정착되지 않은 과도기(Transient state)에 뷰포트가 비정상적으로 작아지거나 화면 밖으로 밀려날 경우, 포털은 렌더링 파이프라인의 충돌을 막기 위해 강제로 isHidden \= true 플래그를 삽입했다.16 그러나 이 동기적 플래그 제어가 역설적으로 시각적 깜빡임을 유발했다.

이를 해결하기 위해 cmux는 지오메트리 조정(Geometry Reconciliation)을 완전히 비동기화하는 아키텍처로 전환했다. Workspace.swift의 scheduleTerminalGeometryReconcile 및 포털의 scheduleDeferredFullSynchronizeAll 루틴은 동기적 분할 연산이 끝난 직후가 아닌, 레이아웃의 이벤트 루프가 완전히 정착된 다음 런루프 틱(Runloop Tick)에서 터미널의 크기와 위치를 재조정하도록 지연(Deferred) 처리된다.16 GhosttyTerminalView의 dismantleNSView 주기에서도 뷰를 의도적으로 숨기지 않도록 방어 로직을 추가하여, 렌더링 갭(Gap)을 제거하고 완벽하게 연속적인 시각적 피드백을 유지한다.16

### **4.2 삼중 지연 포커스 재할당 및 단축키 억제 메커니즘**

터미널을 분할할 때 새 패널로 포커스를 옮기지 않는 백그라운드 분할(Non-focus splits)의 경우, 포커스 손실과 복구가 매우 빠른 시간 내에 반복되며 깜빡임을 유발할 수 있다.16 cmux의 preserveFocusAfterNonFocusSplit 알고리즘은 단일 포커스 재할당에 의존하지 않고, 세 번에 걸친 지연된 포커스 재할당(reassertFocusAfterNonFocusSplit) 과정을 통해 SwiftUI와 AppKit 간의 포커스 상태 불일치를 강제로 동기화한다.16

나아가 개발자가 단축키를 극도로 빠르게 연타할 때 발생하는 상태 붕괴를 막기 위해, 50ms의 포커스 억제(Focus Suppression) 타이밍 윈도우를 아키텍처에 하드코딩했다.16 AppDelegate.swift에 위치한 shouldSuppressSplitShortcutForTransientTerminalFocusState 메서드는 이전의 분할 요청으로 인해 터미널이 아직 과도기적 렌더링 상태에 머물러 있는 경우, 이후 들어오는 단축키 입력 이벤트를 완전히 삼켜버린다(Eat).16 이는 사용자가 시각적 안정성을 체감하게 하면서도, 이면에서는 초당 수십 번의 레이아웃 재계산 폭주로부터 하네스 시스템을 보호하는 극도로 정교한 자원 관리(Resource Management)의 일환이다.16

## **5\. 소켓 API 및 CLI 중심의 프로그래머블 제어 평면(Control Plane)**

하네스 엔지니어링의 핵심은 에이전트에게 통제된 실행 환경을 부여하고(Constrain), 외부의 개입 지점을 열어두는 것이다.7 cmux는 모든 구성 요소를 스크립트로 조작할 수 있도록 강력한 CLI 명령어 세트와 유닉스 도메인 소켓(Unix Domain Socket) 기반의 IPC(Inter-Process Communication) API를 제공한다.1

### **5.1 유닉스 도메인 소켓을 활용한 초저지연 통신 백본**

웹 서버처럼 외부 네트워크 포트를 개방하여 HTTP 요청을 주고받는 방식은 로컬 환경에서 보안 위험을 초래하고 지연 시간을 증가시킨다. cmux는 동일 기기 내의 프로세스 간 통신에 최적화된 유닉스 도메인 소켓을 커뮤니케이션 백본으로 채택했다.19 에이전트가 백그라운드 데몬 프로세스에서 작업을 수행하는 동안, 이 소켓 파이프를 통해 JSON 포맷의 명령 페이로드를 전송하면, 커널 수준의 메모리 복사만으로 즉각 cmux GUI 앱 프로세스로 데이터가 전달된다.10

이러한 메커니즘은 통신의 레이턴시를 제로에 가깝게 단축하여, 에이전트가 작업을 완료하자마자 지연 없이 즉각적으로 UI의 알림 링을 점등시키거나 새로운 분할 화면을 렌더링하는 매끄러운 경험(Seamless experience)을 제공한다.19 v0.61.0 업데이트에서는 이 소켓 통신에 비밀번호 인증을 추가하거나 완전 개방 모드를 선택할 수 있는 소켓 접근 제어(Access Control Modes) 기능이 추가되어 하네스의 보안성(Verify & Constrain)을 한층 강화했다.13

### **5.2 쉘 통합 및 커스텀 에이전트 훅(Hook) 설계**

cmux는 /Applications/cmux.app/Contents/Resources/bin/cmux 경로에 내장된 실행 파일을 /usr/local/bin/cmux로 심볼릭 링크하여 전역 환경에서 사용할 수 있도록 지원한다.20 개발자는 cmux list-workspaces와 같은 명령어를 통해 현재 실행 중인 모든 작업 공간의 상태, 디렉토리, 커스텀 색상 테마 등의 메타데이터를 CLI에서 추출할 수 있으며 20, cmux notify \--title "Build Complete" \--body "Your build finished" 명령어로 직접 네이티브 알림을 발송할 수도 있다.20

이는 하네스 시스템을 기존의 워크플로우에 결합하는 강력한 유연성을 제공한다. 예를 들어, 사용자의 쉘 환경 설정 파일(config/claude/statusline.sh 및 cmux-notify.sh)을 통해 Claude Code 에이전트의 출력을 파싱하고, 현재 사용 중인 모델의 종류나 토큰 사용량을 cmux의 상태바에 주입(Inject)하거나 알림 시스템으로 전달하는 스크립트를 단 몇 줄의 코드로 작성할 수 있다.22 파이썬, 쉘 스크립트 등 에이전트의 구동 언어에 구애받지 않고 오직 유효한 JSON 페이로드와 소켓 경로만으로 통합이 가능한 이 간결성(Simplicity)이야말로, cmux가 제공하는 스크립터블 하네스 아키텍처의 강력한 무기다.9

| cmux CLI 핵심 기능 계층 | 주요 목적 및 활용 사례 | 아키텍처적 의의 |
| :---- | :---- | :---- |
| **표면 제어 (Surface Control)** | create, split, close 등을 통한 터미널/브라우저 패널 동적 생성 및 위치 이동 9 | 에이전트가 자신의 필요에 따라 UI 레이아웃을 자율적으로 재구성할 수 있는 권한 부여 |
| **I/O 스트리밍 제어** | send-text, send-keys, read-screen을 통한 키 스트로크 주입 및 터미널 스크롤백 데이터 추출 1 | 에이전트 간의 파이프라인 형성 및 백그라운드 테스트 자동화의 기반 |
| **메타데이터 파싱** | list-workspaces, set-status, 진행률 및 로그 업데이트 9 | 팩토리 모드에서 다중 에이전트의 상태를 추적하는 실시간 관제 시스템(Observability) 연동 |
| **레거시 호환성** | tmux 스타일의 명령어 별칭(Alias) 제공 9 | 기존 멀티플렉서 사용자들의 완만한 학습 곡선(Learning Curve) 유도 및 마이그레이션 지원 |

## **6\. 브라우저 자동화의 진화: ABP(Agent Browser Protocol) 통합 아키텍처**

AI 코딩 에이전트의 궁극적인 목표 중 하나는 단순히 백엔드 로직을 짜는 것을 넘어, 작성한 코드를 브라우저에서 렌더링하고 동적 UI를 테스트하며 버그를 자율적으로 수정하는 엔드투엔드(End-to-End) 검증이다. 그러나 기존의 Playwright 기반 헤드리스 브라우저를 에이전트에 직접 연결하는 방식은 심각한 결함을 드러냈다.23

### **6.1 '오래된 상태(Stale State)' 문제와 시각적 피드백 루프의 붕괴**

기존 구조에서 에이전트는 브라우저 화면의 스냅샷 이미지를 분석한 뒤, 특정 DOM 요소를 클릭하거나 텍스트를 입력하는 명령을 내린다. 그러나 에이전트가 명령을 생성하고 전송하는 수 초의 지연 시간 동안, 모던 웹 브라우저의 화면은 동적으로 변한다(Dynamic Reflow).23 예를 들어, 에이전트가 로그인 버튼의 좌표를 클릭하려 할 때 화면 하단에 알림 모달(Modal) 창이 튀어나와 버튼을 덮어버리거나, 텍스트를 입력하려는 순간 자동완성 드롭다운이 확장되어 시야를 가리는 현상이 빈번하게 발생한다.23 이 외에도 alert() 창이 실행 흐름을 가로막거나, 백그라운드 다운로드가 발생했을 때 에이전트는 최신의 브라우저 상태를 전혀 파악하지 못한 채 '오래된 상태(Stale State)'를 기반으로 엉뚱한 후속 동작을 수행하여 오류의 늪에 빠지곤 했다.23

### **6.2 cmux 인앱 브라우저와 동결(Freeze) 기반의 ABP 메커니즘**

cmux는 이 문제를 아키텍처 수준에서 해결하기 위해, 터미널과 나란히 분할할 수 있는 강력한 스크립터블 인앱 브라우저(Cmd \+ Shift \+ L로 호출)를 내장했다.1 이 브라우저는 Vercel Labs의 오픈소스 프로젝트인 agent-browser의 통신 API를 포팅하여 탑재하였으며, Agent Browser Protocol (ABP)의 철학을 깊숙이 반영하고 있다.1

ABP 아키텍처의 핵심은 **상호작용의 동기화와 시점 통제**에 있다. 에이전트가 브라우저에 액션(클릭, 타입, 폼 전송 등)을 가한 직후, cmux 내부의 브라우저 엔진은 자바스크립트 실행과 화면 렌더링 루프를 즉각적으로 동결(Freeze)시킨다.23 브라우저가 정지된 이 찰나의 순간에 시스템은 DOM의 접근성 트리(Accessibility Tree) 스냅샷을 완벽하게 추출하고, 요소 참조값(Element Refs)을 맵핑하며, 그 사이 발생한 주목할 만한 이벤트들(파일 선택 창 팝업, 권한 요청, 페이지 이동, 다운로드 등)을 구조화된 로그(Structured Summary)로 취합한다.4

![][image1]  
이렇게 추출된 완벽한 최신 상태 데이터와 화면 스냅샷이 에이전트로 다시 전송된 후에야 브라우저의 동결이 해제된다.23 이러한 아키텍처는 브라우저 상호작용을 예측 불가능한 비동기 이벤트의 연속이 아닌, 멀티모달 챗봇과 대화하듯 순차적이고 동기화된 턴 기반(Turn-based) 챗 루프로 탈바꿈시킨다.23 실제로 ABP 기반의 드라이버 아키텍처는 Online Mind2Web 벤치마크에서 90.5%라는 압도적인 브라우저 제어 성공률을 달성하며 그 효용성을 입증했다.23

결과적으로 개발자는 cmux 터미널 패널 하나에는 Claude Code를 실행하여 로컬 서버를 띄우고, 그 옆에 분할된 cmux 인앱 브라우저 패널을 배치하여 에이전트가 자신이 작성한 로컬 서버의 렌더링 결과물을 직접 탐색(Navigate), 클릭(Click), 자바스크립트 평가(Evaluate JS) 및 콘솔 로그 판독(Read Console Logs)을 수행하도록 지시할 수 있다.1 이는 하네스 엔지니어링의 '검증(Verify)' 단계를 인간의 모니터 안에서 자율적으로 완결 짓는 혁신적인 통합 환경을 완성한다.7

## **7\. 상태 영속성 및 CI/CD 파이프라인의 격리 환경(Sandbox) 연동**

소프트웨어 엔지니어링 하네스는 필연적으로 시스템 종료, 크래시, 혹은 버전 업데이트와 같은 중단 사태를 겪는다. 안정적인 도구는 재해 발생 시 복구 능력을 갖춰야 하며, 이것이 장애 허용(Fault Tolerance)과 영속성(Persistence) 아키텍처다.

### **7.1 세션 복원(Session Restore) 알고리즘**

cmux는 사용자가 앱을 종료(Cmd \+ Q 단축키 경고 억제 기능은 v0.61.0에 추가됨 13)하거나 재시작할 때 이전의 방대한 컨텍스트를 잃지 않도록 1단계 세션 영속성(Session persistence pass 1\) 로직을 구현했다.1 재시작 시 애플리케이션은 디스크에 저장된 직렬화된 레이아웃 데이터를 바탕으로 다음 요소들을 완벽히 복원한다.

* 데스크톱 윈도우 크기와 위치, 다수의 워크스페이스, 수직 및 수평 분할 패널의 트리 구조.1  
* 각 패널의 마지막 작업 디렉토리(Working Directory) 경로 및 터미널의 이전 스크롤백(Scrollback) 텍스트 이력 (최대 한도 내 베스트 에포트 복원).1  
* 분할되어 있던 인앱 브라우저 탭의 이전 URL 및 네비게이션 히스토리.1

다만, 아키텍처의 한계점도 명확히 고지하고 있다. cmux는 운영체제의 프로세스 스냅샷 도구가 아니므로, 메모리 힙에서 실시간으로 돌아가고 있던 라이브 프로세스(예: 백그라운드에서 구동 중이던 Claude Code 챗 루프, tmux 세션, 혹은 vim 편집기 상태)를 강제로 부활시키지는 못한다.1 터미널 에뮬레이터 계층과 PTY(Pseudoterminal) 하위 프로세스 간의 태생적인 경계선 때문이며, 이는 향후 ACP(Agent Client Protocol)와 같이 에이전트의 상태를 직렬화하여 외부에 저장할 수 있는 프로토콜이 표준화되어야 해결될 수 있는 과제다.18

### **7.2 CI/CD 파이프라인과 일회성 샌드박스 연동**

하네스 엔지니어링은 에이전트가 로컬 파일 시스템을 파괴하거나 엉뚱한 의존성을 설치하는 것을 막기 위해 '격리된 환경(Sandbox)'을 강제(Constrain)해야 한다.7 cmux의 CLI는 이러한 CI/CD 파이프라인 구축에 완벽히 호환된다. 사용자는 cmux start./my-project 명령어를 통해 원격 클라우드나 로컬 Docker 컨테이너에 완벽히 격리된 일회성 샌드박스를 스핀업(Spin-up)할 수 있다.28 이 명령어는 고유한 샌드박스 ID(cmux\_abc123)를 반환하며, rsync 프로토콜을 통해 로컬의 작업 디렉토리를 샌드박스 내부로 동기화한다.28

이후 cmux exec cmux\_abc123 "npm install && npm run dev"와 같이 샌드박스 내부에 명령을 주입하거나, cmux pty \<id\>로 원격 터미널 세션에 직접 연결하여 에이전트가 로컬 환경을 오염시키지 않고 안전하게 코드를 컴파일하고 실행 결과를 검증하도록 파이프라인을 구축할 수 있다.28 검증이 끝나면 cmux stop 및 cmux delete 명령어로 샌드박스 생명주기를 파기한다.28 이러한 일회성 샌드박스 통합은 에이전트의 난동(Hallucination)으로부터 코어 코드베이스를 보호하는 가장 강력한 형태의 하네스 엔지니어링 규율을 실천하는 것이다.7

## **8\. 전통적 멀티플렉서(tmux)와의 비교 우위 및 한계 분석**

현장의 실무 엔지니어들이 가장 빈번하게 던지는 질문 중 하나는 "이미 산업 표준으로 자리 잡은 터미널 멀티플렉서인 tmux를 활용하여 에이전트를 백그라운드에서 실행하면 되지 않는가? 굳이 네이티브 앱인 cmux를 도입해야 할 이유가 무엇인가?"이다.2 tmux는 가볍고 강력하며, SSH를 통한 원격 작업 유지에 탁월하다. 그러나 다수의 자율형 코딩 에이전트를 통제하는 하네스 아키텍처의 관점에서 바라보면 두 도구의 목적과 한계가 극명히 갈린다.5

| 비교 속성 및 아키텍처 요소 | 전통적 멀티플렉서 (tmux) | 하네스 엔지니어링 터미널 (cmux) |
| :---- | :---- | :---- |
| **시스템 작동 계층 (Operation Layer)** | 어떠한 터미널 에뮬레이터(iTerm2, Alacritty 등) 내부에서든 구동되는 **PTY 기반의 텍스트 멀티플렉서 데몬** 2 | Swift 및 AppKit을 활용해 GPU 가속 터미널 렌더링 엔진(libghostty)을 결합한 **독립형 네이티브 GUI 애플리케이션** 1 |
| **에이전트 통신 및 상태 파악 (Observability)** | 프로세스의 stdout/stderr 출력 스트림에 전적으로 의존. 에이전트가 대기 상태에 빠졌는지 알기 위해선 **사용자가 수동으로 여러 패널을 순회하며 직접 눈으로 텍스트를 확인**해야 함 5 | IPC 유닉스 도메인 소켓 및 표준 OSC 이스케이프 시퀀스 후킹. 에이전트 블로킹 시 **사이드바 점등, 파란색 알림 링 표출 및 OS 데스크톱 알림의 글로벌 팝오버**로 즉각적 시각 동기화 1 |
| **작업 컨텍스트 시각화 (Context Rendering)** | 패널이나 윈도우의 이름을 개발자가 수동으로 변경하거나 복잡한 플러그인을 설치하여 하단 상태바에 제한적인 텍스트만 표시 가능 5 | 실시간 디렉토리 스캐닝을 통한 **수직 탭(Vertical Tabs)** 아키텍처. Git 브랜치 이름, PR 동기화 상태, 열린 네트워크 포트 등을 쿼리 없이 항시 노출 1 |
| **인지 부하 (Cognitive Load) 관리 단축키** | 이전/다음 패널 이동(e.g., Ctrl+B, N) 위주의 순차적 탐색 강제 | **Cmd \+ Shift \+ U**: 내부 상태 머신을 쿼리하여 가장 최근에 인간의 응답(입력)을 기다리는 에이전트 패널로 즉시 포커스 점프 1 |
| **프론트엔드 검증 파이프라인 (Verification)** | 터미널 내부에 브라우저 엔진을 삽입할 수 없어, 로컬 포트를 외부 크롬이나 사파리에 띄우고 인간이 수동으로 확인해야 함 | **스크립터블 인앱 브라우저** 내장. 브라우저 창을 터미널과 분할하여 띄우고, 에이전트가 소켓 API를 통해 DOM 스냅샷을 획득하고 JS를 직접 평가(Evaluate)하도록 자동화 루프 구축 1 |
| **스크립팅 및 확장성 (Scriptability)** | tmux send-keys 등 터미널 화면 제어 명령어 위주 | 표면(Surface) 제어, 포커스 제어, 텍스트 전송뿐 아니라 웹 요소 탐색과 알림 버스(Notification Bus) 주입을 아우르는 **JSON 스키마 기반 API** 9 |

한 AI 컨설팅 업계 종사자의 실무 분석에 따르면, 단일 클라이언트 프로젝트(예: WhatsApp 봇, CRM 연동, 자동화 파이프라인 구축)를 진행할 때 세밀한 마크다운 스펙(Markdown Spec) 문서를 작성한 뒤, 프론트엔드 담당, 백엔드 담당, 테스트 담당 등 3\~6개의 에이전트 인스턴스를 병렬로 구동시키는 패턴이 개발 기간을 절반으로 단축시킨다고 한다.8

그러나 이러한 병렬 접근법을 tmux에서 시도할 경우, 각 에이전트가 어떤 상태인지 지속적으로 컨텍스트를 스위칭해야 하는 인간의 인지적 피로도(Taxing)가 극도로 상승하며, 제한된 API 토큰을 소진하는 데 쫓기는 현상이 발생한다.5 반면 cmux는 Cmd \+ Shift \+ U 단축키 하나로 응답이 필요한 에이전트를 찾아내고, 알림 링으로 오류 상태를 즉각 시각화하며, 인앱 브라우저로 렌더링 결과를 바로 옆에서 증명(Verify)하는 등, 개발자가 코드를 직접 짜는 윈도우 스플리터(Window Splitter)의 역할에서 벗어나 다수의 워커를 조율하는 '공장장(Factory Mode Supervisor)'의 관점(Abstraction)을 취할 수 있도록 인프라를 재설계했다.8 이는 단순한 UI의 차이가 아닌, 하네스 엔지니어링 패러다임을 반영한 설계 철학의 근본적인 차이점이다.

## **9\. 결론 및 향후 소프트웨어 아키텍처 전망**

AI가 코드를 생성하는 속도가 인간의 타자 속도를 초월한 현시점에서, 미래의 핵심 기술 자본은 '더 빠르게 코드를 생성하는 능력'이 아니라 '무분별하게 생성된 코드를 더 안전하게 통제, 검증, 그리고 반박(Refute)하는 능력'으로 귀결될 것이다.6 인공지능은 동료(Coworker)라기보다는 인간의 능력을 증폭시키는 외골격(Exoskeleton)에 가깝다.6 강력한 외골격을 다루기 위해서는 조종사의 의도를 명확히 전달하고 기계의 폭주를 방어할 수 있는 견고한 콕핏(Cockpit), 즉 하네스(Harness)가 반드시 필요하다.

manaflow-ai/cmux는 이러한 시대적 요구에 가장 발 빠르게 응답한 선도적인 아키텍처 사례를 보여준다.

1. **네이티브 인프라의 재조명:** Electron의 무거움을 버리고 AppKit과 libghostty의 GPU 가속 능력을 결합한 결정은, 대용량 토큰 스트리밍 시대에 클라이언트 애플리케이션이 갖추어야 할 응답성과 메모리 안정성의 모범답안을 제시했다. 포털 렌더링 파이프라인의 비동기 지오메트리 제어와 포커스 억제 로직은 네이티브 환경에서만 달성 가능한 극도의 최적화 수준을 증명한다.  
2. **프로그래머블 경계의 확립:** 유닉스 도메인 소켓 기반의 초저지연 통신 백본과 풍부한 CLI 도구의 결합은, 특정한 AI 에이전트 프레임워크에 종속되지 않는 유연하고 열린(Decoupled) 제어 평면을 완성했다. 이는 하네스 엔지니어링의 핵심인 '제한(Constrain)' 원칙을 완벽히 구현한 것이다.  
3. **동기화된 시각적 피드백 시스템:** 브라우저 렌더링 엔진을 일시 정지(Freeze)시켜 에이전트에게 동기화된 최신 접근성 트리를 제공하는 ABP(Agent Browser Protocol) 통합과, 여러 워크스페이스의 컨텍스트 메타데이터를 쿼리 없이 실시간으로 추출해내는 수직 탭 및 사이드바 시스템은 하네스의 '검증(Verify)' 및 '제공(Inform)' 단계를 혁신적으로 단축시켰다.

결론적으로, 다중 에이전트 시스템(Multi-Agent Systems)이 엔터프라이즈 환경 및 일선 소프트웨어 개발 현장에 깊숙이 뿌리내릴수록, cmux와 같이 에이전트의 생명주기를 관장하는 네이티브 하네스 터미널의 역할은 더욱 중요해질 것이다. 오픈소스 생태계인 AGPL-3.0 라이선스 기반의 활발한 기여와 발 빠른 업데이트 릴리즈 주기 1는 이 프로젝트가 단순한 실험적 도구를 넘어 차세대 소프트웨어 엔지니어링 워크플로우를 관장하는 데표적인 인프라스트럭처로 자리매김할 것임을 강력히 시사한다. 하네스의 품질이 곧 프로덕션 시스템의 신뢰성을 결정짓는 시대에, cmux 아키텍처가 제시한 디커플링, 저지연 통신, 그리고 시각적 인지 부하의 최소화라는 설계 패러다임은 관련 업계가 반드시 주목해야 할 중요한 이정표가 될 것이다.

#### **참고 자료**

1. GitHub \- manaflow-ai/cmux: Ghostty-based macOS terminal with vertical tabs and notifications for AI coding agents, 3월 19, 2026에 액세스, [https://github.com/manaflow-ai/cmux](https://github.com/manaflow-ai/cmux)  
2. cmux — The terminal built for multitasking, 3월 19, 2026에 액세스, [https://www.cmux.dev/](https://www.cmux.dev/)  
3. amp · GitHub Topics, 3월 19, 2026에 액세스, [https://github.com/topics/amp](https://github.com/topics/amp)  
4. Show HN: cmux \- Ghostty-based terminal with vertical tabs and notifications | Hacker News, 3월 19, 2026에 액세스, [https://news.ycombinator.com/item?id=47079718](https://news.ycombinator.com/item?id=47079718)  
5. AI coding helps me with speed, but the mental overload is heavy\! How do you deal with it?, 3월 19, 2026에 액세스, [https://www.reddit.com/r/ClaudeCode/comments/1rkh1aw/ai\_coding\_helps\_me\_with\_speed\_but\_the\_mental/](https://www.reddit.com/r/ClaudeCode/comments/1rkh1aw/ai_coding_helps_me_with_speed_but_the_mental/)  
6. AI News Digest Feb 2026: Anthropic Sabotage Report, Chrome WebMCP, OpenAI Deep Research \- The Neuron, 3월 19, 2026에 액세스, [https://www.theneuron.ai/ai-news-digests/around-the-horn-digest-february-2026/](https://www.theneuron.ai/ai-news-digests/around-the-horn-digest-february-2026/)  
7. Harness Engineering: The Complete Guide to Building Systems That Make AI Agents Actually Work (2026) | NxCode, 3월 19, 2026에 액세스, [https://www.nxcode.io/resources/news/harness-engineering-complete-guide-ai-agent-codex-2026](https://www.nxcode.io/resources/news/harness-engineering-complete-guide-ai-agent-codex-2026)  
8. Parallel coding agents with tmux and Markdown specs | Hacker News, 3월 19, 2026에 액세스, [https://news.ycombinator.com/item?id=47218318](https://news.ycombinator.com/item?id=47218318)  
9. cmux Terminal: A Practical Guide for AI Coding Agents on macOS \- Bitdoze, 3월 19, 2026에 액세스, [https://www.bitdoze.com/cmux-terminal/](https://www.bitdoze.com/cmux-terminal/)  
10. CMUX Terminal Turned My Mac Into an Agent Command Center | Engr Mejba Ahmed, 3월 19, 2026에 액세스, [https://www.mejba.me/blog/cmux-terminal-coding-agents](https://www.mejba.me/blog/cmux-terminal-coding-agents)  
11. README.md \- manaflow-ai/cmux · GitHub, 3월 19, 2026에 액세스, [https://github.com/manaflow-ai/cmux/blob/main/README.md](https://github.com/manaflow-ai/cmux/blob/main/README.md)  
12. Is anyone going towards monorepos because of AI coding agents? \- The Shitty Coders Club, 3월 19, 2026에 액세스, [https://www.answeroverflow.com/m/1475880710295392367?cursor=B75wGd8Cig9AsPX\_bkKmKPND7KgnXYgDOHBbzRM80k3rJpt-RW4AroygJUaNZaPkhcHLt8bqx2Wf9BDWf9A1jzXosUHOrjk98tjFiXQjspRlcVgDXKPihnAVn8MiRJMSSMPObSPFuF9F2nLZaFtyiwoPxgueprbXhX\_DhH7jwYNU3eVTRvumszAsLm8](https://www.answeroverflow.com/m/1475880710295392367?cursor=B75wGd8Cig9AsPX_bkKmKPND7KgnXYgDOHBbzRM80k3rJpt-RW4AroygJUaNZaPkhcHLt8bqx2Wf9BDWf9A1jzXosUHOrjk98tjFiXQjspRlcVgDXKPihnAVn8MiRJMSSMPObSPFuF9F2nLZaFtyiwoPxgueprbXhX_DhH7jwYNU3eVTRvumszAsLm8)  
13. manaflow-ai/cmux v0.61.0 on GitHub \- NewReleases.io, 3월 19, 2026에 액세스, [https://newreleases.io/project/github/manaflow-ai/cmux/release/v0.61.0](https://newreleases.io/project/github/manaflow-ai/cmux/release/v0.61.0)  
14. Releases · manaflow-ai/cmux · GitHub, 3월 19, 2026에 액세스, [https://github.com/manaflow-ai/cmux/releases](https://github.com/manaflow-ai/cmux/releases)  
15. cmux cli demo \- YouTube, 3월 19, 2026에 액세스, [https://www.youtube.com/watch?v=XKc1cVCFLDQ](https://www.youtube.com/watch?v=XKc1cVCFLDQ)  
16. Terminal blinks/lags when splitting or closing panes (Cmd+D, Cmd+Shift+D, Ctrl+D) · Issue \#456 · manaflow-ai/cmux \- GitHub, 3월 19, 2026에 액세스, [https://github.com/manaflow-ai/cmux/issues/456](https://github.com/manaflow-ai/cmux/issues/456)  
17. manaflow-ai \- GitHub, 3월 19, 2026에 액세스, [https://github.com/manaflow-ai](https://github.com/manaflow-ai)  
18. silentEAG/awesome-stars: My Awesome List \- GitHub, 3월 19, 2026에 액세스, [https://github.com/silentEAG/awesome-stars](https://github.com/silentEAG/awesome-stars)  
19. cmux: Native macOS Terminal for AI Coding Agents | Better Stack Community, 3월 19, 2026에 액세스, [https://betterstack.com/community/guides/ai/cmux-terminal/](https://betterstack.com/community/guides/ai/cmux-terminal/)  
20. Getting Started — cmux docs, 3월 19, 2026에 액세스, [https://www.cmux.dev/docs/getting-started](https://www.cmux.dev/docs/getting-started)  
21. manaflow-ai/cmux v0.62.2 on GitHub \- NewReleases.io, 3월 19, 2026에 액세스, [https://newreleases.io/project/github/manaflow-ai/cmux/release/v0.62.2](https://newreleases.io/project/github/manaflow-ai/cmux/release/v0.62.2)  
22. Building my Terminal Setup \- subaud, 3월 19, 2026에 액세스, [https://www.subaud.io/building-my-terminal-setup/](https://www.subaud.io/building-my-terminal-setup/)  
23. Show HN: Open-source browser for AI agents \- Hacker News, 3월 19, 2026에 액세스, [https://news.ycombinator.com/item?id=47336171](https://news.ycombinator.com/item?id=47336171)  
24. I spent a year building the biggest browser-agent library. Here's why agents fail, and what actually works. : r/automation \- Reddit, 3월 19, 2026에 액세스, [https://www.reddit.com/r/automation/comments/1pcxmxb/i\_spent\_a\_year\_building\_the\_biggest\_browseragent/](https://www.reddit.com/r/automation/comments/1pcxmxb/i_spent_a_year_building_the_biggest_browseragent/)  
25. vercel-labs/agent-browser: Browser automation CLI for AI agents \- GitHub, 3월 19, 2026에 액세스, [https://github.com/vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)  
26. Browser Automation AI Agent \- Altruist, 3월 19, 2026에 액세스, [https://altruist.com/engineering-blog/browser-automation-ai-agent/](https://altruist.com/engineering-blog/browser-automation-ai-agent/)  
27. manaflow-ai/cmux v0.0.0-dmg-test on GitHub \- NewReleases.io, 3월 19, 2026에 액세스, [https://newreleases.io/project/github/manaflow-ai/cmux/release/v0.0.0-dmg-test](https://newreleases.io/project/github/manaflow-ai/cmux/release/v0.0.0-dmg-test)  
28. cmux | Skills Marketplace \- LobeHub, 3월 19, 2026에 액세스, [https://lobehub.com/skills/neversight-skills\_feed-cmux](https://lobehub.com/skills/neversight-skills_feed-cmux)  
29. cmux | Skills Marketplace \- LobeHub, 3월 19, 2026에 액세스, [https://lobehub.com/ko/skills/neversight-skills\_feed-cmux](https://lobehub.com/ko/skills/neversight-skills_feed-cmux)  
30. GitHub \- manaflow-ai/manaflow: Open source Claude Code web/Codex Cloud/Devin/Ramp Inspect alternative, 3월 19, 2026에 액세스, [https://github.com/manaflow-ai/manaflow](https://github.com/manaflow-ai/manaflow)

[image1]: <data:image/png;base64,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>