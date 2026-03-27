# E01 — 동일 task를 SOTA vs. 소형 모델로 실행

**Experiment ID**: E01
**Date**: (미정)
**Experimenter**: A
**Cross-validator**: B (E03, E05)
**Target chapter**: Ch.2 (§3 Capability Cliff), Ch.4 (1막)
**Status**: [ ] 계획 / [ ] 진행중 / [ ] 완료 / [ ] 교차검증 완료

---

## Task

T1 (Code Review) 및 T2 (Multi-Step Reasoning) task를 동일 조건에서 SOTA 모델과 소형 모델로 각각 실행한다.
Task 정의: `experiments/design-specification.md §1` 기준.

---

## 5변수 설정

| 변수 | 설정 |
|------|------|
| **조작 변수** | 모델 (SOTA vs. 소형) |
| **모델** | SOTA: `google/gemini-2.5-pro` / 소형: `google/gemini-2.5-flash-lite` (OpenRouter) |
| **Harness config** | harness=OFF (baseline, harness-off 조건) |
| **Surface** | CLI |
| **Compute environment** | GCP e2-micro (free tier) |
| **Token budget** | T1: 32K / T2: 64K |

**통제 변수**: surface=CLI, harness=OFF, token budget 동일, task 동일

---

## 관찰 대상

- tool call 패턴 (TCA: Tool Call Accuracy)
- task 완료율 (TCR per task type)
- 실패 지점의 성격 (tool call 실패 vs. reasoning 실패 vs. format 오류)
- ARCC sub-component 측정 (TCA, IFR, MSRD_n, CUE)

**핵심 가설 (pre-registered)**: ARCC가 특정 threshold 이하에서 TCR이 선형이 아닌 급락한다 (Capability Cliff). Cliff position은 task type(T1/T2)에 따라 다르다.

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

**TCR (T1)**:
**TCR (T2)**:
**ARCC (SOTA)**:
**ARCC (소형)**:

---

## 분석

### Primary bottleneck
**1차 병목**:
**근거**:

### Balloon effect
[ ] 관찰됨 / [ ] 관찰 안 됨

---

## 측정값

| 지표 | SOTA | 소형 |
|------|------|------|
| Token usage (input) | | |
| Token usage (output) | | |
| 실행 시간 | | |
| 비용 (API) | | |
| TCA | | |
| IFR | | |
| MSRD_n | | |
| CUE | | |

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

- Fig 1 — Agent Capability Cliff (E01 확장): ARCC scatter plot + task-conditional sigmoid fit
- Fig 1b — Quantization Tax Curve (E02 연결)
