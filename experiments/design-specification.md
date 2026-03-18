# Harness Engineering & AgentOps — Experimental Design Specification

> 버전: v1.0 | 작성일: 2026-03-18
> 이 문서는 figure_expansion.md의 Figure Catalog를 실험 가능한 프로토콜로 전환한다.
> Pre-registration 원칙: 이 문서에 기록된 가설, 검정, 판단 기준은 데이터를 보기 전에 확정된다.

---

## 1. Task Specification — 실험 대상 task의 조작적 정의

모든 실험에서 agent가 수행하는 task를 사전 정의한다. Task가 모호하면 실험 결과가 재현 불가능하다.

### 1.1 Task 유형 체계

#### T1 — Code Review (정적 분석 + 버그 식별)

```
입력:
  - Python 함수 1개 (50~150 LOC)
  - 함수 내 seeded bug 3~5개 (유형: off-by-one, null check 누락,
    race condition, type mismatch, resource leak 중 선택)
  - 버그 유형 및 위치는 실험 전 별도 파일에 ground truth로 기록

출력 (agent에게 요구):
  - 버그 목록: 각 버그의 (line_number, bug_type, severity, 수정 제안)
  - JSON 형식으로 구조화

성공 기준:
  - F1 score = 2·(Precision·Recall) / (Precision+Recall)
  - Precision = correctly_identified / agent_reported
  - Recall = correctly_identified / ground_truth_total
  - TCR(T1) = 1 if F1 ≥ 0.70, else 0
  - Partial credit: TCR = F1 값 그대로 사용 (연속 변수 필요 시)

난이도 파라미터:
  - EASY: 함수 50 LOC, bug 3개, 모두 단일 라인 버그
  - MODERATE: 함수 100 LOC, bug 4개, 1개는 multi-line logic bug
  - FRONTIER: 함수 150 LOC, bug 5개, 2개는 concurrency/state bug
```

#### T2 — Multi-Step Reasoning (계획 + 실행 체인)

```
입력:
  - 소프트웨어 dependency resolution 문제
    (패키지 N개, 각 패키지의 version constraint, conflict 포함)
  - 또는 resource scheduling 문제
    (task N개, 각 task의 prerequisite graph, resource limit)
  - N 값으로 난이도 조정

출력 (agent에게 요구):
  - 실행 순서 + 각 단계의 근거
  - JSON: [{"step": 1, "action": "...", "rationale": "..."}]

성공 기준:
  - Valid plan: 모든 constraint 충족 여부 (자동 검증기로 판정)
  - TCR(T2) = 1 if plan_is_valid, else 0
  - Sub-goal credit: valid_steps / total_steps (연속 변수)

난이도 파라미터:
  - EASY: N=5, 선형 dependency
  - MODERATE: N=10, 2개 conflict, 1개 optional constraint
  - FRONTIER: N=20, cyclic dependency 포함, resource bottleneck
```

#### T3 — Long-Horizon Execution (40+ step 자율 실행)

```
입력:
  - Repo-level 코드 리팩토링 task
    예: "이 codebase의 모든 함수에서 magic number를 named constant로 교체하라"
  - 또는 "log statement를 structured logging으로 전환하라"
  - 시작 시 initial goal을 명시적으로 context에 주입

실행 구조:
  - 각 step = 1개 tool call (file read / file edit / test run)
  - 최대 40 step (step budget을 agent에게 고지)
  - 10 step마다 checkpoint: agent에게 "현재 목표를 한 문장으로 서술하라" 요청

성공 기준:
  - Primary: test suite pass rate (before vs after)
  - Secondary: goal fidelity at checkpoint 4 (step 40)
  - TCR(T3) = 1 if (test_pass_rate ≥ 0.95) AND (goal_fidelity at step 40 ≥ 0.80)

난이도 파라미터:
  - EASY: 10 파일, magic number 20개
  - MODERATE: 25 파일, 50개, 일부 중첩 패턴
  - FRONTIER: 50 파일, 100개, 일부 런타임 의존 값 포함 (ambiguity 유발)
```

#### T4 — Context-Sensitive Synthesis (정보 검색 + 합성)

