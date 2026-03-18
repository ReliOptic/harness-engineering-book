# E08 — Token budget 단계적 감소와 자기평가 정확도

**Experiment ID**: E08
**Date**: (미정)
**Experimenter**: B
**Cross-validator**: A (E08 교차검증)
**Target chapter**: Ch.4 (2막), Ch.5 (실험 결과 분석), Ch.7 (Self-immune)
**Status**: [ ] 계획 / [ ] 진행중 / [ ] 완료 / [ ] 교차검증 완료

---

## Task

T2 (Multi-Step Reasoning) task를 token budget을 단계적으로 감소시키면서 (100%→75%→50%→25%) 실행한다. 각 단계에서 agent의 자기평가(self-assessment)를 elicit하고 실제 성능과 비교한다.

---

## 5변수 설정

| 변수 | 설정 |
|------|------|
| **조작 변수** | Compute (token budget: 100%→75%→50%→25%) |
| **모델** | claude-sonnet-4-6 via Anthropic API |
| **Harness config** | harness=ON (E04 기준) |
| **Surface** | CLI |
| **Compute environment** | GCP e2-micro |
| **Token budget** | T2 기준: 64K (100%) → 48K (75%) → 32K (50%) → 16K (25%) |

**통제 변수**: 모델=claude-sonnet-4-6, surface=CLI, harness=ON, task=T2 동일

---

## 관찰 대상

- 자기평가 정확도 저하 시점: budget 감소 단계 중 어느 시점에서 자기평가가 실제 성능과 괴리되기 시작하는가
- self-immune 가능성 탐색: agent가 compute constraint를 인식하고 행동을 조정하는가
- overconfidence 패턴: budget 부족 상황에서 agent가 성공 가능성을 과대평가하는가

**핵심 가설**: 자기평가 정확도는 token budget과 단조롭게 감소하지 않는다 — 특정 budget 임계치(50% 또는 25%)에서 급격한 calibration 저하가 발생하며, 이것이 self-immune 시스템 설계의 핵심 경계조건이 된다.

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

| budget 단계 | token budget | TCR | 자기평가 정확도 | overconfidence 발생 |
|------------|-------------|-----|--------------|-------------------|
| 100% | 64K | | | |
| 75% | 48K | | | |
| 50% | 32K | | | |
| 25% | 16K | | | |

---

## 분석

### Primary bottleneck
**1차 병목**:
**근거**:

### Balloon effect
[ ] 관찰됨 / [ ] 관찰 안 됨

---

## 측정값

| 지표 | 100% | 75% | 50% | 25% |
|------|------|-----|-----|-----|
| Token usage (input) | | | | |
| Token usage (output) | | | | |
| 실행 시간 | | | | |
| 비용 (API) | | | | |
| 자기평가 정확도 (calibration score) | | | | |

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
