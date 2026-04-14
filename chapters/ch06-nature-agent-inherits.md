# Ch.6 — Agent가 모델로부터 무엇을 물려받는가

> 상태: 🔴 초고 v0.1 (2026-03-20) — §1~§7 초고 완성, [X] 플레이스홀더는 실험 데이터 보완 필요
> 담당: TBD (Experimenter A primary)
> 목표 분량: 10,000~12,000자

---

## 핵심 메시지

Agent는 모델 선택에서 비롯된 capability 편향을 상속하며, 이 편향은 task 유형에 따라 비선형적으로 작동한다. Vendor tier나 벤치마크 점수는 agent viability의 유효한 predictor가 아니다. 도구 호출 정확도, instruction following rate, multi-step reasoning depth, context 활용 효율로 측정된 모델-task 조합은 특정 threshold 이하에서 TCR이 선형이 아닌 급락하는 패턴을 형성하며, 이 급락 지점은 task 유형마다 다르다. Quantization과 distillation은 이 급락 지점을 다른 속도로 이동시킨다.

## 왜 Feature 중심 서사인가

이 챕터의 서사를 vendor 이름이나 모델 계열 중심으로 전개하지 않고 feature 중심으로 전개하는 이유는 방법론적 필수조건 때문이다. 실험서의 설명 단위는 "개입 가능한 변수"여야 한다. 모델 벤더는 관찰 가능한 라벨이지만, 엔지니어가 직접 조작할 수 있는 것은 도구 호출 정확도, instruction following rate, multi-step reasoning depth, context 활용 효율 같은 feature와 그 feature를 바꾸는 runtime 구성이다. 설명 단위를 라벨에 두면 처방은 "모델 교체"로 수렴하고, 설명 단위를 feature에 두면 처방은 "어떤 실패를 어떤 메커니즘으로 줄일 것인가"로 분해된다.

둘째, feature 중심 서사는 task 간 해석 안정성이 높다. 동일 모델도 T1과 T2에서 성과 순서가 달라질 수 있지만, 실패 양상(예: tool-call failure, silent logical drift)과 instruction 준수 패턴은 feature 축에서 비교 가능하다. 즉 모델 순위는 변해도 실패 메커니즘의 분류 체계는 유지된다. 이 안정성이 있어야 Ch.6의 결과를 Ch.8/Ch.9 운영 해석으로 연결할 수 있다.

셋째, feature 중심 서사만이 반증 가능하다. "어느 벤더가 더 낫다"는 진술은 조건이 바뀌면 쉽게 붕괴하지만, "모델의 agent task 수행 능력이 task별 임계점 이하이면 TCR이 급락한다"는 진술은 실험 설계와 통계 검정으로 반증 가능하다. 따라서 이 챕터는 vendor 우열 서사가 아니라 feature-메커니즘-결과의 인과 사슬을 기준으로 작성한다. 2026-03-20/21 파일럿 모델 매트릭스 결과는 이 방향을 탐색적으로 지지하지만(표본이 작아 보정 후 유의성 미달), 본문의 확정적 결론은 scale-up 실험 결과에만 의존한다.

## 학습 결과

- 도구 호출 정확도, instruction following rate, multi-step reasoning depth, context 활용 효율의 조작적 정의와 측정 절차를 이해하고, 자신의 환경에서 유사한 측정을 설계할 수 있다.
- 비선형 성능 급락의 존재와 메커니즘(multi-step chain에서의 오류 증폭)을 이해하고, "이 양자화 모델로 이 task는 된다"를 판단하는 근거를 갖는다.
- Quantization Tax Curve와 Distillation Efficiency Frontier의 차이를 이해하고, 동일 parameter budget에서 어느 전략이 agent viability 관점에서 더 효율적인지 판단할 수 있다.
- 모델 능력이 1차 병목이 되는 조건과, 그 조건이 충족되었을 때 병목이 harness 또는 실행 환경 제약으로 이동하는 조건을 구분할 수 있다.

## 집필 노트

- 관련 DR: DR-2.1 (agent 벤치마크), DR-2.2 (OpenRouter routing), DR-2.3 (distillation/quantization)
- 관련 실험: E01 (성능 급락 — 모델 능력 × task type × TCR), E02 (frontier vs. distilled), E03 (mid-run model switching), E10 (model capability floor for self-monitoring)
- 관련 Figure: Fig 1 (성능 급락 scatter + sigmoid fit), Fig 1b (Quantization Tax Curve), Fig 1c (Distillation Efficiency Frontier)

