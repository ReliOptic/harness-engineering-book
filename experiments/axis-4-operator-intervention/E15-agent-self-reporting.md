# E15 — Agent 자기인식과 operator intervention 전환점

**Experiment ID**: E15
**Date**: (미정)
**Experimenter**: C
**Cross-validator**: B (E15 교차검증)
**Target chapter**: Ch.4 (3막), Ch.7 (Self-immune, Agent-2 전환 조건)
**Status**: [ ] 계획 / [ ] 진행중 / [ ] 완료 / [ ] 교차검증 완료

---

## Task

T2 (Multi-Step Reasoning) task에서 agent가 자신의 실패를 인식하고 operator에게 개입을 요청하는 시나리오를 설계한다. intervention → 내재화 전환점을 탐색한다.

---

## 5변수 설정

| 변수 | 설정 |
|------|------|
| **조작 변수** | Intervention (외부 개입 → agent 자기인식 내재화 전환점) |
| **모델** | claude-sonnet-4-6 via Anthropic API |
| **Harness config** | harness=ON (self-reporting 프롬프트 포함) |
| **Surface** | CLI |
| **Compute environment** | GCP e2-micro |
| **Token budget** | T2: 64K |

**통제 변수**: 모델=claude-sonnet-4-6, surface=CLI, harness=ON, task=T2 동일

---

## 관찰 대상

- agent 자기인식 정확도: 실패를 얼마나 정확히 인식하는가 (E10과 비교)
- 개입 요청 타이밍: 실제로 개입이 필요한 시점 대비 agent의 요청 시점
- 내재화 전환 조건: operator 개입 없이 agent 스스로 복구를 시도하는 조건
- E10 연결: capability floor 이하에서 self-reporting이 무너지는 패턴 확인

**핵심 가설**: agent 자기인식이 충분히 정확할 때(모델 능력 지표 > capability floor), operator 개입 요청의 타이밍 정확도가 높아지고 불필요한 개입 요청이 줄어든다. 이 조건이 harness internalization의 전제다.

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

| 시나리오 | 자기인식 정확도 | 개입 요청 타이밍 정확도 | 불필요 요청 비율 | 내재화 전환 발생 |
|---------|--------------|---------------------|--------------|--------------|
| 실패 유형 A | | | | |
| 실패 유형 B | | | | |
| 실패 유형 C | | | | |

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
| 자기인식 정확도 (전체) | |
| 개입 요청 타이밍 오차 (step) | |

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

- E10: capability floor 기준값 참조
- E16, E17, E18: 내재화 전환 조건이 self-immune 설계의 입력
