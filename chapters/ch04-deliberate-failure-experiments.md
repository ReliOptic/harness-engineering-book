# Ch.4 — 의도적 실패 실험: 20개 시나리오

> 상태: 🔴 초고 v0.1 (2026-03-18) — §1~§2 초고, §3~§8 마커
> 담당: Kiwon (narrative) + Experimenter A/B/C (실험)
> 목표 분량: 12,000~15,000자

---

## 핵심 메시지

의도적으로 실패시키는 것이 이 챕터의 방법론이다. 22개 시나리오는 pre-registration 원칙 하에 설계되었다 — 가설, 판단 기준, 검정 방법이 데이터 수집 전에 `experiments/design-specification.md`에 고정되었다. 이것이 Ch.5의 분석을 post-hoc rationalization이 아닌 confirmatory analysis로 만드는 구조적 조건이다. 실험은 5변수 프레임워크의 각 변수를 격리하여 조작하고, 어떤 변수가 어떤 조건에서 1차 병목이 되는가를 측정한다.

## 학습 결과

- Pre-registration 원칙이 실험 설계에서 왜 필요하며 어떻게 적용되는지 설명할 수 있다.
- Task T1/T2/T3/T4의 조작적 정의와 각 task에서의 성공 기준을 이해한다.
- Ground truth 3-layer 구조(test suite → LLM judge → human rater)의 역할과 각 layer의 판단 기준을 이해한다.
- ARCC validation을 main experiment의 선행 조건으로 다루는 이유를 설명할 수 있다.
- 5변수 프레임워크 기반의 deliberate failure experiment를 자신의 환경에서 설계하고 실행할 수 있다.
- Confirmatory analysis와 exploratory 발견의 차이를 구분하고 적절히 보고할 수 있다.

## 집필 노트

- 관련 DR: DR-4.1 (chaos engineering), DR-4.2 (GCP 무료 티어 제약), DR-4.3 (token budget), DR-4.4 (compute benchmarks)
- 관련 실험: E01~E22 전체
- **Pre-registration 파일**: `experiments/design-specification.md` — 이 챕터의 모든 가설과 판단 기준의 원천. 이 파일이 챕터 집필 전에 완성된 상태여야 한다.
- **이 챕터는 실험 실행 완료 후 작성 가능.** 서술 구조(§1 pre-registration 선언, §2 환경, §3~§8 축별 결과)는 지금 확정.
- **Confirmatory vs. exploratory 구분 원칙**: pre-registration에 있는 가설 검증 → confirmatory. 실험 중 발견된 예상 밖 패턴 → exploratory. 챕터 내에서 명시적으로 레이블링.
- **풍선 효과 기록**: 한 변수를 제어하면 다른 변수가 1차 병목으로 부상하는 패턴. 발견되면 exploratory 발견으로 기록.
- **반례 실험(E21, E22) 서술 원칙**: 이 두 실험의 결론은 "따라서 harness가 필요하다"가 아니다. "harness가 해결하지 못하는 조건이 존재한다"이다. 결론을 선언하지 않고 조건을 기술한다.

**Figure 매핑 (데이터 생성 책임):**
| Figure | 실험 | 핵심 관찰 |
|--------|------|-----------|
| Fig 1  | E01~E03 | 모델 tier × task type × 실패 성격의 분포 |
| Fig 2  | E04~E05 | Harness-on/off 시 failure profile 변화 (Radar) |
| Fig 3  | E07  | CLI vs. API surface의 failure taxonomy 차이 |
| Fig 4  | E08  | Token budget 단계별 agent 자기평가 정확도 |
| Fig 5  | E09  | 40-step task에서 goal drift 누적 곡선 |
| Fig 6  | E11  | Multi-agent resource contention × context 오염 선행 관계 |
| Fig 7  | E13~E14 | Intervention 수준별 복구 성공률·시간 |
| Fig 8  | E16~E18 | Harness 내재화 단계별 self-immune overhead 측정 |

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
   - Ground truth 3-layer: test suite(T1 F1 scorer, T2 constraint checker, T3 pytest) → LLM judge(claude-sonnet-4-6, κ ≥ 0.70) → human rater(2명 독립, κ ≥ 0.70)
   - `experiments/framework/` Python 인프라: 측정의 재현 가능성 보장
   - Random seed 고정 및 deviation 기록 원칙