**모델 능력 측정 지표 (조작적 정의):**
- 도구 호출 정확도 (Tool Call Accuracy): 전체 tool call 중 schema-valid이고 semantically-correct한 비율
- Instruction Following Rate: 주어진 instruction의 명시적 constraint를 모두 충족한 output 비율
- Multi-Step Reasoning Depth (n): n-step chain 완료 시 논리적 오류 없이 유지된 단계 수 / n
- Context 활용 효율: relevant context proportion 변화가 output quality에 미치는 영향
- 이 네 지표의 weighted composite로 모델의 agent task 수행 능력을 측정. weights는 task type별로 다르며 sensitivity analysis가 필수.

**Construct Validation:**
- holdout task set에서 이 composite가 TCR을 예측하는 R² ≥ 0.65이어야 유효한 predictor로 사용.
- R² < 0.65이면 weight 재조정 또는 이 챕터의 주요 주장을 잠정적으로 표시.
- Validation이 실패할 경우의 처리 방식도 사전에 기록 (`experiments/design-specification.md` §2).

**비선형 성능 급락 메커니즘 (mechanism-first):**
- 왜 급락인가: 각 sub-task가 이전 sub-task의 출력에 의존하는 구조에서, 초기 오류가 증폭된다.
- 모델 능력 지표가 낮은 모델은 단일 단계는 통과하더라도 multi-step chain에서 오류 누적이 임계점을 초과한다.
- Sigmoid fit이 이 non-linearity를 포착한다. Piecewise linear vs. sigmoid: AIC 비교로 결정.

**예상 반박 대비:**
- "벤치마크가 agent capability proxy로 부족하다는 것은 알려진 사실": 모델 능력 지표는 agent-specific composite이며, 기존 벤치마크가 포착하지 못하는 차원(tool call accuracy, multi-step)을 명시적으로 포함한다. 이것이 측정 기여다.
- "Cliff가 아니라 측정 노이즈": 95% CI band를 그리고, cliff position의 신뢰구간을 보고한다. CI가 좁으면 cliff가 신호다.
- "양자화 방법마다 다른데 뭘 비교하는가": 양자화 방법을 통제변수가 아닌 독립변수로 취급. 같은 bit-width에서 방법 간 TCR 차이가 유의하면 그 자체가 발견이다.

**스냅샷 마커:** "2026년 3월 기준으로 측정한 모델별 모델 능력 지표 분포와 cliff position"

---

## Outline

**계획된 섹션:**

1. **물려받는 경향: reasoning, tool use, consistency, confidence**
   - 모델이 agent runtime에 도입하는 네 가지 행동 편향의 성격
   - 왜 이 네 가지가 서로 다른 task 유형에서 다르게 작동하는가
   - Mechanism first: 동일 input, 다른 모델, 다른 결과가 나타나는 구조적 이유 — 확률 분포의 차이가 multi-step에서 어떻게 증폭되는가

2. **모델 능력 측정 — 벤치마크가 포착하지 못하는 것**
   - Vendor tier와 벤치마크가 agent viability의 유효한 predictor가 아닌 이유 (측정 내용의 불일치)
   - 도구 호출 정확도, instruction following rate, multi-step reasoning depth, context 활용 효율의 조작적 정의 및 측정 절차
   - Composite weight 결정 원리와 sensitivity analysis
   - Construct validation: holdout R² ≥ 0.65 기준과 그 기준의 의미 — 이 기준이 통과되지 않으면 이후 분석에 어떤 조건이 붙는가

3. **비선형 성능 급락 — 선형이 아닌 급락이 발생하는 조건**
   - E01 실험 설계: 모델 능력 지표 scatter plot × task type × TCR (harness-off 조건)
   - Task-conditional sigmoid fit: T1(Code Review), T2(Multi-Step), T3(Long-Horizon)에서 cliff position이 다른 이유
   - 최소 모델 능력 임계점: task별 최소 모델 능력 지표 threshold의 실무적 의미
   - 예상 반박: cliff가 아니라 측정 노이즈일 수 있다 — 95% CI와 AIC 비교로 검증

4. **Quantization Tax Curve — 같은 base model, 다른 bit-width**
   - FP16 → Q8 → Q6 → Q4 → Q3 → Q2 경로에서 모델 능력 지표가 감소하는 비율
   - Adaptive sampling 전략: FP16과 Q4 먼저, cliff 근처에서 Q8/Q6/Q3로 촘촘하게
   - Model family마다 quantization tax가 다른 이유 — base model의 어떤 특성이 tax를 결정하는가
   - 실무적 처방: 어느 bit-width에서 cliff를 건너게 되는가 (task별로 다른 답)

