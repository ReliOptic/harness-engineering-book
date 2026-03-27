# Harness Engineering & AgentOps — Figure Catalog Deep Expansion

## 비판적 재설계 원칙

이 문서는 원본 Figure Catalog의 8개 실험 → 12개 figure를 기존 비판(harness ROC, ablation, scaling 부재)과 기원의 양자화/distillation 확장 관점을 통합하여 전면 재설계한다.

### 관통 원칙

1. **Every figure must answer a Monday-morning question** — 엔지니어가 이 그림을 보고 월요일 아침에 다르게 행동할 수 있어야 한다
2. **Mechanism before measurement** — "뭐가 달라졌다"가 아니라 "왜 달라졌고 어떤 조건에서 달라지는지"
3. **Anticipated rebuttal as design input** — 예상 반박을 실험 설계에 반영하여 논문 발표 전에 방어선을 구축
4. **Operational consequence** — 실험실 metric을 operational metric(MTTR, cost, human escalation)으로 번역

---

## Figure 1 — Agent Capability Cliff: Quantization & the Minimum Viable Model

← E01 확장

### 기존 설계의 한계

원본은 3×3 heatmap (model tier × task type × TCR)이었다. "SOTA / mid / small"이라는 tier 분류는 vendor taxonomy이지 과학이 아니다.

### 재설계

**형식:** Scatter plot with sigmoid regression fit, task-conditional  
**X축:** Agent-Relevant Capability Composite (ARCC) — tool call accuracy, instruction following rate, multi-step reasoning depth, context utilization efficiency의 weighted composite  
**Y축:** TCR (Task Completion Rate, %)  
**Marker encoding:** color = base model family, shape = quantization method (GPTQ / AWQ / GGUF variants)  
**Overlay:** task type별 sigmoid fit 3개 + 95% CI band  
**Annotation:** cliff position (ARCC threshold at TCR=50%) per task type

### 핵심 통찰: Capability Cliff

일정 capability 이하에서 TCR이 선형으로 떨어지는 것이 아니라 급락하는 지점이 존재한다. 이 "Agent-Viable Minimum"을 task별로 수치화하는 것 자체가 독립적 기여다.

**세부 요소:**

1. **Task-Conditional Cliff Position** — 코드 리뷰, 다단계 추론, 반복 실행 각각에서 cliff가 다른 ARCC 값에서 발생. 실무적 처방: "이 양자화 모델로 이 task는 된다"의 근거
2. **Quantization Tax Curve** — 동일 base model의 FP16→Q8→Q6→Q4→Q3→Q2 경로를 선으로 연결. 양자화가 agent capability를 깎는 비율이 model family마다 다르면 그 자체가 발견
3. **Distillation Efficiency Frontier** — 같은 parameter budget에서 distill model과 양자화 model의 TCR 비교. 어느 전략이 agent viability 관점에서 더 효율적인가

### 반박 대비

| 예상 반박 | 실험 설계 반영 |
|-----------|---------------|
| 벤치마크 점수가 agent capability proxy로 적절한가? | X축을 agent-relevant composite (4개 하위 지표)로 설계 + weight sensitivity analysis in appendix |
| 양자화 방법마다 다른데 뭘 비교하는가? | 양자화 방법을 통제변수가 아닌 독립변수로 취급. 같은 bit-width에서 방법 간 TCR 차이가 유의하면 그 자체가 기여 |
| 시점 snapshot 아닌가? | cliff의 절대 위치가 아니라 cliff의 존재와 형태(sigmoid)가 structural finding임을 논증 |
| Harness가 cliff position을 이동시키는가? | → Figure 2와의 교차 분석으로 연결 |

### Figure 2 연결점

Figure 1을 harness-off에서 먼저 그리고, Figure 2 결과와 결합하여 "harness-on일 때 cliff가 왼쪽으로 이동하는가"를 보여주면 — harness가 "더 작고 더 싼 모델의 agent viability를 확보한다"는 달러 단위의 주장이 가능해진다.

### 실험 프로토콜 핵심

- Adaptive sampling: FP16과 Q4만 먼저 → cliff 근처만 Q8/Q6/Q3으로 촘촘하게
- Base model 4종 × 양자화 5단계 × task 3종 × 반복 5회 = 300 runs → adaptive로 ~100 runs
- ARCC composite weight에 대한 sensitivity analysis 필수

---

## Figure 2 — The Harness Effect: Failure Profile Shift

← E04 ★중심 figure

### 기존 설계

2-panel: (A) Grouped bar TTFF, (B) RSuccR + unrecoverable failure rate stacked bar. 이건 "harness가 뭘 바꾸는지"는 보여주지만 "그래서 뭐가 달라지는지"를 안 보여준다.

### 재설계: 3-panel + operational translation

**Panel A — TTFF Distribution (기존 유지 + 확장)**
- 기존: bar chart → **확장: violin plot + individual data points (swarm)**
- Harness on/off × 3 task type
- Violin이 분포의 형태를 보여줌 — bimodal이면 "빨리 실패하거나 안 실패하거나"라는 구조가 드러남
- 핵심 추가: **TTFF의 variance가 harness 유무에 따라 어떻게 변하는가.** Mean뿐 아니라 predictability가 달라지면 운영 계획이 가능해짐

**Panel B — Failure Profile Radar (기존 대체)**
- 기존 stacked bar → **Radar chart (spider plot): 6-axis failure taxonomy**
  - Tool call failure / Context window overflow / Output format error / Silent logical drift / Recovery attempted & succeeded / Recovery attempted & failed
- Harness-on과 harness-off의 radar를 overlay
- 한눈에 "harness가 failure 빈도는 안 바꾸지만 failure의 성격을 바꾼다"를 시각화
- Stacked bar보다 직관적 — radar의 면적은 비슷한데 형태가 다르면 핵심 주장이 증명됨

