# Ch.2 — Agent 성능을 어떻게 측정할 것인가

> 상태: 🔲 skeleton only → outline 개정 2026-03-27
> 담당: TBD (Experimenter A primary)
> 목표 분량: 10,000~12,000자

---

## 핵심 메시지

기존 LLM 벤치마크는 단일 호출 품질을 측정한다. Agent가 실제로 수행하는 multi-step 연속 실행에서 무엇이 다르게 필요한지를 벤치마크 역사를 통해 먼저 보여주고, 그 공백을 채우는 측정 방법으로 Agent-Relevant Capability Composite를 도입한다. 이 composite로 측정된 모델-task 조합은 특정 임계값 이하에서 Task Completion Rate가 선형이 아닌 급락하는 Capability Cliff를 형성하며, 이 cliff의 위치는 task 유형마다 다르다. 양자화와 distillation은 이 cliff를 다른 속도로 이동시킨다.

## 학습 결과

- LLM 벤치마크의 발전 역사(MMLU → SWE-bench → AgentBench)와 각 세대가 측정하지 못한 차원을 설명할 수 있다.
- Agent-Relevant Capability Composite의 네 구성 요소(Tool Call Accuracy, Instruction Following Rate, Multi-Step Reasoning Depth, Context Utilization Efficiency)의 정의와 측정 절차를 이해하고, 자신의 환경에서 유사한 복합 측정을 설계할 수 있다.
- Construct validation 기준(holdout R² ≥ 0.65)과 그 의미를 이해한다.
- Capability Cliff의 존재와 메커니즘(multi-step chain에서의 오류 증폭)을 이해하고, "이 양자화 모델로 이 task는 된다"를 판단하는 근거를 갖는다.
- 모델 변수가 1차 병목이 되는 조건과, Agent-Relevant Capability Composite가 cliff 이상일 때 1차 병목이 harness 또는 compute로 이동하는 조건을 구분할 수 있다.

## 집필 노트

- 관련 DR: DR-2.1 (agent 벤치마크), DR-2.2 (OpenRouter routing), DR-2.3 (distillation/quantization)
- 관련 실험: E01 (Capability Cliff — ARCC × task type × TCR), E02 (frontier vs. distilled), E03 (mid-run model switching), E10 (model capability floor for self-monitoring)
- 관련 Figure: Fig 1 (Capability Cliff scatter + sigmoid fit), Fig 1b (Quantization Tax Curve), Fig 1c (Distillation Efficiency Frontier)

**ARCC 정의 (조작적):**
- TCA (Tool Call Accuracy): 전체 tool call 중 schema-valid이고 semantically-correct한 비율
- IFR (Instruction Following Rate): 주어진 instruction의 명시적 constraint를 모두 충족한 output 비율
- MSRD_n (Multi-Step Reasoning Depth): n-step chain 완료 시 논리적 오류 없이 유지된 단계 수 / n
- CUE (Context Utilization Efficiency): relevant context proportion 변화가 output quality에 미치는 영향
- ARCC = weighted composite. weights는 task type별로 다르며 sensitivity analysis가 필수.

**ARCC Construct Validation:**
- holdout task set에서 TCR을 예측하는 R² ≥ 0.65이어야 ARCC를 유효한 predictor로 사용.
- R² < 0.65이면 weight 재조정 또는 이 챕터의 주요 주장을 잠정적으로 표시.
- Validation이 실패할 경우의 처리 방식도 사전에 기록 (`experiments/design-specification.md` §2).

**Capability Cliff 메커니즘 (mechanism-first):**
- 왜 급락인가: 각 sub-task가 이전 sub-task의 출력에 의존하는 구조에서, 초기 오류가 증폭된다.
- ARCC가 낮은 모델은 단일 단계는 통과하더라도 multi-step chain에서 오류 누적이 임계점을 초과한다.
- Sigmoid fit이 이 non-linearity를 포착한다. Piecewise linear vs. sigmoid: AIC 비교로 결정.

**예상 반박 대비:**
- "벤치마크가 agent capability proxy로 부족하다는 것은 알려진 사실": ARCC는 agent-specific composite이며, 기존 벤치마크가 포착하지 못하는 차원(tool call accuracy, multi-step)을 명시적으로 포함한다. 이것이 측정 기여다.
- "Cliff가 아니라 측정 노이즈": 95% CI band를 그리고, cliff position의 신뢰구간을 보고한다. CI가 좁으면 cliff가 신호다.
- "양자화 방법마다 다른데 뭘 비교하는가": 양자화 방법을 통제변수가 아닌 독립변수로 취급. 같은 bit-width에서 방법 간 TCR 차이가 유의하면 그 자체가 발견이다.

**스냅샷 마커:** "2026년 3월 기준으로 측정한 모델별 ARCC 분포와 cliff position"

---

## Outline

> 개정 2026-03-27: 서사 구조 재편 — 리뷰 논문 스타일로 시작, Agent-Relevant Capability Composite는 §4에서 등장
> 이전 §1 내용 → §3으로 이동. 이전 §2 내용 → §4로 이동.

**계획된 섹션:**