5. **Distillation Efficiency Frontier — 같은 parameter budget, 다른 전략**
   - Distillation vs. quantization: 동일 parameter budget에서 agent viability 관점의 효율성 비교
   - Pareto frontier 존재 여부: 같은 비용에서 어느 전략이 더 높은 모델 능력 지표를 제공하는가
   - 예상 반박: distillation은 학습 데이터 의존적 — 학습 domain 외 task에서의 generalization 한계

6. **Mid-run model switching의 context continuity 붕괴 (E03)**
   - 실행 도중 모델을 교체하면 무슨 일이 벌어지는가
   - Context state의 암묵적 가정이 모델 교체 시 어떻게 위반되는가
   - 운영 처방: 언제 mid-run switching이 허용 가능하고, 언제 전체 재시작이 필요한가
   - Fig 1b (Quantization Tax Curve)와의 연결: 동일 family 내 switching은 continuity를 얼마나 보존하는가

7. **모델 능력이 1차 병목이 되는 조건**
   - 모델 능력이 임계점 이하인 경우에만 모델이 1차 병목이다
   - 임계점 이상일 때 1차 병목은 harness 또는 실행 환경 제약으로 이동한다 (Ch.7/Ch.8 예고)
   - 이 조건 분류 없이 "모델 교체"를 처방하면 잘못된 개입이 될 수 있다
   - E10: self-monitoring을 위한 model capability floor — Agent-2 전환의 하한 조건 (Ch.11 예고)

---

**핵심 Figure:**

- **Fig 1** — 모델 능력 × task 복잡도 성능 급락: scatter plot + task-conditional sigmoid fit + 95% CI band. 급락 지점 per task type. Harness-off 조건 기준. (E01 확장)
- **Fig 1b** — Quantization Tax Curve: 동일 base model 4종 × 5단계 bit-width → 모델 능력 지표 변화 경로. Model family별 cliff crossing point 표시.
- **Fig 1c** — Distillation Efficiency Frontier: 동일 parameter budget에서 distill vs. quantize의 모델 능력 지표 비교. Pareto frontier 표시.

<!-- 섹션별 초고는 /draft ch02 N 으로 작성 -->

## 참조

- `deep-research/DR-2.1-LLM-agent-benchmarks.md`
- `deep-research/DR-2.2-OpenRouter-model-analysis.md`
- `deep-research/DR-2.3-model-distillation-tool-use.md`
- `experiments/design-specification.md` — §1 (Task specification T1/T2/T3), §2 (모델 능력 지표 composite), §4 (Statistical analysis plan)
- `experiments/figure_expansion.md` — Figure 1 재설계 (성능 급락, Quantization Tax, Distillation Frontier)
- `experiments/framework/arcc.py`
- `experiments/framework/metrics.py`
- `experiments/framework/ground_truth.py`

---

## §1 물려받는 경향: reasoning, tool use, consistency, confidence

> 상태: 🔴 초고 v0.1 (2026-03-18)

Ch.5에서 관찰한 것 — 동일한 모델, 다른 실행 조건, 다른 결과 — 은 모델 변수를 1차 병목에서 배제하는 근거였다. 그러나 모델 변수를 배제한다는 것이 모델 선택이 중요하지 않다는 뜻은 아니다. 모델이 agent runtime에 도입하는 편향은 실재하며, 그 편향이 어떤 task 유형에서 어떤 방식으로 증폭되는가가 이 챕터의 분석 대상이다.

모델은 확률적 텍스트 생성기이며, 그 확률 분포는 학습 데이터와 학습 방법에 의해 형성된다. 단일 LLM 호출에서 이 확률 분포의 차이는 출력 품질의 차이로 나타난다. 그러나 agent가 수행하는 것은 단일 호출이 아니다 — 각 step의 출력이 다음 step의 입력이 되는 multi-step chain에서, 초기 단계의 확률 분포 차이는 downstream step에서 증폭된다. 수학적으로 표현하면: 각 단계에서 오류가 발생할 확률이 p이고 n단계 chain이 있다면, 오류 없이 완료할 확률은 (1-p)^n이다. p=0.05이면 10단계 chain의 성공률은 약 60%이고, 40단계에서는 약 13%다. 이 비선형 감소가 성능 급락의 수학적 기반이다.

필자가 agent runtime에서 관찰한 모델 편향은 네 차원에서 나타났으며, 이 차원들은 독립적으로 작동하는 것이 아니라 오류가 downstream으로 증폭되는 연쇄를 이룬다.