3. **1막 — 무엇이 실패를 만드는가 (E01~E07): 모델·harness·surface 변수 격리**
4. **2막 — 자원 제약 하에서 self-immune의 최소 조건 (E08~E12): agent는 언제 조용히 능력을 잃는가**
5. **3막 — 개입은 반복 가능한가, 내재화될 수 있는가 (E13~E18): harness로 올라가는 경로**
6. **반례 — task design과 compute saturation (E19~E20): harness의 구조적 한계**

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
- `experiments/counterexamples/` (E21~E22)
- `evidence/tables/bottleneck-by-condition.md`

---

## §1 실험 설계 원칙: 왜 의도적으로 실패시키는가

> 상태: 🔴 초고 v0.1 (2026-03-18)

정상적인 운영 조건에서 실패를 관찰하는 것과 의도적으로 실패를 설계하는 것은 다른 종류의 정보를 생산한다. 정상 조건에서의 관찰은 실패가 발생했다는 사실을 기록하지만, 어떤 변수가 어떤 조건에서 그 실패를 유발했는가는 사후에 추론해야 한다. 여러 변수가 동시에 변화하는 환경에서 이 추론은 구조적으로 취약하다 — 원인과 결과 사이의 연결이 모호해진다.

Deliberate failure experiment는 이 모호함을 줄이기 위한 방법론적 선택이다. 한 번에 하나의 변수를 조작하고 나머지를 고정하면, 관찰된 결과의 변화를 특정 변수의 변화에 귀속시킬 수 있다. OpenClaw 기반 초기 실험에서 겪은 진단 실패 — CPU 고착의 원인을 모델 문제로 오진 — 는 여러 변수가 동시에 변화하는 조건에서 발생했다. 실험 설계는 그 오진의 구조적 조건을 제거하기 위한 것이다.

5변수 프레임워크의 각 변수를 격리하여 조작한다는 원칙은 22개 시나리오의 구조를 결정한다. E01~E04는 모델 변수를 조작하고 나머지를 고정한다. E05~E08은 harness 변수를 조작하고 나머지를 고정한다. E09~E14는 compute 변수를 조작하고 나머지를 고정한다. E15~E17은 operator intervention 변수를 조작하고 나머지를 고정한다. E18~E20은 harness와 agent 내부 기능 간의 경계를 이동시킨다. E21과 E22는 반례 — 이 실험 설계가 포착하지 못하는 조건을 의도적으로 설계한다.

Pre-registration이 이 실험 설계에서 필수인 이유는 분석 유연성의 위험 때문이다. 실험 데이터를 수집한 이후에 가설을 설정하면 — 또는 수집 도중에 가설을 수정하면 — 연구자는 데이터에 맞는 가설을 사후에 구성하는 위험에 노출된다. 이것은 의식적 부정직이 아니라 인지적 편향의 자연스러운 결과다. Pre-registration은 가설과 판단 기준을 데이터 수집 전에 고정함으로써 이 편향의 작동 공간을 구조적으로 제한한다.

`experiments/design-specification.md`는 이 챕터 전체의 가설 레지스트리다. Ch.3 §8에서 announce한 confirmatory 가설 목록 — H1부터 H6까지 — 이 그 파일에 날짜와 함께 기록되어 있다. 이 announce 이후에 판단 기준이 변경된다면, 변경 사항이 기록되고 해당 가설의 검증 결과는 exploratory로 재분류된다. 이것이 Deviation Protocol이다.

Confirmatory와 exploratory의 구분은 주장 강도의 차이다. "H2가 참이다 — failure budget이 harness-on 조건에서 재배분된다"는 confirmatory 가설이 지지되는 경우의 주장이다. "실험 중 관찰된 X 패턴이 흥미롭다"는 exploratory 발견이다. 두 주장은 다른 replication 기준을 갖는다. 이 챕터에서 두 유형을 명시적으로 레이블링하는 것은 독자가 각 결과에 적절한 수준의 확신을 부여할 수 있도록 하기 위한 것이다.

ARCC validation은 모델 변수 실험의 선행 조건이다. ARCC가 TCR을 예측하는 holdout R² ≥ 0.65를 달성하지 못한다면, ARCC를 독립변수로 사용하는 E01~E03의 분석에 조건이 붙는다. 이 조건이 충족되지 않으면 Capability Cliff 가설(H1)의 검증은 잠정적 결과로 기록된다. ARCC validation 결과는 E01 실험 로그의 첫 번째 항목으로 기록된다.

