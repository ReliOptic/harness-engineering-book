# /log-experiment [ENN]

실험 로그를 작성하고 해당 axis 폴더에 저장한다.

## 실행 단계

1. `experiments/template.md`의 형식을 읽는다.
2. `experiments/scenario-master.md`에서 해당 실험의 계획을 확인한다.
3. 실험 로그 초안을 작성한다 — 사용자에게 빈 템플릿을 채울 정보를 요청한다.
4. 해당 axis 폴더에 저장한다.

## Axis 배정

| 실험 | 폴더 |
|------|------|
| E01~E04 | `experiments/axis-1-model-variation/` |
| E05~E08 | `experiments/axis-2-harness-surface/` |
| E09~E14 | `experiments/axis-3-constraint-bottleneck/` |
| E15~E17 | `experiments/axis-4-operator-intervention/` |
| E18~E20 | `experiments/axis-5-harness-internalization/` |
| E21~E22 | `experiments/counterexamples/` |

## 필수 필드

로그 작성 시 반드시 포함해야 하는 필드:
- **조작 변수**: 5변수 중 무엇을 조작했는가
- **Primary bottleneck**: 5변수 중 어떤 것이 1차 병목이었는가
- **Balloon effect**: 한 변수를 바꿨을 때 다른 곳에서 에러가 터진 사례
- **Lesson learned**: 핵심 교훈 (다음 Fieldkit 아이템 후보)

## 사용 예시

```
/log-experiment E01
/log-experiment E14
```
