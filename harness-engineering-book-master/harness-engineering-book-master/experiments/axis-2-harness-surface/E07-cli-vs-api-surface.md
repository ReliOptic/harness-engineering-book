# E07 — CLI vs. API surface 비교 실험

**Experiment ID**: E07
**Date**: (미정)
**Experimenter**: A
**Cross-validator**: 없음 (단독)
**Target chapter**: Ch.3 (Harness+AgentOps 정의), Ch.4 (1막)
**Status**: [ ] 계획 / [ ] 진행중 / [ ] 완료 / [ ] 교차검증 완료

---

## Task

T1 (Code Review) 및 T2 (Multi-Step Reasoning) task를 CLI surface와 API surface에서 각각 실행한다.
Task 정의: `experiments/design-specification.md §1` 기준.

---

## 5변수 설정

| 변수 | 설정 |
|------|------|
| **조작 변수** | Surface (CLI vs. API) |
| **모델** | claude-sonnet-4-6 via Anthropic API |
| **Harness config** | harness=ON (동일 구성) |
| **Surface** | CLI (Claude Code CLI) vs. API (Anthropic direct API) |
| **Compute environment** | GCP e2-micro |
| **Token budget** | T1: 32K / T2: 64K |

**통제 변수**: 모델=claude-sonnet-4-6, harness=ON 동일 구성, token budget 동일, task 동일

---

## 관찰 대상

- 입출력 안정성 차이: parsing 오류 / format 불일치 빈도
- 실패 성격 차이: CLI-specific failure vs. API-specific failure
- tool call 동작 차이: surface에 따른 tool 가용성 및 결과 포맷 차이
- 동일 task에서 surface가 TCR에 미치는 독립적 영향

**핵심 가설**: CLI surface에서 발생하는 실패의 상당수는 API surface에서 재현되지 않으며, 그 역도 성립한다 — surface는 독립적인 실패 원인 변수다.

---

## 실행 기록

### Tool usage
- 사용한 tool: (실행 후 기록)
- tool call 횟수:
- tool call 성공률:

### 실행 로그 요약
(실행 후 기록)

---

## 결과

**Success / Failure**: [ ] 성공 / [ ] 실패 / [ ] 부분 성공

**Failure type**:

| surface | TCR (T1) | TCR (T2) | 주요 실패 유형 | parsing 오류 빈도 |
|---------|----------|----------|-------------|----------------|
| CLI | | | | |
| API | | | | |

---

## 분석

### Primary bottleneck
**1차 병목**:
**근거**:

### Balloon effect
[ ] 관찰됨 / [ ] 관찰 안 됨

---

## 측정값

| 지표 | CLI | API |
|------|-----|-----|
| Token usage (input) | | |
| Token usage (output) | | |
| 실행 시간 | | |
| 비용 (API) | | |
| format 오류 횟수 | | |

---

## Human Intervention

**개입 여부**: [ ] 없음 / [ ] 있음

---

## Recovery

**복구 시도**: [ ] 없음 / [ ] 있음

---

## Lesson Learned

(실행 후 기록)

---

## 교차검증 메모

교차검증 없음 (단독 실험).

---

## 관련 Figure

- Fig 3 — Surface Comparison: CLI vs. API 실패 성격 분포 및 TCR 비교
