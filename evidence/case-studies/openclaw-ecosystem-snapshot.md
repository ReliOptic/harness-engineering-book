# 케이스 스터디: 2026 H1 에코시스템 스냅샷 — Agent-First CLI 도구 등장

**소스:** DR-1.1-OpenClaw-ecosystem.md + FD-2026-03-17-002-cli-renaissance.md
**챕터 참조:** Ch.1 섹션 3 (에코시스템 스냅샷)
**형식:** 2026년 상반기 CLI agent 도구 등장 현황. 수렴 속도가 증거. 서사 없음.

---

## 1. 2026 H1 Agent-First CLI 도구 등장 현황

### 1A. OpenClaw 파생 프레임워크 (2025 후반–2026 H1)

OpenClaw(250,829+ GitHub Stars, Node.js 단일 프로세스, 430K LoC)의 아키텍처 한계를 공통 출발점으로 삼아 독립 개발된 대안 프레임워크들.

| 프레임워크 | 언어 | 핵심 차별점 | GitHub Stars | Agent-First 설계 증거 |
|-----------|------|------------|-------------|----------------------|
| Nanobot | Python | 4K LoC, MCP Native Host, LiteLLM 라우팅 | 33,100+ | JSON 출력 기본, 2분 내 배포 |
| ZeroClaw | Rust | RAM < 5MB, 트레이트 기반 스왑 | 26,700+ | 명시적 화이트리스트, JSON 출력 |
| PicoClaw | Go | RAM < 10MB, 1초 부팅, 단일 바이너리 | 미상 | sqlite-vec 내장, 구조화 메모리 |
| NullClaw | Zig | 678KB 바이너리, RAM < 1MB, 2ms 부팅 | 2,600+ | 18개 내장 도구, 데몬 모드 |
| Moltis | Rust | 46-crate gateway, Docker/Apple 컨테이너 강제 | 2,000+ | 플러그인 마켓플레이스 배제, 공급망 격리 |
| IronClaw | Rust | WASM 역량 기반 샌드박싱, AES-256 암호화 | 9,800+ | 모든 도구 실행을 WASM 컨테이너 격리 |
| TinyClaw | Bun/TS | 큐 기반 멀티에이전트, 8차원 프로바이더 라우팅 | 2,800+ | 비용 기반 동적 모델 라우팅 |

### 1B. 동일 주(2026-03-09 기준) 독립 등장 도구 (FD-002)

| 도구 | 개발자 / 소속 | 특징 | Agent-First 설계 증거 |
|------|-------------|------|----------------------|
| gogcli | Peter Steinberger (OpenClaw 개발자) | Google Workspace 전체 터미널 제어 | Go, JSON 출력 기반 |
| gws | Justin Poehnelt (Google DevRel) | Google Discovery Service 기반, 명령 런타임 자동 생성 | 구조화 출력, 런타임 스키마 |
| mogcli | Jared Palmer (Microsoft CoreAI VP) | Microsoft 365용 CLI | `--json`, `--dry-run` 옵션 포함 |
| Obsidian CLI | Obsidian 팀 | 에이전트용 공식 CLI 공개 | SaaS가 에이전트를 primary user로 명시 |
| agent-browser `--native` | Vercel | Rust 바이너리 + CDP 직접 호출 | Node.js 레이어 제거, 에이전트 직접 제어 |

---

## 2. 공통 설계 패턴

2025 후반–2026 H1에 등장한 agent-first CLI 도구들에서 반복 관찰되는 설계 선택:

| 패턴 | 관찰된 도구 | 설계 의도 |
|------|-----------|---------|
| JSON 출력 기본값 또는 강제 | gogcli, mogcli, ZeroClaw, Nanobot, CLI-Anything | 에이전트 파싱 오버헤드 제거 |
| `--dry-run` 옵션 | mogcli, CLI-Anything(계획 단계) | 에이전트를 신뢰할 수 없는 운영자로 취급, 사전 검증 |
| 단일 정적 바이너리 | PicoClaw, NullClaw, ZeroClaw | 런타임 의존성 없음 → 에이전트가 설치 없이 즉시 실행 |
| 구조화 스키마 자기 서술 | CLI-Anything(`--help`), gws(런타임 자동 생성) | 에이전트가 제로샷으로 도구 사용법 발견 가능 |
| 샌드박싱 / 격리 | Moltis(Docker 강제), IronClaw(WASM), PicoClaw(보안 감사 대상) | 에이전트 실행 권한 통제 |

