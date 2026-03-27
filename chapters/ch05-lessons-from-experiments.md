# Ch.5 — 실험 결과에서 배운 것: AgentOps와 Harness의 실무

> 상태: 🔲 scaffold (2026-03-18) — Ch.4 실험 완료 후 수치 보완 필요
> 담당: Kiwon
> 목표 분량: 10,000~12,000자

---

## 핵심 메시지

Ch.4의 22개 실험에서 추출하는 패턴은 세 단계의 번역을 거쳐야 실무적 의미를 갖는다. 실험실 metric(TCR, TTFF, RSuccR)에서 운영 metric(MTTR, Human Escalation Rate)으로, 다시 비용 metric(TotalCost, CostIndex)으로. 이 번역 없이 "harness가 효과적이다"는 주장은 "so what?" 질문에 답할 수 없다. 번역을 완료한 결론은 하나다: optimal HOR은 존재하며, 그 점 이상에서는 harness 자체가 새로운 1차 병목이 된다.

## Feature 중심 해석의 필연성

Ch.5가 결과 해석에서 feature 중심 구조를 채택하는 이유는 운영 의사결정의 형태와 직접적으로 연결된다. 운영자는 벤더 라벨을 조정하지 않고, 실패율·복구시간·budget 소모·도구 호출 정확도 같은 feature를 조정한다. 따라서 분석 단위가 vendor 서사에 머물면 운영 규율로 변환되지 않는다. 반대로 분석 단위를 feature로 고정하면 "어떤 구성 변화가 MTTR/HER/TotalCost를 얼마나 바꾸는가"를 계량적으로 기술할 수 있다.

이 챕터의 3단계 번역(실험실→운영→비용)은 그 자체가 feature 중심 논증이다. TCR, TTFF, RSuccR 같은 결과 변수도 원인을 분해할 때는 IFR 저하, TCA 붕괴, goal drift, budget saturation 같은 feature 사건으로 환원되어야 한다. 이 환원이 없으면 CostIndex 변화의 원인을 특정할 수 없어 처방 우선순위(예: memory boundary 우선 vs recovery hook 우선)를 정할 수 없다.

추가로, feature 중심 해석은 과제 확장성에서 우월하다. 모델 우열은 task가 바뀌면 순서가 쉽게 바뀌지만, failure taxonomy와 harness component 기여도는 task가 달라도 비교 가능한 공통 좌표를 제공한다. 따라서 Ch.5는 "어느 모델이 더 강한가"가 아니라 "어떤 feature 조합에서 병목이 어디로 이동하는가"를 중심으로 결론을 제시한다. 이것이 Ch.6 Operational Compiler 설계 원칙으로 직접 연결되는 유일한 경로다.

## 학습 결과

- 실험 결과를 실험실 metric → 운영 metric → 비용 metric으로 번역하는 3단계 체계를 이해하고 적용할 수 있다.
- Failure Budget Reallocation 결과를 정량화하고, harness가 어떤 failure를 어떤 failure로 전환하는지 보고할 수 있다.
- HOR × RSuccR trade-off에서 optimal harness configuration을 판단하는 방법을 이해한다.
- Harness component별 ablation을 통해 각 component의 marginal contribution을 분리하고 도구화 우선순위를 결정할 수 있다.
- Scaling 조건(model capability × harness value)과 temporal stability(harness fatigue)를 해석할 수 있다.
- Confirmatory/exploratory 구분을 유지하면서 실험 결과를 학술적 확장 후보로 분류할 수 있다.

## 집필 노트

- 관련 DR: DR-5.1 (실패 패턴 분석), DR-5.2 (compute cost 최적화), DR-5.3 (VM 리소스 관리)
- 관련 실험: E01~E22 전체 분석 (Ch.4 실험 완료 후 작성)
- Ch.4와의 관계: Ch.4가 실행과 기록이라면, 이 챕터는 confirmatory analysis와 exploratory 발견을 구분하면서 분석한다. Ch.4에서 결과를 보고하고 이 챕터에서 해석한다.

**3단계 번역 체계 (조작적):**
- Level 1 (실험실): TCR, TTFF, RSuccR, ARCC — 실험에서 직접 측정
- Level 2 (운영): MTTR(Mean Time To Recovery, 분), HER(Human Escalation Rate, %) — Level 1에서 파생
- Level 3 (비용): TotalCost = Cost_compute(HOR) + Cost_failure(RSuccR, MTTR) + Cost_escalation(HER)
  - CostIndex = TotalCost / TotalCost(HOR=0) → HOR=0일 때 1.0 기준