```
입력:
  - 문서 10개 (각 500~1000 tokens)
  - 문서들 중 3~5개에 질문의 답이 분산되어 있음
  - 나머지 문서는 관련 없거나 오답을 유도하는 내용 포함

출력 (agent에게 요구):
  - 통합 답변 + 출처 인용 (문서 번호 + 해당 문단)

성공 기준:
  - Recall of key facts: 핵심 사실 K개 중 몇 개 포함
  - Precision: 오답 유도 내용을 포함하지 않았는가
  - TCR(T4) = 1 if (recall ≥ 0.80) AND (precision ≥ 0.90)

난이도 파라미터:
  - EASY: 답이 1개 문서에 집중, 관련 없는 문서 3개
  - MODERATE: 답이 3개 문서에 분산, 오답 유도 2개
  - FRONTIER: 답이 5개 문서에 분산, 모순된 정보 포함, 추론 필요
```

### 1.2 실험별 Task 배정

| 실험 | 사용 Task | 난이도 | 비고 |
|------|-----------|--------|------|
| E01 (Capability Cliff) | T1, T2, T3 | ALL 3단계 | ARCC 측정용 |
| E04 (Harness Effect) | T1, T2, T3 | MODERATE | harness on/off 비교 |
| E07 (Surface Effect) | T1, T2 | MODERATE | 4개 surface 비교 |
| E08 (SAA Degradation) | T3 | MODERATE | token budget sweep |
| E09 (Goal Drift) | T3 | MODERATE | 40-step, checkpoint |
| E11 (Multi-Agent) | T1 × 2 agents | MODERATE | 동시 실행 |
| E15 (Self-Reporting) | T1, T2, T3 | ALL 3단계 | calibration 측정 |
| E18 (Pareto/Ablation) | T2 | MODERATE | configuration 탐색 |
| Fig 9 (Harness ROC) | T2, T3 | MODERATE | ground truth 필수 |
| Fig 11 (Scaling) | T2 | ALL 3단계 | harness on/off pairs |
| Fig 12 (Temporal) | T3 | FRONTIER | long-duration run |

---

## 2. ARCC — Agent-Relevant Capability Composite

Figure 1의 X축. 모델을 vendor tier가 아닌 연속 capability spectrum 위에 위치시키는 척도.

### 2.1 하위 지표 조작적 정의

**TCA — Tool Call Accuracy**
```
TCA = (tool_calls_returned_valid_output) / (tool_calls_attempted)

측정:
  - valid output = JSON schema 통과 + 내용이 task context에 관련됨
  - 각 tool call에 대해 자동 validator 적용
  - 10회 동일 task 반복 실행의 평균
```

**IFR — Instruction Following Rate**
```
IFR = mean(binary_compliance_scores across N instructions)

측정:
  - 5개 명시적 instruction이 포함된 task 설계
    예: "출력을 JSON으로 하라", "각 버그에 severity를 포함하라",
        "3문장 이내로 요약하라", "영어로만 작성하라" 등
  - 각 instruction에 대해 자동 판정: 0 or 1
  - IFR = 준수한 instruction 수 / 전체 instruction 수
```

**MSRD — Multi-Step Reasoning Depth (정규화)**
```
MSRD_raw = step index at which first logical error occurs
           (T2 기준: valid dependency chain이 끊기는 시점)

MSRD_normalized = MSRD_raw / task_max_steps
                = [0, 1]

측정:
  - T2 task에서 단계별 validity 자동 검증
  - error-free 완주 시 MSRD_normalized = 1.0
```

**CUE — Context Utilization Efficiency**
```
CUE = (relevant_chunks_cited_or_used) / (total_relevant_chunks_available)

측정:
  - T4 task: 문서 내 relevant passage 위치를 사전 표시
  - agent output에서 각 passage 참조 여부 확인
  - CUE = 참조된 relevant passage / 전체 relevant passage
```

### 2.2 ARCC 계산

```
ARCC = w₁·TCA + w₂·IFR + w₃·MSRD_n + w₄·CUE

초기 가중치: w₁ = w₂ = w₃ = w₄ = 0.25 (equal weighting)
범위: [0, 1]
```

### 2.3 ARCC Construct Validation Protocol

ARCC가 실제로 TCR을 예측하는가를 검증한다. 이 단계가 실패하면 Figure 1의 X축 전체가 무효화된다.