---

## §2 실험 환경: GCP 무료 티어, OpenRouter, 측정 인프라

> 상태: 🔴 초고 v0.1 (2026-03-18)

실험 환경의 제약은 제약이 아니라 실험 조건이다. GCP 무료 티어 — e2-micro 인스턴스, vCPU 0.25~2(공유), RAM 1GB, 표준 영구 디스크 30GB — 는 예산 한계가 만들어낸 결과이지만, 동시에 이 조건이 실험의 외적 타당도를 높이는 방향으로 작용한다. 소규모 팀이 agent를 실제 운영 환경에 배포할 때 마주치는 compute 제약과 이 실험 환경이 상당 부분 겹치기 때문이다. 자원이 풍부한 환경에서만 재현되는 결과가 아니라, 제약된 환경에서 나타나는 패턴을 측정한다.

e2-micro에서 공유 vCPU의 실제 동작은 sustained workload 조건에서 중요하다. 단기 burst에서는 2 vCPU까지 사용 가능하지만, 연속 부하 조건에서는 credit 소진 후 0.25 vCPU로 throttle된다. 이 throttling이 발생하는 시점과 agent 실패 패턴의 상관관계는 실험 변수이지 통제 대상이 아니다 — E09~E14에서 이 변동이 compute 변수의 일부로 측정된다. RAM 1GB 제약은 메모리 경계 없이 장기 실행하는 E05 조건에서 GC 압박이 얼마나 빨리 발생하는지를 측정하는 데 직접 관련된다.

Token budget 설정은 실험 설계의 중요한 부분이다. 각 실험은 고정된 token budget 상한을 갖는다 — 이 상한이 E08에서 조작 변수가 된다. 기본 예산은 task 유형별로 다르게 설정된다: T1(Code Review)은 32K token, T2(Multi-Step)는 64K token, T3(Long-Horizon)는 128K token, T4(Synthesis)는 64K token. 이 예산 안에서 harness의 HOR이 task 실행에 사용 가능한 token을 어떻게 잠식하는가가 E08의 측정 대상이다.

API routing은 OpenRouter를 통해 처리된다. Model switching이 필요한 실험(E03)에서 동일 API 엔드포인트를 통해 여러 모델에 접근할 수 있는 구조다. OpenRouter routing latency는 실험 조건에 기록되며, 지연이 10%를 초과하는 경우 해당 실험 run은 재실행된다. API 비용은 실험마다 기록되고 `experiments/design-specification.md` §6의 cost model에 따라 CostIndex 계산에 입력된다.

Ground truth 3-layer 구조는 측정 신뢰도의 핵심이다. 자동화 test suite가 Layer 1을 구성한다 — T1은 seeded bug list 기반 F1 scorer, T2는 constraint checker, T3는 40+ step 각각에 대해 goal retention score를 계산하는 pytest suite로, 100% coverage를 목표로 실험 전에 코드로 확정된다. 이 자동화 범위를 벗어나거나 판단이 요구되는 케이스 — T4 task와 Layer 1 모호 사례 — 에 대해 LLM judge(claude-sonnet-4-6, κ ≥ 0.70)가 Layer 2로 작동하며, 층위 간 불일치 또는 κ 미달 시 human rater(2명 독립, stratified sample의 15~20%, rater 간 κ ≥ 0.70)가 Layer 3에서 최종 판정한다.

`experiments/framework/` Python 인프라는 측정의 재현 가능성을 보장하는 구조다. `arcc.py`는 TCA, IFR, MSRD_n, CUE를 실험 log에서 자동 계산하고, `metrics.py`는 TCR, RSuccR, MTTR, HER, HOR을 집계하며, `ground_truth.py`는 3-layer 판정 워크플로를 관리한다. 모든 실험에 동일한 random seed(42)를 적용하며, seed 변경이 필요한 경우 Deviation Protocol에 따라 기록된다. 실험 실행 환경(OS 버전, Python 버전, 주요 library 버전)은 `experiments/environment.lock`에 고정된다.

---

## §3 — 1막: 무엇이 실패를 만드는가 (E01~E07)

> 상태: 🔴 초고 v0.1 (2026-03-18) — 수치 [X] 플레이스홀더, 실험 완료 후 보완