**Cost Model 가정 (명시, 2026년 3월 기준):**
- claude-sonnet-4-6: $3.00/MTok input, $15.00/MTok output
- 시니어 엔지니어 hourly rate: $150/hr
- 3개 scenario: A(API), B(self-hosted GPU, compute×0.4), C(hybrid, compute×0.7, engineer×1.2)
- 3개 scenario에서 동일 optimal HOR 구간 유지 → 결론 robust

**Ablation 분석:**
- Harness component를 하나씩 제거했을 때 RSuccR과 MTTR 변화. Fig 10 (Harness Ablation)의 기반.
- 각 component의 marginal contribution 정량화 → Ch.6 Operational Compiler 구성 우선순위의 근거.
- Component 간 상호의존 탐색: 단독으로는 효과 없고 조합에서만 효과 있는 경우 (exploratory).

**Scaling 분석 (Fig 11):**
- Model capability(ARCC)가 높아질 때 harness value가 감소하는가, 역할이 전환되는가
- 가설: ARCC가 cliff 이상으로 충분히 높아지면 harness의 역할이 "방어(실패 차단)" → "조정(실행 품질 유지)"으로 전환.

**Temporal stability (Fig 12):**
- 72시간 연속 운영에서 동일 harness configuration의 RSuccR 변화
- Harness fatigue 존재 여부와 메커니즘 — 무엇이 degradation을 만드는가

---

## Outline

**계획된 섹션:**

1. **22개 실험 결과 종합: 어떤 변수가 어떤 조건에서 1차 병목이었는가**
2. **Failure Budget Reallocation 정량 분석**
3. **운영 metric 번역: MTTR과 Human Escalation Rate**
4. **비용 metric 번역: TotalCost와 optimal HOR**
5. **Component ablation: 무엇이 얼마나 기여하는가**
6. **Token efficiency를 운영 규율로**
7. **Scaling과 temporal stability: 이 결과는 언제까지 유효한가**
8. **학술적 확장 가능성 — exploratory 발견 목록**

---

**핵심 Figure 분석 매핑:**

| Figure | Ch.5에서의 역할 |
|--------|----------------|
| Fig 1  | §1 모델 병목 조건 규정 (ARCC cliff) |
| Fig 2  | §2 Failure Budget Reallocation 정량화 |
| Fig 4  | §6 Token budget 운영 규율 |
| Fig 5  | §3 Intervention timing → MTTR |
| Fig 8  | §4 Optimal HOR 측정 |
| Fig 9  | §2 Harness ROC (detection precision/recall) |
| Fig 10 | §5 Component ablation |
| Fig 11 | §7 Scaling 분석 |
| Fig 12 | §7 Temporal stability |

<!-- 섹션별 초고는 /draft ch05 N 으로 작성 -->

## 참조

- `deep-research/DR-5.1-failure-analysis-methods.md`
- `deep-research/DR-5.2-compute-cost-optimization.md`
- `deep-research/DR-5.3-vm-resource-management.md`
- `experiments/design-specification.md` — §4 (Statistical analysis), §5 (Power analysis), §6 (Cost model)
- `experiments/figure_expansion.md` — Figure 8~12 상세 설계
- `experiments/framework/metrics.py`
- `evidence/tables/bottleneck-by-condition.md`
- `evidence/tables/computation-requirements.md`
- `evidence/tables/academic-extension-candidates.md`

---

## §1 22개 실험 결과 종합: 어떤 변수가 어떤 조건에서 1차 병목이었는가

> [Ch.4 실험 완료 후 수치 보완]

**분석 구조**: 5변수 프레임워크별로 병목이 된 조건을 `evidence/tables/bottleneck-by-condition.md`의 표를 기반으로 서술한다. 모델이 1차 병목이 되는 조건(ARCC < cliff threshold), harness가 1차 병목이 되는 조건(ARCC ≥ cliff threshold이지만 silent drift 비율이 높음), compute가 1차 병목이 되는 조건(HOR이 token budget 대비 과도하거나 multi-agent N이 임계값 초과). Confirmatory 결과와 exploratory 발견을 명시적으로 구분한다.

---

## §2 Failure Budget Reallocation 정량 분석