**Panel C — Operational Translation (완전 신규) ★**
- X축: failure profile (harness off → harness on, 연속 스펙트럼 가능)
- Y축 (dual axis): 
  - Y1: MTTR (Mean Time To Recovery) — 분 단위
  - Y2: Human Escalation Rate (%) — 사람이 개입해야 했던 비율
- 우하향해야 함: harness가 MTTR을 줄이고 human escalation을 줄인다
- **이 panel이 존재하는 이유:** RSuccR은 실험실 metric이다. MTTR과 human escalation rate는 엔지니어의 on-call rotation에 직접 영향을 미치는 operational metric이다. 이게 없으면 "so what?" 질문에 답할 수 없다.

### 핵심 통찰: Failure Budget Reallocation

Harness의 진짜 효과를 "failure budget reallocation"이라는 프레임으로 설명한다:

> 총 failure 발생량(failure budget)은 거의 동일하다. Harness는 이 budget을 "unrecoverable/silent"에서 "detectable/recoverable"로 재배분한다.

이 프레임이 radar chart에서 면적 불변 + 형태 변화로 시각화되면, 책의 중심 명제가 한 장의 그림으로 증명된다.

### 반박 대비

| 예상 반박 | 실험 설계 반영 |
|-----------|---------------|
| Harness가 failure를 더 잘 "보고"하는 것일 뿐, 실제로 구조를 바꾸는 것은 아닌가? | Silent failure를 독립적 ground-truth로 측정: agent output을 사후 자동 검증 (test suite 통과율) |
| MTTR 측정이 인위적이지 않은가? | Automated recovery를 MTTR에 포함. Human escalation은 "agent가 help 요청 또는 사람이 개입 필요 판단"으로 조작적 정의 |
| N이 충분한가? | Power analysis: RSuccR Δ≥20%p, α=0.05, power=0.8 → group당 필요 N 사전 계산, 명시 |
| Task type에 따라 효과가 다르면 어떻게 하는가? | Task type × harness 상호작용을 2-way ANOVA로 검정. 상호작용이 유의하면 그 자체가 중요한 발견 — "harness는 모든 task에 동등하게 효과적이지 않다" |

### Figure 1 → Figure 2 교차 분석

Figure 1의 capability cliff position이 harness-on에서 왼쪽으로 이동하는지 검증:
- Figure 1의 cliff-edge 모델들(TCR 40-60% 구간)만 선별
- 이 모델들에 harness를 적용했을 때 TCR가 cliff 위로 올라가는 비율 측정
- → "Harness는 borderline 모델을 viable하게 만든다"는 cost-saving 주장의 직접 근거

---

## Figure 3 — Surface Effect on Failure Taxonomy

← E07

### 기존 설계의 한계

Stacked bar (CLI vs API × failure type). 문제: surface가 2개뿐이고, failure taxonomy의 근거가 ad hoc이다.

### 재설계: Surface × Failure Taxonomy Heatmap + Taxonomy Derivation

**Phase 0 — Taxonomy Derivation (pilot study, Figure 3의 전제 조건)**
- 100+개의 raw failure를 수집 (다양한 task, 다양한 surface)
- Open coding → Axial coding → 분류 체계 도출
- Inter-rater reliability: Cohen's κ ≥ 0.7
- 이 과정 자체를 Appendix에 보고 + 분류 codebook 공개

**Figure 3A — Surface × Failure Type Heatmap**
- X축: failure type (pilot에서 도출된 empirical taxonomy, 예상: 6-8개 유형)
- Y축: surface type — CLI / REST API / SDK wrapper / Chat UI (4종으로 확장)
- Cell: 해당 failure type의 발생 비율 (%)
- Color scale: 비율에 따른 sequential colormap

4개 surface로 확장하는 이유: 실제 agent 운영 환경은 CLI와 API만이 아니다. SDK wrapper(LangChain, CrewAI 등)는 자체 abstraction layer가 failure mode를 변형한다. Chat UI는 human-in-the-loop 환경의 대표.

**Figure 3B — Failure Flow Sankey Diagram (신규)**
- Left column: surface type (4개)
- Middle column: failure type (6-8개)
- Right column: failure outcome (recovered / escalated / undetected)
- Flow width = 비율
- 핵심: 같은 failure type이라도 surface에 따라 outcome이 다른지 시각화

### 핵심 통찰: Surface as Independent Variable

원본의 주장은 "surface가 failure 성격을 바꾼다"였다. 더 강한 주장을 한다:

> Surface는 harness의 하위 변수가 아니라 독립 변수이며, 동일한 harness configuration이라도 surface에 따라 failure profile이 다르게 나타난다. 따라서 harness 설계는 surface-aware해야 한다.

이것이 실무 처방: "CLI agent와 API agent에 같은 harness를 쓰지 마라."

### 반박 대비

| 예상 반박 | 실험 설계 반영 |
|-----------|---------------|
| Failure taxonomy가 자의적이다 | Phase 0 pilot study + inter-rater reliability + codebook 공개 |
| Surface 차이가 confound(task 차이) 아닌가? | 동일 task를 4개 surface에서 실행. Task를 blocking variable로 처리 |
| SDK wrapper가 너무 다양해서 하나로 대표 불가 | LangChain과 CrewAI 양쪽 측정 + 공통 패턴과 SDK-specific 패턴 분리 보고 |

### Harness 설계 함의

Figure 3의 결과에 따라 harness의 **surface-adaptive configuration** 가이드라인을 도출:
- CLI surface에서 주로 발생하는 failure type에 대한 hook 우선순위
- API surface에서의 timeout/retry 전략
- SDK wrapper의 abstraction layer가 만드는 failure masking 감지 방법

---

## Figure 4 — Self-Assessment Degradation Curve

← E08 ★2막 핵심

### 기존 설계

