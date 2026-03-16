# FD-2026-03-17-002: CLI의 귀환 — GN#348이 기록한 생태계 이동

**Date:** 2026-03-17
**Reporter:** Kiwon
**Source:** GeekNews Weekly #348 (2026-03-09), https://news.hada.io/weekly/202610
**Category:** ECOSYSTEM_SHIFT
**챕터 연관:** Ch.1, Ch.3, Ch.6, Ch.7 (커누스+Opus / Autoresearch — self-immune 외부 좌표)

---

## 무슨 일이 일어났는가

GeekNews Weekly #348 "AI 에이전트가 불러낸 CLI의 귀환"은 2026년 3월 첫째 주 한 주간의 기록이지만, 단일 트렌드가 이 정도 밀도로 수렴한 것은 이례적이다. 필자가 Ch.3과 DR-3.2에서 CLI-Anything 분석을 통해 도달한 결론—"에이전트에게 CLI가 최선의 surface다"—이 같은 시점에 독립적으로 여러 방향에서 확인되고 있다.

**수렴 사례 목록 (일주일 사이에 등장한 것들):**

- Obsidian이 에이전트용 CLI 공개 — SaaS 서비스가 에이전트를 primary user로 인식한 첫 주요 사례
- OpenClaw 개발자 Peter Steinberger의 **gogcli** — Google Workspace 전체를 터미널에서 직접 제어, JSON 출력 기반, Go 작성
- Google DevRel Justin Poehnelt의 **gws** — Google Discovery Service 기반으로 명령을 런타임에 자동 생성하는 CLI
- Microsoft CoreAI VP Jared Palmer의 **mogcli** — Microsoft 365용 CLI, `--json`/`--dry-run` 옵션 포함
- Vercel의 **agent-browser** `--native` 기능 — Rust 바이너리 + CDP 직접 호출, Node.js 레이어 제거

한 주 사이에 Google, Microsoft, Vercel, 그리고 OpenClaw 생태계 개발자가 동시에 "에이전트를 위한 CLI"를 만들고 있다는 사실 자체가 신호다. 이는 개별 판단이 아니라 생태계 수렴이다.

---

## 핵심 논쟁: MCP vs CLI

"MCP는 죽었다. CLI 만세"라는 글이 이 시점에 등장한 것은 우연이 아니다. 요지: LLM은 이미 CLI 환경에 익숙하고, 별도 서버나 인증 체계 없이 대부분의 작업을 수행할 수 있으며, 인간과 동일한 명령으로 실행·디버깅이 가능하다. CLI는 조합성과 인증, 권한 제어 면에서 안정적이고, MCP 서버 구축보다 API와 CLI 제공에 집중하는 편이 유지보수성이 높다.

"AI 에이전트를 위해선 CLI를 다시 작성해야 합니다"는 한 걸음 더 나간다: 인간 중심 CLI와 에이전트 중심 CLI의 **설계 철학이 근본적으로 다르다**. 에이전트용 CLI는 중첩 JSON 입력을 자연스럽게 처리하고, 설명 문서 대신 기계가 읽을 수 있는 스키마와 구조화된 출력을 제공해야 한다. 또한 에이전트를 신뢰할 수 없는 운영자로 보고 웹 API처럼 입력 검증·샌드박싱·`--dry-run` 방어 장치를 CLI 수준에서 구현해야 한다.

이 논쟁은 이 책의 5변수 프레임워크에서 **surface 변수**가 왜 독립적으로 다뤄져야 하는지를 생태계 스스로 증명하는 장면이다. CLI-Anything(DR-3.2)이 기술적으로 분석한 내용을 업계가 실천 차원에서 독립적으로 도달하고 있다.

---

## 공급망 위협: 프롬프트 인젝션이 재귀적 공격으로

"GitHub 이슈의 제목을 이용해 4,000대 개발자 머신이 감염됨"은 이 주 가장 구조적으로 무거운 사례다.

