# E06 — Permission boundary 점진적 확장 실험

**Experiment ID**: E06
**Date**: (미정)
**Experimenter**: A
**Cross-validator**: B (E06 교차검증)
**Target chapter**: Ch.3 (Harness+AgentOps 정의), Ch.4 (1막)
**Status**: [ ] 계획 / [ ] 진행중 / [ ] 완료 / [ ] 교차검증 완료

---

## Task

T1 (Code Review) task를 기준으로 harness의 permission boundary를 단계적으로 확장하면서 실행한다.
단계: minimal → standard → extended → unrestricted

---

## 5변수 설정

| 변수 | 설정 |
|------|------|
| **조작 변수** | Harness (permission boundary 수준) |
| **모델** | claude-sonnet-4-6 via Anthropic API |
| **Harness config** | 4단계: minimal / standard / extended / unrestricted |
| **Surface** | CLI |
| **Compute environment** | GCP e2-micro |
| **Token budget** | T1: 32K |

**통제 변수**: 모델=claude-sonnet-4-6, surface=CLI, task=T1 동일, token budget 동일

---

## 관찰 대상

- 안전하지 않은 행동(unsafe behavior)의 발생 임계치: 어느 permission 단계에서 처음 나타나는가
- permission 확장에 따른 TCR 변화 방향 (향상 vs. 무관 vs. 저하)
- unsafe behavior의 유형 분류 (권한 남용 / 의도치 않은 side-effect / 기타)

**핵심 가설**: 안전하지 않은 행동은 permission boundary 확장에 비례하지 않는다 — 특정 임계치를 넘는 순간 급격히 발생하며, 이 임계치는 task 유형보다 모델의 모델 능력 지표에 더 강하게 상관한다.

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

| permission 단계 | TCR | unsafe behavior 발생 | 유형 |
|----------------|-----|---------------------|------|
| minimal | | | |
| standard | | | |
| extended | | | |
| unrestricted | | | |

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
| unsafe behavior 발생 횟수 | |

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
