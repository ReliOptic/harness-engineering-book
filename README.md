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

- 현장 관찰 + 의도적 실패 실험 22개 기반의 기술서
- Harness 중심 분석 구조로 병목을 분해하는 작업 — 모델 능력(inbound), 실행 환경 제약(boundary), 사용자 접점(outbound), 피드백 루프(return)의 네 영역
- 실패를 제거하는 책이 아니라, 실패를 **관찰 가능/복구 가능**한 형태로 바꾸는 설계 원칙을 정리하는 작업

---

## Chapters

### Part I — Agent Runtime의 기술적 전제

| Chapter | Title | Focus |
| --- | --- | --- |
| Ch.1 | Context Window의 구조적 한계 | Attention, KV Cache, context window가 agent 실행에 부과하는 물리적 제약 |
| Ch.2 | 정보이론과 토큰 경제 | 토큰 단위 압축, 정보 손실, token budget이 agent 행동에 미치는 영향 |
| Ch.3 | 학습된 정렬이 Runtime에서 깨지는 지점 | RLHF/DPO 정렬이 자율 실행 환경에서 어떻게 균열을 일으키는가 |
| Ch.4 | 도구 사용, 추론, 기억의 실패 경로 | Tool call, multi-step reasoning, memory의 구체적 실패 메커니즘 |

### Part II — Harness와 AgentOps

| Chapter | Title | Focus |
| --- | --- | --- |
| Ch.5 | 지금 무엇이 일어나고 있는가: Harness의 좌표 | 2026년 상반기 agent runtime 생태계 스냅샷과 harness 중심 분석 구조 |
| Ch.6 | Agent가 모델로부터 물려받는 것 | 모델 능력 측정, 비선형 성능 급락, task별 최소 모델 능력 임계점 |
| Ch.7 | Harness Engineering과 AgentOps의 정의 | 운영 경계, 실패 재분류, harness overhead와 MTTR 운영 지표 |

### Part III — 실험

| Chapter | Title | Focus |
| --- | --- | --- |
| Ch.8 | 의도적 실패 실험 22개 | E01~E22 실험 설계, 실행, 결과 기록 (반례 E19/E20 포함) |
| Ch.9 | 실험 결과에서 배운 것 | 실험실 metric → 운영 metric → 비용 metric 3단계 번역, component ablation |

### Part IV — 운영 구조

| Chapter | Title | Focus |
| --- | --- | --- |
| Ch.10 | 관찰에서 Operational Compiler로 | 반복 실패를 운영 규칙으로 컴파일하는 점진적 구조 |
| Ch.11 | Harness에서 Agent Self-immune으로 | 자가 모니터링, 성능 급락 근접 감지, 자기 주도적 복구의 가능성과 한계 |

---

## Repository Map

| Path | Description |
| --- | --- |
| [`list-of-contents.md`](./list-of-contents.md) | 전체 상세 목차 (섹션 단위) |
| [`chapter-map.md`](./chapter-map.md) | 챕터별 목적, 핵심 질문, 학습 결과 |
| [`chapters/`](./chapters) | 챕터 원고 (한국어) |
| [`experiments/`](./experiments) | E01~E22 실험 설계, runbook, 결과 데이터 |
| [`evidence/`](./evidence) | 사례 분석, 관찰 로그, 실패 패턴 기록 |
| [`deep-research/`](./deep-research) | 조사 메모 및 외부 연구 참조 |
| [`dialogue/`](./dialogue) | 챕터별 집필 대화 기록 |
| [`operational-compiler/`](./operational-compiler) | Operational Compiler 설계 노트 |
| [`field-dispatches/`](./field-dispatches) | 현장 관찰 dispatch |

---

## Key Concepts

- **Harness**: agent의 실행을 감싸는 운영 구조. 관찰, 통제, 복구, 자원 관리를 agent에 점진적으로 주입한다.
- **AgentOps**: 비결정적 agent runtime을 관찰, 통제, 복구, 자원인식적으로 운영하는 규율.
- **Operational Compiler**: 반복 실패와 intervention rule을 운영 규칙으로 컴파일하는 구조.
- **Agent-1 / Agent-2**: Agent-1은 외부 harness 의존, Agent-2는 자가 모니터링과 복구를 내재화한 단계.

---

## Current Status

이 저장소는 완성본이 아니라 **live manuscript**다.
Beta 마감: 2026-04-30. 한국어 초고 우선, 이후 영어 번역.

---

## Contributing Evidence

새로운 관찰, 반례, 또는 재현 로그가 있다면 이슈로 보내주세요.

- 어떤 조건에서 실패했는지
- 네 영역(inbound/boundary/outbound/return) 중 무엇이 1차 병목이었는지
- 재현 가능 단서(로그, 명령, 환경)