1. **[신규] LLM 평가의 역사 — MMLU에서 AgentBench까지**
   - MMLU(2021): 지식 범위 측정의 시작, 그리고 한계
   - HumanEval(2021): 코드 생성 품질 — 단일 함수 수준에서의 측정
   - BIG-Bench(2022): 다양성 확장, 그러나 여전히 단일 호출 기준
   - SWE-bench(2023): 실제 GitHub 이슈 해결 — agent-adjacent 평가의 등장
   - AgentBench / WebArena / GAIA(2024~2025): multi-step, 도구 사용, long-horizon 평가
   - 각 세대가 등장한 이유 — 이전 기준이 포착하지 못한 것이 무엇이었는가

2. **[신규] Agent 운용 관점의 측정 공백**
   - 기존 agent 벤치마크가 운영 현장과 다른 점: 실험실 조건 vs. 실제 배포 조건
   - Multi-step chain에서 오류가 누적되는 방식이 측정에 포착되지 않는 이유
   - 연속 도구 호출, 맥락 유지, 자원 제약 — 기존 지표가 놓치는 세 차원
   - 이 공백이 실무에서 어떻게 드러나는가: 벤치마크 점수 높은 모델의 운용 실패 패턴

3. **물려받는 경향: reasoning, tool use, consistency, confidence** *(이전 §1)*
   - 모델이 agent runtime에 도입하는 네 가지 행동 성향의 성격
   - 왜 이 네 가지가 서로 다른 task 유형에서 다르게 작동하는가
   - 확률 분포의 차이가 multi-step에서 어떻게 증폭되는가

4. **Agent-Relevant Capability Composite — 운용 관점의 측정 방법** *(이전 §2)*
   - 네 차원의 설계 근거: Tool Call Accuracy, Instruction Following Rate, Multi-Step Reasoning Depth, Context Utilization Efficiency
   - 복합 가중치 결정 원리와 민감도 분석
   - Construct validation: holdout R² ≥ 0.65 기준과 그 기준의 의미
   - 기존 벤치마크(SWE-bench, AgentBench)와의 관계 — 대체가 아닌 보완

5. **Capability Cliff — 비선형 급락이 발생하는 조건**
   - E01 실험 설계: scatter plot × task type × Task Completion Rate (harness-off 조건)
   - Task-conditional sigmoid fit: T1(Code Review), T2(Multi-Step), T3(Long-Horizon)에서 cliff position이 다른 이유
   - Agent-Viable Minimum: task별 최소 임계값의 실무적 의미
   - 예상 반박: cliff가 아니라 측정 노이즈일 수 있다 — 95% CI와 AIC 비교로 검증

6. **양자화 비용 곡선 — 같은 base model, 다른 bit-width**
   - FP16 → Q8 → Q6 → Q4 → Q3 → Q2 경로에서 성능이 감소하는 비율
   - Model family마다 양자화 비용이 다른 이유
   - 어느 bit-width에서 cliff를 건너게 되는가 (task별로 다른 답)

7. **Distillation Efficiency Frontier — 같은 parameter budget, 다른 전략**
   - Distillation vs. 양자화: 동일 parameter budget에서 agent 운용 관점의 효율성 비교
   - Pareto frontier 존재 여부
   - 학습 domain 외 task에서의 일반화 한계

8. **실행 중 모델 교체의 맥락 연속성 문제 (E03)**
   - 실행 도중 모델을 교체하면 무슨 일이 벌어지는가
   - Context state의 암묵적 가정이 모델 교체 시 어떻게 위반되는가
   - 운영 처방: 언제 교체가 허용 가능하고, 언제 전체 재시작이 필요한가

9. **모델 변수가 1차 병목이 되는 조건**
   - Agent-Relevant Capability Composite가 cliff 이하인 경우에만 모델이 1차 병목이다
   - cliff 이상일 때 1차 병목은 harness 또는 compute로 이동한다 (Ch.3/Ch.4 예고)
   - E10: self-monitoring을 위한 model capability floor — Agent-2 전환의 하한 조건 (Ch.7 예고)

---

**핵심 Figure:**

- **Fig 1** — Agent Capability Cliff: ARCC scatter plot + task-conditional sigmoid fit + 95% CI band. Cliff position per task type. Harness-off 조건 기준. (E01 확장)
- **Fig 1b** — Quantization Tax Curve: 동일 base model 4종 × 5단계 bit-width → ARCC 변화 경로. Model family별 cliff crossing point 표시.
- **Fig 1c** — Distillation Efficiency Frontier: 동일 parameter budget에서 distill vs. quantize의 ARCC 비교. Pareto frontier 표시.

<!-- 섹션별 초고는 /draft ch02 N 으로 작성 -->

## 참조

- `deep-research/DR-2.1-agent-benchmarks.md`
- `deep-research/DR-2.2-openrouter-routing.md`
- `deep-research/DR-2.3-distillation-tool-use.md`
- `experiments/design-specification.md` — §1 (Task specification T1/T2/T3), §2 (ARCC composite), §4 (Statistical analysis plan)
- `experiments/figure_expansion.md` — Figure 1 재설계 (Capability Cliff, Quantization Tax, Distillation Frontier)
- `experiments/framework/arcc.py`
- `experiments/framework/metrics.py`
- `experiments/framework/ground_truth.py`
