# E10 — 모델 capability floor와 self-reporting 정확도

**Experiment ID**: E10
**Date**: (미정)
**Experimenter**: B
**Cross-validator**: 없음 (단독)
**Target chapter**: Ch.7 (Self-immune, Agent-2 하한 조건)
**Status**: [ ] 계획 / [ ] 진행중 / [ ] 완료 / [ ] 교차검증 완료

---

## Task

다양한 모델 tier에서 self-reporting (자기 능력 보고) 정확도를 측정한다.
E01 데이터(ARCC 측정값)를 기반으로 tier별 self-reporting calibration을 분석한다.

---

## 5변수 설정

| 변수 | 설정 |
|------|------|
| **조작 변수** | 모델 tier (ARCC 기준 분류) |
| **모델** | tier-A (ARCC > 0.8) / tier-B (0.5 < ARCC ≤ 0.8) / tier-C (ARCC ≤ 0.5): TBD (E01 결과 기반) |
| **Harness config** | harness=ON |
| **Surface** | CLI |
| **Compute environment** | GCP e2-micro |
| **Token budget** | T1: 32K |

**통제 변수**: surface=CLI, harness=ON, task=T1 동일, token budget 동일

---

## 관찰 대상

- self-reporting 정확도 per tier: 모델이 자신의 성능을 얼마나 정확히 예측하는가
- capability floor 식별: self-reporting 자체가 불가능해지는 ARCC 하한
- E15와의 연결: agent 자기인식 정확도가 operator intervention 가능성에 미치는 영향

**핵심 가설**: self-reporting 정확도에는 capability floor가 존재한다 — ARCC가 특정 값 이하로 떨어지면 self-reporting 자체가 신뢰할 수 없게 되며, 이것이 Agent-2 전환의 전제조건이다.

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

| 모델 tier | ARCC (E01 참조) | self-reporting 정확도 | capability floor 도달 |
|----------|----------------|---------------------|---------------------|
| tier-A | | | |
| tier-B | | | |
| tier-C | | | |

---

## 분석

### Primary bottleneck
**1차 병목**:
**근거**:

### Balloon effect
[ ] 관찰됨 / [ ] 관찰 안 됨

---

## 측정값

| 지표 | tier-A | tier-B | tier-C |
|------|--------|--------|--------|
| Token usage (input) | | | |
| Token usage (output) | | | |
| 실행 시간 | | | |
| 비용 (API) | | | |
| self-reporting calibration score | | | |

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

- E01: ARCC 측정 기준값 제공
- E15: agent 자기인식과 operator intervention 연결