경위: GitHub 이슈 제목에 삽입된 프롬프트 인젝션 명령 → Cline의 AI 이슈 분류 봇에 주입 → npm 토큰 탈취 및 악성 패키지 배포 → Cline이 또 다른 AI 에이전트(OpenClaw)를 설치하도록 조작.

GN#348은 이를 "AI가 AI를 설치하는 재귀적 공급망 위협의 첫 실제 사례"로 규정했다. CI/CD 환경에서 비신뢰 입력과 비밀 접근권이 결합될 때 발생하는 구조적 위험이다.

Ch.3에서 harness의 기능 중 하나로 "신뢰 경계 관리"를 다루는데, 이 사건은 그 필요성을 실증한다. 에이전트가 실행 권한을 가진 상태에서 외부 입력을 그대로 처리할 때 harness 없이 운영하는 것이 어떤 결과를 낳는지 보여주는 실제 사례로 인용 가능하다.

---

## 에이전틱 엔지니어링 패턴 (Simon Willison)

*Agentic Engineering Patterns* — 코드 작성 비용이 급격히 낮아진 시대에 맞는 엔지니어링 원칙 모음. 단순한 코드 생성이 아니라, 테스트·리뷰·프롬프트 설계 등 에이전트 중심 개발의 품질 관리 구조를 다룬다.

이 책의 Ch.5 (실험 결과에서 배운 것)와 직접 비교 좌표가 될 수 있다. Willison이 코드 생성 관점에서 정리한 패턴과, 이 책이 agent 운영 관점에서 정리한 패턴이 어디서 겹치고 어디서 다른지를 Ch.5 집필 시 명시적으로 좌표화할 필요가 있다.

---

## Context Mode: 컨텍스트 소비 98% 절감 MCP 서버

Claude Code의 MCP 도구 호출 과정에서 발생하는 대량의 원시 출력 데이터를 98%까지 압축. 샌드박스 구조로 각 실행을 격리하고 stdout만 전달. SQLite FTS5 기반 지식베이스로 마크다운 문서 인덱싱. 결과: 동일한 200K 토큰 한도에서 세션 지속 시간 3배 이상.

이는 이 책의 compute 변수와 token efficiency 섹션(Ch.5, 섹션 4)에 직접 인용 가능한 현장 수치다. "어떤 harness 기능이 compute 제약을 완화하는가"라는 질문에 대한 구체적 구현 사례.

---

## 도널드 커누스 + Claude Opus 4.6

커누스가 직접 풀지 못했던 조합론 미해결 문제(방향 그래프 해밀토니안 사이클 분해)를 Claude Opus 4.6이 31회의 파이썬 탐색과 자체 피드백 루프를 거쳐 해결. 커누스는 이를 "자동 연역과 창의적 탐구의 결합"으로 평가.

Ch.7 (self-immune system, Agent-2 전환)의 맥락에서: 에이전트가 외부 harness의 도움 없이 자체 피드백 루프를 구성하여 문제를 해결한 사례. 단, 이것이 **harness 없는 성공**인지 아니면 **Claude Code 자체가 harness 역할을 한 것**인지 구분이 필요하다. 스냅샷 마커로 기록해두고 Ch.7 집필 시 재검토.

---

## 우리 책과 어떻게 연결되는가

### 책 보강: 기존 챕터에 직접 삽입 가능

**Ch.1 (생태계 스냅샷 섹션):**
이 주의 CLI 수렴 사례들은 "2026년 상반기 생태계 스냅샷"에 직접 삽입 가능하다. OpenClaw 주변 프로젝트들의 레퍼런스로 gogcli, gws, mogcli를 명시하고, "SaaS까지 에이전트용 CLI를 고민하기 시작했다"는 흐름의 증거로 쓴다.

