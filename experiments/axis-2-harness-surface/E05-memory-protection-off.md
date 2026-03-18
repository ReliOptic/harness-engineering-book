# E05 — Harness memory 보호 해제 조건에서 실행

**Experiment ID**: E05
**Date**: (미정)
**Experimenter**: A
**Cross-validator**: B (E05 교차검증)
**Target chapter**: Ch.3 (Harness+AgentOps 정의), Ch.4 (1막)
**Status**: [ ] 계획 / [ ] 진행중 / [ ] 완료 / [ ] 교차검증 완료

---

## Task

T2 (Multi-Step Reasoning) task를 harness의 memory 보호 기능만 선택적으로 해제한 조건에서 실행한다.
baseline: E04 harness=OFF 및 harness=ON 데이터 활용.

---

## 5변수 설정

| 변수 | 설정 |
|------|------|
| **조작 변수** | Harness (memory 보호 해제) |
| **모델** | claude-sonnet-4-6 via Anthropic API |
| **Harness config** | 부분: memory 보호=OFF, 나머지 harness 기능=ON |
| **Surface** | CLI |
| **Compute environment** | GCP e2-micro |
| **Token budget** | T2: 64K |

**통제 변수**: 모델=claude-sonnet-4-6, surface=CLI, task=T2 동일, token budget 동일

---

## 관찰 대상

- context leakage 패턴: 어떤 단계에서 어떤 방식으로 발생하는가
- leakage가 task 완료에 미치는 영향 (즉각적 vs. 지연 효과)
- memory 보호 복원 시 이미 발생한 leakage의 복구 가능성
- E04 결과와의 비교: memory 보호 기능의 독립적 기여

**핵심 가설**: memory 보호 해제는 단순히 context 오류 빈도를 높이는 것이 아니라 특정 단계(context window 50% 초과 시점)에서 급격한 TCR 저하를 유발한다.

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

| 조건 | TCR (T2) | context leakage 발생 단계 | leakage 유형 |
|------|----------|--------------------------|------------|
| memory 보호=OFF | | | |
| memory 보호=ON (E04 참조) | | | |

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
| context leakage 발생 횟수 | |

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
