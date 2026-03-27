# 실험 프로그램 개요

> 5변수 프레임워크에 기반한 20개 의도적 실패 실험.
> Ch.4의 핵심이며, Ch.5 분석의 입력이다.

---

## 실험 설계 원칙

1. **의도적 실패**: 실패를 두려워하지 않고, 의도적으로 실패시킨다.
2. **5변수 명시**: 각 실험에서 조작 변수와 통제 변수를 명시한다.
3. **1차 병목 식별**: "어떤 조건에서 무엇이 1차 병목이 되는가?"를 관찰한다.
4. **풍선 효과 기록**: 한 변수를 바꾸면 다른 곳에서 에러가 터지는 것을 놓치지 않는다.
5. **교차검증**: 핵심 실험은 다른 experimenter가 교차검증한다.

---

## 5개 관찰 축

| 축 | 폴더 | 실험 |
|----|------|------|
| 1. 모델 변경 | `axis-1-model-variation/` | E01~E04 |
| 2. Harness/surface 변경 | `axis-2-harness-surface/` | E05~E08 |
| 3. 제약 환경 병목 | `axis-3-constraint-bottleneck/` | E09~E14 |
| 4. Operator intervention | `axis-4-operator-intervention/` | E15~E17 |
| 5. AgentOps 내재화 | `axis-5-harness-internalization/` | E18~E20 |
| 반례 | `counterexamples/` | E19~E20 |
| 교차검증 | `cross-validation/` | xval 로그 |

---

## 교차검증 배정

```
Experimenter A: E01~E08 실행 → B가 E03, E05 교차검증
Experimenter B: E09~E16 실행 → A가 E11, E14 교차검증
Experimenter C: E17~E20 실행 → B가 E19, E20 교차검증
```

---

## 파일 형식

- 각 실험 로그: `ENN-[설명].md` (`template.md` 참조)
- 교차검증 로그: `xval-ENN-by-[A/B/C].md`
- 축 요약: 각 `axis-N-xxx/summary.md`

---

## 관련 도구

- `/log-experiment [ENN]` — Claude Code skill로 실험 로그 작성
- `scenario-master.md` — 20개 시나리오 전체 목록
- `template.md` — 실험 로그 템플릿 v4
