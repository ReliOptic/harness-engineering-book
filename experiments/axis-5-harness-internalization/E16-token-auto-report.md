# E16 — Token 자동 보고 내재화 실험

**Experiment ID**: E16
**Date**: (미정)
**Experimenter**: C
**Cross-validator**: B (E16 교차검증)
**Target chapter**: Ch.7 (Self-immune, Harness internalization)
**Status**: [ ] 계획 / [ ] 진행중 / [ ] 완료 / [ ] 교차검증 완료

---

## Task

T2 (Multi-Step Reasoning) task에서 harness의 token 모니터링 기능을 agent가 내재화하는 실험을 수행한다. agent가 스스로 token 소비를 추적하고 보고하도록 프롬프트 수준에서 설계한다.

---

## 5변수 설정

| 변수 | 설정 |
|------|------|
| **조작 변수** | Harness 내재화 (token 자동 보고: 외부 harness → 내재화 프롬프트) |
| **모델** | claude-sonnet-4-6 via Anthropic API |
| **Harness config** | 비교: 외부 harness token monitoring vs. 내재화 token self-report |
| **Surface** | CLI |
| **Compute environment** | GCP e2-micro |
| **Token budget** | T2: 64K |

**통제 변수**: 모델=claude-sonnet-4-6, surface=CLI, task=T2 동일, token budget 동일

---

## 관찰 대상

- self-reporting 정확도: agent의 자체 보고 token 소비량 vs. 실제 API 측정값
- overhead 비교: 외부 harness monitoring vs. 내재화 self-report의 token 비용 차이
- 행동 변화: self-reporting 내재화 후 agent가 token을 더 효율적으로 사용하는가

**핵심 가설**: token self-reporting 내재화는 외부 harness와 동등한 정확도를 달성하지 못하지만, overhead가 낮고 행동 변화(token 절약 경향)라는 부수 효과가 발생한다.

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

| 조건 | self-reporting 정확도 | overhead (tokens) | 행동 변화 관찰 | TCR |
|------|---------------------|------------------|------------|-----|
| 외부 harness | | | | |
| 내재화 self-report | | | | |

---

## 분석

### Primary bottleneck
**1차 병목**:
**근거**:

### Balloon effect
[ ] 관찰됨 / [ ] 관찰 안 됨

---

## 측정값

| 지표 | 외부 harness | 내재화 |
|------|------------|--------|
| Token usage (input) | | |
| Token usage (output) | | |
| 실행 시간 | | |
| 비용 (API) | | |
| self-report 오차 (tokens) | | |
| self-report overhead (tokens) | | |

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

## 연결 실험

- E17: failure 감지+재시도와 결합하여 E18 mini self-immune 구성
- E12: overhead 예산 비교 기준