Reasoning의 문제는 multi-step constraint tracking에서 시작된다. 어떤 모델은 constraint를 명시적으로 추적하면서 multi-step plan을 구성하지만, 다른 모델은 표면적으로 타당해 보이면서도 중간 단계에서 암묵적 constraint를 위반하는 plan을 생성한다. 후자의 위반은 해당 단계에서 감지되지 않고 전체 task 수준에서 드러난다. 이 reasoning 실패가 tool call 레이어에서 증폭된다. Reasoning이 constraint를 놓친 상태에서 생성된 plan은 schema를 완벽하게 준수하는 tool call을 만들어내면서도 현재 task 단계와 무관한 도구를 호출한다 — TCA(Tool Call Accuracy)에 semantic 차원이 필요한 이유가 여기 있다.

이 두 편향이 겹치는 환경에서 consistency 저하가 각 단계의 오류를 심화시킨다. Consistency는 동일한 prompt와 context 조건에서 출력 분포의 분산을 가리킨다. Consistency가 낮은 모델은 reasoning 오류와 tool call 오류가 각 단계에서 다른 방식으로 발현되기 때문에 오류 패턴이 예측 불가능하고, harness 없이 장기 실행할 때 성능 범위를 설정하기 어렵다.

Calibration이 이 cascade를 recovery 시스템이 감지하기 어렵게 만든다. Calibration이란 모델이 자신의 출력에 부여하는 확신도와 실제 출력 정확도의 일치 정도를 말한다. Calibration이 낮은 모델은 틀린 출력을 확신과 함께 생성하기 때문에, agent의 recovery 메커니즘이 이 출력을 재시도 대상으로 식별하기 어렵다. Tool call이 schema를 통과하고 출력이 형식적으로 완결된 상태에서 방향이 틀린 경우가 여기에 해당한다.

이 네 가지 편향이 task 유형에 따라 다르게 증폭되는 구조를 측정하는 것이 모델 능력 지표이며, 그 측정에서 드러나는 비선형 패턴이 성능 급락다. Ch.5에서 관찰 수준으로 언급된 이 패턴을 Ch.6에서 측정 가능한 형태로 정의하고, Ch.8에서 실험적으로 검증한다.

---

## §2 모델 능력 측정 — 벤치마크가 포착하지 못하는 것

> 상태: 🔴 초고 v0.1 (2026-03-20)

Vendor tier가 agent viability의 예측 변수로 불충분하다는 주장은 처음에는 자명해 보이지 않는다. GPT-4o나 Claude Opus가 GPT-3.5나 Haiku보다 성능이 낫다는 것은 대부분의 벤치마크가 확인한다. 그러나 "성능이 낫다"는 측정이 agent runtime에서의 성능과 일치하는가는 별개의 질문이다. MMLU나 HumanEval 같은 표준 벤치마크는 단일 LLM 호출의 품질을 측정한다 — 독립적인 문제를 얼마나 잘 푸는가. Agent가 수행하는 것은 다르다. 각 호출의 출력이 다음 호출의 입력이 되는 연쇄 구조에서, 단일 호출 품질이 높더라도 다음 단계로 전달되는 오류의 패턴이 다르면 chain 전체의 결과는 다르게 나온다. 벤치마크 점수가 포착하지 못하는 것이 tool call의 semantic 정확도, instruction constraint의 누적 추적 정확도, 장기 chain에서의 오류 누적 저항성이다. 모델 능력 지표는 이 세 차원을 포함하도록 설계된 composite metric이다.

모델 능력 지표의 네 하위 지표는 §1에서 서술한 네 가지 편향에 각각 대응한다. TCA(Tool Call Accuracy)는 tool use 편향을 포착한다 — 전체 tool call 중 schema를 만족하고 semantically correct한 비율. Schema validity만으로는 부족하다는 것이 §1의 관찰이었다. Schema를 통과하면서도 현재 task 단계와 무관한 도구를 호출하는 경우, TCA의 semantic 차원이 이를 실패로 기록한다. IFR(Instruction Following Rate)은 reasoning 편향을 측정한다 — 주어진 instruction의 명시적 constraint를 모두 충족한 output의 비율. 이진 판정이다: constraint 하나라도 위반하면 해당 step의 IFR = 0. §1의 (1-p)^n 공식에서 p는 IFR 기반으로 추정된다. MSRD_n(Multi-Step Reasoning Depth)은 consistency 편향을 측정한다 — n-step chain을 완료했을 때 논리적 오류 없이 유지된 단계 수를 n으로 나눈 값. n이 클수록 consistency 요구가 높아지기 때문에, MSRD_40과 MSRD_10은 같은 모델에서도 다른 값이 나온다. CUE(Context Utilization Efficiency)는 calibration 편향을 간접적으로 측정한다 — relevant context proportion 변화가 output quality에 미치는 영향의 크기. Calibration이 낮은 모델은 relevant context가 줄어도 확신 수준을 유지하며, 이것이 CUE 값의 불안정성으로 나타난다.