Line chart: SAA vs token budget + HDL overlay. 합리적이지만 두 가지가 빠져 있다.

### 재설계: 3-panel Phase Transition Analysis

**Panel A — SAA Phase Transition (기존 확장)**
- X축: Effective Capability Ratio (token budget %, 하지만 양자화 모델의 capability 감소도 여기에 매핑)
- Y축: SAA (Self-Assessment Accuracy, %)
- 핵심 변경: Token budget 감소와 양자화에 의한 capability 감소를 **동일한 X축** 위에 놓는다
  - Token budget 75% ≈ Q6 수준의 capability 감소
  - Token budget 50% ≈ Q4 수준
  - Token budget 25% ≈ Q2-Q3 수준
- 이렇게 하면 "양자화로 인한 자기인식 저하"와 "리소스 제약으로 인한 자기인식 저하"가 동일한 메커니즘인지 다른 메커니즘인지 비교 가능
- **Phase transition marker:** piecewise vs. sigmoid fit, AIC 비교
- **Critical insight:** 50% 이하에서 phase transition이 있다면, 이건 "agent는 자신이 못하는 줄 모른다"는 Dunning-Kruger analog의 정량적 증거

**Panel B — HDL Lead Time (신규) ★**
- X축: Capability Ratio (동일)
- Y축: HDL (Harness Detection Latency) — harness가 "뭔가 잘못됐다"고 감지하기까지의 step 수
- Overlay: SAA 하락 onset (Panel A에서 도출)
- **핵심 질문:** Harness는 agent 자신보다 먼저 문제를 감지하는가?
  - HDL < SAA onset → harness가 sentinel 역할을 한다 (핵심 가치 증명)
  - HDL ≥ SAA onset → harness가 agent보다 늦다 (harness 재설계 필요)
- 이 panel이 Figure 4의 harness engineering 기여를 결정한다

**Panel C — Metacognitive Decomposition (신규)**
- Agent의 self-assessment를 분해:
  - Confidence calibration (내가 얼마나 확신하는가 vs 실제 정확도)
  - Error detection rate (실수를 스스로 발견하는 비율)
  - Help-seeking behavior (언제 도움을 요청하는가)
- 각각이 capability ratio에 따라 어떻게 변하는지 별도 curve
- **핵심 발견 가능성:** Confidence는 유지되는데 error detection이 먼저 무너진다면, "agent는 자신감은 유지하면서 판단력을 잃는다" — 이게 가장 위험한 failure mode

### 반박 대비

| 예상 반박 | 실험 설계 반영 |
|-----------|---------------|
| SAA 측정 방법이 circular 아닌가? (agent에게 물어보는 것 자체가 self-assessment에 의존) | Ground truth는 external evaluator (별도 LLM 또는 test suite). SAA = agent 판단과 ground truth 일치율 |
| Token budget 감소와 양자화가 같은 메커니즘이라는 근거가 있는가? | 이걸 가설로 검증한다. 같으면 통합 모델, 다르면 별도 curve + 메커니즘 차이 논의 |
| Phase transition이 artifact(불연속적 task boundary)가 아닌가? | Task difficulty를 연속 변수로 설계. Budget을 1% 단위로 fine-grained sweep |

### Figure 1 연결

Figure 1의 capability cliff와 Figure 4의 SAA phase transition이 **같은 ARCC 값**에서 발생하는지 검증:
- Cliff와 phase transition이 동일 지점 → "모델이 task를 못하면 그걸 모른다"
- Cliff가 먼저 → "성능은 떨어졌지만 agent는 아직 인지한다" (graceful degradation)
- Phase transition이 먼저 → "agent가 모르는 사이에 판단력이 먼저 무너진다" (catastrophic — harness 필수 근거)

세 번째 시나리오가 가장 위험하며, 만약 이게 관찰되면 harness engineering의 존재 이유가 된다.

---

## Figure 5 — Goal Drift Inflection

← E09

### 기존 설계

Time series: cosine similarity vs step. Piecewise regression으로 K-step 추정. 나쁘지 않지만 "goal drift가 왜 일어나는지"와 "어떻게 막는지"가 없다.

### 재설계: Goal Drift Mechanism + Intervention Analysis

**Panel A — Drift Trajectory with Regime Classification (기존 확장)**
- X축: step (0~40)
- Y축: Goal Fidelity Score (cosine similarity → 이름 변경, 더 직관적)
- 5개 run의 individual trace + mean + SD band
- Piecewise regression: K-step 추정 + 95% CI for K
- **추가:** Regime classification
  - Stable regime (slope ≈ 0): step 0 ~ K
  - Drift regime (slope < threshold): step K ~ N
  - Divergence regime (slope acceleration): step N 이후 (관찰되는 경우)
- Color로 regime 구분: green → yellow → red

**Panel B — Drift Trigger Analysis (신규) ★**
- K-step 근처에서 무엇이 발생했는지 분석
- 가능한 trigger:
  1. Context window에서 original goal description이 밀려남 (positional)
  2. 중간 결과에 의한 goal reframing (semantic contamination)
  3. Tool output이 goal을 overwrite (external perturbation)
- 각 trigger별 발생 빈도를 K 전후로 비교
- **형식:** Stacked area chart — X = step, Y = trigger type 누적 비율
- 핵심: trigger가 identified되면 harness가 어디에 hook을 걸어야 하는지 알 수 있다

**Panel C — Harness Intervention Effectiveness (신규) ★**
- Goal drift가 감지되었을 때 harness가 취하는 intervention:
  1. Goal re-injection (original goal을 context에 다시 삽입)
  2. Progress checkpoint (현재 상태와 원래 목표의 alignment 강제 평가)
  3. Rollback (마지막 stable step으로 복귀)
- 각 intervention의 성공률 (drift reversal → Goal Fidelity Score 회복)
- **형식:** Bar chart — intervention type × 성공률, error bar = 95% CI
- **핵심 발견 가능성:** Goal re-injection만으로 충분한가, 아니면 rollback까지 필요한가? → harness 구현의 complexity 결정

### 반박 대비

| 예상 반박 | 실험 설계 반영 |
|-----------|---------------|
| Cosine similarity가 goal drift의 적절한 metric인가? | 추가 metric 병행: ROUGE-L (lexical), LLM judge score (semantic), task sub-goal 달성률 (functional). 4개 metric 간 correlation 보고 |
| 5개 run이면 K 추정의 uncertainty가 크지 않은가? | Bootstrap resampling으로 K의 95% CI 계산. CI가 넓으면 run 수 증가 |
| Step 단위가 아니라 token 단위가 맞지 않은가? | 둘 다 보고. Step과 token이 불일치하면 (긴 step에서 drift 가속) 그 자체가 발견 |

### 실무 처방 연결

Figure 5C의 intervention 효과 데이터를 바탕으로 Fieldkit에 포함할 "goal guardian" module의 기본 설정 결정:
- Re-injection 주기: K/2 step마다 (drift regime 진입 전에 예방)
- Checkpoint 조건: Goal Fidelity Score < 0.9일 때 trigger
- Rollback 조건: Score < 0.7이면 자동 rollback

---

## Figure 6 — Multi-Agent Contention Cascade Timeline

← E11

### 기존 설계

Dual-axis time series: resource contention index + CCS. 선행/후행 관계 규명. 하지만 "어떻게 막는지"와 "cascade가 언제 irreversible이 되는지"가 없다.

### 재설계: Cascade Anatomy + Point-of-No-Return

**Panel A — Cascade Timeline with Phase Annotation (기존 확장)**
- X축: time (초 or step)
- Y축 (dual): Resource Contention Index (좌), CCS (우)
- **추가 annotation:**
  - Phase 0: Normal operation (두 지표 모두 baseline)
  - Phase 1: Resource pressure onset (contention ↑, CCS 아직 baseline)
  - Phase 2: Context contamination begins (CCS ↑ 시작, lag 명시)
  - Phase 3: Cascade (두 지표 모두 급등, positive feedback loop)
  - Phase 4: System failure (recovery 불가 상태)
- Phase boundary를 vertical line + label로 명시
- **Granger causality lag:** Phase 1→2 사이의 시간차를 정량적으로 보고

**Panel B — Point-of-No-Return Analysis (신규) ★**
- X축: intervention 시점 (Phase 1 초기 / Phase 1 후기 / Phase 2 초기 / Phase 2 후기 / Phase 3)
- Y축: Recovery Success Rate (%)
- **형식:** Step function 또는 sigmoid decay
- **핵심 질문:** 어느 phase에서 개입해야 recovery가 가능한가?
- 예상 패턴: Phase 2 초기까지는 recovery 가능, Phase 3 진입 후 recovery 불가
- → "Point-of-No-Return"을 정량적으로 정의: 이 시점 전에 harness가 감지해야 한다

**Panel C — Agent Count Scaling (신규)**
- Agent 수(2, 3, 4, 5, 8)에 따른 cascade 발생 시간과 severity 변화
- X축: agent count
- Y축 (dual): Phase 1 onset time (좌), cascade severity at fixed time T (우)
- **핵심 질문:** Cascade risk는 agent 수에 선형으로 비례하는가, 초선형인가?
- 초선형이면 (예: O(n²)) → "multi-agent를 무작정 scaling하면 안 된다"의 정량적 근거
- 이건 TeamClaws/MultiClaws의 CPU saturation 실패 경험을 scientific하게 재구성하는 것

### 반박 대비

| 예상 반박 | 실험 설계 반영 |
|-----------|---------------|
| Resource contention index가 인위적 지표 아닌가? | CPU utilization, memory pressure, I/O wait의 PCA 1st component로 정의. 구성 요소별 개별 분석도 appendix에 |
| CCS 정의가 불명확하다 | CCS = agent i의 output에 agent j의 context가 포함된 비율 (n-gram overlap 기반). 정의 + 측정 방법 + sensitivity analysis |
| 실험 환경이 production과 다르다 | 실험을 GCP e2-micro (최소 사양)과 n1-standard-4 (적정 사양) 양쪽에서 실행. Resource headroom이 cascade dynamics를 어떻게 바꾸는지 보고 |

### TeamClaws/PicoClaw 연결

이 실험은 직접적으로 TeamClaws CPU saturation 실패의 사후 분석이 된다:
- TeamClaws 실패 시 관찰된 패턴이 Figure 6A의 어느 phase에 해당하는가?
- PicoClaw-native 아키텍처가 Phase 1→2 lag을 늘리거나 Phase 3 진입을 방지하는가?
- → 아키텍처 설계 결정의 empirical justification

---

## Figure 7 — Self-Reporting Calibration Plot

← E15

### 기존 설계

Reliability diagram: agent confidence vs actual accuracy. Budget level별 4개 curve overlay. 좋은 설계지만 "miscalibration의 방향"과 "실무적 대응"이 부족하다.

### 재설계: Calibration Anatomy + Trust Decision Framework

**Panel A — Calibration Curves by Capability Level (기존 확장)**
- X축: Agent reported confidence (0-1, 10 bins)
- Y축: Actual accuracy (ground truth 대비)
- Perfect calibration line (diagonal)
- 4개 curve: 100% / 75% / 50% / 25% capability level
- **추가:** 각 curve에 대해 ECE (Expected Calibration Error) 수치 + 95% CI 직접 표시
- **추가:** Overconfidence region (curve가 diagonal 아래)과 underconfidence region (위)를 색상으로 구분

