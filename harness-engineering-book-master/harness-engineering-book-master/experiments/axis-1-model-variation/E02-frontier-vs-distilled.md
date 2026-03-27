# E02 — 동일 코드 리뷰를 frontier vs. distilled 모델로 실행

**Experiment ID**: E02
**Date**: (미정)
**Experimenter**: A
**Cross-validator**: 없음 (단독)
**Target chapter**: Ch.2 (§4 Quantization Tax Curve, §5 Distillation Efficiency Frontier)
**Status**: [ ] 계획 / [ ] 진행중 / [ ] 완료 / [ ] 교차검증 완료

---

## Task

T1 (Code Review) task를 동일 조건에서 frontier 모델 vs. distilled 모델로 실행.
동일 base model의 FP16→Q8→Q4→Q2 경로에서 ARCC 변화 측정 포함.

---

## 5변수 설정

| 변수 | 설정 |
|------|------|
| **조작 변수** | 모델 (frontier vs. distilled / quantization bit-width) |
| **모델** | Frontier: `google/gemini-2.5-pro` / Mid: `google/gemini-2.5-flash` / Small: `google/gemini-2.5-flash-lite` + `openai/gpt-5-mini` (OpenRouter) |
| **Harness config** | harness=OFF |
| **Surface** | CLI |
| **Compute environment** | GCP e2-micro |
| **Token budget** | T1: 32K |

**통제 변수**: task=T1 동일, surface=CLI, harness=OFF

---

## 관찰 대상

- 리뷰 품질 차이가 일관되는가 (task 구조에 따라 달라지는가)
- Quantization Tax Curve: bit-width별 ARCC 감소 비율
- Distillation Efficiency Frontier: 동일 parameter budget에서 전략별 ARCC 비교

**핵심 가설**: Quantization Tax Curve — FP16→Q2 경로에서 ARCC가 비선형 감소. Distillation이 동일 parameter budget에서 quantization보다 agent viability 관점에서 효율적이다.

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

**TCR per 모델**:
**ARCC per 모델**:

| 모델 | bit-width | ARCC | TCR(T1) |
|------|-----------|------|---------|
| | FP16 | | |
| | Q8 | | |
| | Q4 | | |
| | Q2 | | |
| Distilled | — | | |

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

교차검증 없음 (단독 실험).

---

## 관련 Figure

- Fig 1b — Quantization Tax Curve
- Fig 1c — Distillation Efficiency Frontier