모델 능력 지표는 이 네 지표의 weighted composite이다. 가중치는 task 유형에 따라 다르게 설정된다 — T1(Code Review)에서는 TCA와 IFR의 비중이 높고, T3(Long-Horizon Execution)에서는 MSRD_n의 비중이 높다. 가중치 설정은 sensitivity analysis를 동반한다. 모델 능력 지표가 가중치 변화에 얼마나 민감한가 — 즉 특정 가중치 조합에서만 유효한 결론이 나오는가를 확인하는 절차다. Sensitivity analysis를 생략하면 가중치 선택이 결론을 만들어내는 circular 구조가 될 수 있다.

Construct validation은 모델 능력 지표가 측정하려는 것을 실제로 측정하는지 확인하는 단계다. 기준은 하나다: holdout task set에서 모델 능력 지표가 TCR을 예측하는 R² ≥ 0.65. 이 기준을 통과하지 못하면 모델 능력 지표를 독립 변수로 사용하는 이후 분석 — 성능 급락 측정, Quantization Tax 비교, Distillation Frontier 탐색 — 전체가 잠정적으로 표시된다. R² < 0.65이면 가중치를 재조정하거나 하위 지표 조합을 수정한다. 이 과정과 결과는 `experiments/design-specification.md` §2에 기록된다.

---

## §3 비선형 성능 급락 — 선형이 아닌 급락이 발생하는 조건

> 상태: 🔴 초고 v0.1 (2026-03-20)

E01은 단순한 실험이다. 여러 모델에 대해 모델 능력 지표를 측정하고, 동일한 모델들을 harness-off 조건에서 T1/T2/T3 task에 실행하여 TCR을 측정한다. 그 두 값을 scatter plot에 올린다. 질문은 하나다: 모델 능력 지표와 TCR 사이의 관계가 선형인가.

E01의 scatter plot에서 검증하려는 패턴은 선형 관계가 아니다. 모델 능력 지표가 높은 구간에서는 TCR도 높고, 모델 능력 지표가 낮은 구간에서는 TCR도 낮다 — 이것만 보면 선형처럼 보인다. 이 초고가 현재 가정하는 것은, 모델 능력 지표가 task-specific threshold를 건너는 지점에서 TCR이 급락할 가능성이 높다는 점이다. Threshold 이상에서는 TCR이 모델 능력 지표 변화에 상대적으로 둔감하고, threshold 이하로 내려가는 순간 TCR이 선형이 아닌 가파른 경사로 떨어질 수 있다. Sigmoid 함수가 이 패턴을 piecewise linear보다 더 잘 포착하는지 여부는 AIC 비교로 결정하며, 수치는 `[X]` 플레이스홀더가 채워진 뒤 확정적으로 서술한다.

Threshold의 위치도 task 유형에 따라 달라질 가능성이 높다. 이 초고 단계에서는 T3(Long-Horizon Execution)의 cliff position이 T1(Code Review)보다 높게 나타날 것이라고 가정한다. 이유는 §1의 수학적 구조에서 나온다 — 40단계 chain이 10단계 chain보다 각 단계의 오류에 더 민감하기 때문에, 동일한 모델 능력 지표에서도 T3의 TCR은 T1보다 낮아질 가능성이 높다. 실제 cliff position은 T1/T2/T3 각각의 `[X]` 측정값이 확보된 뒤 수치로 확정한다.

최소 모델 능력 임계점은 이 cliff position을 실무 언어로 번역한 개념이다. 특정 task 유형에서 agent를 harness-off 조건으로 배포할 때, TCR이 허용 가능한 수준을 유지하는 최소 모델 능력 지표 threshold. 이 개념이 중요한 것은 부정을 통해서다: 최소 모델 능력 임계점 이하의 모델을 선택하면 harness를 아무리 정교하게 설계해도 TCR의 기초가 손상된다. Harness는 모델 capability를 보완하는 것이 아니라, 충분한 capability를 가진 모델이 만드는 failure를 관리 가능한 형태로 재배분하는 구조다.

95% CI band를 scatter plot에 함께 표시하는 이유는 "cliff가 아니라 측정 노이즈"라는 반박에 대한 구조적 응답이다. CI band가 좁고 cliff position 근방에서 TCR의 하강이 CI 범위를 벗어난다면 — 즉 여러 실행에서 일관되게 같은 지점에서 급락이 관찰된다면 — 그것은 노이즈가 아니라 신호로 읽을 수 있다. cliff position의 95% CI 폭은 `[X]` 측정값이 채워진 뒤에만 본문 수치로 고정한다.

---

## §4 Quantization Tax Curve — 같은 base model, 다른 bit-width

> 상태: 🔴 초고 v0.1 (2026-03-20)

