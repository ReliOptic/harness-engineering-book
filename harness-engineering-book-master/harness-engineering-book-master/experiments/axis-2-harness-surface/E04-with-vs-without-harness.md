# E04 — Harness on vs. off 조건에서 동일 task 실행

**Experiment ID**: E04
**Date**: (미정)
**Experimenter**: A
**Cross-validator**: B
**Target chapter**: Ch.3 (Harness+AgentOps 정의), Ch.4 (1막), Ch.5 (실험 결과 분석)
**Status**: [ ] 계획 / [ ] 진행중 / [ ] 완료 / [ ] 교차검증 완료

---

## Task

T1 (Code Review) 및 T2 (Multi-Step Reasoning) task를 harness=ON 조건과 harness=OFF 조건에서 각각 실행한다.
Task 정의: `experiments/design-specification.md §1` 기준.

---

## 5변수 설정

| 변수 | 설정 |
|------|------|
| **조작 변수** | Harness (on vs. off) |
| **모델** | claude-sonnet-4-6 via Anthropic API |
| **Harness config** | ON: 전체 harness 구성 / OFF: baseline (no harness) |
| **Surface** | CLI |
| **Compute environment** | GCP e2-micro |
| **Token budget** | T1: 32K / T2: 64K |

**통제 변수**: 모델=claude-sonnet-4-6, surface=CLI, token budget 동일, task 동일

---

## 관찰 대상

- failure 빈도 차이 (harness on vs. off)
- failure 성격 차이 (tool call 실패 / context 손실 / compute 포화 / format 오류)
- 복구 가능성 차이 (harness on에서 자동 복구 발생 여부)
- Failure Profile Radar: 5가지 실패 유형의 분포 비교

**핵심 가설**: harness=ON 조건에서 failure 빈도가 낮을 뿐 아니라 failure 성격이 달라진다 — tool call 실패와 context 손실이 줄고, 복구 가능한 형태의 실패 비중이 늘어난다.

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

| 조건 | TCR (T1) | TCR (T2) | failure 빈도 | 복구 성공률 |
|------|----------|----------|------------|-----------|
| harness=ON | | | | |
| harness=OFF | | | | |

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
| TCA | | |
| IFR | | |

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

**교차검증자**: B
**교차검증 날짜**:
**검증 방법**: 동일 조건 재현
**검증 결과**:
**불일치 사항**:

---

## 관련 Figure

- Fig 2 — Failure Profile Radar (E04 기반): harness on/off 조건별 5가지 실패 유형 분포