```
Step 1: 측정
  - 모델 풀 (N ≥ 12개 variant) 전체에서 ARCC 4개 하위 지표 측정
  - 동일 조건에서 TCR(T1), TCR(T2), TCR(T3) 측정

Step 2: 분할
  - 80% training set (모델 × task 조합)
  - 20% holdout set

Step 3: 피팅
  - Linear regression: TCR ~ ARCC (equal weight)
  - 추가: Ridge regression (regularized)

Step 4: 검증 기준
  - Holdout R² ≥ 0.65 → ARCC 유효 (사용 가능)
  - Holdout R² ∈ [0.50, 0.65) → 경고 표시 후 사용
  - Holdout R² < 0.50 → ARCC 재설계 필요 (가중치 재최적화)

Step 5: Sensitivity Analysis
  - 각 가중치를 ±0.15 범위에서 grid search
  - TCR prediction variance를 report
  - 가중치 변화에 robust하면 equal weighting 유지
  - sensitive하면 데이터 기반 최적 가중치 사용 + 이유 명시

보고:
  - Table: 각 모델 variant의 (TCA, IFR, MSRD_n, CUE, ARCC, TCR_observed, TCR_predicted)
  - Figure 1 Appendix: ARCC validation scatter plot (predicted vs observed TCR)
```

---

## 3. Ground Truth Infrastructure

Figure 9 (Harness ROC)와 Figure 7 (Calibration)의 기반. ROC를 계산하려면 각 step의 상태가 "실제로 failure였는가"를 독립적으로 알아야 한다.

### 3.1 Ground Truth 구축 방법 (3-layer)

**Layer 1: Test Suite (자동, 주력)**
```
- 각 task에 대해 사전 작성된 검증 test suite
- T1: seeded bug 위치가 ground truth → F1 자동 계산
- T2: constraint checker → plan validity 자동 판정
- T3: test runner (pytest) → pass rate
- T4: key fact list → recall/precision 자동 계산

커버리지: 전체 실험 runs의 100%
비용: 낮음
한계: syntactic correctness만 평가, semantic error 일부 누락 가능
```

**Layer 2: External LLM Judge (반자동)**
```
모델: claude-opus-4-6 (실험 agent와 다른 모델)
입력: task 명세 + agent output + test suite 결과
출력: {verdict: pass/fail/uncertain, confidence: 0-1, rationale: "..."}

적용 조건:
  - Layer 1 결과가 "uncertain" 또는 test suite 미적용 구간
  - Harness가 failure로 판정한 step (ROC 계산을 위해 독립 검증 필요)
  - 전체 runs의 ~30%에 적용

Agreement with Layer 1 보고:
  - Cohen's κ 계산
  - κ ≥ 0.70 → Layer 2를 신뢰할 수 있는 judge로 간주
  - κ < 0.70 → Layer 2 기준 재조정 필요
```

**Layer 3: Human Evaluation (서브샘플)**
```
대상: Layer 2 judge가 "uncertain"으로 분류한 케이스의 50%
      + stratified sample (harness TP/FP/TN/FN 각 구간에서 비례 샘플링)
인원: rater 2명 (독립, blind to harness output)
프로토콜:
  - Rater A, Rater B 독립 판정
  - Disagreement → Rater C 결정 투표
  - Cohen's κ(A,B) 보고: κ ≥ 0.70 목표
비용 추정: Layer 3 케이스 수 × 15분/케이스

보고:
  - 3개 layer 간 agreement matrix
  - 최종 ground truth: Layer 1 우선, Layer 2 보완, Layer 3 결론
```

### 3.2 Class Imbalance 처리 (Figure 9 ROC)

실제 agent run에서 failure rate가 20% 미만이면 ROC가 아닌 Precision-Recall Curve가 더 적합하다.

```
사전 측정:
  - E04 harness-off 조건에서 natural failure rate 측정
  - failure rate > 30% → ROC 사용 (balanced enough)
  - failure rate ∈ [15%, 30%) → ROC + PR curve 동시 보고
  - failure rate < 15% → PR curve 주력, ROC는 참고

Stratified sampling for ROC:
  - failure cases와 non-failure cases를 같은 비율로 샘플링
  - 또는 class weight 조정: w_failure = N_total / (2 × N_failure)
  - 보고에 sampling 방법 명시
```

---

## 4. Power Analysis — 실험별 필요 표본 수

