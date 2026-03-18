# E20 — 완벽한 harness + SOTA 모델에서도 compute 부족 시 실패 (반례 2)

**Experiment ID**: E20
**Date**: (미정)
**Experimenter**: C
**Cross-validator**: 없음 (단독)
**Target chapter**: Ch.4 (반례), Ch.5 (실험 결과 분석), Ch.7 (Self-immune 한계)
**Status**: [ ] 계획 / [ ] 진행중 / [ ] 완료 / [ ] 교차검증 완료

---

## Task

harness가 완전하고 모델도 SOTA인 조건에서, compute를 극단적으로 제약하여 실패를 재현한다. E12의 overhead 측정값을 활용하여 harness 자체의 overhead가 작업 가능한 budget을 소진하는 지점을 탐색한다.

---

## 5변수 설정

| 변수 | 설정 |
|------|------|
| **조작 변수** | Compute (극단적 제약: token budget을 harness overhead 수준으로 압축) |
| **모델** | claude-sonnet-4-6 via Anthropic API (SOTA) |
| **Harness config** | harness=ON (완전한 harness 구성, E04 기준) |
| **Surface** | CLI |
| **Compute environment** | GCP e2-micro |
| **Token budget** | E12 overhead 측정값 기반 단계적 감소: TBD (E12 완료 후 결정) |

**통제 변수**: 모델=SOTA (최선), harness=완전 ON, surface=CLI, task=T1 동일

---

## 반례 설계

**설계 의도**: harness가 완벽하고 모델도 SOTA인 조건에서, compute 제약만으로 실패를 재현한다.

**반례 의의**: compute는 독립적인 실패 변수다. 충분한 compute 없이는 아무리 좋은 harness와 모델도 task를 완료할 수 없다. 이것은 5변수 프레임워크의 귀류법적 증명이다.

**E12 연결**: E12에서 측정한 harness overhead 값이 이 실험의 critical token budget threshold를 결정한다.

---

## 관찰 대상

- compute 제약이 임계값을 넘는 시점에서 harness overhead 자체가 작업 완료를 방해하는가
- harness가 compute 부족을 인식하고 self-degradation을 선택하는가 (기능 일부를 비활성화)
- 실패 양상이 E19(task 모호성)와 어떻게 다른가

**핵심 가설 (반례)**: token budget이 E12에서 측정한 harness overhead의 2배 이하로 줄어들면, harness=ON 조건이 harness=OFF보다 TCR이 낮아지는 역전 현상이 발생한다.

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

| token budget | TCR (harness=ON) | TCR (harness=OFF) | 역전 발생 | 비고 |
|-------------|-----------------|-----------------|---------|------|
| TBD (E12 기반 4K) | | | | |
| TBD (E12 기반 8K) | | | | |
| TBD (E12 기반 16K) | | | | |
| 32K (E04 baseline) | | | | |

---

## 분석

### Primary bottleneck
**1차 병목**: compute (반례 — 모델/harness/surface 모두 정상)
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
| harness overhead 실측 (E12 비교) | |
| 역전 발생 token budget threshold | |

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

- E12: harness overhead 측정값 → E20 실험 설계 입력
- E19: 두 반례 비교 — task 설계 실패 vs. compute 제약 실패의 차이
