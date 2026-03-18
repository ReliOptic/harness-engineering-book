# E19 — 모호한 task 설계로 인한 실패 (반례 1)

**Experiment ID**: E19
**Date**: (미정)
**Experimenter**: C
**Cross-validator**: A (E19 교차검증)
**Target chapter**: Ch.4 (반례), Ch.5 (실험 결과 분석)
**Status**: [ ] 계획 / [ ] 진행중 / [ ] 완료 / [ ] 교차검증 완료

---

## Task

harness와 모델이 모두 정상 조건에서, task 정의의 모호성만으로 실패가 발생하는 시나리오를 설계하고 실행한다. 이 실험은 반례(counterexample)로서, 5변수 프레임워크에서 task design이 독립적인 실패 원인이 될 수 있음을 보인다.

---

## 5변수 설정

| 변수 | 설정 |
|------|------|
| **조작 변수** | Task design (의도적으로 모호하게 설계된 task 정의) |
| **모델** | claude-sonnet-4-6 via Anthropic API (SOTA) |
| **Harness config** | harness=ON (완전한 harness 구성) |
| **Surface** | CLI |
| **Compute environment** | GCP e2-micro |
| **Token budget** | T2: 64K (충분한 budget) |

**통제 변수**: 모델=SOTA (최선), harness=완전 ON, surface=CLI, token budget=충분

---

## 반례 설계

**설계 의도**: harness가 완벽하고 모델도 SOTA인 조건에서, task 정의의 모호성만으로 실패를 재현한다.

**모호성 유형**:
- 목표 불명확: "가능하면 코드를 개선하라"
- 성공 기준 불명확: 완료 조건이 정의되지 않음
- 범위 불명확: task의 경계가 열려 있음

**반례 의의**: 5변수 프레임워크는 모델, harness, surface, intervention, compute 외에 task design 자체도 실패 원인이 될 수 있음을 인식한다. 이 실험은 해당 주장의 증거다.

---

## 관찰 대상

- task 모호성 유형별 실패 양상의 차이
- 모델이 모호성을 어떻게 해소하려 시도하는가 (합리화 vs. 질문 vs. 임의 결정)
- harness가 task 모호성으로 인한 실패를 감지하는가, 감지한다면 어떻게 반응하는가

**핵심 가설 (반례)**: harness와 모델이 완전히 정상일 때도 task 정의가 모호하면 TCR이 0에 수렴한다. 이는 실패가 항상 모델 능력이나 harness 부재에서 기인하지 않는다는 반례다.

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

| 모호성 유형 | TCR | 실패 양상 | 모델 해소 전략 | harness 감지 여부 |
|-----------|-----|---------|------------|----------------|
| 목표 불명확 | | | | |
| 성공 기준 불명확 | | | | |
| 범위 불명확 | | | | |
| 명확한 task (대조군) | | | | |

---

## 분석

### Primary bottleneck
**1차 병목**: task design (반례 — 모델/harness/surface/compute 모두 정상)
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

**교차검증자**: A
**교차검증 날짜**:
**검증 방법**: 동일 조건 재현
**검증 결과**:
**불일치 사항**:
