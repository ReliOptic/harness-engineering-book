# Ch.10 — 관찰에서 도구로: Operational Compiler

> 상태: 🔴 초고 v0.1 (2026-03-18)
> 담당: Kiwon
> 목표 분량: 8,000~10,000자

---

## 핵심 메시지

Operational Compiler는 harness overhead × 성공률 trade-off의 pareto frontier를 따라 점진적으로 구성된다. Ch.9의 component ablation에서 marginal ROI가 가장 높은 component부터 운영 규칙으로 컴파일하고, 각 단계에서 overhead 증가가 MTTR 감소를 정당화하는지 확인한다. "한 번에 전체 harness를 구축한다"는 접근은 overhead를 최적점 이상으로 높여 harness 자체를 1차 병목으로 만든다. 우선순위의 근거는 설계 직관이 아니라, 반복 관찰된 failure pattern과 ΔMTTR / Δoverhead 측정값이다.

## 학습 결과

- Ch.9의 ablation 결과에서 Operational Compiler 구성 우선순위를 결정하는 방법을 이해한다.
- harness overhead × MTTR trade-off를 관리하는 점진적 Operational Compiler 업데이트 전략을 설계할 수 있다.
- 각 Operational Compiler component가 어떤 failure 유형을 어떻게 처리하는지 설명할 수 있다.
- 도구화 대상이 아닌 것(task 모호성, compute saturation)을 도구화 대상과 구분할 수 있다.
- CLI-Anything 방법론과 이 책의 접근이 어디서 수렴하고 어디서 다른지 설명할 수 있다.

## 집필 노트

- 관련 DR: DR-6.1 (CLI 설계 패턴), DR-6.2 (점진적 capability injection)
- 관련 실험: E18 (token auto-report), E19 (failure detect auto-retry), E20 (mini self-immune)
- 관련 Figure: Fig 8 (Cost-Reliability Frontier), Fig 10 (Harness Ablation)

**Operational Compiler 구성 원칙 (조작적):**
- 원칙: Ch.9 ablation에서 marginal ROI = ΔMTTR / ΔHOR 순서로 component 도입.
- 각 component 추가 시 CostIndex 변화를 측정한다. CostIndex가 증가하면 그 component는 현재 조건에서 이익이 없다.
- Operational Compiler는 harness component의 부분집합이다 — 전체 harness가 아니라 현재 실험 조건에서 ROI가 양수인 subset.

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

1. **Ch.8-9에서 추출한 반복 실패 패턴 → 도구화 후보 식별**
2. **Operational Compiler 설계 원칙**
3. **점진적 업데이트 원칙: pareto frontier를 따라 이동하는 전략**
4. **Skill로 쓸 수 있는 능력의 극대화**
5. **CLI-Anything 방법론 비교: 독립적 수렴의 의미**

---

**핵심 Figure:**

- **Fig 8** (Ch.8/9 기반, Ch.10에서 활용) — Cost-Reliability Frontier: harness overhead × RSuccR trade-off 곡선. Optimal harness overhead 위치. Operational Compiler 구성의 나침반.
- **Fig 10** (Ch.8/9 기반, Ch.10에서 활용) — Harness Ablation: component별 marginal ROI. Operational Compiler 구성 우선순위의 근거.

<!-- 섹션별 초고는 /draft ch06 N 으로 작성 -->

## 참조

- `deep-research/DR-6.1-cli-design-patterns.md`
- `deep-research/DR-6.2-incremental-capability-injection.md`
- `experiments/axis-5-harness-internalization/E18-token-auto-report.md`
- `experiments/axis-5-harness-internalization/E19-failure-detect-auto-retry.md`
- `experiments/axis-5-harness-internalization/E20-mini-self-immune.md`
- `experiments/figure_expansion.md` — Figure 8 (Cost-Reliability Frontier), Figure 10 (Ablation)
- `experiments/framework/harness.py`
- `operational-compiler/README.md`
- `operational-compiler/failure-to-tool-map.md`

---

## §1 Ch.8-9에서 추출한 반복 실패 패턴 → 도구화 후보 식별

> 상태: 🔴 초고 v0.1 (2026-03-18)

Ch.8와 Ch.9는 실험 조건에서 무엇이 실패하는가를 보여준다. Ch.10의 질문은 그 다음 단계에 있다 — 반복 관찰된 실패 패턴 중 어떤 것이 운영 규칙으로 컴파일될 가치가 있는가. 모든 실패가 컴파일의 대상이 되는 것은 아니다. 판단 기준은 세 가지다: 반복 빈도, 컴파일 이후의 marginal ROI(ΔMTTR / ΔHOR), 그리고 규칙 기반 처리로 환원 가능한 패턴인지 여부.