**Ch.3 (surface 변수 정의):**
- CLI가 에이전트에게 최선의 surface인 이유를 이 주의 논쟁들이 실천 차원에서 확인해주고 있다
- DR-3.2(CLI-Anything)가 기술적으로 도달한 결론을 업계가 독립적으로 수렴하고 있다는 관찰 추가
- 에이전트 친화적 CLI 설계 원칙 (중첩 JSON 입력, 스키마 인트로스펙션, `--dry-run`) → harness가 surface와 맞닿는 경계 설계 원칙으로 연결

**Ch.4/5 (실험 및 결과 분석):**
- GitHub 프롬프트 인젝션 사례 → harness 없는 에이전트 운영의 보안 비용 실증 사례 (E-시리즈 중 보안 실험 설계 시 참조)

**Ch.6 (Fieldkit):**
- Context Mode 98% 절감 → compute 제약을 harness로 완화하는 구체적 패턴
- `--dry-run`, `--output json` 같은 점진적 도입 권고는 Fieldkit 설계 원칙과 직접 일치

### 책 확장 필요: 기존 챕터를 넓혀야 하는 것

**Ch.2 (모델 변수):**
- Qwen3.5-Medium이 로컬에서 Claude Sonnet 수준의 성능에 도달했다는 보고 → 모델 변수가 고정되어 있지 않고, 로컬/클라우드 경계가 실질적으로 이동하고 있음을 반영해야 한다
- Karpathy의 Autoresearch — 에이전트가 자신의 학습 코드를 직접 수정하는 자율 루프 → Ch.7(self-immune) 집필 전에 이 사례와의 좌표 정렬이 필요하다

**Ch.7 (self-immune):**
- 커누스+Opus 4.6 사례는 이미 이 dispatch에서 다뤘으나, Karpathy Autoresearch와 함께 "외부 harness 없는 자율 루프"와 "harness 내재화"의 경계를 Ch.7에서 명확히 정의할 필요가 있다

### 책의 빈자리: 현재 어느 챕터에도 없는 것

**인간/조직 차원** — GN#348에는 이 책이 현재 다루지 않는 영역이 밀집해 있다:
- "AI가 코딩을 쉽게, 엔지니어링은 더 어렵게 만들었다"
- "AI가 주니어 개발자를 쓸모없게 만들고 있다"
- "60살인데요. Claude Code 덕분에 다시 열정이 불타오른다"
- "엔지니어링 매니저가 되지 마세요" / "단순함으로는 승진하지 못한다"

이 책의 독자는 에이전트를 운영하는 실무자이면서, 동시에 이 변화 속에서 자신의 역할을 재정의하려는 사람이다. 위의 질문들은 독자가 하루에도 한 번씩 마주치는 현실이다. 이것이 새 챕터를 요구하는가, Preface나 Ch.1에서 짧게 다뤄야 하는가는 Ch.1/Preface 집필 시 판단한다. 기록만 해두고 무시하면 독자와의 거리가 생긴다.

> **참고:** GN#348 전체 아이템의 폭넓은 분류와 테마별 분석은 `FD-2026-03-17-002-wide-survey.md`를 참조.

---

## 즉시 행동이 필요한가

- [x] 기록만 해두면 됨 (Ch.1/3/5/6 집필 시 참조)
- [ ] Ch.3 집필 시 gogcli/gws/mogcli를 surface 변수의 현장 증거로 인용
- [ ] Ch.3 집필 시 "MCP vs CLI" 논쟁을 harness surface 선택 맥락에서 좌표화
- [ ] Ch.3/4 집필 시 GitHub 프롬프트 인젝션 사례를 harness 보안 필요성의 실증으로 인용
- [ ] Ch.5 집필 시 Willison의 *Agentic Engineering Patterns*와 비교 좌표 명시
- [ ] Ch.7 집필 시 커누스+Opus 4.6 사례 재검토 (자체 루프 vs harness 지원 성공의 구분)

---

## Tags

`#CLI` `#surface` `#ecosystem` `#security` `#prompt-injection` `#compute` `#harness` `#MCP` `#AgentOps`
