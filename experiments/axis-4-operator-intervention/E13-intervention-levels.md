# E13 — Operator 개입 수준별 복구 효과 비교

**Experiment ID**: E13
**Date**: (미정)
**Experimenter**: C
**Cross-validator**: 없음 (단독)
**Target chapter**: Ch.4 (3막), Ch.5 (실험 결과 분석)
**Status**: [ ] 계획 / [ ] 진행중 / [ ] 완료 / [ ] 교차검증 완료

---

## Task

T2 (Multi-Step Reasoning) task를 실행하다가 의도적으로 실패를 유발한 후, 세 가지 수준의 operator 개입을 적용하고 복구 효과를 비교한다.

개입 수준:
- 수준 0: 개입 없음 (agent 자율 진행)
- 수준 1: 힌트 제공 (방향 암시만 제공)
- 수준 2: 직접 개입 (구체적 지시 또는 수동 수정)

---

## 5변수 설정

| 변수 | 설정 |
|------|------|
| **조작 변수** | Intervention 수준 (없음 / 힌트 / 직접) |
| **모델** | claude-sonnet-4-6 via Anthropic API |
| **Harness config** | harness=ON |
| **Surface** | CLI |
| **Compute environment** | GCP e2-micro |
| **Token budget** | T2: 64K |

**통제 변수**: 모델=claude-sonnet-4-6, surface=CLI, harness=ON, task=T2 동일, 실패 유발 조건 동일

---

## 관찰 대상

- 복구 성공률: 개입 수준별 task 완료율
- 복구 소요 시간: 개입부터 task 재개까지의 wall clock time
- 부작용: 개입이 이후 단계에 미치는 의도치 않은 영향
- 개입 효율: 복구 성공률 / 개입 비용 (token + time)

**핵심 가설**: 직접 개입이 힌트 개입보다 즉각적 복구 성공률은 높지만, 이후 단계에서의 부작용(의존성 증가, 자율성 저하)으로 인해 최종 TCR 차이는 예상보다 작다.

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

| 개입 수준 | 복구 성공률 | 복구 소요 시간 | 부작용 발생 | 최종 TCR |
|----------|-----------|-------------|-----------|---------|
| 수준 0 (없음) | | | | |
| 수준 1 (힌트) | | | | |
| 수준 2 (직접) | | | | |

---

## 분석

### Primary bottleneck
**1차 병목**:
**근거**:

### Balloon effect
[ ] 관찰됨 / [ ] 관찰 안 됨

---

## 측정값

| 지표 | 수준 0 | 수준 1 | 수준 2 |
|------|--------|--------|--------|
| Token usage (input) | | | |
| Token usage (output) | | | |
| 실행 시간 | | | |
| 비용 (API) | | | |
| 개입 token 비용 | | | |

---

## Human Intervention

**개입 여부**: [ ] 없음 / [ ] 있음
**개입 종류**: 실험 설계상 의도된 개입 (수준별 비교)
**개입 효과**: (실행 후 기록)

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

- Fig 5 — Intervention Effectiveness Matrix: 개입 수준 × 실패 유형 × 복구 성공률
