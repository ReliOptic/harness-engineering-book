# E18 — Mini self-immune 시스템 통합 실험

**Experiment ID**: E18
**Date**: (미정)
**Experimenter**: C
**Cross-validator**: 없음 (단독)
**Target chapter**: Ch.7 (Self-immune, Agent-2 전환 조건)
**Status**: [ ] 계획 / [ ] 진행중 / [ ] 완료 / [ ] 교차검증 완료

---

## Task

E16 (token 자동 보고)과 E17 (failure 감지+재시도)을 결합한 mini self-immune 시스템을 구성하고 T2 task에서 통합 안정성을 검증한다.

---

## 5변수 설정

| 변수 | 설정 |
|------|------|
| **조작 변수** | Harness 내재화 (E16+E17 결합: mini self-immune 통합) |
| **모델** | claude-sonnet-4-6 via Anthropic API |
| **Harness config** | mini self-immune = E16 내재화 + E17 내재화 통합 |
| **Surface** | CLI |
| **Compute environment** | GCP e2-micro |
| **Token budget** | T2: 64K |

**통제 변수**: 모델=claude-sonnet-4-6, surface=CLI, task=T2 동일, token budget 동일

---

## 관찰 대상

- 통합 안정성: E16과 E17을 결합했을 때 각각의 기능이 온전히 유지되는가
- 상호 간섭: token 보고와 failure 감지가 서로의 동작에 간섭하는가
- E12 대비 overhead 비교: mini self-immune의 실제 compute overhead
- Cost-Reliability Frontier: overhead 증가 대비 TCR 향상의 효율 곡선

**핵심 가설**: E16과 E17의 단순 결합은 각각의 TCR 향상을 합산하지 않는다 — 두 기능 간 상호 간섭으로 인해 통합 TCR이 단일 기능 TCR보다 낮을 수 있다. 이 간섭이 mini self-immune 설계의 핵심 과제다.

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

| 조건 | TCR | overhead (tokens) | 상호 간섭 발생 | 안정성 평가 |
|------|-----|-----------------|------------|----------|
| harness=OFF (baseline) | | | — | |
| E16 단독 | | | | |
| E17 단독 | | | | |
| E16+E17 통합 (mini self-immune) | | | | |

---

## 분석

### Primary bottleneck
**1차 병목**:
**근거**:

### Balloon effect
[ ] 관찰됨 / [ ] 관찰 안 됨

---

## 측정값

| 지표 | baseline | E16 단독 | E17 단독 | 통합 |
|------|---------|---------|---------|------|
| Token usage (input) | | | | |
| Token usage (output) | | | | |
| 실행 시간 | | | | |
| 비용 (API) | | | | |
| overhead 비율 (%) | | | | |
| 상호 간섭 횟수 | | | | |

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

- Fig 8 — Cost-Reliability Frontier (E18 기반): overhead 증가 vs. TCR 향상 효율 곡선

---

## 연결 실험

- E12: overhead 예산 제약 기준 (E12 측정값이 E18 설계 상한)
- E16, E17: 각 단독 실험 결과가 통합 기준선