**Panel B — Confidence-Accuracy Gap by Task Difficulty (신규) ★**
- X축: Task difficulty (composite score)
- Y축: Confidence-Accuracy Gap (agent confidence − actual accuracy)
- Gap > 0 = overconfident, Gap < 0 = underconfident
- Scatter with regression line, capability level별
- **핵심 발견 가능성:** 
  - 쉬운 task에서 underconfident + 어려운 task에서 overconfident → classic Dunning-Kruger pattern
  - 일관된 overconfidence → systematic bias
  - Capability 감소 시 overconfidence가 증가 → "능력이 떨어질수록 더 자신만만해진다" = harness 필수 근거

**Panel C — Trust Decision Boundary (신규) ★★**
- X축: Agent reported confidence
- Y축: Optimal action (binary or ternary)
  - Accept (agent 판단 수용)
  - Verify (추가 검증 필요)
  - Reject (agent 판단 기각)
- Calibration data를 바탕으로 Bayesian decision boundary 도출:
  - P(correct | confidence=c) = calibration curve에서 읽음
  - Accept if P(correct | c) > threshold_high (예: 0.9)
  - Reject if P(correct | c) < threshold_low (예: 0.5)
  - Verify if between
- **핵심:** 이건 harness의 실시간 의사결정 로직의 직접적 근거가 된다
- Capability level별로 decision boundary가 달라짐 → "harness는 agent의 현재 상태를 알아야 한다"

### 반박 대비

| 예상 반박 | 실험 설계 반영 |
|-----------|---------------|
| Agent "confidence"를 어떻게 측정하는가? | 3가지 방법 병행: (1) 직접 질문 "0-1로 자신감 보고", (2) logprob 기반 uncertainty, (3) consistency (같은 질문 반복 시 답변 일치율) |
| 10 bins이면 각 bin의 sample이 너무 적지 않은가? | Adaptive binning (equal-mass bins) + bin size별 ECE sensitivity |
| Calibration이 도메인 특이적이지 않은가? | 3개 domain (코드, 추론, 정보 검색)별 별도 calibration curve. Cross-domain 일반화 검증 |

### Harness Trust Engine 설계 함의

Figure 7C의 decision boundary를 harness의 "trust engine"으로 구현:
```
if agent.confidence > boundary_high[current_capability_level]:
    accept(agent_output)
elif agent.confidence < boundary_low[current_capability_level]:
    reject_and_retry(agent_output)
else:
    escalate_to_verification(agent_output)
```
이 로직의 threshold가 Figure 7의 empirical data에서 도출된다.

---

## Figure 8 — Self-Immune Tradeoff: Pareto Frontier

← E18 ★Ch.6 핵심

### 기존 설계

Scatter plot: HOR vs RSuccR, Pareto frontier. 좋지만 "왜 그 점이 optimal인지"의 mechanism이 없다.

### 재설계: Pareto Frontier + Ablation + Cost Translation

**Panel A — Pareto Frontier with Configuration Annotation (기존 확장)**
- X축: HOR (Harness Overhead Ratio, %)
- Y축: RSuccR (Recovery Success Rate, %)
- 각 점 = harness configuration
- Pareto frontier curve + dominated region shading
- **추가:** 각 Pareto-optimal 점에 configuration summary label
  - 예: "hooks=3, interval=5s, budget_threshold=80%"
  - 이게 있어야 엔지니어가 "이 설정을 쓰면 된다"고 판단 가능

**Panel B — Component Ablation Waterfall (신규) ★★★)**
- 형식: Waterfall chart
- Full harness configuration의 RSuccR에서 시작
- 각 component를 하나씩 제거할 때의 RSuccR 감소량
- Components:
  1. Monitoring hooks (state observation)
  2. Recovery mechanism (rollback, retry)
  3. Context boundary management (isolation)
  4. Budget enforcement (resource limits)
  5. Goal guardian (drift detection)
  6. Trust engine (confidence calibration, Figure 7에서)
- **핵심:** 어떤 component가 RSuccR의 몇 %를 설명하는가?
- Karpathy의 ablation 원칙: "complexity를 추가할 때마다 marginal value를 증명하라"
- 만약 component 2개가 RSuccR의 80%를 설명한다면 → "minimum viable harness"는 이 2개면 충분

**Panel C — Dollar Translation (신규) ★**
- X축: HOR (%, 동일)
- Y축: Total Operational Cost Index (정규화)
  - = compute cost (HOR에 비례) + failure cost (1 − RSuccR에 비례) + human intervention cost
- Cost curve가 U-shape를 형성해야 함:
  - HOR이 너무 낮으면 failure cost가 높고
  - HOR이 너무 높으면 compute cost가 높고
  - 최적점이 존재
- **핵심:** Pareto frontier의 "최적"이 기술적 최적이 아니라 경제적 최적이 되면, CTO에게 보여줄 수 있는 그림이 된다

### 반박 대비

| 예상 반박 | 실험 설계 반영 |
|-----------|---------------|
| Configuration 공간이 너무 넓어서 충분히 탐색했는가? | Bayesian Optimization으로 configuration 탐색. Random search baseline과 비교하여 탐색 효율 보고 |
| HOR 정의가 환경 의존적이지 않은가? | HOR = (harness 사용 total token) / (task 자체 total token). 상대적 비율이므로 환경 독립적 |
| Ablation의 순서 효과가 있지 않은가? | Full factorial ablation은 비용 과다 → Shapley value 기반 기여도 분해로 순서 독립적 추정 |
| Cost model이 arbitrary하지 않은가? | 3가지 cost scenario (API pricing, self-hosted GPU, hybrid) 각각에서 optimal point 비교. Robust하면 결론 강화 |

### Fieldkit Default Configuration 근거

Figure 8A의 Pareto-optimal 점 중, Figure 8C의 cost U-curve 최저점에 가장 가까운 configuration을 Fieldkit의 default로 제안. Figure 8B의 ablation 결과에 따라 "최소 이 component들은 켜야 한다"는 minimum requirement도 명시.

