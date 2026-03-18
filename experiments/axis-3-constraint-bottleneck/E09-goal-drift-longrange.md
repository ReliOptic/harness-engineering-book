# E09 — 장거리 task에서 goal drift 측정

**Experiment ID**: E09
**Date**: (미정)
**Experimenter**: B
**Cross-validator**: A (E09 교차검증)
**Target chapter**: Ch.4 (2막), Ch.5 (실험 결과 분석)
**Status**: [ ] 계획 / [ ] 진행중 / [ ] 완료 / [ ] 교차검증 완료

---

## Task

40-step으로 구성된 장거리 T2 (Multi-Step Reasoning) task를 실행하면서 10-step 간격으로 goal alignment를 측정한다.

---

## 5변수 설정

| 변수 | 설정 |
|------|------|
| **조작 변수** | Compute (40-step 장거리 task, step별 goal drift 측정) |
| **모델** | claude-sonnet-4-6 via Anthropic API |
| **Harness config** | harness=ON (E04 기준) vs. harness=OFF (비교용) |
| **Surface** | CLI |
| **Compute environment** | GCP e2-micro |
| **Token budget** | T2 확장: 128K |

**통제 변수**: 모델=claude-sonnet-4-6, surface=CLI, task 동일

---

## 관찰 대상

- goal drift 측정: 10-step 간격으로 원래 목표와의 alignment score 측정
- drift 유형 분류: 목표 범위 확장 / 목표 대체 / 목표 망각
- harness 유무에 따른 goal drift 억제 효과
- drift 발생 시점과 compute 소비량의 상관관계

**핵심 가설**: goal drift는 step 증가에 따라 단조 증가하지 않는다 — context window 압박이 시작되는 특정 step (약 20-25 step)에서 급격히 증가하며, harness가 이 임계 구간을 완충한다.

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

| step | goal alignment score (harness=ON) | goal alignment score (harness=OFF) | drift 유형 |
|------|----------------------------------|-----------------------------------|-----------|
| 10 | | | |
| 20 | | | |
| 30 | | | |
| 40 | | | |

---

## 분석

### Primary bottleneck
**1차 병목**:
**근거**:

### Balloon effect
[ ] 관찰됨 / [ ] 관찰 안 됨

---

## 측정값

| 지표 | harness=ON | harness=OFF |
|------|-----------|------------|
| Token usage (input) | | |
| Token usage (output) | | |
| 실행 시간 | | |
| 비용 (API) | | |
| 최종 TCR | | |
| goal drift 발생 첫 step | | |

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

**교차검증자**: A
**교차검증 날짜**:
**검증 방법**: 동일 조건 재현
**검증 결과**:
**불일치 사항**:

---

## 관련 Figure

- Fig 9 — Harness ROC (E09 기반): harness 개입 시점 vs. goal drift 억제 효과
