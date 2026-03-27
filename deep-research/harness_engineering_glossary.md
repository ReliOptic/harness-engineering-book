# Harness Engineering & AgentOps — Backbone Glossary

> **용도**: *Harness Engineering and AgentOps* 교과서 집필용 핵심 용어집  
> **출처**: OpenAI "Harness Engineering: Leveraging Codex in an Agent-First World" (2026.02.13) 및 관련 해설 문헌 크로스레퍼런스  
> **작성일**: 2026-03-20  
> **구조**: 용어 → 정의 → 원문 맥락 → 실험 설계 제안

---

## 목차

1. [핵심 프레임워크 용어](#1-핵심-프레임워크-용어)
2. [Context Engineering 계열](#2-context-engineering-계열)
3. [Architectural Constraints 계열](#3-architectural-constraints-계열)
4. [Entropy Management 계열](#4-entropy-management-계열)
5. [Agent Workflow & Orchestration 계열](#5-agent-workflow--orchestration-계열)
6. [Human Role 재정의 계열](#6-human-role-재정의-계열)
7. [Feedback Loop & Verification 계열](#7-feedback-loop--verification-계열)
8. [Scale & Metrics 계열](#8-scale--metrics-계열)
9. [Cross-Reference: 외부 프레임워크 대응표](#9-cross-reference-외부-프레임워크-대응표)

---

## 1. 핵심 프레임워크 용어

### 1.1 Harness (하네스)

- **정의**: AI 에이전트가 생산적이고 안정적으로 작업할 수 있도록 설계된 제약(constraint), 도구(tool), 문서(documentation), 피드백 루프(feedback loop)의 총체적 시스템
- **어원**: 말(horse)을 제어하는 마구(tack) — 고삐, 안장, 재갈의 세트. 강력하지만 방향을 모르는 동물을 생산적 경로로 유도하는 장비 전체를 지칭
- **원문 맥락**: OpenAI 팀은 "agent가 아니라 harness가 어려운 부분"이라 선언. Mitchell Hashimoto(Terraform 창시자)가 명명한 용어를 채택
- **🧪 실험**: 동일 모델(예: Claude Sonnet)에 harness 유무 조건을 나눠 동일 태스크 수행 → 정확도, 완료 시간, 아키텍처 일관성 비교. LangChain의 TerminalBench 2.0 결과(52.8% → 66.5%, harness만 변경)를 재현 실험으로 설계 가능

### 1.2 Harness Engineering (하네스 엔지니어링)

- **정의**: 에이전트가 신뢰성 있게 작업할 수 있는 환경을 설계·구축·유지보수하는 엔지니어링 분야
- **핵심 축**: Constrain(제한) → Inform(알림) → Verify(검증) → Correct(교정)의 4단계 사이클
- **원문 맥락**: OpenAI 엔지니어의 본업이 "코드 작성"에서 "환경 설계, 의도 명세, 피드백 루프 구축"으로 전환되었음을 기술
- **🧪 실험**: 4단계 사이클 중 하나씩 제거한 ablation study — 어떤 축이 빠졌을 때 에이전트 성능 저하가 가장 큰지 측정

### 1.3 Agent-First World (에이전트 퍼스트 월드)

- **정의**: 소프트웨어 개발의 1차 실행 주체가 인간이 아닌 AI 에이전트인 패러다임
- **원문 맥락**: OpenAI 팀의 핵심 제약 — "no manually-written code". 인간은 단 한 줄도 직접 작성하지 않음으로써 harness 구축을 강제(forcing function)
- **🧪 실험**: 팀 A(인간 코딩 허용) vs 팀 B(에이전트 only, 0-human-code 제약) → 동일 기간 동일 스펙으로 프로덕트 빌드 후 코드 품질, 아키텍처 일관성, 문서 커버리지 비교

### 1.4 The Three Pillars (3대 기둥)

- **정의**: Harness Engineering의 3대 구성 범주 — Context Engineering, Architectural Constraints, Entropy Management("Garbage Collection")
- **원문 맥락**: Birgitta Böckeler(Thoughtworks)가 OpenAI 원문을 해석하며 3범주로 분류. 각각 결정론적(deterministic) 접근과 LLM 기반 접근이 혼합
- **🧪 실험**: 3기둥 각각의 성숙도 레벨을 0–3으로 점수화 → 프로젝트 6개월 생존율, 기술부채 축적 속도와의 상관관계 종단 추적

---

## 2. Context Engineering 계열

### 2.1 Context Engineering (컨텍스트 엔지니어링)

- **정의**: 에이전트가 올바른 정보를 올바른 시점에 접근할 수 있도록 정보 환경을 설계하는 행위
- **핵심 원칙**: "에이전트 관점에서, in-context로 접근할 수 없는 것은 존재하지 않는다"
- **원문 맥락**: Google Docs, Slack 스레드, 사람 머릿속에 있는 지식은 에이전트에게 보이지 않음 → 레포지토리가 유일한 진실의 원천(single source of truth)이어야 함
- **🧪 실험**: 동일 프로젝트에서 context를 (a) repo 내부에만 배치 vs (b) repo + 외부 wiki 혼합 → 에이전트의 태스크 완료율, 환각(hallucination) 빈도 비교

### 2.2 Static Context (정적 컨텍스트)

- **정의**: 레포지토리에 버전 관리되어 있는 고정 참조 자료 — 아키텍처 스펙, API 계약, 스타일 가이드 등
- **구성요소**: AGENTS.md, 설계 문서, 스키마 정의, 실행 계획(execution plan)
- **🧪 실험**: static context 문서량(100줄 vs 500줄 vs 2000줄)에 따른 에이전트 태스크 정확도 변화 — 과잉 컨텍스트의 성능 저하 임계점(tipping point) 탐색

### 2.3 Dynamic Context (동적 컨텍스트)

- **정의**: 실행 시점에 변하는 정보 — 관측성 데이터(로그, 메트릭, 트레이스), 디렉토리 구조 매핑, CI/CD 파이프라인 상태
- **원문 맥락**: 에이전트에게 브라우저 자동화 도구를 통한 E2E 테스트 접근을 부여하자 정확도가 극적으로 향상
- **🧪 실험**: 에이전트에게 (a) 코드만 제공 vs (b) 코드 + 실시간 로그/메트릭 접근 → 버그 재현·수정 성공률 비교

### 2.4 AGENTS.md

- **정의**: 레포지토리 루트에 위치하는 에이전트용 README — 빌드 명령, 테스트 커맨드, 코딩 규칙, 아키텍처 제약, 주요 실패 패턴을 기술
- **원문 맥락**: OpenAI는 AGENTS.md를 "백과사전"이 아닌 "목차(table of contents)"로 취급. ~100줄의 짧은 맵에서 심층 문서로 포인터를 제공
- **핵심 운용 원칙**: "에이전트가 실수할 때마다 그 실수가 재발하지 않도록 AGENTS.md를 업데이트한다" (Hashimoto)
- **🧪 실험**: AGENTS.md 업데이트 빈도(에이전트 실수 후 즉시 vs 주 1회 배치)에 따른 동일 유형 실수 재발률 추적

### 2.5 Repository as Single Source of Truth (레포지토리 = 유일한 진실의 원천)

- **정의**: 에이전트가 참조하는 모든 지식이 버전 관리되는 레포지토리 내부에 존재해야 한다는 원칙
- **원문 맥락**: "Slack에서 아키텍처 패턴에 합의했다면, 에이전트가 발견할 수 없으면 3개월 후 합류한 신입 사원에게도 알려지지 않는 것과 같다"
- **🧪 실험**: 아키텍처 의사결정을 (a) Slack에서만 기록 vs (b) ADR(Architecture Decision Record)로 repo 커밋 → 3개월 후 에이전트의 해당 결정 준수율 비교

### 2.6 In-Repository Knowledge Store (레포 내 지식 저장소)

- **정의**: 레포지토리 내 docs/ 디렉토리에 구조화된 지식 베이스 — 검증 상태, 핵심 신념(core beliefs), 도메인별 설계 문서 포함
- **구성**: Architecture Documentation (도메인 맵, 패키지 레이어링), Quality Document (도메인/레이어별 품질 등급, 시간 추적)
- **🧪 실험**: knowledge store를 (a) 마크다운 flat files vs (b) JSON 구조화 vs (c) 하이브리드 → 에이전트의 참조 정확도, 부적절 수정(overwrite) 빈도 비교. Anthropic 팀은 JSON이 마크다운보다 에이전트의 부적절 편집 방지에 효과적이었다고 보고

---

## 3. Architectural Constraints 계열

### 3.1 Dependency Layering (의존성 레이어링)

- **정의**: 코드 모듈 간 의존 방향을 엄격하게 단방향으로 강제하는 아키텍처 제약
- **OpenAI 레이어 순서**: `Types → Config → Repo → Service → Runtime → UI`
- **원문 맥락**: 각 레이어는 자기 왼쪽 레이어만 import 가능. "제안"이 아닌 구조적 테스트와 CI 검증으로 강제
- **🧪 실험**: 레이어 제약을 (a) 문서로만 명시 vs (b) CI 린터로 강제 → 에이전트의 의존성 위반 빈도 비교. 제약 강제가 없는 경우 entropy 축적 속도 측정

### 3.2 Mechanical Enforcement (기계적 강제)

- **정의**: 아키텍처 규칙을 프롬프트나 문서가 아닌 결정론적 도구(린터, 구조 테스트, pre-commit hook)로 강제하는 접근
- **원문 맥락**: "인간 중심 워크플로에서는 이런 규칙이 시시콜콜하게 느껴질 수 있다. 에이전트에게는 승수(multiplier)가 된다 — 한번 인코딩하면 모든 곳에 즉시 적용"
- **🧪 실험**: 동일 규칙을 (a) AGENTS.md 자연어 기술 vs (b) custom linter 강제 → 500 PR 이후 규칙 준수율 비교

### 3.3 Custom Linter (커스텀 린터)

- **정의**: 프로젝트 고유의 아키텍처 규칙을 검증하는 맞춤 정적 분석 도구
- **원문 맥락**: OpenAI의 커스텀 린터는 Codex가 직접 생성. 에러 메시지가 단순 위반 표시가 아닌 수정 방법 가이드(remediation instruction) 역할
- **🧪 실험**: 린터 에러 메시지를 (a) 일반적 위반 표시 vs (b) 구체적 수정 지침 포함 → 에이전트의 1차 수정 성공률(first-fix rate) 비교

### 3.4 Structural Tests (구조적 테스트)

- **정의**: 코드의 기능이 아닌 구조(모듈 경계, 의존 방향, 네이밍 규칙)를 검증하는 테스트
- **유사 도구**: Java의 ArchUnit과 동일 개념이지만 AI 생성 코드에 최적화
- **🧪 실험**: 구조적 테스트 도입 전후 6개월간 아키텍처 드리프트(drift) 속도 비교 — 도메인 경계 위반, 순환 의존성 발생 건수 추적

### 3.5 Constraint Paradox (제약의 역설)

- **정의**: 에이전트의 솔루션 공간을 제한하면 오히려 생산성이 향상되는 현상
- **원문 맥락**: "에이전트가 아무거나 생성할 수 있으면 토큰을 막다른 길 탐색에 낭비한다. 하네스가 명확한 경계를 정의하면 에이전트는 올바른 해에 더 빨리 수렴"
- **🧪 실험**: 동일 코딩 태스크에 (a) 제약 없음 vs (b) 아키텍처 제약 3종 vs (c) 아키텍처 + 스타일 + 네이밍 전체 제약 → 완료 시간, 토큰 소비량, 코드 품질 비교. 과잉 제약(over-constraint)의 역효과 임계점 탐색

---

## 4. Entropy Management 계열

### 4.1 Entropy Management / Garbage Collection (엔트로피 관리)

- **정의**: AI 생성 코드베이스에 시간이 지나며 축적되는 불일치, 드리프트, 죽은 코드를 주기적으로 정리하는 시스템
- **원문 맥락**: 문서-코드 불일치, 네이밍 규칙 이탈, 불필요 의존성 등을 자동 스캔하는 에이전트가 일/주/이벤트 트리거로 실행
- **🧪 실험**: garbage collection 에이전트를 (a) 미적용 vs (b) 주 1회 vs (c) 매일 실행 → 3개월 후 코드베이스의 "문서-코드 일치도", dead code 비율, 순환 의존성 수 비교

### 4.2 Documentation Consistency Agent (문서 일관성 에이전트)

- **정의**: 코드 변경 후 관련 문서가 실제 코드와 일치하는지 검증·수정하는 주기적 에이전트
- **원문 맥락**: AGENTS.md 자체도 이 에이전트가 관리 — "documentation for agents, by agents"
- **🧪 실험**: 의도적으로 코드와 불일치하는 문서 20건을 주입 → 에이전트 발견율, 오탐율, 자동 수정 정확도 측정

### 4.3 Pattern Enforcement Agent (패턴 강제 에이전트)

- **정의**: 확립된 코딩 패턴에서 벗어난 코드를 식별·수정하는 에이전트
- **🧪 실험**: 100개 PR 중 의도적으로 삽입된 패턴 위반 10건의 detection rate 측정. False positive(정상 코드를 위반으로 판단) 비율 동시 추적

### 4.4 Stale Documentation Detection (부실 문서 탐지)

- **정의**: 레포 내 문서 중 현재 코드베이스와 괴리가 발생한 문서를 자동 탐지하는 메커니즘
- **원문 맥락**: OpenAI의 백그라운드 에이전트가 부실 문서를 스캔하고 정리 PR을 자동 오픈
- **🧪 실험**: 문서 신선도(freshness) 메트릭 정의 → (최종 수정일 - 관련 코드 최종 수정일) 기반 부실도 점수화 → 부실도와 에이전트 태스크 실패율 상관분석

---

## 5. Agent Workflow & Orchestration 계열

### 5.1 Agent Loop (에이전트 루프)

- **정의**: 에이전트가 태스크를 받아 실행하는 핵심 반복 사이클 — prompt 해석 → 계획 → 실행 → 검증 → PR 제출
- **원문 맥락**: Codex App Server가 이 루프를 표준 프로토콜로 노출 — CLI, IDE 확장, 웹앱이 동일 하네스 사용
- **🧪 실험**: 루프 내 각 단계의 소요 시간·토큰 분포 프로파일링 → 병목 단계 식별

### 5.2 Attended Parallelization (유인 병렬화)

- **정의**: 인간이 여러 에이전트 세션을 동시에 적극 관리하며 필요시 개입하는 작업 방식
- **원문 맥락**: Peter Steinberger(OpenClaw)가 5–10개 에이전트를 동시 운용하는 방식
- **🧪 실험**: 동시 에이전트 수(1, 3, 5, 10)에 따른 인간 엔지니어의 인지 부하(cognitive load) 측정 — 오류 개입 지연 시간, 컨텍스트 스위칭 비용

### 5.3 Unattended Parallelization (무인 병렬화)

- **정의**: 인간이 태스크를 위임한 후 완료·리뷰 시점까지 개입하지 않는 방식
- **원문 맥락**: Stripe Minions — Slack에 태스크 게시 → CI 통과 → PR 오픈까지 인간 개입 제로
- **🧪 실험**: attended vs unattended 조건에서 동일 유형 태스크 50건 → 코드 품질, 리뷰 리젝률, 총 소요시간 비교

### 5.4 Middleware Architecture (미들웨어 아키텍처)

- **정의**: 에이전트 요청/응답 파이프라인에 조합 가능한(composable) 처리 레이어를 삽입하는 설계
- **LangChain 구현**: `LocalContextMiddleware → LoopDetectionMiddleware → ReasoningSandwichMiddleware → PreCompletionChecklistMiddleware`
- **🧪 실험**: 미들웨어 레이어를 하나씩 추가/제거하며 벤치마크 성능 변화 측정 — 어떤 조합이 최적인지 factorial 실험 설계

### 5.5 Reasoning Sandwich (추론 샌드위치)

- **정의**: 계획·검증 단계에는 고수준 추론(high reasoning), 구현 단계에는 중간 수준 추론을 적용하는 전략
- **원문 맥락**: LangChain이 TerminalBench 2.0 성능 도약에 기여한 핵심 기법
- **🧪 실험**: 추론 수준 배분을 (a) 균일 high vs (b) 균일 medium vs (c) sandwich 패턴 → 토큰 비용 대비 정확도 최적점 탐색

### 5.6 Loop Detection (루프 탐지)

- **정의**: 에이전트가 동일 파일을 반복 수정하는 "doom loop"를 탐지·차단하는 메커니즘
- **🧪 실험**: 의도적으로 모호한 요구사항(doom loop 유발)을 주입 → 루프 탐지 유무에 따른 에이전트 행동 차이, 토큰 낭비량 비교

### 5.7 Devbox (개발 샌드박스)

- **정의**: 에이전트가 실행되는 격리된 개발 환경 — 프로덕션, 인터넷과 차단
- **원문 맥락**: Stripe의 Minion이 인간 엔지니어와 동일한 사전 준비된(pre-warmed) 개발 환경에서 실행
- **🧪 실험**: devbox 격리 수준(네트워크 완전 차단 vs 특정 도메인 허용 vs 무제한)에 따른 보안 사고·태스크 완료율 트레이드오프

---

## 6. Human Role 재정의 계열

### 6.1 Environment Designer (환경 설계자)

- **정의**: 코드를 직접 작성하는 대신, 에이전트가 코드를 작성할 수 있는 환경을 설계하는 엔지니어 역할
- **원문 맥락**: "에이전트가 막히면 그것을 환경 설계 문제로 취급 — 어떤 능력이 빠져 있고 어떻게 에이전트에게 legible하고 enforceable하게 만들 것인가?"
- **🧪 실험**: 전통적 개발자 vs 환경 설계자 역할 수행 그룹의 에이전트 활용 효과성 비교 — 동일 기간 PR throughput, 코드 리젝률

### 6.2 Intent Specification (의도 명세)

- **정의**: 에이전트에게 "무엇을 만들 것인가"를 정밀하게 기술하는 행위 — 프롬프트보다 넓은 개념
- **원문 맥락**: 엔지니어가 태스크를 기술하고 에이전트를 실행하면 에이전트가 PR을 오픈하는 흐름
- **🧪 실험**: intent 명세의 정밀도를 3단계(high-level 1줄 / medium 5줄 / detailed 20줄 with acceptance criteria)로 분류 → 에이전트 산출물 품질 비교

### 6.3 Agents Captain (에이전트 캡틴)

- **정의**: 팀 내에서 에이전트 워크플로 최적화를 전담하는 역할
- **원문 맥락**: Greg Brockman의 권고 — "모든 팀이 에이전트 캡틴을 지정하라"
- **🧪 실험**: 에이전트 캡틴이 있는 팀 vs 없는 팀의 6개월 에이전트 활용도, 하네스 성숙도 비교

### 6.4 Benevolent Dictator (선의의 독재자)

- **정의**: 에이전트 산출물의 코드를 읽지 않더라도 아키텍처 일관성을 수호하는 역할
- **원문 맥락**: Steinberger가 OpenClaw에서 수행 — "코드가 아닌 아키텍처와 큰 결정만 논의"
- **🧪 실험**: 아키텍처 가디언 유무에 따른 6개월 코드베이스 구조적 일관성(structural coherence score) 비교

### 6.5 Bullshit Detection (허튼소리 탐지 능력)

- **정의**: 에이전트 산출물이 과도하게 영리하거나, 과도하게 반복적이거나, 장기 유지보수에 문제가 될 패턴을 식별하는 인간의 판단력
- **원문 맥락**: Charlie Guo(Artificial Ignorance) — "산출물 양이 증가할수록 이 능력이 덜 중요해지는 게 아니라 더 중요해진다"
- **🧪 실험**: 에이전트 생성 PR에 의도적 결함(over-abstraction, 불필요 에러 처리, 문서 드리프트) 삽입 → 리뷰어의 결함 탐지율을 경험 수준별 비교

### 6.6 No Manually-Written Code (수동 코드 금지 제약)

- **정의**: 인간이 직접 코드를 작성하지 않는 것을 의도적 제약(forcing function)으로 설정하는 원칙
- **원문 맥락**: OpenAI 팀의 핵심 철학 — 이 제약이 하네스 구축을 강제하고 에이전트 중심 워크플로 성숙을 가속
- **🧪 실험**: "절대 수동 코드 금지" vs "긴급시 수동 개입 허용" 정책 → 하네스 품질, 에이전트 자율성 성장 곡선 비교

---

## 7. Feedback Loop & Verification 계열

### 7.1 Iterative Harness Refinement (반복적 하네스 정련)

- **정의**: 에이전트가 실패할 때 이를 신호로 삼아 빠진 도구·가드레일·문서를 식별하고 다시 레포에 반영하는 사이클
- **원문 맥락**: "에이전트가 어려움을 겪으면 신호로 취급 — 빠진 것이 무엇인지 식별하고 항상 Codex가 직접 수정을 작성하게 한다"
- **🧪 실험**: 실패 → 하네스 업데이트의 반응 시간(minutes vs hours vs days)에 따른 동일 유형 실패 재발률 감소 곡선

### 7.2 Linter Error as Remediation Instruction (린터 에러 = 수정 지침)

- **정의**: 린터 에러 메시지가 단순 위반 플래그가 아닌, 에이전트에게 수정 방법을 가르치는 교육 도구로 기능하는 설계
- **원문 맥락**: OpenAI 원문에서 "perhaps the cleverest idea"로 평가된 기법
- **🧪 실험**: 린터 에러 메시지 스타일 3종 비교 — (a) "Violation: X" (b) "Violation: X. Fix by Y" (c) "Violation: X. Fix by Y. Example: Z" → 에이전트 자가 수정 성공률

### 7.3 Self-Verification Loop (자기 검증 루프)

- **정의**: 에이전트가 태스크 완료 전 사전 정의된 체크리스트를 스스로 검증하는 메커니즘
- **원문 맥락**: LangChain의 PreCompletionChecklistMiddleware — 제출 전 에러를 자체 포착
- **🧪 실험**: 자기 검증 체크리스트 항목 수(3, 5, 10, 20)에 따른 (a) 검출률 (b) 위양성 (c) 태스크 완료 지연 트레이드오프

### 7.4 Shift Handoff Pattern (교대 인수인계 패턴)

- **정의**: 새 에이전트 세션이 이전 세션의 작업 상태를 빠르게 파악할 수 있도록 구조화된 진행 파일(progress file)을 남기는 패턴
- **원문 맥락**: Anthropic 팀이 "서로 만난 적 없는 엔지니어 간 교대 인수인계"에 비유. JSON이 마크다운보다 에이전트의 부적절 편집 방지에 효과적
- **🧪 실험**: 인수인계 포맷 3종 비교 — (a) 없음 (b) Markdown (c) JSON → 신규 세션 에이전트의 프로젝트 상태 파악 정확도, 중복 작업 비율

### 7.5 Initializer Agent (초기화 에이전트)

- **정의**: 하이레벨 프롬프트로부터 포괄적 기능 목록(feature list)을 생성하는 전용 에이전트
- **원문 맥락**: Anthropic 접근 — 단일 웹앱 프롬프트에서 200+ 개별 기능을 분해, 각각에 테스트 스텝 명시, 초기 상태 "failing"
- **🧪 실험**: 초기화 에이전트 사용 vs 미사용 → 프로젝트 완성도, 조기 완료 선언(premature victory) 빈도 비교

---

## 8. Scale & Metrics 계열

### 8.1 PR Throughput (PR 처리량)

- **정의**: 에이전트가 단위 시간당 생성·머지하는 Pull Request 수
- **원문 데이터**: OpenAI — 엔지니어 1인당 일 3.5 PR, 팀 확장 후에도 처리량 증가. Stripe — 주 1,000+ 머지 PR
- **🧪 실험**: 하네스 성숙도 단계별(Level 1/2/3) PR throughput 추이 추적 — throughput이 하네스 투자의 ROI 프록시

### 8.2 Agent-Generated Code Ratio (에이전트 생성 코드 비율)

- **정의**: 전체 코드베이스에서 에이전트가 생성한 코드의 비율
- **참고 데이터**: OpenAI 100%, Anthropic 90%+
- **🧪 실험**: 비율 50%, 70%, 90%, 100%에서의 코드 품질, 유지보수 비용 비교

### 8.3 First-Fix Rate (1차 수정 성공률)

- **정의**: 에이전트가 린터/테스트 실패 후 첫 번째 시도에서 올바르게 수정하는 비율
- **🧪 실험**: 린터 에러 메시지 상세도와 first-fix rate의 상관관계 회귀분석

### 8.4 Architectural Coherence Score (아키텍처 일관성 점수)

- **정의**: 코드베이스가 정의된 아키텍처 규칙을 얼마나 잘 준수하는지의 정량 지표
- **측정 방법**: 의존성 위반 수, 순환 참조 수, 네이밍 규칙 위반 수의 가중 합
- **🧪 실험**: 시간에 따른 일관성 점수 추이 — entropy management 에이전트 도입 전후 기울기 변화

### 8.5 Harness Maturity Level (하네스 성숙도 레벨)

- **정의**: 하네스의 완성도를 단계화한 모델
- **NxCode 분류**: Level 1 (Basic: AGENTS.md + pre-commit) → Level 2 (Team: CI 강제 + 공유 프롬프트) → Level 3 (Production: 미들웨어 + 관측성 + 엔트로피 관리)
- **🧪 실험**: 각 레벨에서의 에이전트 자율 작업 성공률 benchmark suite 구축

---

## 9. Cross-Reference: 외부 프레임워크 대응표

| Harness Engineering 용어 | AgentOps (기원 프레임워크) 대응 | 비고 |
|---|---|---|
| Harness | Agent Runtime Environment | OpenClaw/TeamClaws의 운영 환경 |
| AGENTS.md | CLAUDE.md / AgentOps Config | 에이전트 지시 파일 계열 |
| Context Engineering | Context Window Management | MacroLens의 stdout JSON도 context engineering |
| Architectural Constraints | ARIA 제약 체계 | ARIA(Agentic Runtime Intervention & Alignment) |
| Entropy Management | Drift Detection / GC Agent | PicoClaw 경량 에이전트 적용 가능 |
| Iterative Harness Refinement | Experiment Log → Config Update | 책의 "실험 기록" 챕터와 직결 |
| No Manually-Written Code | Claude Code as Central Axis | 책의 핵심 제약 — Claude Code 중심 레포 관리 |
| Shift Handoff Pattern | Multi-session Continuity | TeamClaws v3의 세션 간 상태 전달 |
| Middleware Architecture | Antfarm Orchestration | 뉴스 브리핑 자동화의 파이프라인 구조 |
| PR Throughput | Commit/PR velocity | OpenClaw의 6,600+ commits/month와 직접 비교 |
| Reasoning Sandwich | Compute Budget Allocation | 모델별 추론 비용 최적화 전략 |
| Devbox | GCP/OCI Free-tier VM | 인프라 격리 및 비용 최적화 |

---

## 부록: 실험 우선순위 매트릭스

| 우선순위 | 실험명 | 난이도 | 기대 인사이트 |
|---|---|---|---|
| ★★★ | Constraint Paradox 검증 (3.5) | 중 | 제약과 생산성의 역설적 관계 정량화 |
| ★★★ | AGENTS.md 업데이트 빈도 vs 실수 재발률 (2.4) | 하 | 가장 접근성 높은 harness 개선 효과 측정 |
| ★★★ | Harness 유무 A/B 테스트 (1.1) | 중 | 책의 핵심 주장을 뒷받침하는 기초 데이터 |
| ★★☆ | Linter Error 상세도 vs First-Fix Rate (7.2) | 하 | 즉시 적용 가능한 실무 가이드라인 도출 |
| ★★☆ | Shift Handoff 포맷 비교 (7.4) | 하 | JSON vs Markdown — Anthropic 결과 독립 재현 |
| ★★☆ | Attended vs Unattended 병렬화 (5.2/5.3) | 중 | 팀 규모별 최적 운용 모드 가이드 |
| ★☆☆ | Entropy Management 주기 최적화 (4.1) | 중 | GC 에이전트 실행 빈도의 경제성 분석 |
| ★☆☆ | Static Context 과잉 임계점 (2.2) | 중 | context window 효율의 이론적 한계 탐색 |

---

> **편집 노트**: 이 Glossary는 *Harness Engineering and AgentOps* 교과서의 backbone으로서, 각 챕터가 하나 이상의 glossary 항목을 심층 전개하는 구조로 설계됨. 실험 제안은 3명의 실험자(co-author)가 분담 가능한 단위로 분해됨. Claude Code 레포에 `docs/glossary/` 경로로 커밋 후 AGENTS.md에서 참조 추가 권장.