Failure taxonomy 6축 중 도구화 후보로 먼저 부상하는 것은 tool call failure와 output format error다. 이 두 유형은 반복 빈도가 높고, 구조적으로 감지 가능하며, 규칙 기반 처리가 가능하다. Tool call이 schema를 위반하면 즉시 감지되고 retry 로직이 작동할 수 있다. Output format이 예상 스키마에서 벗어나면 format correction hook이 개입할 수 있다. 두 경우 모두 명시적 구조를 검증하는 것이기 때문에 하드코딩된 규칙으로 표현 가능하다.

Context overflow는 다른 성격의 도구화 후보다. 발생 자체는 예측 가능하다 — token 소비가 budget threshold에 근접하는 것은 점진적으로 모니터링할 수 있다. 그러나 대응의 적절성은 task 상태에 따라 달라진다. 현재 step이 중요한 맥락에 있다면 context compression보다 operator escalation이 더 적절할 수 있다. 이것은 규칙으로 처리할 수 없는 판단 요소를 포함한다 — 도구화가 가능하지만 도구의 설계가 복잡하다.

Silent logical drift는 현 세대 컴파일 범위 밖에 있다. Ch.11에서 서술하는 것처럼, 이것은 harness가 접근할 수 없는 semantic 레이어의 문제다. Tool call이 schema를 통과하고 출력이 형식을 만족하면서도 방향이 틀린 경우 — 규칙 기반 검증이 통과를 신호로 내보낸 상황에서 drift를 감지하는 것은 agent 자신의 모델 능력 지표 self-monitoring에 의존한다. Self-immune system(Ch.11)의 영역이지 Operational Compiler component의 영역이 아니다.

도구화하면 안 되는 두 가지 유형은 명확히 구분한다. E21이 보여준 task 모호성 — instruction 자체의 암묵적 constraint 부재 — 은 harness component로 해결할 수 없다. IFR이 낮은 이유가 constraint가 명시되지 않아서라면, recovery hook을 추가해도 IFR이 개선되지 않는다. 이 경우 처방은 도구화가 아니라 task 재설계다. E22가 보여준 compute saturation — HOR이 이미 token budget 임계점에 근접한 조건 — 에서는 새 component 추가가 TCR을 오히려 낮춘다. 도구를 더하는 것이 아니라 줄이는 것이 처방이다.

도구화 전에 먼저 수동으로 해본다는 원칙은 이 챕터 전체의 전제다. 한 번도 수동으로 처리해보지 않은 실패 유형을 미리 자동화하면 두 가지 문제가 생긴다. 자동화가 처리해야 할 실제 케이스의 다양성을 이해하지 못한 채 규칙을 설계하게 되고, 그 규칙이 실제 운영에서 얼마나 많은 edge case를 놓치는지 배포 전에 알 수 없다. 반복이 충분히 쌓인 이후의 도구화는 그 반복이 만든 패턴 위에서 작동한다.

---

## §2 Operational Compiler 설계 원칙

> 상태: 🔴 초고 v0.1 (2026-03-18)

Operational Compiler component를 추가하는 결정은 네 가지 원칙이 교차하는 지점에서 이루어진다. 이 원칙들은 서로 제약 관계에 있다 — 원칙 하나를 최적화하면 다른 원칙이 압박을 받는다. 이 압박을 명시적으로 측정하는 것이 Operational Compiler 설계의 구조적 특징이다.

각 component를 추가할 때마다 harness overhead × MTTR trade-off를 측정한다는 것이 이 방법론의 전제다. 새 component 추가 전후에 harness overhead와 MTTR을 측정하고 ΔMTTR / Δharness overhead가 양수인 경우에만 component를 유지한다 — 이 측정이 없으면 harness overhead가 최적점을 넘어서는 것을 알아채지 못한다. 그 측정이 가능하려면 도구가 실패 히스토리에서 나와야 한다. 발생하지 않은 실패의 예측 정확도는 낮으며, 그 예측을 위한 도구는 실제 문제를 해결하지 못하면서 harness overhead만 높인다. 실패 히스토리에 기반한 도구여야 기여가 측정 가능하고, 기여가 측정 가능해야 E22 조건처럼 harness overhead가 token budget 임계점에 근접했을 때 어떤 component를 제거할지 판단할 수 있다. 제거 가능성이 설계에 없으면 이 판단을 실행할 수 없다.