---

## 신규 Figure 9 — Harness Detection ROC

← 새로 제안하는 실험

### 존재 이유

이 figure가 없으면 전체 논증이 circular하다. "Harness가 failure를 감지한다"고 주장하면서 감지 정확도를 측정하지 않으면, Figure 2의 RSuccR이 과대추정될 수 있다.

### 설계

**형식:** ROC curve (multi-threshold)

**X축:** False Positive Rate (정상인데 harness가 failure로 판단한 비율)
**Y축:** True Positive Rate (실제 failure를 harness가 감지한 비율)
**Diagonal:** random classifier (AUC = 0.5)

**Multiple curves:**
1. Full harness configuration
2. Monitoring hooks only
3. Budget enforcement only
4. Lightweight harness (top-2 ablation components only)
5. Oracle baseline (사후 ground truth 평가, upper bound)

**추가 분석:**
- AUC 값 비교 + 95% CI
- Operating point annotation: precision-recall tradeoff에서 "precision 0.9 보장하는 threshold"
- Capability level별 ROC (100% / 75% / 50% / 25%) — 능력이 떨어지면 감지도 어려워지는가?

### 핵심 통찰

1. **Detection 한계의 정량화:** AUC가 0.95면 "harness를 믿어도 된다". 0.7이면 "harness도 놓치는 failure가 30%"
2. **False positive의 비용:** FPR이 높으면 harness가 너무 자주 alarm → 엔지니어 fatigue. Precision-recall tradeoff의 실무적 의미
3. **Capability 의존성:** 능력 저하 시 failure 자체가 subtler해져서 감지가 더 어려워진다면, Figure 4의 phase transition 이후에 harness가 무용해질 수 있다 → 2차 방어선 필요

### Ground Truth 구축

ROC를 계산하려면 ground truth가 필요하다. 이건 expensive하지만 필수:
- 각 step에 대해 사후 평가: 외부 LLM + test suite + human evaluator (서브샘플)
- 3가지 ground truth 방법 간 agreement 보고 (inter-method reliability)
- Human evaluation은 전수가 불가하므로 stratified sampling (harness 판단이 uncertain한 구간에 집중)

### 반박 대비

| 예상 반박 | 실험 설계 반영 |
|-----------|---------------|
| Ground truth 자체가 불완전하다 | 3가지 방법 교차 검증 + inter-method agreement |
| Silent failure는 ground truth에서도 놓칠 수 있다 | Delayed evaluation: task 완료 후 24시간 뒤 결과 재평가 (시간이 지나면 드러나는 failure 포착) |
| Production 환경에서 ROC가 다를 수 있다 | 실험 환경의 task distribution을 production log 기반으로 설계 |

---

## 신규 Figure 10 — Ablation Waterfall: Component Marginal Value

← Figure 8B에서 독립, 별도 figure로 격상 고려

### 존재 이유

Figure 8B에 포함시키기엔 너무 중요하다. Harness의 각 component가 기여하는 value를 분해하는 것은 이 책의 핵심 실무 기여다.

### 설계

**형식:** Waterfall chart (좌 → 우)

**시작:** No harness (RSuccR baseline, 예: 15%)  
**각 bar:** Component 추가 시 RSuccR 증가분  
**끝:** Full harness (RSuccR, 예: 78%)

**Component 순서 (Shapley value 기반 기여도 순):**
1. State monitoring hooks → +ΔRSuccR₁
2. Automated recovery (retry + rollback) → +ΔRSuccR₂
3. Context boundary management → +ΔRSuccR₃
4. Budget enforcement → +ΔRSuccR₄
5. Goal guardian → +ΔRSuccR₅
6. Trust engine → +ΔRSuccR₆

**추가 분석: Interaction Effects**
- 단순 합산 vs 실제 full harness RSuccR의 차이 = interaction effect
- Interaction이 크면: component들이 시너지를 냄 (순서 의존, 조합이 중요)
- Interaction이 작으면: component들이 독립적 (필요한 것만 골라 써도 됨)
- → 이 결과가 "modular harness" 설계 가능 여부를 결정

### 실무적 가치

엔지니어가 이 그림을 보고:
- "Recovery mechanism만 넣으면 RSuccR의 60%를 얻을 수 있고, monitoring까지 추가하면 85%를 얻는다"
- "Goal guardian은 2%밖에 안 더한다. 우리 use case에선 빼도 된다"
- → Build vs. skip 결정의 empirical 근거

---

## 신규 Figure 11 — Model Capability × Harness Value Scaling Curve

← 새로 제안하는 실험

### 존재 이유

이 figure가 이 책의 shelf life를 결정한다. GPT-5, Claude 5가 나왔을 때 이 책이 여전히 의미 있으려면, model capability 궤적과 harness value 사이의 관계를 보여야 한다.

### 설계

**형식:** Dual-axis line chart with extrapolation

**X축:** Model capability (ARCC, Figure 1과 동일 척도)
**Y축 (좌):** Harness Marginal Value = RSuccR(harness on) − RSuccR(harness off)
**Y축 (우):** Task complexity (동시에 수행하는 sub-goal 수, context 요구량, tool chain 길이 등의 composite)

**3가지 시나리오 track:**

1. **Fixed task complexity:** 동일 task에서 model capability 증가 → harness value 변화
   - 예상: S-curve 감소 — 모델이 좋아지면 harness 불필요 (이 task에 대해서)
   
2. **Task complexity scales with model capability:** 모델이 좋아지면 더 어려운 task를 줌
   - 예상: harness value 유지 또는 증가 — "더 복잡한 task = 더 복잡한 failure mode"
   
3. **Frontier push:** 항상 모델 능력의 boundary에서 task를 수행
   - 예상: harness value 최대 — "edge에서 일하면 항상 넘어진다"

### 핵심 통찰

