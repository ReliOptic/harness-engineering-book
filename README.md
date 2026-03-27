# Harness Engineering and AgentOps

<p>
  <em>Observing What Makes Agents Work — and What Breaks Them</em>
</p>

<p>
  <img alt="Live Draft" src="https://img.shields.io/badge/Manuscript-Live%20Draft-0f766e">
  <img alt="Language" src="https://img.shields.io/badge/Primary%20Language-Korean-1d4ed8">
  <img alt="Domain" src="https://img.shields.io/badge/Focus-Agent%20Runtime%20Operations-7c3aed">
  <img alt="Method" src="https://img.shields.io/badge/Method-Deliberate%20Failure%20Experiments-b45309">
</p>

2026년 상반기 agent runtime은 이미 실전에 들어와 있지만, 실패는 여전히 재현 가능하게 설명되지 않는다.  
이 프로젝트는 "모델이 문제인가, harness가 문제인가"라는 이원론 대신, 아래 질문 하나를 실험으로 추적한다.

> **어떤 조건에서 무엇이 1차 병목이 되는가?**

---

## What This Book Is

- 현장 관찰 + 실험 로그 기반의 기술서
- 5변수 프레임워크(모델, harness, surface, intervention, compute)로 병목을 분해하는 작업
- 실패를 제거하는 책이 아니라, 실패를 **관찰 가능/복구 가능**한 형태로 바꾸는 설계 원칙을 정리하는 작업

앵커 레퍼런스:
- OpenAI, *Harness Engineering: Leveraging Codex in an Agent-First World* (2026)
- Chip Huyen, *AI Engineering* (2025)

---

## Five-Variable Framework

| Variable | 질문 |
| --- | --- |
| `Model` | 모델 고유 특성이 실패를 직접 만들었는가? |
| `Harness` | 운영 경계(권한/복구/메모리)가 실패를 증폭 또는 완화했는가? |
| `Product Surface` | CLI/API/IDE surface가 agent 행동을 어떻게 유도했는가? |
| `Operator Intervention` | 인간 개입이 언제 도움이 되고 언제 오히려 오염을 만들었는가? |
| `Compute/Resource Budget` | CPU/RAM/token/cost 제약이 다른 변수를 압도했는가? |

---

## Book Structure

| Chapter | Focus |
| --- | --- |
| `Preface` | 왜 이 책이 필요한가, 무엇을 다루고 무엇을 다루지 않는가 |
| `Ch.1` | 2026 상반기 agent runtime 생태계 스냅샷 |
| `Ch.2` | Agent가 모델로부터 물려받는 특성 측정 |
| `Ch.3` | Harness Engineering + AgentOps 정의와 실험 프레임 |
| `Ch.4` | 의도적 실패 실험(E01-E22) 실행 기록 |
| `Ch.5` | 실험 결과를 운영 실무로 번역 |
| `Ch.6` | 반복 실패를 운영 규칙으로 컴파일(Operational Compiler) |
| `Ch.7` | Harness 내재화와 self-immune system 가능성 |

상세 목차: [`list-of-contents-final.md`](./list-of-contents-final.md)

---

## Repository Map

| Path | Description |
| --- | --- |
| [`writing-plan.md`](./writing-plan.md) | 집필 전략/마일스톤/결정 로그 (single source of truth) |
| [`chapter-map.md`](./chapter-map.md) | 챕터별 목적, 질문, 학습 결과 |
| [`chapters/`](./chapters) | 챕터 원고 |
| [`experiments/`](./experiments) | E01-E22 실험 설계 및 로그 |
| [`field-dispatches/`](./field-dispatches) | 현장 관찰 dispatch |
| [`evidence/`](./evidence) | 사례/근거 자료 |
| [`deep-research/`](./deep-research) | 조사 메모 및 링크 (원문 추적용) |
| [`operational-compiler/`](./operational-compiler) | 규칙 컴파일 설계 |
| [`.claude/`](./.claude) | 프로젝트 전용 집필 워크플로(명령/에이전트) |

---

## Reading Paths

### 1) 빠른 이해 (30분)
1. [`writing-plan.md`](./writing-plan.md) — 문제 정의와 방법
2. [`chapter-map.md`](./chapter-map.md) — 전체 구조
3. [`chapters/ch04-deliberate-failure-experiments.md`](./chapters/ch04-deliberate-failure-experiments.md) — 실험 중심 장

### 2) 실무 적용
1. `Ch.3` 정의
2. `Ch.4` 실패 패턴
3. `Ch.5` 운영 번역
4. [`operational-compiler/`](./operational-compiler) 설계 노트

---

## Current Mode

이 저장소는 완성본이 아니라 **live manuscript**다.  
문서/실험/정의는 동기화되며, 섹션 단위로 갱신된다.

검토 시 우선순위:
1. 주장-근거 연결이 충분한가
2. 실험 ID와 수치가 정확한가
3. 용어 정의가 챕터 간 일관적인가

---

## Contributing Evidence

새로운 관찰, 반례, 또는 재현 로그가 있다면 이슈로 보내주세요.

- 어떤 조건에서 실패했는지
- 5변수 중 무엇이 1차 병목이었는지
- 재현 가능 단서(로그/명령/환경)

질문보다 **증거**가 이 프로젝트에 더 큰 기여를 만든다.