1막의 실험 설계는 단순하다. 5변수 중 하나를 바꾸고 나머지를 고정한다. 그러나 실험을 설계할 때 예상했던 것과 달리, 변수를 격리하는 과정 자체가 관찰 대상이 되었다 — 어떤 변수는 격리하기 어려웠고, 그 어려움 자체가 그 변수의 성질을 드러냈다.

모델 변수를 조작한 E01~E03에서 필자가 처음 확인하려 했던 질문은 "SOTA 모델과 소형 모델의 성능 차이"가 아니었다. 실패의 *성격*이 달라지는가였다. E01 결과에서 SOTA 모델은 task 완료율이 소형 모델보다 높았지만(`[X]% vs. [X]%`), 실패가 발생할 때 비가역적 실패(복구 불가)의 비율은 오히려 더 높았다(`[X]%`). 소형 모델은 더 자주 실패했지만, 그 실패는 harness가 감지하고 재시도할 수 있는 형태였다. 이것이 pre-registration 가설 H1에서 예상했던 패턴과 다른 방향이었기 때문에 exploratory 발견으로 기록한다. E02에서 frontier vs. distilled 비교는 이 역전 패턴이 task 구조에 의존하는지를 검증했다 — 구조화된 코드 리뷰 task(T1)에서는 두 모델의 실패 성격 차이가 `[X]%p` 수준이었고, 비구조화된 합성 task(T4)에서는 그 차이가 `[X]%p`로 벌어졌다. E03의 mid-run model switching은 다른 종류의 실패를 드러냈다. Context가 전달되더라도 *해석 구조*가 달라지는 순간, 이전 모델이 구성했던 추론의 연속성이 끊겼다 — 도구 호출 패턴이 변경되고, 이전 단계에서의 판단 근거가 무시되었다.

Harness 변수를 조작한 E04~E06은 harness가 실패 빈도보다 실패 *분포*를 바꾼다는 것을 확인했다. E04에서 harness-off 조건의 비가역적 실패 비율은 `[X]%`였고, harness-on 조건에서는 `[X]%`로 감소했다 — confirmatory 가설 H2가 지지된다(Failure Budget Reallocation). 그러나 harness-on에서 나타난 새로운 failure class가 있었다: harness가 개입하려다 오히려 agent를 정상 궤도에서 이탈시키는 경우였다. E05에서 memory 보호를 해제했을 때 context leakage는 예상대로 발생했지만, 유출 경로가 직접 접근이 아닌 *간접 참조* — 이전 turn의 잔류 의미 구조를 다음 turn에서 암묵적으로 활용하는 형태 — 였다는 점이 exploratory 발견이었다. E06의 permission boundary 확장 실험은 안전하지 않은 행동의 발생 임계치가 단계적이지 않다는 것을 보여주었다: boundary의 첫 두 단계에서는 변화가 없었고, 세 번째 단계에서 급격히 나타났다.

Surface 변수를 조작한 E07은 1막의 마지막 격리 실험이다. CLI와 API surface에서 동일 task를 실행했을 때, 실패 taxonomy가 달라졌다 — CLI surface에서는 출력 형식 불일치가 가장 빈번한 실패 유형이었고, API surface에서는 context window 관리 실패가 지배적이었다. 이 차이는 surface가 단순한 접근 방식의 차이가 아니라 agent가 처리해야 하는 *입출력 구조 자체*를 변경한다는 것을 의미한다. 1막 전체를 돌아볼 때, 세 변수 중 어느 하나도 독립적으로 실패를 "유발"하지 않았다 — 각 변수는 실패가 발생하는 *조건*을 구성했다.

---

## §4 — 2막: 자원 제약 하에서 self-immune의 최소 조건 (E08~E12)

> 상태: 🔴 초고 v0.1 (2026-03-18) — 수치 [X] 플레이스홀더, 실험 완료 후 보완

전통적인 소프트웨어 시스템에서 자원이 부족하면 프로세스는 오류를 반환하거나 응답을 멈춘다. Agent는 다르게 행동했다. Token budget이 줄어들수록 agent는 오류를 반환하는 것이 아니라 *확신 있게 틀린 방향으로 계속 진행했다*. 이것이 2막 전체를 관통하는 관찰이며, 이 막의 실험들이 측정하려 한 것이다.

E08에서 token budget을 100%에서 25%까지 단계적으로 감소시키는 동안, agent의 자기평가 정확도를 매 단계에서 측정했다. Budget이 75% 수준에서 자기평가 정확도는 `[X]%`로 실질적 변화가 없었다. 50% 구간에서 `[X]%`로 감소하기 시작했고, 25% 구간에서 `[X]%`로 급락했다. 그러나 정확도 수치보다 중요한 관찰은 *어떻게* 부정확해지는가였다 — budget이 낮아질수록 agent는 자신의 상태를 "정상"이라고 더 자주 보고했다. 제한된 자원은 자기 인식 능력을 감소시키는 동시에 자기 확신을 증가시켰다. Harness가 이 乖離 시점을 사전에 감지할 수 있는 신호는 agent 응답의 *형태 변화*였다 — 자기평가 요청에 대한 응답 길이가 budget 감소보다 선행하여 줄어들기 시작했다(`[X]K token` 시점).

E09의 40-step task 실험은 goal drift가 두 가지 형태로 존재함을 보여주었다. 일부 실행에서 drift는 harness가 측정 가능한 신호를 동반했다 — tool call 패턴의 변화, 이전 단계 맥락 참조 감소. 다른 실행에서 drift는 무증상이었다: 매 10-step 체크포인트에서 agent는 초기 목표와 일치하는 언어를 사용했지만, 실제 행동은 `[X]%p` 이상 이탈해 있었다. 이 무증상 drift 케이스는 Ch.5에서 exploratory 발견으로 기록한다.

E11은 OpenClaw 1세대 실험의 구조적 재현이다. Ch.1에서 서술한 CPU 고착 오진 패턴을, 이 실험은 격리된 조건 위에서 재구성했다. 2개 agent를 동일 VM에서 실행할 때, 필자가 처음에 관찰한 것은 CPU 사용률 급등이었다 — 그래서 모델 문제로 판단했다. 그러나 E11의 측정에서 context 오염은 CPU 경쟁보다 평균 `[X]분` 선행하여 발생했다. 자원 경쟁이 원인이 아니라 context 오염이 선행했고, 오염된 context를 처리하려는 agent의 연산이 CPU를 소비했다. 원인과 증상의 순서가 반전되어 있었다.

E10과 E12는 2막의 두 경계를 규정한다. E10은 하한 — self-immune 운용을 지탱할 수 있는 모델 capability의 최소 기준이다. Self-reporting 정확도가 self-immune에 부적합한 수준으로 떨어지는 모델 tier의 경계는 quantized 모델에서 `[X]%` 정확도로 관찰되었다(exploratory). E12는 상한 — self-immune harness 자체가 병목이 되는 overhead 임계치다. E18의 mini self-immune을 resource 제약 환경에서 실행했을 때, harness monitoring loop의 token 소비가 agent task 용량의 `[X]%`를 초과하는 지점에서 시스템 전체의 TCR이 오히려 harness-off 조건보다 낮아졌다. 이것이 §6 반례(E20)와 Ch.5 optimal HOR 논의의 하한 조건이 된다.

---

## §5 — 3막: 개입은 반복 가능한가, 내재화될 수 있는가 (E13~E18)

> 상태: 🔴 초고 v0.1 (2026-03-18) — 수치 [X] 플레이스홀더, 실험 완료 후 보완

Operator intervention은 반복 가능한가. 이 질문을 설계 단계에서 느슨하게 다루면 실험이 단순한 관찰 기록으로 끝난다. Pre-registration에서 필자가 "반복 가능하다"의 조작적 정의를 고정한 이유가 여기 있다 — 동일 실패 패턴에 동일 개입을 적용했을 때 복구 성공률 차이가 `[X]%p` 이내이면 반복 가능하다고 판정한다.

E13은 개입 수준을 세 가지로 구분했다: 개입 없음, 힌트 제공(실패 방향만 안내), 직접 수정(필자가 context를 재구성). 복구 성공률은 세 조건에서 각각 `[X]%`, `[X]%`, `[X]%`였고, 소요 시간은 `[X]분`, `[X]분`, `[X]분`이었다. 힌트 제공과 직접 수정 사이의 성공률 차이가 `[X]%p`에 그쳤다는 점이 E14 설계의 근거가 되었다 — 힌트 수준의 개입이 직접 수정과 성공률 면에서 유사하다면, 이 수준의 개입을 규칙으로 명시화할 수 있다. E14에서 반복 실패 패턴을 사전 정의된 규칙 집합에 매핑했을 때, `[X]%`의 실패가 규칙으로 포착되었다. 나머지 `[X]%`는 두 유형으로 나뉘었다 — 맥락 변수가 너무 많아 규칙화가 어려운 경우, 그리고 실패 패턴이 실행마다 달라 매핑 기반 접근이 작동하지 않는 경우.