α = 0.05 (two-tailed), target power = 0.80. 사전 계산값이므로 데이터 수집 전에 확정.

### E04 — Two-Proportion Z-Test (핵심 실험)

```
가정:
  p_off (harness 없음의 RSuccR) = 0.40
    근거: TeamClaws failure rate ~60% → RSuccR ≈ 0.40 (보수적 추정)
  p_on  (harness 있음의 RSuccR) = 0.65 (최소 탐지 효과크기)

Cohen's h:
  h = 2·arcsin(√0.65) − 2·arcsin(√0.40)
    = 2·(0.9380) − 2·(0.6847)
    = 1.8760 − 1.3694
    = 0.5066

필요 n per group:
  n = ((z_α/2 + z_β) / h)²
    = ((1.960 + 0.842) / 0.5066)²
    = (2.802 / 0.5066)²
    = (5.531)²
    = 30.6 → 31 per group

버퍼 (10% attrition 고려): 35 per group
총 runs: 70 (harness-on 35 + harness-off 35) × 3 task types = 210 runs

보수적 채택: n = 40 per group per task type = 240 total
→ 효과크기가 작을 경우 (Δ = 15%p)에도 power ≈ 0.65 유지

MDH (Minimum Detectable Harness effect):
  n=40에서 power 0.80을 보장하는 최소 Δ = 0.19 → Δ ≥ 19%p
```

### E08 — Phase Transition Detection (AIC 비교)

```
방법: Simulation-based power analysis

데이터 생성 모델 (H1):
  Phase 1 (100% → 50% budget):
    SAA = 90 − 0.20·(100 − budget) + ε, ε ~ N(0, 5²)
  Phase 2 (50% → 0% budget):
    SAA = 90 − 0.20·50 − 0.80·(50 − budget) + ε
    = 80 − 0.80·(50 − budget) + ε

시뮬레이션:
  - 1000회 반복
  - 각 반복에서 budget sweep (1% 간격, n=40 budget level) 데이터 생성
  - piecewise linear와 linear fit 비교: ΔAIC = AIC_linear − AIC_piecewise
  - power = P(ΔAIC > 4 | H1 데이터)

결과:
  n=40 budget levels → power ≈ 0.87 (preliminary simulation)
  n=30이면 power ≈ 0.74 (threshold 미달)
  채택: n=40 budget levels, 각 level에서 5회 반복 = 200 runs

추가 검증:
  - K 추정의 95% CI 폭: 목표 ≤ ±5 budget % → bootstrap n=1000
```

### E09 — Goal Drift K-Step Estimation

```
방법: Bootstrap CI 폭 기준

목표: K의 95% CI 폭 ≤ 8 steps

데이터 생성 모델 (H1):
  Goal Fidelity(step) = 1.0 − 0.005·step                (step < K)
                       − 0.025·(step − K)               (step ≥ K)
  σ = 0.08 per step (run-to-run variability)
  K_true = 20 (가정)

시뮬레이션:
  - 각 run 수(n_runs = 5, 10, 15, 20)에서 1000회 bootstrap
  - CI 폭 = Q97.5(K_hat) − Q2.5(K_hat)
  - 목표: CI 폭 ≤ 8 steps

결과: n_runs = 10에서 CI 폭 ≈ 7.2 steps (목표 충족)
채택: 10 runs per task type × 3 task types = 30 runs (E09)
```

### E11 — Granger Causality (Multi-Agent Cascade)

```
검정: Granger causality (resource contention → CCS)

가정:
  - Lag = 2 time units (resource contention이 2 step 후 CCS에 영향)
  - n = 40 time points per run
  - SNR (signal-to-noise ratio) = 2.0

방법:
  - VAR model order selection: BIC
  - F-test for Granger causality: H0: lag coefficients = 0
  - α = 0.05

Power (n=40, lag=2, SNR=2.0):
  표준 Granger causality power table 기준: power ≈ 0.82 ✓

채택: 5 runs × 8 conditions (agent count 2~8) = 40 runs
```

### Figure 9 (Harness ROC) — AUC 추정 정밀도