이 네 원칙이 수렴하는 지점은 다음 섹션에서 서술하는 pareto frontier다. 원칙 1이 ΔMTTR / ΔHOR을 최대화하는 방향을 정하고, 원칙 2가 컴파일 후보를 실패 히스토리로 제한하며, 원칙 3이 언제든 후퇴할 수 있는 구조를 유지하고, 원칙 4가 frontier 위에서 현재 위치를 확인하는 역할을 한다.

---

## §3 점진적 업데이트 원칙: pareto frontier를 따라 이동하는 전략

> 상태: 🔴 초고 v0.1 (2026-03-18)

harness overhead-RSuccR 공간의 pareto frontier는 동일한 harness overhead에서 가장 높은 RSuccR을 달성하는 configuration들의 집합이다. Fig 8(Cost-Reliability Frontier)에서 이 frontier는 harness overhead가 낮은 쪽에서 시작해 optimal harness overhead를 지나 harness overhead가 과도해지는 영역으로 이어지는 곡선 형태를 취한다. Frontier 위에 있는 configuration은 현재 조건에서 더 이상 개선할 수 없는 최적 상태다. Frontier 아래에 있는 configuration은 동일한 HOR로 더 높은 RSuccR을 달성할 수 있는 여지가 있다.

Operational Compiler 업데이트의 전략적 목표는 이 frontier를 따라 이동하는 것이다 — frontier 아래에서 frontier 위로, 그리고 frontier 위에서 더 나은 (더 낮은 harness overhead, 더 낮은 MTTR) 방향으로. Ch.9 ablation이 제안하는 component 추가 순서는 이 이동의 첫 번째 경로다. Marginal ROI가 가장 높은 component부터 추가하면 frontier를 따라 이동하는 것과 동일한 효과가 있다.

E22에서 관찰한 바에 따르면, harness overhead가 token budget의 임계점에 근접한 상태에서 component를 추가하면 TCR이 감소했다. 전체 component를 동시에 활성화하면 harness overhead가 한번에 크게 상승하고, 그 harness overhead가 optimal point를 넘어서는지 여부를 중간 과정 없이 알 수 없다. E22가 보여주는 것처럼 harness overhead가 optimal을 넘으면 TCR이 감소하기 시작한다 — harness가 agent의 실행 공간을 잠식하는 시점. 이 시점에서 어떤 component가 문제인지를 역추적하는 것은 component를 하나씩 추가하면서 측정했을 때보다 훨씬 어렵다.

E20(mini self-immune)이 이 원칙의 극단적 사례다. Self-monitoring 자체가 token을 소비한다. Agent가 자신의 모델 능력 지표를 estimate하고, cliff-proximity를 계산하며, recovery 필요 여부를 판단하는 과정에 harness overhead가 추가된다. 이 overhead가 self-immune이 제공하는 MTTR 감소를 정당화하는지 여부는 모델 능력 지표 수준과 task 복잡도에 따라 달라진다. 모델 능력 지표가 충분히 높고 task가 충분히 복잡할 때는 self-immune의 harness overhead 추가가 MTTR 개선을 통해 회수된다. 모델 능력 지표가 낮거나 task가 단순하면 self-immune은 비용이 이익을 초과하는 component다.

Bayesian optimization은 이 frontier 탐색을 가속하는 방법이다. Fig 8의 Cost-Reliability Frontier는 E18의 Bayesian optimization 결과가 제안하는 component 추가 경로를 포함한다. 각 iteration에서 현재까지의 측정값을 기반으로 다음에 시도할 harness overhead 지점을 선택하고, 그 지점에서 RSuccR을 측정한다. Bayesian optimization이 제안하는 경로가 수동 시도보다 frontier를 더 효율적으로 탐색하는가 — 이것이 E18의 confirmatory 가설이다. 수치는 Ch.9 결과에서 보완된다 (`[X]` 플레이스홀더).

---

## §4 Skill로 쓸 수 있는 능력의 극대화

> 상태: 🔴 초고 v0.1 (2026-03-18)

Skill과 Operational Compiler component는 다른 레이어에서 작동한다. Skill은 agent가 반복적으로 수행하는 작업의 추상화다 — code review, web search, document synthesis 같은 작업이 호출 가능한 단위로 정의된다. Operational Compiler component는 그 skill이 실행되는 환경의 안전성을 보장하는 구조다. Skill이 실행되는 context가 오염되어 있거나, token budget이 이미 소진되어 있거나, 이전 step의 output이 잘못된 상태에서 skill을 호출하면 skill 자체의 품질과 무관하게 결과가 잘못된다.