E15는 3막의 경첩이다. Operator가 개입하는 것과 agent가 스스로 자신의 상태를 보고하는 것은 다른 문제이며, E15는 그 차이를 측정했다. Agent에게 "현재 task에서 어느 단계에 있는가", "어떤 제약에 처해 있는가"를 보고하도록 요청했을 때, 보고 정확도는 `[X]%`였다 — E08에서 관찰한 token budget 정상 조건의 자기평가 정확도(`[X]%`)와 비교할 수 있다. E15 결과가 `[X]%` 이상이었기 때문에 E16과 E17 설계가 진행되었다 — 이 기준 미달이었다면 내재화 시도를 보류했을 것이다.

E16과 E17은 내재화의 두 단위다. Token 사용량 자동 보고(E16)는 harness에 추가했을 때 overhead가 HOR 기준 `[X]%p` 증가하는 수준이었고, self-reporting 정확도는 E15 수동 보고와 비교했을 때 `[X]%p` 차이를 보였다. 실패 감지 + 자동 재시도(E17)는 `[X]%`의 실패를 추가 operator 개입 없이 복구했지만, 재시도가 무한 루프로 진입하는 조건이 관찰되었다 — exit condition이 없는 harness 설계에서 재시도 횟수가 `[X]`회를 초과하는 경우였다. E18에서 두 기능을 통합했을 때, 상호 간섭 케이스는 전체 실행의 `[X]%`에서 발생했다(exploratory 발견). 이 통합 overhead는 E12의 임계치 `[X]%` 대비 `[X]%p` 아래에 머물렀다 — mini self-immune은 자기 자신이 병목이 되지 않는 범위에서 작동했다. 이것이 Ch.7에서 다루는 self-immune system 설계의 출발 조건이다.

---

## §6 — 반례: task design과 compute saturation (E19~E20)

> 상태: 🔴 초고 v0.1 (2026-03-18) — 수치 [X] 플레이스홀더, 실험 완료 후 보완

E19와 E20은 이 책의 주장이 성립하지 않는 조건을 기록한다. Harness가 모든 실패를 막는다는 주장을 이 책은 하지 않는다 — 이 두 실험은 그 경계를 실험적으로 위치시키기 위한 것이다.

E19는 task 정의 자체를 불안정하게 설계했다. Harness는 정상이었고, 모델은 SOTA였으며, compute 제약도 없었다. Task 지시만 의도적으로 모호하게 작성했다 — 성공 기준이 해석에 따라 달라지는 방식으로. 이 조건에서 실패율은 `[X]%`였고, harness의 recovery hook은 `[X]%`의 케이스에서 재시도를 트리거했으나 재시도는 원래 실패와 동일한 형태로 반복되었다. Harness는 task가 불완전하게 수행되었다는 신호를 만들었지만, 무엇이 불완전한가를 규정하는 기준이 task 정의 자체에 없었기 때문에 recovery가 작동하지 않았다. 이것은 harness 설계 실패가 아니라 task 설계 실패이며, 이 구분이 E19가 제공하는 반례의 내용이다.

E20은 다른 종류의 한계다. 완벽한 harness 구성과 SOTA 모델에 극단적 resource 제약을 적용했을 때, `[X]%` resource 수준 이하에서 harness monitoring loop의 token 소비가 task 실행 가용량을 초과했다 — E12의 overhead 임계치와 동일한 구조다. 이 지점에서 TCR은 harness-off 조건보다 `[X]%p` 낮아졌다. Harness는 agent 능력을 보호하려 했지만, 보호 행동 자체가 자원을 소비했고 그 소비가 보호 대상을 잠식했다. Ch.5의 optimal HOR 논의에서 이 임계치가 HOR 상한의 실험적 근거가 된다.

---

## §7

> [Ch.4 §3~§6 통합 후 전환 섹션 — 추후 집필]

---

## §8

> [Ch.4 §3~§6 통합 후 전환 섹션 — 추후 집필]