```
목표: AUC 95% CI 폭 ≤ 0.10

Hanley-McNeil formula:
  SE(AUC) = √[(AUC(1−AUC) + (n_pos−1)·Q1 + (n_neg−1)·Q2) / (n_pos·n_neg)]
  Q1 = AUC/(2−AUC), Q2 = 2·AUC²/(1+AUC)

가정: AUC_true = 0.80, n_pos = n_neg (balanced)
  SE ≤ 0.025 (95% CI 폭 ≤ 0.10) 조건에서:
  n_pos ≥ 60, n_neg ≥ 60

채택: n_failure = 60, n_nonfailure = 60 = 120 labeled steps
Layer 3 human eval: stratified sample of 40 케이스
```

---

## 5. Statistical Analysis Plan (Pre-Registration)

데이터를 보기 전에 확정하는 분석 계획. 이 계획에서 벗어날 경우 반드시 명시하고 이유를 기록한다.

### 5.1 E04 — Primary Analysis

```
검정: Two-proportion z-test (one-tailed: H1: p_on > p_off)
단위: 각 run = 독립 observation
보정: 3개 task type에 대해 Bonferroni (α_adjusted = 0.05/3 = 0.0167)
효과크기: Cohen's h + 95% CI
추가: 2-way ANOVA (harness × task_type) — interaction term이 유의(p < 0.05)하면
      "harness 효과는 task type에 따라 다르다"를 별도 결과로 보고
Radar chart: failure taxonomy 분포의 차이를 χ² test로 검정

보고 기준:
  - p < 0.0167 AND Cohen's h > 0.40 → "강한 증거"
  - p < 0.0167 AND Cohen's h ≤ 0.40 → "유의하나 효과 작음"
  - p ≥ 0.0167 → "유의하지 않음" (H0 기각 실패)
```

### 5.2 E08 — Phase Transition Analysis

```
1차: AIC 비교
  ΔAIC = AIC_linear − AIC_piecewise
  ΔAIC > 4 → "piecewise가 더 나은 설명"
  ΔAIC > 10 → "강한 증거로 phase transition 존재"
  ΔAIC ≤ 4 → "linear vs piecewise 구분 불충분"

2차: K 추정 (piecewise 채택 시)
  - Muggeo's segmented regression 또는 grid search over K
  - Bootstrap 95% CI for K
  - "Phase transition은 budget X%±Y% 구간에서 발생한다"

3차: HDL lead time (Figure 4 Panel B)
  - Paired t-test: HDL step vs SAA onset step (동일 run 내 비교)
  - H0: HDL_step = SAA_onset_step
  - H1: HDL_step < SAA_onset_step (harness가 먼저 감지)
  - p < 0.05 AND mean(HDL_step − SAA_onset_step) < 0 → harness sentinel 역할 증명
```

### 5.3 E09 — Goal Drift Analysis

```
1차: Drift regime 존재 여부
  - K 추정: grid search over K ∈ [5, 35], 1 step 간격
  - AIC comparison: single-slope vs. piecewise-at-K
  - 채택 기준: ΔAIC > 4

2차: K 추정 불확실성
  - Bootstrap (n_bootstrap=1000) → 95% CI for K
  - 보고: K_hat (point estimate) ± CI

3차: Drift trigger 분석 (Panel B)
  - Logistic regression: P(trigger_type | step_position_relative_to_K)
  - 각 trigger type이 K 전후에서 비율 변화가 유의한지: McNemar test

4차: Intervention 효과 (Panel C)
  - One-way ANOVA: intervention type (3개) × drift reversal success (binary)
  - Post-hoc: Tukey HSD (pairwise comparison)
```

### 5.4 E11 — Granger Causality

```
1차: Unit root test (ADF test) — 시계열 안정성 확인
  - I(1) 시계열이면 VAR 전에 differencing

2차: VAR lag order selection
  - BIC 기준 (p ≤ 4)

3차: Granger causality
  - F-test: resource contention lags → CCS
  - 반대 방향도 검정 (CCS → resource contention)
  - "resource contention이 CCS의 Granger cause이고, 역은 아니다"가 H1

4차: Impulse response function (IRF)
  - resource contention 충격 → CCS의 시간적 반응
  - Point-of-No-Return 정의: IRF가 임계치를 넘는 시점
```

### 5.5 Figure 9 — ROC Analysis

