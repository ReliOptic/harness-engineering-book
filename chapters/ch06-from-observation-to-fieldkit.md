# Ch.6 — 관찰에서 도구로: Operational Fieldkit

> 상태: 🔲 skeleton only
> 담당: Kiwon
> 목표 분량: 8,000~10,000자

---

## 핵심 메시지

Fieldkit은 HOR × RSuccR trade-off의 pareto frontier를 따라 점진적으로 구성된다. Ch.5의 component ablation에서 marginal ROI가 가장 높은 component부터 도구화하고, 각 단계에서 HOR 증가가 MTTR 감소를 정당화하는지 확인한다. "한 번에 전체 harness를 구축한다"는 접근은 HOR을 최적점 이상으로 높여 harness 자체를 1차 병목으로 만든다. 직접 써보고 실패하고 기록한 히스토리만이 이 우선순위를 신뢰할 수 있게 만든다.

## 학습 결과

- Ch.5의 ablation 결과에서 Fieldkit 도구화 우선순위를 결정하는 방법을 이해한다.
- HOR × MTTR trade-off를 관리하는 점진적 Fieldkit 업데이트 전략을 설계할 수 있다.
- 각 Fieldkit component가 어떤 failure 유형을 어떻게 처리하는지 설명할 수 있다.
- 도구화 대상이 아닌 것(task 모호성, compute saturation)을 도구화 대상과 구분할 수 있다.
- CLI-Anything 방법론과 이 책의 접근이 어디서 수렴하고 어디서 다른지 설명할 수 있다.

## 집필 노트

- 관련 DR: DR-6.1 (CLI 설계 패턴), DR-6.2 (점진적 capability injection)
- 관련 실험: E18 (token auto-report), E19 (failure detect auto-retry), E20 (mini self-immune)
- 관련 Figure: Fig 8 (Cost-Reliability Frontier), Fig 10 (Harness Ablation)

**Fieldkit 구성 원칙 (조작적):**
- 원칙: Ch.5 ablation에서 marginal ROI = ΔMTTR / ΔHOR 순서로 component 도입.
- 각 component 추가 시 CostIndex 변화를 측정한다. CostIndex가 증가하면 그 component는 현재 조건에서 이익이 없다.
- Fieldkit은 harness component의 부분집합이다 — 전체 harness가 아니라 현재 실험 조건에서 ROI가 양수인 subset.

**점진적 원칙의 실험적 근거:**
- Fig 8 (Cost-Reliability Frontier): Bayesian optimization 결과가 제안하는 component 추가 순서.
- 전체 component 동시 활성화는 대부분의 조건에서 CostIndex를 최소화하지 않는다.
- 순차적 추가가 pareto frontier를 따라 이동하는 전략이다.

**"도구화하면 안 되는 것"의 기준:**
- E21 (task 모호성): IFR이 낮은 이유가 instruction 자체의 암묵적 constraint 부재일 때, harness component를 추가해도 IFR이 개선되지 않는다. 도구화가 아니라 task 재설계가 필요한 경우.
- E22 (compute saturation): HOR이 이미 token budget의 임계점에 근접했을 때 새 component 추가는 TCR을 낮춘다. 도구를 더하는 것이 아니라 줄이는 것이 처방이다.

---

## Outline

**계획된 섹션:**

1. **Ch.4-5에서 추출한 반복 실패 패턴 → 도구화 후보 식별**
   - Failure taxonomy(6축) 중 반복 빈도가 높고 도구화 marginal ROI가 높은 것
   - Fig 10 (Harness Ablation) 순위를 도구화 우선순위로 전환하는 기준
   - 도구화 대상이 아닌 것: task 자체의 모호함(E21), compute saturation(E22) — 이것들을 도구로 해결하려 하면 HOR만 높아진다
   - "도구화 이전": 먼저 수동으로 몇 번 반복한 이후에 도구화한다. 한 번도 해보지 않은 것을 미리 자동화하지 않는다.

2. **Operational Fieldkit 설계 원칙**
   - 원칙 1: HOR × MTTR trade-off를 매 component 추가 시 측정한다
   - 원칙 2: 도구는 실패 히스토리에서 나온다 — 아직 발생하지 않은 실패를 위한 도구를 만들지 않는다
   - 원칙 3: 각 도구는 제거 가능해야 한다 — HOR이 과도해지면 제거할 수 있는 구조
   - 원칙 4: 도구의 기여를 측정한다 — 추가 전/후 RSuccR, MTTR, CostIndex 비교

3. **점진적 업데이트 원칙: pareto frontier를 따라 이동하는 전략**
   - HOR-MTTR 공간의 pareto frontier: Fig 8에서 도출된 이동 경로
   - Bayesian optimization 결과가 제안하는 component 추가 순서
   - "한 번에 전체 harness" 접근이 실패하는 이유: HOR 최적점을 넘어서면 TCR이 오히려 감소
   - E20 (mini self-immune)이 이 원칙의 극단적 사례인 이유: self-monitoring 자체가 token을 소비한다

4. **Skill로 쓸 수 있는 능력의 극대화**
   - Harness engineering이 skill의 사전 조건인 이유: skill이 실행되는 context를 harness가 보호한다
   - Skill catalog와 Fieldkit component의 연결 구조
   - 어떤 종류의 반복 작업이 skill화 가능하고, 어떤 것은 harness component로 처리해야 하는가
   - Token budget 관리가 skill 실행의 사전 조건인 이유 (HOR이 skill 실행 공간을 잠식하지 않아야 한다)

5. **CLI-Anything 방법론 비교: 독립적 수렴의 의미**
   - CLI-Anything이 도달한 것과 이 책이 도달한 것의 공통 지점
   - 차이: CLI-Anything은 surface 설계(HARNESS.md)를 중심에 둔다. 이 책은 harness component의 단계적 ROI 기반 구성을 중심에 둔다.
   - 두 접근이 수렴하는 지점: "먼저 직접 써보고, 실패하고, 기록하고, 그 히스토리를 도구로 만든다"
   - 독립 수렴이 의미하는 것: 이 방법론은 특정 프로젝트의 ad-hoc이 아니다

---

**핵심 Figure:**

- **Fig 8** (Ch.4/5 기반, Ch.6에서 활용) — Cost-Reliability Frontier: HOR × RSuccR trade-off 곡선. Optimal HOR 위치. Fieldkit 구성의 나침반.
- **Fig 10** (Ch.4/5 기반, Ch.6에서 활용) — Harness Ablation: component별 marginal ROI. Fieldkit 도구화 우선순위의 근거.

<!-- 섹션별 초고는 /draft ch06 N 으로 작성 -->

## 참조

- `deep-research/DR-6.1-cli-design-patterns.md`
- `deep-research/DR-6.2-incremental-capability-injection.md`
- `experiments/axis-5-harness-internalization/E18-token-auto-report.md`
- `experiments/axis-5-harness-internalization/E19-failure-detect-auto-retry.md`
- `experiments/axis-5-harness-internalization/E20-mini-self-immune.md`
- `experiments/figure_expansion.md` — Figure 8 (Cost-Reliability Frontier), Figure 10 (Ablation)
- `experiments/framework/harness.py`
- `fieldkit/README.md`
- `fieldkit/failure-to-tool-map.md`
