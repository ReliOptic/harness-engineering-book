# Ch.5 — 실험 결과에서 배운 것: AgentOps와 Harness의 실무

> 상태: 🔲 skeleton only
> 담당: Kiwon
> 목표 분량: 10,000~12,000자

---

## 핵심 메시지

Ch.4의 22개 실험에서 추출하는 패턴은 세 단계의 번역을 거쳐야 실무적 의미를 갖는다. 실험실 metric(TCR, TTFF, RSuccR)에서 운영 metric(MTTR, Human Escalation Rate)으로, 다시 비용 metric(TotalCost, CostIndex)으로. 이 번역 없이 "harness가 효과적이다"는 주장은 "so what?" 질문에 답할 수 없다. 번역을 완료한 결론은 하나다: optimal HOR은 존재하며, 그 점 이상에서는 harness 자체가 새로운 1차 병목이 된다.

## 학습 결과

- 실험 결과를 실험실 metric → 운영 metric → 비용 metric으로 번역하는 3단계 체계를 이해하고 적용할 수 있다.
- Failure Budget Reallocation 결과를 정량화하고, harness가 어떤 failure를 어떤 failure로 전환하는지 보고할 수 있다.
- HOR × RSuccR trade-off에서 optimal harness configuration을 판단하는 방법을 이해한다.
- Harness component별 ablation을 통해 각 component의 marginal contribution을 분리하고 도구화 우선순위를 결정할 수 있다.
- Scaling 조건(model capability × harness value)과 temporal stability(harness fatigue)를 해석할 수 있다.
- Confirmatory/exploratory 구분을 유지하면서 실험 결과를 학술적 확장 후보로 분류할 수 있다.

## 집필 노트

- 관련 DR: DR-5.1 (실패 패턴 분석), DR-5.2 (compute cost 최적화), DR-5.3 (VM 리소스 관리)
- 관련 실험: E01~E20 전체 분석 (Ch.4 실험 완료 후 작성)
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
- 각 component의 marginal contribution 정량화 → Ch.6 Fieldkit 구성 우선순위의 근거.
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
   - 5변수 프레임워크별 병목 분포 (`evidence/tables/bottleneck-by-condition.md` 핵심 표)
   - 모델이 1차인 조건: ARCC가 cliff 이하. Harness 투자 전에 모델 교체가 먼저.
   - Harness가 1차인 조건: ARCC가 cliff 이상, 그러나 failure budget의 silent drift 비율이 높음.
   - Compute가 1차인 조건: HOR이 token budget 대비 과도, 또는 multi-agent N이 임계값 초과.
   - Confirmatory 결과와 exploratory 발견의 명시적 구분

2. **Failure Budget Reallocation 정량 분석**
   - Fig 2 (Failure Profile Radar) 결과 해석: 6축 profile의 harness-off → on 변화
   - "총 failure budget 보존" 가설 검증: 실제로 보존되는가, 아니면 감소하는가
   - Silent logical drift 감소와 recovery succeeded 증가의 교환 비율
   - Reallocation이 가장 잘 일어나는 조건과 그렇지 않은 조건 (task type별 차이)

3. **운영 metric 번역: MTTR과 Human Escalation Rate**
   - Level 1 → Level 2 번역: TCR과 RSuccR이 MTTR에 연결되는 경로
   - Fig 2 Panel C (Operational Translation): harness-on 조건에서 MTTR과 HER의 실측값
   - Predictability 변화: TTFF variance 감소가 운영 계획 가능성에 미치는 영향
   - Intervention timing 결과 (Fig 5): IFR decay 시작 시점 개입이 MTTR을 얼마나 줄이는가

4. **비용 metric 번역: TotalCost와 optimal HOR**
   - Level 2 → Level 3 번역: cost model 가정과 TotalCost 공식
   - Fig 8 (Cost-Reliability Frontier) 결과: optimal HOR의 실험적 측정값
   - 3개 cost scenario에서 robustness 확인 — 동일 optimal HOR 구간인가
   - HOR 최적점 이상에서 harness가 새로운 1차 병목이 되는 조건
   - Sensitivity: engineer rate ±50% 변동 시 optimal HOR 변화

5. **Component ablation: 무엇이 얼마나 기여하는가**
   - Fig 10 (Harness Ablation): memory boundary / permission layer / recovery hook / evaluation hook 각각의 marginal contribution
   - 어떤 component를 먼저 구현해야 하는가: marginal ROI 순위 → Ch.6 Fieldkit 구성 근거
   - Component 간 상호의존: 단독으로는 효과 없고 조합에서만 효과 있는 경우 (exploratory)
   - Ablation이 가르쳐주는 것: 전체 harness 중 가장 적은 HOR로 가장 큰 MTTR 감소를 달성하는 subset

6. **Token efficiency를 운영 규율로**
   - Fig 4 (Token Budget Depletion Curve): TCR이 급락하는 budget threshold 측정
   - 운영 규율: token budget을 HOR 관리와 연결하는 실무 기준
   - E20 (compute saturation) 반례가 규율 설계에 주는 시사점: HOR 상한을 어디에 두어야 하는가
   - Token efficiency가 운영 규율이 되는 조건: agent가 장기 자율 루프로 실행될 때

7. **Scaling과 temporal stability: 이 결과는 언제까지 유효한가**
   - Fig 11 (Model × Harness Scaling): ARCC 증가가 harness value를 감소시키는가 vs. 역할을 전환시키는가
   - 전환 가설 검증: 방어 역할의 harness value가 감소하고 조정 역할의 value가 유지된다면, harness는 model capability 향상에 robust하다
   - Fig 12 (Temporal Stability): 72시간 운영에서 harness fatigue가 관찰되는가
   - Harness fatigue의 메커니즘: context 누적, rule drift, 아니면 모델 측 변화인가
   - 이 스냅샷의 유효기간: 어떤 조건 변화가 이 결론을 무력화하는가

8. **학술적 확장 가능성 — exploratory 발견 목록**
   - Capability Cliff sigmoid 형태의 보편성: 다른 task type, 다른 모델 family에서도 성립하는가
   - Failure Budget Reallocation의 보존 법칙: 다른 agent runtime에도 성립하는가
   - Component ablation 순위의 task-dependence: task type이 달라지면 순위가 바뀌는가
   - Harness fatigue의 재보정 mechanism: 무엇이 temporal stability를 복원하는가
   - 이 목록의 각 항목은 이 책이 답하지 않는다. 이 책의 실험들이 그 질문들을 측정 가능한 형태로 정의했다.

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