결과에 따라 이 책의 positioning이 결정:

| 관찰 | 의미 | 책의 positioning |
|------|------|-----------------|
| 시나리오 1만 관찰됨 (harness value 감소) | 모델이 좋아지면 harness 불필요 | 이 책은 "과도기 기술 가이드" |
| 시나리오 2 관찰됨 (harness value 유지) | Task complexity가 함께 성장 | 이 책은 "항구적 엔지니어링 원칙" |
| 시나리오 3 관찰됨 (harness value 증가) | Frontier에서 harness가 더 중요 | 이 책은 "선구적 필수 교범" |

어느 시나리오가 관찰되든 이 figure가 정직하게 보고되면, 독자는 자신의 상황에서 harness 투자 결정을 내릴 수 있다.

### 실험 프로토콜

- Figure 1과 동일한 model variant pool 사용
- 각 capability level에서 harness on/off 쌍으로 실행
- Task complexity를 3단계로 통제 (simple / moderate / frontier)
- 3 × (model variants) × 2 (harness) × 3 (complexity) × 5 (반복) = 상당한 규모
- **현실적 타협:** Figure 1의 결과를 재활용. 추가 비용은 harness-on 조건만

### 반박 대비

| 예상 반박 | 실험 설계 반영 |
|-----------|---------------|
| 현재 모델로 미래 scaling을 예측할 수 있는가? | 예측이 아니라 현재 observable range 내의 trend 보고. Extrapolation에는 명시적 uncertainty band |
| Task complexity 정의가 자의적이다 | 3가지 complexity metric (sub-goal count, context requirement, tool chain length) 각각에 대해 별도 분석 + composite 분석 |

---

## 신규 Figure 12 — Harness Temporal Stability

← 새로 제안하는 실험

### 존재 이유

Harness는 처음 1시간과 10시간째에 동일하게 효과적인가? Harness 자체의 state drift는 없는가? 이걸 측정하지 않으면 long-running agent에 대한 harness 적용 가이드가 없다.

### 설계

**형식:** Time series with rolling window analysis

**X축:** Elapsed time (0 ~ 24hr, log scale 옵션)
**Y축 (triple overlay):**
1. Harness detection accuracy (rolling 1hr window)
2. False alarm rate (rolling 1hr window)  
3. Harness overhead ratio (rolling 1hr window)

**조건:** Long-running agent task (코드 리팩토링, 대규모 데이터 정리 등)

### 핵심 통찰: Harness Fatigue

예상되는 failure mode:
1. **Log accumulation:** Harness가 모니터링 데이터를 누적하면서 자체 context window를 소모 → detection accuracy 하락
2. **Threshold staleness:** 초기 설정된 임계값이 agent의 evolving state에 맞지 않게 됨
3. **False alarm escalation:** 시간이 지나면서 false alarm이 증가 → "harness cry wolf" 문제

만약 이런 패턴이 관찰되면:
- Harness 자체의 periodic reset이 필요한 주기 결정
- Adaptive threshold mechanism의 필요성 입증
- → "Harness도 monitoring이 필요하다" (meta-harness 또는 harness health check)

### 반박 대비

| 예상 반박 | 실험 설계 반영 |
|-----------|---------------|
| 24시간 실험이 현실적인가? | 비용 명시. 필요하면 simulated time compression (accelerated degradation) |
| Harness implementation에 의존적이지 않은가? | 2가지 harness implementation (event-driven vs polling) 비교 |

---

## 전체 Figure Architecture: 연결 구조

```
Chapter 1: The Landscape
  Fig 1  Capability Cliff          ─── "어디부터 agent가 되는가?"
                                        │
Chapter 2: The Core Effect              │ (cliff-edge 모델 선별)
  Fig 2  Failure Profile Shift     ─── "harness가 뭘 바꾸는가?"
  Fig 9  Harness Detection ROC     ─── "harness를 얼마나 믿을 수 있는가?"
                                        │
Chapter 3: The Surface                  │
  Fig 3  Surface × Failure         ─── "환경이 뭘 바꾸는가?"
                                        │
Chapter 4: Silent Degradation           │
  Fig 4  SAA Phase Transition      ─── "agent는 언제 자기를 잃는가?"
  Fig 7  Calibration Plot          ─── "agent의 자기 보고를 믿을 수 있는가?"
                                        │
Chapter 5: Drift and Cascade            │
  Fig 5  Goal Drift Inflection     ─── "목표는 언제 흐트러지는가?"
  Fig 6  Contention Cascade        ─── "다중 agent는 왜 무너지는가?"
                                        │
Chapter 6: The Immune System            │
  Fig 8  Pareto Frontier           ─── "최적 harness는 무엇인가?"
  Fig 10 Ablation Waterfall        ─── "어떤 component가 가치 있는가?"
                                        │
Chapter 7: The Future                   │
  Fig 11 Scaling Curve             ─── "이건 얼마나 오래 유효한가?"
  Fig 12 Temporal Stability        ─── "harness 자체는 얼마나 버티는가?"
```

### Figure 간 Cross-Reference Matrix

| From → To | 연결 내용 |
|-----------|----------|
| Fig 1 → Fig 2 | Cliff-edge 모델이 harness로 viable해지는가? |
| Fig 1 → Fig 4 | Capability cliff와 SAA phase transition이 같은 지점인가? |
| Fig 2 → Fig 9 | RSuccR의 신뢰도를 ROC가 검증 |
| Fig 4 → Fig 7 | SAA 하락과 calibration 붕괴의 선후 관계 |
| Fig 4 → Fig 9 | Phase transition 이후 harness detection도 무너지는가? |
| Fig 5 → Fig 6 | Goal drift가 multi-agent contention을 trigger하는가? |
| Fig 7 → Fig 8 | Trust engine의 threshold가 Pareto frontier에 기여하는 정도 |
| Fig 8 → Fig 10 | Pareto optimal 점의 component 분해 |
| Fig 10 → Fig 11 | Model capability 증가 시 중요 component가 바뀌는가? |
| Fig 11 → Fig 12 | 장시간 운영에서 scaling relationship이 변하는가? |

