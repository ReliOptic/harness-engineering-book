# E17 — Failure 감지 및 자동 재시도 내재화 실험

**Experiment ID**: E17
**Date**: (미정)
**Experimenter**: C
**Cross-validator**: B (E17 교차검증)
**Target chapter**: Ch.7 (Self-immune, Harness internalization)
**Status**: [ ] 계획 / [ ] 진행중 / [ ] 완료 / [ ] 교차검증 완료

---

## Task

T2 (Multi-Step Reasoning) task에서 harness의 failure 감지 및 재시도 기능을 agent가 내재화하는 실험을 수행한다. agent가 스스로 실패를 감지하고 재시도 전략을 결정하도록 설계한다.

---

## 5변수 설정

| 변수 | 설정 |
|------|------|
| **조작 변수** | Harness 내재화 (failure 감지+재시도: 외부 harness → 내재화 프롬프트) |
| **모델** | claude-sonnet-4-6 via Anthropic API |
| **Harness config** | 비교: 외부 harness failure recovery vs. 내재화 self-recovery |
| **Surface** | CLI |
| **Compute environment** | GCP e2-micro |
| **Token budget** | T2: 64K |

**통제 변수**: 모델=claude-sonnet-4-6, surface=CLI, task=T2 동일, token budget 동일

---

## 관찰 대상

- self-recovery 성공률: 내재화된 재시도 전략의 실패 복구 효과
- 무한 루프 조건: 재시도가 새로운 실패를 야기하는 패턴
- 외부 harness 대비 내재화의 복구 성공률 차이
- 재시도 횟수와 token 소비의 상관관계

**핵심 가설**: 내재화된 failure 감지는 외부 harness보다 false positive 비율이 높고(정상을 실패로 오인), 무한 재시도 루프 위험이 있다. 그러나 특정 실패 유형(format 오류, tool call 실패)에서는 내재화 방식이 더 빠른 복구를 달성한다.

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

| 조건 | self-recovery 성공률 | 무한 루프 발생 | 평균 재시도 횟수 | TCR |
|------|-------------------|------------|-------------|-----|
| 외부 harness | | | | |
| 내재화 self-recovery | | | | |

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
| 재시도 횟수 (총) | | |
| false positive 비율 | | |
| 무한 루프 발생 횟수 | | |

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

- E16: token 자동 보고와 결합하여 E18 mini self-immune 구성
- E18: E16+E17 통합 시 상호 간섭 여부 확인
