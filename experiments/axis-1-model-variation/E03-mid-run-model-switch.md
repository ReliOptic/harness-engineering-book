# E03 — 모델을 workflow 중간에 교체 (mid-run switching)

**Experiment ID**: E03
**Date**: (미정)
**Experimenter**: A
**Cross-validator**: B (E03 교차검증)
**Target chapter**: Ch.2 (§6 Mid-run model switching)
**Status**: [ ] 계획 / [ ] 진행중 / [ ] 완료 / [ ] 교차검증 완료

---

## Task

T2 (Multi-Step Reasoning) task를 실행하다가 중간(step 5, step 10, step 15)에 모델을 교체한다.

---

## 5변수 설정

| 변수 | 설정 |
|------|------|
| **조작 변수** | 모델 (mid-run switching 시점) |
| **모델** | 시작: `google/gemini-2.5-flash` → 교체: 동일 family=`google/gemini-2.5-flash-lite` / 다른 family=`openai/gpt-5-mini` (OpenRouter) |
| **Harness config** | harness=OFF (baseline) |
| **Surface** | CLI |
| **Compute environment** | GCP e2-micro |
| **Token budget** | T2: 64K |

**통제 변수**: task=T2 동일, surface=CLI, harness=OFF

---

## 관찰 대상

- context 연속성이 어떤 방식으로 깨지는가
- 동일 family 내 switching vs. 다른 family switching의 context continuity 차이
- switching 시점(step 5 vs. 10 vs. 15)에 따른 degradation 차이

**핵심 가설**: mid-run switching 시 context state의 암묵적 가정이 위반되어 TCR이 급락한다. 동일 family 내 switching은 다른 family switching보다 continuity를 더 보존한다.

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

| switching 시점 | switching 유형 | TCR | 주요 실패 양상 |
|---------------|---------------|-----|--------------|
| step 5 | 동일 family | | |
| step 10 | 동일 family | | |
| step 15 | 동일 family | | |
| step 5 | 다른 family | | |
| step 10 | 다른 family | | |
| step 15 | 다른 family | | |
| 교체 없음 (baseline) | — | | |

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
| Token usage (input) | |
| Token usage (output) | |
| 실행 시간 | |
| 비용 (API) | |

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
**검증 방법**: 동일 조건 재현 (switching 시점 step 10)
**검증 결과**:
**불일치 사항**:
