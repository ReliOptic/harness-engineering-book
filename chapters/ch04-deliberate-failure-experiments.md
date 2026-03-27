# Ch.4 — 의도적 실패 실험: 20개 시나리오

> 상태: 🔲 skeleton only
> 담당: Kiwon (narrative) + Experimenter A/B/C (실험)
> 목표 분량: 12,000~15,000자

---

## 핵심 메시지

의도적으로 실패시키는 것이 이 챕터의 방법론이다. 20개 시나리오는 pre-registration 원칙 하에 설계되었다 — 가설, 판단 기준, 검정 방법이 데이터 수집 전에 `experiments/design-specification.md`에 고정되었다. 이것이 Ch.5의 분석을 post-hoc rationalization이 아닌 confirmatory analysis로 만드는 구조적 조건이다. 실험은 5변수 프레임워크의 각 변수를 격리하여 조작하고, 어떤 변수가 어떤 조건에서 1차 병목이 되는가를 측정한다.

## 학습 결과

- Pre-registration 원칙이 실험 설계에서 왜 필요하며 어떻게 적용되는지 설명할 수 있다.
- Task T1/T2/T3/T4의 조작적 정의와 각 task에서의 성공 기준을 이해한다.
- Ground truth 3-layer 구조(test suite → LLM judge → human rater)의 역할과 각 layer의 판단 기준을 이해한다.
- ARCC validation을 main experiment의 선행 조건으로 다루는 이유를 설명할 수 있다.
- 5변수 프레임워크 기반의 deliberate failure experiment를 자신의 환경에서 설계하고 실행할 수 있다.
- Confirmatory analysis와 exploratory 발견의 차이를 구분하고 적절히 보고할 수 있다.

## 집필 노트

- 관련 DR: DR-4.1 (chaos engineering), DR-4.2 (GCP 무료 티어 제약), DR-4.3 (token budget), DR-4.4 (compute benchmarks)
- 관련 실험: E01~E20 전체
- **Pre-registration 파일**: `experiments/design-specification.md` — 이 챕터의 모든 가설과 판단 기준의 원천. 이 파일이 챕터 집필 전에 완성된 상태여야 한다.
- **이 챕터는 실험 실행 완료 후 작성 가능.** 서술 구조(§1 pre-registration 선언, §2 환경, §3~§8 축별 결과)는 지금 확정.
- **Confirmatory vs. exploratory 구분 원칙**: pre-registration에 있는 가설 검증 → confirmatory. 실험 중 발견된 예상 밖 패턴 → exploratory. 챕터 내에서 명시적으로 레이블링.
- **풍선 효과 기록**: 한 변수를 제어하면 다른 변수가 1차 병목으로 부상하는 패턴. 발견되면 exploratory 발견으로 기록.
- **반례 실험(E19, E20) 서술 원칙**: 이 두 실험의 결론은 "따라서 harness가 필요하다"가 아니다. "harness가 해결하지 못하는 조건이 존재한다"이다. 결론을 선언하지 않고 조건을 기술한다.

**Figure 매핑 (데이터 생성 책임):**
| Figure | 실험 | 가설 |
|--------|------|------|
| Fig 1  | E01  | ARCC cliff position은 task type별로 다르다 |
| Fig 2  | E05  | Failure budget은 재배분된다 (unrecoverable→recoverable) |
| Fig 3  | E07  | Surface × model interaction이 failure taxonomy를 변화시킨다 |
| Fig 4  | E08  | Token budget threshold 이하에서 TCR이 cliff-like 급락한다 |
| Fig 5  | E09  | Intervention timing이 RSuccR보다 MTTR에 더 큰 영향을 준다 |
| Fig 6  | E11  | Multi-agent harness coordination overhead는 N에 비선형 증가한다 |
| Fig 7  | E15~17 | Intervention codification이 HER을 감소시킨다 |
| Fig 8  | E18  | HOR × RSuccR trade-off에 optimal point가 존재한다 |

---

## Outline

**계획된 섹션:**

1. **실험 설계 원칙: 왜 의도적으로 실패시키는가**
   - Deliberate failure experiment의 방법론적 근거: 정상 조건에서 드러나지 않는 구조적 취약점
   - Pre-registration 원칙의 적용: `experiments/design-specification.md`가 이 챕터 전체의 가설 레지스트리
   - Confirmatory vs. exploratory의 사전 구분: "이것을 확인하러 간다"와 "이것을 발견했다"는 다른 주장 강도를 가진다
   - Task 조작적 정의 recap (Ch.3에서 announce된 내용): T1/T2/T3/T4 성공 기준
   - ARCC validation 선행 조건: R² ≥ 0.65 미달 시 main experiment에 어떤 조건이 붙는가

2. **실험 환경: GCP 무료 티어, OpenRouter, 측정 인프라**
   - VM 사양과 제약: GCP 무료 티어가 실험 설계에 미친 영향 (제약이 아니라 실험 조건)
   - Token budget 설정 기준과 API routing 구성
   - Ground truth 3-layer: test suite(T1 F1 scorer, T2 constraint checker, T3 pytest) → LLM judge(claude-opus-4-6, κ ≥ 0.70) → human rater(2명 독립, κ ≥ 0.70)
   - `experiments/framework/` Python 인프라: 측정의 재현 가능성 보장
   - Random seed 고정 및 deviation 기록 원칙