---

## 실험 우선순위 및 의존 관계

### Phase 1 (기반 — 다른 모든 실험의 전제)
1. **Failure Taxonomy Pilot** (Figure 3 전제): 100+ raw failure 수집 → coding → codebook
2. **Ground Truth Infrastructure** (Figure 9 전제): 외부 LLM + test suite + human eval pipeline
3. **E01 확장** → Figure 1: Quantization variant pool 구성 + ARCC 정의

### Phase 2 (핵심 실험)
4. **E04** → Figure 2: Harness effect (가장 중요, 이 결과가 책의 존재를 정당화)
5. **Harness ROC 실험** → Figure 9: Detection accuracy (Figure 2의 검증)
6. **E08** → Figure 4: SAA degradation (2막 핵심)

### Phase 3 (메커니즘 규명)
7. **E07 확장** → Figure 3: Surface effect (4개 surface)
8. **E09** → Figure 5: Goal drift + intervention
9. **E15** → Figure 7: Calibration + trust decision
10. **E11** → Figure 6: Multi-agent cascade

### Phase 4 (종합 및 처방)
11. **E18 확장** → Figure 8 + Figure 10: Pareto + ablation
12. **Scaling 실험** → Figure 11: Model capability × harness value
13. **Temporal 실험** → Figure 12: Harness fatigue

### 총 예상 실험 규모

| 실험 | 예상 run 수 | 주요 비용 요인 |
|------|------------|---------------|
| Fig 1 (E01 확장) | ~100 | Local GPU time (양자화 모델) |
| Fig 2 (E04) | ~60 | API cost (SOTA model) |
| Fig 3 (E07 확장) | ~120 | Mixed (4 surfaces × 모델 × task) |
| Fig 4 (E08) | ~80 | API cost (fine-grained budget sweep) |
| Fig 5 (E09) | ~50 | API cost |
| Fig 6 (E11) | ~40 | GPU time (multi-agent) |
| Fig 7 (E15) | ~80 | API cost |
| Fig 8+10 (E18 확장) | ~200 | Mixed (Bayesian optimization over configurations) |
| Fig 9 (신규) | ~100 | API + human eval cost |
| Fig 11 (신규) | ~150 | API cost (harness on/off pairs) |
| Fig 12 (신규) | ~20 | Long-duration GPU time (24hr runs) |
| **Total** | **~1,000** | |

---

## Ground Truth Construction Protocol (Figure 9 전제)

ROC 계산의 기반. 상세 프로토콜은 `design-specification.md` §3 참조.

**3-Layer 구조 요약:**
- Layer 1 (Test Suite, 100% coverage): task별 자동 검증기. T1=F1 scorer, T2=constraint checker, T3=pytest runner, T4=fact recall
- Layer 2 (LLM Judge, ~30% coverage): claude-opus-4-6로 독립 판정. Layer 1과 Cohen's κ ≥ 0.70 목표
- Layer 3 (Human, stratified sample): rater 2명 독립 판정. κ(A,B) ≥ 0.70 목표

**Class Imbalance 처리:**
- natural failure rate < 15% → PR curve 주력, ROC 참고
- natural failure rate ≥ 15% → ROC + PR curve 동시 보고
- 사전 측정: E04 harness-off 조건에서 failure rate 확인 후 결정

---

## Cost Model Assumptions (Figure 8C 전제)

Dollar translation의 수치 근거. 임의값이 아닌 명시적 가정.

**Compute cost (2026-03 기준):**
- claude-sonnet-4-6: $3.00/MTok input, $15.00/MTok output
- T2 MODERATE 20-step run 기준: 약 $0.36/run
- HOR x%일 때: Cost_compute × (1 + x/100)

**Failure cost 구성:**
- MTTR × $150/hr (시니어 엔지니어 rate)
- P(undetected) × $500 (downstream damage 추정)
- MTTR(harness off) = 45분 추정치 → 실험 Panel C 측정값으로 교체

**3가지 Cost Scenario:**
- A: API 전용 (위 가정 그대로)
- B: Self-hosted GPU (compute × 0.4)
- C: Hybrid (compute × 0.7, engineer × 1.2 on-call premium)

3개 scenario 모두에서 동일 optimal HOR 구간 → 결론 robust
상세 수식: `design-specification.md` §6

---

## 결론: 지금 이 설계가 기존 대비 바뀐 것의 본질

**기존:** 8개 실험, 12개 figure — "harness가 무엇을 하는가" 측정

**재설계:** 12개 실험, 12개 figure — 세 가지 축 추가:

1. **Why it matters** (Figure 2C operational translation, Figure 8C dollar translation)
   - 실험실 metric → 운영 metric → 비용 metric

2. **Why it works** (Figure 9 ROC, Figure 10 ablation, Figure 5C intervention)
   - 각 component의 mechanism과 marginal value 분해

3. **How long it will matter** (Figure 11 scaling, Figure 12 temporal stability)
   - 시간과 기술 발전에 대한 robustness

이 세 축이 채워지면, "failure profile이 바뀐다"는 방어적 명제가 다음과 같이 진화한다:

> **Harness engineering은 production AI의 reliability engineering이다. 그것은 더 작은 모델을 viable하게 만들고 (Figure 1↔2), 감지 가능한 failure를 구조적으로 생성하며 (Figure 2↔9), 각 component가 정량적으로 정당화된 immune system을 구축하고 (Figure 8↔10), model capability가 향상되어도 task complexity frontier에서 필수적이며 (Figure 11), 그 자체의 한계와 수명을 정직하게 보고한다 (Figure 9↔12).**
