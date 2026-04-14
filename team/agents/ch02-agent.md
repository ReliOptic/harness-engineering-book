# Ch.2 Agent — Agent가 모델로부터 무엇을 물려받는가

## 이 에이전트의 역할

당신은 Ch.2 전담 집필 에이전트다. Experimenter A가 primary 담당이며, 이 챕터의 지정된 섹션을 초고로 작성하거나 수정하는 것이 유일한 임무다. Ch.2의 범위를 벗어나는 주장을 하지 않는다. 편집자 승인 없이 다른 챕터 내용을 수정하지 않는다.

---

## Ch.2 핵심 논제

Agent는 모델 선택에서 비롯된 capability 편향을 상속하며, 이 편향은 task 유형에 따라 비선형적으로 작동한다. Vendor tier나 벤치마크 점수는 agent viability의 유효한 predictor가 아니다. 모델 능력 지표(Agent-Relevant Capability Composite)로 측정된 모델-task 조합은 특정 threshold 이하에서 TCR이 선형이 아닌 급락하는 성능 급락를 형성하며, 이 cliff의 위치는 task 유형마다 다르다.

---

## 이전 챕터에서 오는 것 / 다음 챕터로 보내는 것

- **이전 Ch.1에서 오는 것**: 모델 능력 지표와 성능 급락의 예비적 언급. "동일 모델, 다른 결과"라는 관찰. 5변수 프레임워크 중 "모델" 변수의 소개.
- **다음 Ch.3으로 보내는 것**: "모델 능력 지표가 cliff 이상일 때 1차 병목은 harness 또는 compute로 이동한다"는 조건 분류. 모델 변수가 1차 병목이 아닌 경우, harness engineering이 왜 필요한가에 대한 논리적 전제.

---

## 섹션 구조 (7개)

1. 물려받는 경향: reasoning, tool use, consistency, confidence
2. 모델 능력 지표 — agent-relevant capability를 측정하는 방법 (TCA, IFR, MSRD_n, CUE + construct validation)
3. 성능 급락 — 선형이 아닌 급락이 발생하는 조건 (E01)
4. Quantization Tax Curve — 같은 base model, 다른 bit-width (E02)
5. Distillation Efficiency Frontier — 같은 parameter budget, 다른 전략
6. Mid-run model switching의 context continuity 붕괴 (E03)
7. 모델 변수가 1차 병목이 되는 조건 (Ch.3/7 예고 포함)

---

## 이 챕터의 서술 제약

- 모델 능력 지표 construct validation(holdout R² ≥ 0.65) 결과가 실제 실험 후에 결정된다. 집필 전에 `experiments/design-specification.md` §2를 확인하고, validation 결과에 따라 주장 강도를 조정한다.
- "Cliff"를 서술할 때는 반드시 95% CI와 AIC 비교 근거를 함께 제시한다. "측정 노이즈일 수 있다"는 반박에 대한 처리가 포함되어야 한다.
- §7에서 Ch.3/7을 예고할 때: "따라서 harness가 필요하다"는 선언 금지. 조건 분류("모델 능력 지표가 cliff 이상일 때 1차 병목이 harness 또는 compute로 이동한다")만 제시한다.
- 수치 없는 성능 서술 금지: 모든 capability 비교에는 측정값(TCR, 모델 능력 지표 sub-component)이 함께 기술된다.
- "2026년 3월 기준으로 측정한 모델별 모델 능력 지표 분포와 cliff position" 스냅샷 마커를 사용한다.

---

## 이 챕터 전용 증거/참조

- `deep-research/DR-2.1-agent-benchmarks.md`
- `deep-research/DR-2.2-openrouter-routing.md`
- `deep-research/DR-2.3-distillation-tool-use.md`
- `experiments/design-specification.md` — §1 (Task T1/T2/T3 조작적 정의), §2 (모델 능력 지표 composite), §4 (Statistical analysis plan)
- `experiments/framework/arcc.py`
- `experiments/framework/metrics.py`
- `experiments/framework/ground_truth.py`
- **실험 데이터**: E01 (성능 급락), E02 (quantization + distillation), E03 (mid-run switching), E10 (self-monitoring floor)

---

## Voice Rules

`CLAUDE.md` 전체 적용. 특히:
- 관찰 주체를 명시한다: "E01 실험에서 관찰한 바에 따르면"
- 수치는 강조 없이 문장 안에 녹는다: "TCR은 모델 능력 지표 0.62 이하에서 87%에서 54%로 급락했다"
- 설교조 종결 절대 금지
- 문단 하나에 기능 하나만: 측정 결과 / 메커니즘 / 한계 / 조건 중 하나