Quantization은 모델 배포 비용을 낮추는 표준 기법이다. FP16에서 Q4로 줄이면 메모리 사용량이 절반 이하로 줄어들고, 추론 속도가 빨라지며, 같은 하드웨어에서 더 많은 요청을 처리할 수 있다. 이 이점은 단일 LLM 호출 benchmark에서도 상당 부분 유지되는 것으로 알려져 있다. 문제는 agent task에서의 모델 능력 지표 하락이 벤치마크 하락보다 더 크고, 비선형적이며, 모델 family마다 다른 패턴을 보일 가능성이 있다는 점이다. 초고 단계의 `[X]` 수치는 이 비교가 실제로 얼마나 벌어지는지를 나중에 확정하기 위한 자리다.

Quantization Tax Curve는 동일 base model의 bit-width 단계별 모델 능력 지표 변화를 기록한다. FP16 → Q8 → Q6 → Q4 → Q3 → Q2 경로에서 모델 능력 지표를 측정하는데, 모든 단계를 균등한 간격으로 측정하지 않는다. 적응형 샘플링 전략을 쓴다: FP16과 Q4를 먼저 측정하여 모델 능력 지표 하락의 전체 범위를 파악한다. 그 다음 cliff position 근방 — 즉 모델 능력 지표가 해당 task의 최소 모델 능력 임계점 근처를 통과하는 구간 — 에서 Q8, Q6, Q3를 추가로 측정한다. Cliff 근처의 bit-width에서 모델 능력 지표 변화율이 급격하기 때문에, 이 구간의 해상도가 실무적으로 중요하다. "Q4는 되고 Q3는 안 된다"와 "Q6까지는 되고 Q4에서 cliff를 건넌다"는 다른 처방을 만든다.

Model family마다 quantization tax가 다른 이유는 base model의 구조적 특성에서 나온다. 탐색적 관찰 수준에서, attention head 수가 많고 activation 분산이 낮은 모델은 같은 bit-width에서 모델 능력 지표를 더 잘 유지하는 경향이 있었다. 이것은 단일 large weight의 영향이 작을수록 quantization으로 인한 정보 손실이 분산되기 때문으로 보인다 — 그러나 이 해석은 현재 실험의 관찰 범위를 넘는다. 실무적으로는: 동일 parameter size의 두 모델이 있을 때, 어느 쪽이 quantization에 더 강한지는 사전에 알 수 없고 모델 능력 지표를 직접 측정해야 한다.

2026년 3월 기준 실험이 완료되면, 4개 모델 family의 quantization tax 패턴은 이 구간 차이를 구체적으로 보여줄 가능성이 있다. 현재 초고가 보존하는 가설은, T3 task에서 cliff를 건너는 bit-width가 모델 family에 따라 Q6에서 Q3까지 분포할 수 있고, T1 task에서는 더 낮은 bit-width까지 최소 모델 능력 임계점을 유지할 수 있다는 점이다. 이 비대칭 — task 유형에 따른 cliff crossing bit-width의 차이 — 이 quantization 결정의 핵심 정보가 된다. 개별 모델명과 bit-width 수치는 `[X]`가 채워진 뒤 확정한다.

---

## §5 Distillation Efficiency Frontier — 같은 parameter budget, 다른 전략

> 상태: 🔴 초고 v0.1 (2026-03-20)

Distillation과 quantization은 다른 경로로 같은 목적에 도달한다. Quantization은 기존 모델의 수치 정밀도를 낮춰 크기를 줄인다. Distillation은 더 작은 모델을 더 큰 모델의 출력 분포에서 학습시킨다 — 결과물은 크기가 작지만 독립적으로 학습된 모델이다. 두 전략이 agent viability 관점에서 어느 쪽이 효율적인가라는 질문은 배포 결정에서 반복적으로 나타난다. E02가 이 비교를 설계한 방식은 parameter budget을 통제 변수로 고정하는 것이다: 동일한 추론 비용을 소비하는 조건에서, FP16 대형 모델의 quantized 버전과 동급 크기의 distilled 모델 중 어느 쪽이 더 높은 모델 능력 지표를 제공하는가.

E02가 확인하려는 것은 pareto frontier의 존재 여부다. 동일 parameter budget에서 모든 task 유형에 걸쳐 distillation이 우월하거나 quantization이 우월한 것이 아니라, task 유형에 따라 우위가 갈릴 가능성이 높다. 초고 단계에서는 T1(Code Review)와 T3(Long-Horizon Execution)에서 우위가 달라질 수 있다는 가설만 유지하고, `[X]%p` 수치와 frontier 위치는 측정 이후에만 확정적으로 적는다.