반복 가능한 개입 패턴이 skill화의 대상이 되는 기준은 두 가지다. 동일한 input 조건에서 동일한 output을 반복적으로 생산할 수 있고, 충분한 반복 관찰을 거쳐 도구화의 효과가 확인된 작업이 skill화의 대상이다. 두 조건 중 하나라도 충족되지 않으면, 해당 작업은 skill이 아니라 operator의 맥락 판단을 요구하는 실행이다.

Token budget 관리가 skill 실행의 사전 조건인 이유는 harness overhead와의 관계에서 나온다. Skill 실행에는 token이 필요하다. Operational Compiler component의 harness overhead가 높으면 skill 실행에 사용 가능한 token 공간이 줄어든다. Optimal harness overhead가 존재한다는 가설 — Ch.9 §4에서 Fig 8을 통해 검증하는 — 은 이 관점에서 다시 표현할 수 있다: skill 실행 공간을 최대화하면서 harness의 보호 기능을 유지하는 harness overhead 지점이 있다. Operational Compiler는 그 지점을 찾고 유지하는 구조다.

어떤 종류의 반복 작업이 skill화 가능하고, 어떤 것은 harness component로 처리해야 하는가. Rule of thumb은 이렇다: 판단이 필요한 것은 harness component로, 판단이 없는 것은 skill로. Token 사용량 모니터링은 판단이 필요 없다 — 숫자를 추적하고 threshold를 확인하는 것은 명확한 규칙으로 표현 가능하다. 이것은 harness component다. Synthesis task에서 output 품질을 평가하는 것은 판단이 필요하다 — 어떤 기준으로 평가하는가, 어떤 weight를 부여하는가가 context에 따라 달라진다. 이것은 operator 또는 agent의 모델 능력 지표에 의존하는 영역이다.

---

## §5 CLI-Anything 방법론 비교: 독립적 수렴의 의미

> 상태: 🔴 초고 v0.1 (2026-03-18)

CLI-Anything과 이 책의 접근이 수렴하는 지점을 먼저 정확히 명시한다. 두 접근 모두 runtime 상태 관리와 복구 경로를 핵심으로 다룬다. CLI-Anything의 6속성 중 결정론적신뢰성과 복원력은 이 책의 harness 정의에서 recovery hook과 permission layer에 해당하는 우려를 공유한다. 그리고 두 접근 모두 "먼저 직접 써보고, 실패하고, 기록하고, 그 히스토리를 도구로 만든다"는 방향으로 수렴한다.

차이 지점은 범위와 추상화 레이어다. CLI-Anything은 surface 설계에 집중한다 — 개별 CLI 소프트웨어가 agent와 상호작용할 때 어떤 인터페이스 속성을 가져야 하는가. 구조화된 출력, 스키마 자기 서술, 에이전트 최우선 설계 원칙 — 이것들은 agent가 도구를 호출하는 인터페이스 레이어의 설계다. 이 책은 agent 프로세스 전체의 operational envelope을 다룬다 — 개별 tool call의 인터페이스가 아니라 그 tool call들이 발생하는 agent의 실행 환경 전체.

비유하면: CLI-Anything이 도로 위의 교통 신호 체계를 설계하는 것이라면, 이 책은 차량(agent) 자체의 안전 시스템을 설계하는 것이다. 신호 체계가 잘 설계되어 있어도 차량의 브레이크가 없으면 사고가 난다. 차량의 브레이크가 있어도 신호 체계가 없으면 충돌이 일어난다. 두 설계는 다른 레이어에서 다른 문제를 해결하며, 동시에 필요하다.

독립적 수렴이 의미하는 것을 과도하게 해석하지 않는 것도 중요하다. 수렴은 두 팀이 독립적으로 동일한 결론에 도달했다는 사실을 보여주지만, 그것이 그 결론이 유일하게 올바른 방향임을 증명하지는 않는다. 다른 맥락, 다른 제약 조건에서 출발한 팀이 다른 방향으로 수렴할 수도 있다. 수렴의 의미는 더 제한적이다: 두 팀이 공유하는 우려 — runtime 상태 관리와 복구 경로의 필요성 — 가 특정 프로젝트의 ad-hoc 발견이 아니라, CLI 기반 agent 운영에서 독립적으로 관찰되는 구조적 패턴이라는 것.

2026년 3월 기준으로 CLI-Anything 방법론과 이 책의 Operational Compiler 접근이 상호 참조할 수 있는 상태는 아직 만들어지지 않았다. 두 접근이 공유하는 구조적 우려가 더 명확해지고, 각각의 실험 결과가 누적되면 비교 지점이 더 구체화될 것이다. 현재 시점에서 기록할 수 있는 것은 수렴의 방향이지, 수렴의 정도가 아니다.