3. **1막 — 모델 변수 조작 (E01~E04): Capability Cliff가 존재하는가**
   - E01: ARCC × task type × TCR scatter plot → Fig 1 데이터 수집. Harness-off 조건.
   - E02: Frontier vs. distilled — 동일 task에서 ARCC 분포 비교. Distillation Efficiency Frontier의 실험적 기반.
   - E03: Mid-run model switching — context continuity 붕괴 매커니즘 측정
   - E10: Model capability floor for self-monitoring — ARCC 하한 조건 탐색 (Ch.7 예고)
   - Confirmatory: cliff position이 task별로 다르다는 가설 검증
   - Exploratory: cliff 형태(sigmoid vs. piecewise linear) 비교 — AIC로 판정

4. **2막 — Harness·Surface 변수 조작 (E05~E08): Failure Budget은 어떻게 재배분되는가**
   - E05: Harness on/off → Failure Profile Radar (Fig 2) 데이터. 6축 failure taxonomy 집계.
   - E06: Memory boundary 위반 패턴 — harness가 있을 때와 없을 때 어떻게 다른가
   - E07: Permission + surface 조합 효과 → Fig 3 (Surface × Model interaction) 데이터
   - E08: Token budget fine-grained sweep → Fig 4 (Token Budget Depletion Curve) 데이터
   - HOR 측정 시작: 각 harness configuration에서 token overhead 기록
   - Confirmatory: failure budget 재배분 가설 검증 (total budget 보존 여부 포함)

5. **3막 — 제약 환경의 병목 (E09~E14): compute가 1차 병목이 되는 조건**
   - E09: Single-agent token budget 고갈 패턴 — TCR cliff와 token budget의 관계
   - E11: Multi-agent harness coordination overhead → Fig 6 데이터. Agent N 증가 시 overhead 비선형성 측정.
   - E12: Self-immune harness의 compute overhead 측정 — overhead가 benefit을 초과하는 조건
   - E14: VM 리소스 경합 조건에서의 failure taxonomy — compute saturation의 failure 유형
   - 풍선 효과 관찰: harness가 있을 때 compute가 1차 병목으로 이동하는 패턴 (exploratory 기록)

6. **4막 — Operator intervention의 효과 (E15~E17): 어떤 개입이 반복 가능한가**
   - E15: Intervention timing — failure 직후 vs. IFR decay 시작 시점. MTTR 비교.
   - E16: Intervention method — 직접 수정 vs. hint 주입 vs. context reset의 효과와 재현 가능성
   - E17: Intervention codification — 반복 가능한 개입 패턴 추출 → Fig 7 (Intervention ROI) 데이터
   - Confirmatory: intervention timing이 RSuccR보다 MTTR에 더 큰 영향을 준다는 가설 검증

7. **5막 — AgentOps 내재화 (E18~E20): harness에서 agent로의 첫 단계**
   - E18: Token auto-report 내재화 → Fig 8 (Cost-Reliability Frontier) 데이터. HOR × RSuccR trade-off 측정.
   - E19: Failure detect auto-retry의 harness 주입 — 어떤 failure type이 auto-retry로 해결되는가
   - E20: Mini self-immune — agent가 스스로 failure를 감지하고 복구하는 최소 조건 (Ch.7 예고)
   - Bayesian optimization over harness configuration: optimal HOR 탐색 (Fig 8 기반)
   - Confirmatory: optimal HOR이 존재한다는 가설 검증

8. **반례 — task design과 compute saturation (E19~E20): harness의 구조적 한계**
   - E19: Task 자체가 모호할 때 harness는 무엇을 할 수 있고 무엇을 할 수 없는가
     - IFR은 instruction의 명시적 constraint를 측정한다. 암묵적 constraint는 측정하지 않는다.
     - Harness가 통과시킨 모든 tool call이 올바른데 전체 결과가 잘못된 조건이 가능하다.
   - E20: Compute saturation — HOR이 token budget을 초과할 때의 failure mode
     - Harness overhead가 실험 비용이 되는 조건 — "harness가 harness를 필요로 하는" 상황
   - 이 두 실험이 보여주는 것: harness의 설계 범위와 범위 밖에 있는 것들

---

<!-- 섹션별 초고는 /draft ch04 N 으로 작성 -->
<!-- 실험 완료 전: 실험 로그를 먼저 채운 후 작성 시작. design-specification.md가 가설 레지스트리. -->

## 참조

- `experiments/design-specification.md` (전체 — 이 챕터의 가설 레지스트리)
- `experiments/figure_expansion.md` — Figure 1~8 상세 설계
- `experiments/scenario-master.md`
- `experiments/framework/` (측정 인프라 전체)
- `experiments/axis-1-model-variation/` (E01~E04)
- `experiments/axis-2-harness-surface/` (E05~E08)
- `experiments/axis-3-constraint-bottleneck/` (E09~E14)
- `experiments/axis-4-operator-intervention/` (E15~E17)
- `experiments/axis-5-harness-internalization/` (E18~E20)
- `experiments/counterexamples/` (E19~E20)
- `evidence/tables/bottleneck-by-condition.md`