이 결과에는 중요한 조건이 있다. Distillation된 모델의 성능은 teacher 모델의 출력 분포와 distillation 학습 데이터의 domain에 강하게 의존한다. E02에서 사용한 distilled 모델들은 일반적인 code 및 reasoning task로 학습된 것들이다. T1 task에서 distillation이 우위를 보인 것은 이 모델들의 학습 domain과 T1이 겹치는 부분이 크기 때문일 수 있다. T1과 다른 domain의 code review task나, 이 모델들이 학습하지 않은 유형의 instruction constraint를 가진 T2 task에서는 이 우위가 유지되지 않을 수 있다. Distillation 전략을 선택할 때 해당 distilled 모델의 학습 domain이 실제 배포 task와 얼마나 겹치는지를 확인하는 것이 선행되어야 한다.

---

## §6 Mid-run model switching의 context continuity 붕괴 (E03)

> 상태: 🔴 초고 v0.1 (2026-03-20)

실행 도중 모델을 교체하는 상황은 드물지 않다. 비용 예산이 소진될 때, 특정 단계에서 더 강력한 모델이 필요할 때, 또는 모델 API가 중단되어 대체 모델로 전환할 때 mid-run switching이 발생한다. Context가 전달된다면 — 이전 모델이 생성한 conversation history와 tool call 결과를 새 모델에게 그대로 전달한다면 — 실행이 이어질 수 있을 것처럼 보인다. E03은 이 기대가 어떤 조건에서 충족되지 않는지를 설계한 실험이다.

Context state는 단순한 텍스트 이력이 아니다. 이전 모델이 생성한 context에는 그 모델의 추론 패턴이 암묵적으로 반영되어 있다. 어떤 도구가 이미 호출되었고 어떤 결과가 관련 있다고 판단했는가, constraint를 어떤 방식으로 추적하고 있었는가, 다음 단계에서 어떤 행동을 예상하고 있었는가 — 이 암묵적 구조가 새 모델에게는 그저 텍스트 토큰으로 전달된다. 새 모델은 이 context를 자신의 추론 패턴으로 재해석한다. 두 모델의 추론 패턴이 충분히 다르면, 동일한 context에서 다른 해석이 나오고 이전 단계가 암묵적으로 가정했던 연속성이 끊긴다.

E03에서 관찰된 패턴은 세 가지로 분류되었다. 첫 번째는 tool call 패턴 전환이다 — 이전 모델이 사용하던 도구 호출 시퀀스를 새 모델이 다른 시퀀스로 교체했다. 같은 task를 다른 도구 조합으로 접근하는 것 자체는 문제가 아니지만, 이전 단계에서의 tool call이 특정 상태를 만들었다면 — 예를 들어 파일을 특정 형식으로 수정한 상태 — 새 모델이 그 상태를 전제하지 않은 채 다른 도구를 호출하면 충돌이 발생한다. 두 번째는 이전 단계 판단 무시다 — 새 모델이 이전 모델이 이미 검토하고 제외한 option을 재고려하기 시작했다. 세 번째는 constraint 재설정이다 — 이전 모델이 instruction에서 추출한 암묵적 constraint를 새 모델이 다르게 해석하여 task 방향이 바뀌었다.

Switching의 충격은 model family 간 거리에 비례할 가능성이 높다. 동일 family 내에서의 switching이 family를 넘는 switching보다 context continuity를 더 잘 유지할 것이라는 가설은 자연스럽지만, `[X]%` 수치가 채워지기 전까지는 관찰 사실처럼 단정하지 않는다. 따라서 이 절의 운영 처방도 잠정적이다: mid-run switching이 불가피할 때는 동일 family 내에서 tier를 이동하는 것이 context continuity 보존에 유리할 가능성이 높고, Family를 넘는 switching이 필요하다면 switching 지점에서 명시적 handoff protocol이나 전체 재시작을 비교해야 한다.

---

## §7 모델 능력이 1차 병목이 되는 조건

> 상태: 🔴 초고 v0.1 (2026-03-20)

이 챕터가 모델 능력 지표와 성능 급락를 측정하는 이유는 inbound 방향을 가장 중요한 것으로 자리매김하기 위해서가 아니다. 반대다 — model capability가 1차 병목이 되는 조건을 명확히 해야, 그 조건이 충족되지 않을 때 다른 방향에서 답을 찾을 수 있다.

모델 변수가 1차 병목인 조건은 하나다: 현재 배포된 모델의 모델 능력 지표가 실행할 task의 최소 모델 능력 임계점 이하에 있을 때. 이 조건에서는 harness를 정교하게 설계하거나 compute를 추가해도 TCR이 구조적으로 제한된다. §3의 sigmoid fit에서 cliff 이하 구간의 기울기가 가파르다는 것은, 이 구간에서의 성능 개선이 모델 모델 능력 지표를 올리지 않고는 어렵다는 것을 의미한다. 이 조건이 진단된다면 모델 업그레이드 또는 quantization 수준 재검토가 1순위 개입이다.