> [Ch.4 실험 완료 후 수치 보완]

**분석 구조**: Fig 2(Failure Profile Radar)에서 harness-off → on 전환 시 6축 profile의 변화를 정량화한다. Silent logical drift 감소율과 recovery succeeded 증가율의 교환 비율, task type별 재배분 패턴의 차이. "총 failure budget 보존" 가설의 검증 — 면적이 보존되는가, 감소하는가. 재배분이 가장 잘 일어나는 조건과 그렇지 않은 조건을 기술한다.

---

## §3 운영 metric 번역: MTTR과 Human Escalation Rate

> [Ch.4 실험 완료 후 수치 보완]

**분석 구조**: TCR과 RSuccR에서 MTTR로 연결되는 번역 경로를 서술한다. Fig 2 Panel C의 실측값(harness-on 조건에서 MTTR과 HER), TTFF variance 감소가 운영 계획 가능성에 미치는 영향. Fig 5(Intervention timing) 결과: IFR decay 시작 시점 개입이 MTTR을 얼마나 줄이는가. 수치는 `[X]` 플레이스홀더.

---

## §4 비용 metric 번역: TotalCost와 optimal HOR

> [Ch.4 실험 완료 후 수치 보완]

**분석 구조**: Cost model 가정(2026년 3월 기준 API 가격, 엔지니어 hourly rate)을 명시한 후 TotalCost 공식을 전개한다. Fig 8(Cost-Reliability Frontier)에서 optimal HOR의 실험적 측정값, 3개 cost scenario에서 optimal HOR 구간의 robustness. HOR 최적점 이상에서 harness가 1차 병목이 되는 조건. Sensitivity: engineer rate ±50% 변동 시 optimal HOR 변화. 수치는 `[X]` 플레이스홀더.

---

## §5 Component ablation: 무엇이 얼마나 기여하는가

> [Ch.4 실험 완료 후 수치 보완]

**분석 구조**: Fig 10(Harness Ablation)에서 memory boundary / permission layer / recovery hook / evaluation hook 각각의 marginal contribution을 ΔMTTR / ΔHOR 비율로 정량화한다. 이 순위가 Ch.6 Operational Compiler 구성 우선순위의 실험적 근거가 된다. Component 간 상호의존 — 단독으로는 효과 없고 조합에서만 효과 있는 경우 — 은 exploratory 발견으로 레이블링한다. 수치는 `[X]` 플레이스홀더.

---

## §6 Token efficiency를 운영 규율로

> [Ch.4 실험 완료 후 수치 보완]

**분석 구조**: Fig 4(Token Budget Depletion Curve)에서 TCR이 급락하는 budget threshold를 측정하고, 이것을 HOR 관리와 연결하는 운영 규율로 번역한다. E22(compute saturation) 반례가 HOR 상한 설정에 주는 시사점. Token efficiency가 운영 규율로 필요한 조건: agent가 장기 자율 루프로 실행될 때. 수치는 `[X]` 플레이스홀더.

---

## §7 Scaling과 temporal stability: 이 결과는 언제까지 유효한가

> [Ch.4 실험 완료 후 수치 보완]

**분석 구조**: Fig 11(Model × Harness Scaling)에서 ARCC 증가가 harness value를 감소시키는가 vs. 역할을 전환시키는가. 전환 가설 검증: 방어 역할의 harness value가 감소하고 조정 역할의 value가 유지된다면, harness는 model capability 향상에 robust하다. Fig 12(Temporal Stability)에서 72시간 운영 후 harness fatigue가 관찰되는가, 메커니즘은 무엇인가. 이 스냅샷의 유효기간: 어떤 조건 변화가 이 결론을 무력화하는가. 수치는 `[X]` 플레이스홀더.

---

## §8 학술적 확장 가능성 — exploratory 발견 목록

> [Ch.4 실험 완료 후 수치 보완]

**분석 구조**: Capability Cliff sigmoid 형태의 보편성, Failure Budget Reallocation의 보존 법칙, component ablation 순위의 task-dependence, harness fatigue의 재보정 mechanism — 이 네 가지를 측정 가능한 형태의 미해결 질문으로 기술한다. 각 항목은 "이 책이 답하지 않는다"는 선언이 아니라, 검증에 필요한 구체적 조건(실험 설계, 데이터 규모, validation 기준)으로 서술한다.
