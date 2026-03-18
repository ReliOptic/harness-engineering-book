# E12 — Self-immune 시스템의 compute overhead 측정

**Experiment ID**: E12
**Date**: (미정)
**Experimenter**: B
**Cross-validator**: 없음 (단독)
**Target chapter**: Ch.7 (Self-immune), Ch.5 (실험 결과 분석)
**Status**: [ ] 계획 / [ ] 진행중 / [ ] 완료 / [ ] 교차검증 완료

---

## Task

E18에서 구현할 mini self-immune 시스템의 compute overhead를 사전에 측정한다.
harness 기능별 overhead 분해: monitoring / recovery / self-reporting 각각의 token 및 시간 비용.

---

## 5변수 설정

| 변수 | 설정 |
|------|------|
| **조작 변수** | Harness overhead under constraint (compute 제약 조건에서 harness 자체의 비용) |
| **모델** | claude-sonnet-4-6 via Anthropic API |
| **Harness config** | 기능별 분해: monitoring-only / recovery-only / self-reporting-only / 통합 |
| **Surface** | CLI |
| **Compute environment** | GCP e2-micro |
| **Token budget** | T1: 32K (제약 조건에서 측정) |

**통제 변수**: 모델=claude-sonnet-4-6, surface=CLI, task=T1 동일

---

## 관찰 대상

- self-immune 자체의 compute overhead: 각 기능별 token 소비량 분해
- overhead와 남은 token budget의 상호작용: overhead가 작업 가능 budget을 어떻게 잠식하는가
- overhead가 TCR 향상 대비 정당화되는 조건 (cost-reliability trade-off)

**핵심 가설**: self-immune overhead는 token budget 절대량보다 비율(%)로 관리해야 한다 — 32K 환경에서 monitoring 단독 overhead가 전체의 15% 이상이면 net TCR 향상이 사라진다.

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

| harness 기능 | token overhead | 시간 overhead | TCR 변화 | 순 효과 |
|-------------|---------------|-------------|---------|--------|
| monitoring-only | | | | |
| recovery-only | | | | |
| self-reporting-only | | | | |
| 통합 (E18 예상) | | | | |
| harness=OFF (baseline) | 0 | 0 | | |

---

## 분석

### Primary bottleneck
**1차 병목**:
**근거**:

### Balloon effect
[ ] 관찰됨 / [ ] 관찰 안 됨

---

## 측정값

| 지표 | 값 |
|------|----|
| harness=OFF token usage (baseline) | |
| monitoring 추가 overhead (tokens) | |
| recovery 추가 overhead (tokens) | |
| self-reporting 추가 overhead (tokens) | |
| 통합 overhead 합계 | |
| overhead 비율 (총 budget 대비) | |

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

## 연결 실험

- E18: mini self-immune 구현 시 이 overhead 측정값을 설계 제약으로 활용
- E20: 극단적 compute 제약에서 overhead가 작업 자체를 불가능하게 만드는 조건
