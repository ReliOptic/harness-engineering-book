# Ch.3 — 정렬에서 자율로: 모델은 어떻게 행동을 배우는가

> **Part I — 기반: Agent를 만든 논문들**

**한 줄**: RLHF에서 Constitutional AI까지의 계보를 따라, 모델이 행동을 학습하는 메커니즘을 이해하고, 학습 단계의 정렬이 왜 runtime 문제를 해결하지 못하는지를 규명한다.

**Backbone 논문**:
- Ouyang et al., *Training Language Models to Follow Instructions with Human Feedback* (InstructGPT, NeurIPS 2022, ~18,000 citations)
- Lee et al., *RLAIF: Scaling Reinforcement Learning from Human Feedback with AI Feedback* (2023)
- Bai et al., *Constitutional AI: Harmlessness from AI Feedback* (Anthropic, 2022, ~3,000 citations)

**이 챕터가 도입하는 개념**: supervised fine-tuning, reward model, PPO, preference data, RLHF cost structure, AI feedback scaling, self-critique loop, constitution

**챕터 종료 시 독자 상태**: "모델이 aligned되었는데 왜 agent가 여전히 실패하는가"를 학습-runtime 경계의 구조적 차이로 설명할 수 있다. Constitutional AI의 self-critique가 Ch.11 self-immune의 이론적 선행 좌표임을 이해한다.

---

## §1. 모델에게 지시를 따르게 가르치기 — InstructGPT와 RLHF

**직관 앵커**: 신입 사원에게 피드백을 주면서 가르치는 것. "이 답이 좋다/나쁘다"를 반복하면 사원의 행동이 바뀐다. RLHF는 이 과정의 수학적 형식화다.

**정밀 정의**:
- 3단계: SFT(시범 보이기) → Reward Model 학습(선호 판단 학습) → PPO(보상 최대화 학습)
- 비용 구조: 인간 평가자가 병목. 수만 건의 comparison data 필요.

**운영 번역**: RLHF로 학습된 모델은 "평균적으로 좋은 응답"을 생성하지만, 특정 task의 특정 constraint를 일관되게 따르는 것은 학습하지 않았다. 이것이 runtime에서 instruction following rate가 task마다 다른 이유의 한 원천이다.

**탐구 질문**: RLHF의 reward model이 포착하지 못하는 task-specific constraint는 어떤 종류인가? 이 gap이 harness의 존재 이유와 어떻게 연결되는가?

<!-- TODO: 본문 집필 -->

---

## §2. 인간 없이 스케일하기 — RLAIF

**직관 앵커**: 신입 사원 교육에 선배 사원을 투입한다. 팀장이 모든 피드백을 줄 필요 없이, 선배가 대신 판단하면 스케일이 늘어난다.

**정밀 정의**: AI가 preference를 생성 → reward model 학습. Lee et al.의 핵심 발견: RLAIF와 RLHF의 성능이 거의 동등.

**운영 번역**: 학습 비용 하락의 기술적 메커니즘. 모델 품질이 빠르게 향상되는 이유. 그러나 품질 향상이 runtime 안정성을 보장하지 않는 구조적 이유는 §4에서.

**탐구 질문**: RLAIF가 RLHF와 동등한 성능을 달성한다면, AI feedback의 편향이 agent runtime에서 새로운 형태의 실패를 만들 가능성은 없는가?

<!-- TODO: 본문 집필 -->

---

## §3. 스스로 교정하기 — Constitutional AI

**직관 앵커**: 규칙집을 받은 사원이 자기 답을 스스로 검토하고 수정한다. 외부 감독자 없이 내부 비평 루프를 운영하는 것.

**정밀 정의**:
- Constitution = 원칙 목록. 모델이 자기 출력을 constitution 기준으로 평가하고 수정.
- 학습 단계의 self-critique: 출력 생성 → 자기 비평 → 수정 → 수정된 데이터로 재학습

**운영 번역**:
- Constitutional AI는 **학습 단계**의 자기 교정이다. 한 번 학습이 끝나면 루프가 멈춘다.
- Ch.11의 self-immune은 **런타임 단계**의 자기 교정이다. 실행 중에 루프가 계속 돌아간다.
- 이 둘은 같은 계보에 있지만 동일하지 않다. 이 구분선이 학습과 운영의 경계다.

**탐구 질문**: Constitutional AI의 constitution이 학습 시점에 고정된다는 사실이, runtime에서 변화하는 조건에 대응하지 못하는 구조적 한계를 만드는가?

<!-- TODO: 본문 집필 -->

---

## §4. 학습 정렬이 Runtime 문제를 풀지 못하는 구조적 이유

**이 섹션은 Part I과 Part II를 연결하는 다리다.**

학습 단계에서 해결하는 것:
- 평균적인 응답 품질 향상
- 명시적 유해 출력 감소
- 일반적 instruction following 향상

학습 단계에서 해결하지 않는 것:
- 특정 task의 특정 constraint를 40 step 동안 유지하는 것 (→ instruction following rate decay, Ch.6)
- Context가 오염된 상태에서 올바른 판단을 내리는 것 (→ context contamination, Ch.8)
- 자신의 능력 한계를 실시간으로 감지하는 것 (→ self-monitoring, Ch.11)
- Token budget이 소진되는 상황에서 graceful degradation (→ compute 변수, Ch.8)

**Callout**: "Aligned model ≠ reliable agent. 학습이 해결하는 것은 '평균적으로 좋은 행동'이고, 운영이 해결해야 하는 것은 '이 순간, 이 조건에서, 이 task를 완수하는 행동'이다. 그 간극에 harness가 있다."

**탐구 질문**: 학습-runtime 경계에서 발생하는 gap을 정량적으로 측정할 수 있는가? 이 gap의 크기가 모델 세대에 따라 줄어드는가, 성격이 바뀌는가?

<!-- TODO: 본문 집필 -->