**공통 전제:** 에이전트를 primary user로 설계. 인간 가독성(색상 코드, 프로그레스 바)보다 기계 파싱 가능성 우선.

---

## 3. 수렴 속도 — 동일 주에 독립적으로 3개 이상 등장

**수렴 이벤트:** 2026-03-09 기준 단일 주(GeekNews Weekly #348 수집 기간) 내에 gogcli, gws, mogcli가 독립적으로 공개.

| 항목 | 값 |
|------|-----|
| 동일 주 내 독립 등장 수 | 3개 (gogcli, gws, mogcli) |
| 개발자 소속 | OpenClaw 생태계 개발자, Google DevRel, Microsoft CoreAI VP |
| 공통 설계 선택 | CLI 기반, JSON/구조화 출력, Go 또는 TypeScript |
| 사전 조율 증거 | 없음 (독립 병렬 개발) |

이 수렴이 증거로 기능하는 방식: 경쟁 관계에 있는 세 생태계(OpenClaw 계열, Google, Microsoft)가 동시에 동일한 설계 방향(에이전트용 CLI + 구조화 출력)으로 이동한 사실은 개별 판단이 아닌 생태계 수준의 수렴 신호. 이 책이 Ch.1에서 "surface 변수가 독립적으로 다뤄져야 하는 이유"를 생태계 증거로 제시하는 데 직접 인용 가능.

---

## 4. 에코시스템의 현재 한계

| 한계 | 관찰 |
|------|------|
| 오케스트레이션 레이어 부재 | 개별 CLI 도구는 다수 등장했으나, 이 도구들을 에이전트들이 조율하는 레이어(harness)는 2026 H1 기준 표준화되지 않음 |
| Harness 없이 도구만 존재 | gogcli/gws/mogcli는 agent-first surface를 제공하나, 에이전트 자원 관리·복원력·관찰 가능성은 각 프레임워크에 위임 |
| 보안 미성숙 | PicoClaw 공식 보안 감사(2026-02)에서 정규식 기반 우회 가능 필터링 확인. 에이전트 실행 격리 표준 미확립. |
| 상호운용성 없음 | MCP vs CLI 논쟁 진행 중(FD-002). 에이전트-도구 프로토콜 표준 없음. |

**이 책의 위치:** 이 에코시스템 스냅샷은 "도구는 생겼지만 harness가 없다"는 상태를 2026 H1 기준으로 기록한다. Ch.1의 "왜 지금인가"(섹션 5)와 Ch.3의 harness 정의 필요성의 배경으로 직접 인용.

---

## 5. 5변수 진단 — 생태계 수준

| 변수 | 2026 H1 상태 |
|------|-------------|
| 모델 | 다양한 선택지 존재 (Claude, GPT-4o, Gemini, 로컬 sLLM) |
| **harness** | **표준 없음. 프레임워크별 제각각 (OpenClaw: 없음 / Moltis: Docker 격리 / IronClaw: WASM / PicoClaw: 보안 취약점 존재)** |
| surface | Agent-first CLI로의 수렴 진행 중 (이 스냅샷이 증거) |
| intervention | Watchdog/AgentOps 레이어 미표준화 |
| compute | 메모리 효율화 경쟁 활발 (1GB → 678KB 바이너리까지) |

**생태계 수준 1차 병목: `harness`** — surface와 모델은 빠르게 발전 중이나, 에이전트 runtime 안정성을 담당하는 harness 레이어가 생태계 표준으로 자리잡지 못한 상태.

---

## 6. Ch.1 섹션 3 인용 좌표

- **직접 인용 가능 수치:** gogcli/gws/mogcli 동일 주 등장, OpenClaw 250,829 Stars, NullClaw 678KB 바이너리
- **연결 FD:** FD-2026-03-17-002 (수렴 사례 상세)
- **연결 DR:** DR-1.1 (프레임워크 비교 상세), DR-1.2 (에이전트 인터페이스 트렌드)
- **다음 섹션 연결:** Ch.1 섹션 5 (왜 지금인가) → 이 스냅샷이 "지금"의 정의

---

*추출 기준: 2026-03-17. 소스: DR-1.1-OpenClaw-ecosystem.md + FD-2026-03-17-002-cli-renaissance.md.*