모델 능력 지표가 최소 모델 능력 임계점 이상에 있을 때 1차 병목은 모델 변수가 아니다. §1의 편향들 — reasoning, tool use, consistency, calibration — 이 실재하더라도, 그 편향이 만드는 실패를 harness가 관리 가능한 형태로 전환할 수 있다면 모델 교체보다 harness 변수 조작이 효율적이다. Ch.7에서 정의하는 실패 재분류이 이 조작의 효과를 측정하는 방법이고, Ch.8 E05~E08에서 harness 변수를 격리하여 실험적으로 검증한다.

이 조건 분류 없이 "성능이 나쁘다 → 모델을 교체한다"는 처방 경로는 구조적으로 취약하다. 모델 능력 지표가 최소 모델 능력 임계점 이상인 상태에서 더 비싼 모델로 교체하면 compute 비용이 증가하지만 TCR 개선이 기대에 미치지 못한다 — 병목이 inbound 방향이 아니었기 때문이다. 반대로 모델 능력 지표가 최소 모델 능력 임계점 이하인 상태에서 harness를 강화하면 HOR만 올라가고 fundamental failure rate는 변하지 않는다. Harness 중심의 네 영역에서 inbound의 역할은 이 분류 기준을 제공하는 것이다.

E10은 이 분류의 하한을 측정한다. Agent가 자신의 모델 능력 지표 sub-components를 self-estimate하는 self-monitoring 능력은 그 자체로 모델 능력 지표를 요구한다. E10은 self-monitoring이 신뢰 가능하게 작동하기 시작하는 최소 모델 능력 지표 threshold를 탐색한다. 이 threshold가 중요한 것은 Ch.11에서 서술하는 Agent-2 전환과 직결되기 때문이다 — self-immune system의 하한 조건은 "self-monitoring이 신뢰 가능한 모델 능력 지표 이상"이라는 가설이다. E10의 측정값 `[X]`이 채워지기 전까지는 하한의 존재만 잠정적으로 제시한다.

---
## §8 정량적 스냅샷과 추가 관찰 (2026-03 업데이트)

앞서 서술된 개념적 프레임워크와 더불어, 최근의 연구 동향(DR-2.1, DR-2.3)은 모델 능력 지표와 성능 급락의 존재를 뒷받침하는 추가적인 정량적 단서들을 제공하고 있다. 모델이 환경 내에서 복잡한 도구를 다루는 능력을 평가하는 최신 벤치마크(예: ToolGym, CallNavi) 결과에 따르면, 모델의 매개변수 크기가 일정 수준(threshold) 이하로 떨어질 때 함수 호출(function calling)의 구조적 정확도뿐만 아니라 맥락을 반영한 '의미론적 정확도(semantic accuracy)'가 비선형적으로 급락하는 현상이 일관되게 관찰된다.

특히 양자화(Quantization)와 관련하여, 4-bit 양자화 환경에서 특정 모델들이 단순한 텍스트 생성에서는 성능 저하가 크지 않지만 다단계 에이전트 작업(Multi-agent coding 등)에서는 최대 24%에 달하는 '플립 현상(성공이 실패로 뒤집히는 현상)'을 보인다는 실증 연구(arXiv:2407.09141)는 이 챕터에서 설정한 'Quantization Tax Curve'의 기울기가 작업 복잡도에 따라 얼마나 가파를 수 있는지를 시사한다.

또한 도구 호출에 특화된 모델 증류(Distillation) 기법들(예: ODIA, ToolACE)은 훈련 단계에서부터 도구 사용의 맥락적 한계를 보완하려는 시도로, §5에서 논의한 'Distillation Efficiency Frontier'를 특정 방향(Tool-use 향상)으로 강하게 밀어붙이고 있다. 동일한 파라미터 예산 내에서 범용 추론 모델을 양자화할 것인가, 아니면 도구 사용에 특화된 소형 모델을 증류할 것인가에 대한 결정은 향후 실험 수치(`[X]`)가 채워짐에 따라 더욱 명확한 파레토 프론티어(Pareto Frontier)로 시각화될 것이다.

이러한 관찰들은 "어느 지점에서 모델이 시스템의 1차 병목이 되는가?"라는 이 챕터의 핵심 질문을 더욱 구체화하며, 하네스(Harness)와 같은 외부 구조적 개입이 불가피해지는 임계점을 설정하는 데 중요한 척도를 제공한다.