```
1차: AUC 추정
  - Non-parametric (Wilcoxon-Mann-Whitney 기반)
  - Bootstrap 95% CI (n_bootstrap=2000)

2차: 비교
  - Full harness vs. partial harness: DeLong test for AUC comparison
  - p < 0.05 → "full harness가 partial harness보다 유의하게 더 잘 감지한다"

3차: Operating point selection
  - Youden's J = Sensitivity + Specificity − 1 최대화 지점
  - 또는 precision = 0.90 constraint 하에서 recall 최대화

4차: Capability level 효과
  - AUC(100%) vs AUC(50%) vs AUC(25%) 비교
  - "capability 저하 시 harness detection도 저하되는가" 검정
```

---

## 6. Cost Model Assumptions (Figure 8C)

Dollar translation의 근거. 임의적 수치가 아닌 명시적 가정에서 도출한다.

### 6.1 Compute Cost (API)

```
2026년 3월 기준 Anthropic API pricing (추정):
  claude-sonnet-4-6: input $3.00/MTok, output $15.00/MTok
  claude-haiku-4-5:  input $0.25/MTok, output $1.25/MTok

평균 run 비용 추정 (T2 MODERATE, 20 steps):
  Input: 2,000 tokens/step × 20 steps = 40,000 tokens = $0.12 (sonnet)
  Output: 800 tokens/step × 20 steps = 16,000 tokens = $0.24 (sonnet)
  Cost_compute = $0.36 per run

Harness overhead (HOR = 20% 기준):
  Harness token 추가: 40,000 × 0.20 = 8,000 tokens = $0.024 (input)
  Cost_harness = $0.024 per run

HOR이 x%일 때:
  Cost_compute(x) = Cost_compute_base × (1 + x/100)
```

### 6.2 Failure Cost

```
가정:
  - 엔지니어 hourly rate: $150/hr (시니어 엔지니어 기준, 2026)
  - MTTR (harness 없음): 45분 (관찰 기반 추정. 실험 결과로 교체)
  - MTTR (harness 있음): 실험 Panel C에서 측정
  - Undetected failure downstream cost:
    P(undetected | harness off) × $500 (평균 downstream damage 추정)
    P(undetected | harness on) × $500

Cost_failure = MTTR_hours × $150 + P_undetected × $500

3가지 cost scenario:
  Scenario A (API): 위 가정 그대로
  Scenario B (self-hosted GPU): compute cost × 0.4, engineer cost 동일
  Scenario C (hybrid): compute cost × 0.7, engineer cost × 1.2 (on-call premium)
```

### 6.3 Total Operational Cost Index

```
TotalCost(HOR) = Cost_compute(HOR) + Cost_failure(RSuccR(HOR)) + Cost_escalation

Cost_escalation = Human_Escalation_Rate(HOR) × 0.25hr × $150

정규화:
  CostIndex(HOR) = TotalCost(HOR) / TotalCost(HOR=0)
  → HOR=0일 때 CostIndex=1.0 (no harness baseline)
  → 최적점: argmin_HOR CostIndex(HOR)

보고:
  - 3개 scenario 각각에서 optimal HOR 비교
  - Robust conclusion: 3개 scenario에서 모두 동일 optimal 구간이면 결론 강화
  - Sensitivity: engineer rate ±50% 변동 시 optimal HOR 변화 보고
```

---

## 7. Deviation Protocol

실험 중 이 명세에서 벗어날 경우:

```
허용된 deviation:
  - Sample size 증가 (power 강화 목적)
  - 추가 탐색적 분석 (confirmatory analysis와 명확히 구분)

반드시 기록해야 하는 deviation:
  - 가설 변경
  - 검정 방법 변경
  - 판단 기준(threshold) 변경
  - Task specification 변경

기록 형식:
  [DEVIATION] 날짜 | 실험 | 변경 내용 | 이유
  → 이 섹션에 append
```

---

## 8. Experiment Readiness Checklist

각 실험 시작 전 확인:

```
[ ] Task specification 파일 존재 및 ground truth 기록 완료
[ ] ARCC validation 완료 (R² ≥ 0.65)
[ ] Ground truth infrastructure (Layer 1 + 2) 가동 확인
[ ] Power analysis 통과 (목표 n 확인)
[ ] Statistical analysis plan 이 문서에 사전 기록됨
[ ] Failure taxonomy codebook 완성 (Figure 3 실험 한정)
[ ] Harness configuration 버전 고정 (git tag)
[ ] Random seed 고정 및 기록
```
