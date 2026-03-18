# E14 — 규칙 기반 자동 개입 범위 탐색

**Experiment ID**: E14
**Date**: (미정)
**Experimenter**: C
**Cross-validator**: B (E14 교차검증)
**Target chapter**: Ch.4 (3막), Ch.6 (Fieldkit)
**Status**: [ ] 계획 / [ ] 진행중 / [ ] 완료 / [ ] 교차검증 완료

---

## Task

T1 (Code Review) 및 T2 (Multi-Step Reasoning) task에서 규칙 기반 자동 개입 시스템을 적용한다. 자동화 가능한 개입의 범위와 한계를 탐색한다.

---

## 5변수 설정

| 변수 | 설정 |
|------|------|
| **조작 변수** | Intervention (규칙 기반 자동화 vs. 수동 개입 vs. 개입 없음) |
| **모델** | claude-sonnet-4-6 via Anthropic API |
| **Harness config** | harness=ON + rule-based auto-intervention 레이어 추가 |
| **Surface** | CLI |
| **Compute environment** | GCP e2-micro |
| **Token budget** | T1: 32K / T2: 64K |

**통제 변수**: 모델=claude-sonnet-4-6, surface=CLI, task 동일

---

## 관찰 대상

- 자동화 가능한 개입 범위: 어떤 유형의 실패가 규칙으로 처리 가능한가
- 자동 개입의 한계: 규칙으로 처리하지 못하는 실패 유형은 무엇인가
- 자동 개입과 수동 개입의 복구 성공률 비교
- 오탐(false positive) 비율: 자동 개입이 정상 실행을 방해하는 경우

**핵심 가설**: 규칙 기반 자동 개입은 tool call 실패와 format 오류에 대해서는 수동 개입과 동등한 복구 성공률을 달성하지만, reasoning 실패와 goal drift에 대해서는 수동 개입이 필수적이다.

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

| 실패 유형 | 자동 개입 성공률 | 수동 개입 성공률 | 자동화 가능 판정 |
|----------|---------------|---------------|--------------|
| tool call 실패 | | | |
| format 오류 | | | |
| context 손실 | | | |
| reasoning 실패 | | | |
| goal drift | | | |

---

## 분석

### Primary bottleneck
**1차 병목**:
**근거**:

### Balloon effect
[ ] 관찰됨 / [ ] 관찰 안 됨

---

## 측정값

| 지표 | 자동 개입 | 수동 개입 | 개입 없음 |
|------|---------|---------|---------|
| Token usage (input) | | | |
| Token usage (output) | | | |
| 실행 시간 | | | |
| 비용 (API) | | | |
| 전체 TCR | | | |
| 오탐 비율 | | | |

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

## 관련 Figure

- Fig 7 — Auto-intervention Coverage Map: 실패 유형별 자동화 가능 범위
