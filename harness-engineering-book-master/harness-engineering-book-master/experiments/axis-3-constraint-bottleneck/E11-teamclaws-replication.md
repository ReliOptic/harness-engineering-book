# E11 — TeamClaws 재현: multi-agent resource contention

**Experiment ID**: E11
**Date**: (미정)
**Experimenter**: B
**Cross-validator**: A (E11 교차검증)
**Target chapter**: Ch.4 (2막), Ch.5 (실험 결과 분석)
**Status**: [ ] 계획 / [ ] 진행중 / [ ] 완료 / [ ] 교차검증 완료

---

## Task

TeamClaws 시나리오를 재현한다: 다중 agent가 동일 compute 자원을 경합하는 조건에서 context 오염이 어떻게 전파되는가를 관찰한다.

---

## 5변수 설정

| 변수 | 설정 |
|------|------|
| **조작 변수** | Compute (multi-agent resource contention) |
| **모델** | claude-sonnet-4-6 via Anthropic API (다중 인스턴스) |
| **Harness config** | harness=ON (isolation 설정 포함) vs. harness=OFF |
| **Surface** | CLI |
| **Compute environment** | GCP e2-micro (단일 VM에서 multi-agent 시뮬레이션) |
| **Token budget** | 각 agent T2: 32K (총 resource 64K를 2 agent가 경합) |

**통제 변수**: 모델=claude-sonnet-4-6, surface=CLI, task=T2 동일

---

## 관찰 대상

- context 오염 전파 경로: agent A의 오염이 agent B에 어떻게 전달되는가
- resource contention이 context 오염을 어떻게 가속시키는가
- harness isolation이 오염 전파를 차단하는 효과

**핵심 가설**: context 오염은 직접 공유 메모리를 통해서만 전파되는 것이 아니라 shared compute resource 경합을 통해서도 간접적으로 전파된다 (GC Death Spiral 연쇄 효과).

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

| 조건 | agent A TCR | agent B TCR | 오염 전파 발생 | 전파 경로 |
|------|------------|------------|-------------|---------|
| harness=ON (isolation) | | | | |
| harness=OFF | | | | |

---

## 분석

### Primary bottleneck
**1차 병목**:
**근거**:

### Balloon effect
[ ] 관찰됨 / [ ] 관찰 안 됨

---

## 측정값

| 지표 | harness=ON | harness=OFF |
|------|-----------|------------|
| Token usage 합계 | | |
| 실행 시간 | | |
| 비용 (API) | | |
| context 오염 전파 발생 횟수 | | |
| 전체 TCR (두 agent 평균) | | |

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
