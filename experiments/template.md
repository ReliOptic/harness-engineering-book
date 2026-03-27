# 실험 로그 템플릿 v4

> 이 템플릿을 복사하여 각 실험 로그를 작성한다.
> 5변수 프레임워크, bottleneck, balloon effect, 교차검증 필드 포함.

---

```markdown
# [ENN] — [실험 제목]

**Experiment ID**: ENN
**Date**: YYYY-MM-DD
**Experimenter**: [A / B / C]
**Cross-validator**: [담당 experimenter]
**Target chapter**: Ch.N
**Status**: [ ] 계획 / [ ] 진행중 / [x] 완료 / [ ] 교차검증 완료

---

## Task

[구체적 task 설명. 무엇을 agent에게 시킨 것인가]

---

## 5변수 설정

| 변수 | 설정 |
|------|------|
| **조작 변수** | [5변수 중 무엇을 조작했는가] |
| **모델** | [모델명 + provider, 예: claude-opus-4-6 via OpenRouter] |
| **Harness config** | [harness 구성 상세 — 있음/없음/부분] |
| **Surface** | [CLI / API / 기타] |
| **Compute environment** | [VM 사양, 티어, CPU/RAM] |
| **Token budget** | [총 budget, 제한 여부] |

**통제 변수**: [조작하지 않은 변수들의 고정 조건]

---

## 실행 기록

### Tool usage
- 사용한 tool:
- tool call 횟수:
- tool call 성공률:

### 실행 로그 요약
[주요 단계, 분기점, 에러 발생 시점]

---

## 결과

**Success / Failure**: [ ] 성공 / [ ] 실패 / [ ] 부분 성공

**Failure type**: [분류 — tool call 실패 / context 손실 / compute 포화 / 기타]

---

## 분석

### Primary bottleneck
**1차 병목**: [5변수 중 무엇이었는가]
**근거**: [관찰된 증거]

### Balloon effect
[ ] 관찰됨 / [ ] 관찰 안 됨

[관찰된 경우: 어떤 변수를 조작했을 때 어떤 다른 변수에서 에러가 터졌는가]

---

## 측정값

| 지표 | 값 |
|------|----|
| Token usage (input) | |
| Token usage (output) | |
| 실행 시간 | |
| CPU 사용률 (peak) | |
| RAM 사용률 (peak) | |
| 비용 (API) | |

---

## Human Intervention

**개입 여부**: [ ] 없음 / [ ] 있음
**개입 종류**: [없으면 생략]
**개입 효과**: [없으면 생략]

---

## Recovery

**복구 시도**: [ ] 없음 / [ ] 있음
**복구 성공**: [ ] / **방법**: [없으면 생략]

---

## Lesson Learned

[핵심 교훈 — Operational Compiler 컴파일 후보 여부 포함]

---

## 교차검증 메모

**교차검증자**: [이름]
**교차검증 날짜**: YYYY-MM-DD
**검증 방법**: [동일 조건 재현 / 다른 조건 비교]
**검증 결과**: [일치 / 불일치 / 부분 일치]
**불일치 사항**: [있으면 기록]
```
