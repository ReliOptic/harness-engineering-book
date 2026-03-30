# List of Contents v6

> **상태**: 집필 방향 재설정안 (2026-03-30)
> **변경 사유**: 핵심 논문들을 각 소주제의 backbone으로 세우고, 논문을 이해하기 위한 개념까지 포괄하는 구조로 확장
> **참조 모델**: `compression lens 챕터 -learning curve reference.docx` — 3단계 학습 곡선(직관 앵커 → 정밀 정의 → 운영 번역)의 모범 구현
> **적용 원칙**: `editorial-learning-curve-guideline.md` — 모든 챕터에 동일한 교육 설계 구조 적용

---

## 구조 전환의 논리

v4까지의 구조는 실험서로서의 정체성을 중심에 두었다. v6는 그 실험서의 앞에 **역사적 계보 챕터**를 배치한다. 이 책은 더 이상 순수 실험서가 아니라, **권위 있는 논문들을 역사적 좌표로 배열한 뒤, 그것이 왜 오늘의 runtime 실패와 연결되는지를 실험으로 다시 묻는 책**이다. Part I은 논문 서베이가 아니라 계보이고, Part II~IV는 그 계보를 현재 조건에서 검증하는 장이다. 10년 뒤에 AI agent를 처음 설계해야 하는 학생이 이 책을 펼쳤을 때, Part I이 역사적 배경을 제공하고 Part II~IV가 2026년의 실험 기록을 제공하는 구조다.

이유는 세 가지다.

첫째, 현재 원고의 핵심 개념들(Capability Cliff, Failure Budget Reallocation, Self-immune, 모델 관찰 지표)은 정보이론, attention 메커니즘, alignment 계보, tool use 연구 위에 서 있으나, 그 기반이 본문에서 암묵적으로 전제되어 있다. 독자가 이 전제를 공유하지 않으면 Ch.5 이후의 실험 해석이 부유한다.

둘째, compression lens 챕터가 증명한 것은 **논문 하나를 backbone으로 삼아 prerequisite 개념부터 agent operations 번역까지 한 챕터 안에서 완결하는 구조**가 실무서의 속도를 유지하면서도 개념적 기반을 확보할 수 있다는 점이다. 이 패턴을 핵심 논문 4편에 확장한다.

셋째, learning curve guideline의 3단계 구조(직관 앵커 → 정밀 정의 → 운영 번역)가 Part I의 각 챕터를 관통하면, Part II 이후에서는 재정의보다 현장 정당화에 집중할 수 있다. Part I에서 확립된 개념은 Part II 이후에서 한 문장 재도입 후, 현장 관찰과 연결하는 것으로 충분해진다.

---

## 전체 구조

```
Preface   왜 이 책이 필요한가

Part I — 기반: Agent를 만든 논문들
  Ch.1    Attention과 Context: 모델은 어떻게 보는가
  Ch.2    압축 렌즈: 모든 언어 모델은 압축기다
  Ch.3    정렬에서 자율로: 모델은 어떻게 행동을 배우는가
  Ch.4    도구, 추론, 기억: Agent는 어떻게 행동하는가

Part II — 프레임워크: 관찰과 측정
  Ch.5    지금 무슨 일이 일어나고 있는가
  Ch.6    Agent가 모델로부터 무엇을 물려받는가
  Ch.7    Harness Engineering과 AgentOps

Part III — 실험: 의도적 실패
  Ch.8    22개 시나리오
  Ch.9    실험이 보여준 것

Part IV — 진화: 관찰에서 시스템으로
  Ch.10   Operational Compiler
  Ch.11   Self-Immune System: Harness에서 Agent로

Appendices
```

**v4 → v6 구조 변경 요약**:
- Part I (4챕터) 신설: 핵심 논문 backbone + prerequisite 개념 + agent operations 번역
- v4의 Part I "Agent Runtime의 현장" (Ch.1-3) → v6 Part II (Ch.5-7)로 재배치. Part I 기반 위에서 더 가벼워짐
- v4의 Ch.2 "Agent의 작동 원리와 실패 구조" → Part I Ch.4에서 논문 기반으로 흡수
- v4의 Ch.3 "5변수 프레임워크" → v6 Ch.5에 통합 (Part I 기반이 있으므로 별도 챕터 불필요)
- 총 11챕터 + Preface + Appendices

---

## Preface — 왜 이 책이 필요한가

v5 초고 유지. 단, 마지막 문장("이정표를 얻게 될 것이다") 재작성 — voice rule 위반.

**수정 방향**: 독자에게 약속하는 문장 대신, 이 책이 다루는 질문의 경계를 명시하는 문장으로 교체.

---

# Part I — 기반: Agent를 만든 논문들

> **Part I의 원칙**: 각 챕터는 1~2편의 핵심 논문을 backbone으로 삼는다. 논문을 이해하기 위해 필요한 개념을 3단계 학습 곡선(직관 앵커 → 정밀 정의 → 운영 번역)으로 도입하고, 마지막 섹션에서 반드시 agent operations 실무로 번역한다. compression lens 챕터가 이 패턴의 참조 구현이다.

> **Part I과 Part II의 관계**: Part I은 "왜 이런 일이 일어나는가"의 이론적 기반이고, Part II는 "지금 현장에서 무슨 일이 일어나고 있는가"의 관찰 기록이다. Part I 없이 Part II를 읽을 수 있지만, Part I을 거치면 Part II의 관찰이 메커니즘으로 연결된다.

---

## Ch.1 — Attention과 Context: 모델은 어떻게 보는가

**한 줄**: Transformer의 attention 메커니즘이 정보를 처리하는 방식을 이해하고, 그 구조적 한계가 agent runtime에서 어떤 실패로 나타나는지를 연결한다.

**Backbone 논문**:
- Vaswani et al., *Attention Is All You Need* (NeurIPS 2017, ~140,000 citations)
- Liu et al., *Lost in the Middle: How Language Models Use Long Contexts* (TACL 2024, ~1,500 citations)

**이 챕터가 도입하는 개념**: embedding, dot product similarity, softmax, K-Q-V mechanism, multi-head attention, positional encoding, U-shaped attention curve

**챕터 종료 시 독자 상태**: "왜 context window를 늘려도 agent가 중간 정보를 놓치는가"를 attention 메커니즘으로 설명할 수 있다.

### §1. 단어가 숫자가 되는 순간 — embedding과 벡터 공간

**직관 앵커**: "왕 - 남자 + 여자 = 여왕"이라는 유명한 예시. 단어가 숫자 벡터가 되면 의미의 산술이 가능해진다.
**정밀 정의**: embedding, 벡터 공간, 차원, dot product similarity, cosine similarity
**운영 번역**: agent가 tool description을 "이해"하는 것은 embedding 공간에서의 유사도 계산이다. 유사한 tool description이 혼동을 만드는 구조적 이유.

### §2. 주의를 기울인다는 것 — Attention 메커니즘의 해부

**직관 앵커**: 시끄러운 파티에서 자기 이름이 불리면 들린다. 모든 소리를 동일하게 처리하는 것이 아니라, 관련 있는 정보에 가중치를 부여하는 것이 attention이다.
**정밀 정의**: Query-Key-Value, attention score = softmax(QK^T / √d_k), weighted sum of Values
**운영 번역**: agent가 context window에서 "어떤 정보에 주의를 기울이는가"는 Q와 K의 dot product가 결정한다. 이것이 확률적이라는 사실이 agent 출력의 비결정성의 한 원천이다.

### §3. 여러 관점으로 동시에 보기 — Multi-Head Attention

**직관 앵커**: 같은 문서를 법무팀과 재무팀이 다르게 읽는다. Multi-head attention은 동일한 입력을 여러 관점에서 동시에 분석한다.
**정밀 정의**: head 분할, 독립적 Q/K/V projection, concatenation + linear projection
**운영 번역**: head 수가 많을수록 양자화 저항성이 높아지는 경향 — Ch.6 Quantization Tax Curve의 배경.

### §4. 순서를 기억하는 방법 — Positional Encoding

**직관 앵커**: "개가 사람을 물었다"와 "사람이 개를 물었다" — 같은 단어, 다른 순서, 다른 의미.
**정밀 정의**: sinusoidal positional encoding, 상대적 위치 표현, RoPE
**운영 번역**: positional encoding의 한계가 long context에서 위치 편향을 만든다. 이것이 §5의 Lost in the Middle 현상으로 이어진다.

### §5. 긴 입력에서 무엇이 사라지는가 — Lost in the Middle

**직관 앵커**: 20페이지 보고서를 읽을 때, 첫 페이지와 마지막 페이지는 기억하지만 중간은 흐릿해진다.
**정밀 정의**: Liu et al.의 실험 — 문서를 입력 위치별로 배치했을 때 정보 활용도의 U-shaped curve. 중간 위치 정보의 활용도가 시작/끝 대비 현저히 낮다.
**운영 번역**:
- Context window를 늘리는 것이 만능이 아닌 이유: "Right Context > Big Context"
- Agent의 context 활용 효율이 context 길이에 따라 비선형적으로 감소하는 메커니즘
- Ch.6에서 관찰하는 context 활용 효율 지표가 이 현상을 포착한다

### §6. Agent Operations를 위한 시사점

**이 섹션은 Stage 3(운영 번역)의 종합이다.**

- **Context window = attention capacity**: 토큰 수가 아니라, 모델이 실제로 활용할 수 있는 정보량이 진정한 한계
- **Attention 오배분 → Hallucination 경로**: K-Q-V에서 Query가 잘못된 Key에 높은 점수를 부여하면, 관련 없는 Value가 출력에 혼입된다. 이것이 tool call hallucination의 구조적 기원 중 하나
- **System prompt 설계 원칙**: 중요한 instruction은 context의 시작과 끝에 배치한다 (Lost in the Middle 대응)
- **Ch.6 연결**: 도구 사용 정확도의 semantic 차원, context 활용 효율의 측정 근거가 이 챕터에서 확립된다

**Callout**: "Context window 128K는 128K 토큰을 '이해'한다는 뜻이 아니다. Attention이 실제로 활용하는 정보량은 위치와 관련성에 따라 비선형적으로 감소한다."

---

## Ch.2 — 압축 렌즈: 모든 언어 모델은 압축기다

**한 줄**: 언어 모델이 확률적 텍스트 생성기인 동시에 압축 알고리즘이라는 사실을 정보이론으로 보이고, 이 등가성이 agent runtime 현상을 읽는 하나의 해석 렌즈가 됨을 보여준다. 이 챕터는 HOR이나 모델 관찰 지표의 직접 근거를 세우는 것이 아니라, Part II 이후에서 사용할 정보이론적 어휘를 제공한다.

**Backbone 논문**:
- Delétang et al., *Language Modeling Is Compression* (ICLR 2024)
- Shannon, *A Mathematical Theory of Communication* (1948)

**이 챕터가 도입하는 개념**: information content, entropy, cross-entropy, KL divergence, arithmetic coding, autoregressive chain rule, bits-per-byte, compression ratio

**챕터 종료 시 독자 상태**: "왜 더 좋은 모델이 더 잘 압축하는가"를 수식으로 설명할 수 있고, 이것을 prompt 최적화와 모델 비교에 적용할 수 있다.

> **참조 구현**: `compression lens 챕터 -learning curve reference.docx`의 한국어 적응 + 확장. 영어 원고의 7개 섹션 구조를 유지하되, 한국어 voice rule 적용 및 이 책의 5변수 프레임워크와의 연결을 강화한다.

### §1. 정보량: 놀라움을 측정하는 방법

**직관 앵커**: "오늘 아침 해가 떴다" vs. "7월 서울에 3미터 눈이 내렸다" — 놀라운 사건이 더 많은 정보를 담는다.
**정밀 정의**: I(x) = −log₂(p), bit 단위, Shannon의 세 가지 필요조건(연속, 단조, 가법성)
**운영 번역**: 모델이 다음 토큰을 95% 확신으로 예측하면 ~0.07 bits, 1% 확신이면 ~6.6 bits. 예측 능력이 곧 비용이다.

### §2. 엔트로피: 놀라움의 평균 비용

**직관 앵커**: 공정한 동전 vs. 편향된 동전(앞면 90%). 편향된 동전은 예측 가능하므로 기록에 필요한 비트가 적다.
**정밀 정의**: H(P) = −Σ p(x) · log₂ p(x), Shannon의 소스 코딩 정리 — 엔트로피가 압축의 이론적 하한
**운영 번역**: 모델의 엔트로피가 낮다 = 예측이 정확하다 = 데이터가 잘 압축된다. Temperature가 이 엔트로피를 조절하는 운영 파라미터.

### §3. Cross-Entropy와 KL Divergence: 틀린 모델의 대가

**직관 앵커**: 편향된 동전(90:10)을 공정한 동전이라고 가정하면 기록에 0.53 bits/flip을 낭비한다. 이 낭비가 "모델이 틀린 정도"다.
**정밀 정의**: H(P,Q) = −Σ p(x) · log₂ q(x), D_KL(P‖Q) = H(P,Q) − H(P)
- Cross-entropy = 진짜 엔트로피 + 모델 오차에 대한 벌금
- 학습 loss = cross-entropy loss. 학습 = cross-entropy 최소화 = KL divergence 최소화
**운영 번역**: prompt drift를 KL divergence의 언어로 읽을 수 있다 — 의도한 행동 분포와 실제 출력 분포 사이의 괴리를 정보량으로 표현하는 하나의 방법.

### §4. Arithmetic Coding: 확률이 압축된 파일이 되는 과정

**직관 앵커**: 숫자 선 [0, 1)을 확률에 비례하여 쪼개는 과정. 높은 확률의 토큰은 넓은 구간 = 적은 비트, 낮은 확률의 토큰은 좁은 구간 = 많은 비트.
**정밀 정의**: interval narrowing, 압축 크기 ≈ cross-entropy
**운영 번역**: 좋은 예측 = 좋은 압축. 이 등가성이 모델 비교의 보편 척도를 제공한다.

### §5. Autoregressive 구조: 언어 모델은 태생적 압축기다

**정밀 정의**: P(x_t | x_1,...,x_{t-1}), chain rule, arithmetic coding과의 구조적 동일성
- 생성(generation)과 압축(compression)은 같은 연산의 다른 사용
- 생성: 분포에서 sampling → 새 텍스트 생성
- 압축: 실제 토큰의 bit cost 기록 → 기존 텍스트 인코딩
**운영 번역**: 토큰별 bit cost가 균일하지 않다. "The capital of France is Paris"에서 "Paris"는 ~0.1 bits, "The"는 ~8 bits. 예측 가능한 토큰은 거의 무료.

### §6. Bits-per-Byte: 모델을 비교하는 보편 척도

**정밀 정의**: bits-per-byte = 압축 후 총 비트 ÷ 원본 바이트 수. Tokenizer에 무관한 비교 가능.
- Compression ratio = 압축 크기 ÷ 원본 크기. Black-box 모델에도 적용 가능.
- 두 척도의 관계: bits-per-byte ≈ 8 × compression ratio
**운영 번역**: 어떤 모델이 더 나은가의 보편 답: 더 잘 압축하는 모델이 더 나은 모델이다.

### §7. Agent Operations를 위한 시사점

**종합 운영 번역 (compression lens 챕터 Section 7 한국어 적응)**:

| 개념 | Agent Operations 번역 |
|------|----------------------|
| Context window | Bit budget — 정보량의 상한 |
| Temperature | 엔트로피 조절기 — 낮으면 예측 가능, 높으면 다양 |
| Prompt 최적화 | Cross-entropy 최소화 — 동일 의미를 더 적은 비트로 |
| CLAUDE.md | Lossy compression artifact — 프로젝트 전체를 수백 줄로 |
| Prompt drift | KL divergence 증가 — 의도와 실제의 괴리 |
| 모델 비교 | Bits-per-byte — tokenizer 무관 보편 척도 |

**Callout**: "Prompt를 줄였는데 성공률이 유지되었다면, 제거된 토큰은 0-bit 정보를 담고 있었다. 줄였는데 실패했다면, 제거된 토큰에 대체 불가능한 신호가 있었다."

**Ch.6 연결**: Ch.6의 모델 관찰 지표(도구 사용 정확도, instruction following rate, multi-step reasoning depth, context 활용 효율)는 이 챕터의 정보이론적 어휘로 읽을 수 있다. Cross-entropy와 bit cost의 프레임은 이 지표들을 해석하는 하나의 렌즈이지, 지표의 정의 자체를 도출하는 근거는 아니다.

---

## Ch.3 — 정렬에서 자율로: 모델은 어떻게 행동을 배우는가

**한 줄**: RLHF에서 Constitutional AI까지의 계보를 따라, 모델이 행동을 학습하는 메커니즘을 이해하고, 학습 단계의 정렬이 왜 runtime 문제를 해결하지 못하는지를 규명한다.

**Backbone 논문**:
- Ouyang et al., *Training Language Models to Follow Instructions with Human Feedback* (InstructGPT, NeurIPS 2022, ~18,000 citations)
- Lee et al., *RLAIF: Scaling Reinforcement Learning from Human Feedback with AI Feedback* (2023)
- Bai et al., *Constitutional AI: Harmlessness from AI Feedback* (Anthropic, 2022, ~3,000 citations)

**이 챕터가 도입하는 개념**: supervised fine-tuning, reward model, PPO, preference data, RLHF cost structure, AI feedback scaling, self-critique loop, constitution

**챕터 종료 시 독자 상태**: "모델이 aligned되었는데 왜 agent가 여전히 실패하는가"를 학습-runtime 경계의 구조적 차이로 설명할 수 있다. Constitutional AI의 self-critique가 Ch.11 self-immune의 이론적 선행 좌표임을 이해한다.

### §1. 모델에게 지시를 따르게 가르치기 — InstructGPT와 RLHF

**직관 앵커**: 신입 사원에게 피드백을 주면서 가르치는 것. "이 답이 좋다/나쁘다"를 반복하면 사원의 행동이 바뀐다. RLHF는 이 과정의 수학적 형식화다.
**정밀 정의**:
- 3단계: SFT(시범 보이기) → Reward Model 학습(선호 판단 학습) → PPO(보상 최대화 학습)
- 비용 구조: 인간 평가자가 병목. 수만 건의 comparison data 필요.
**운영 번역**: RLHF로 학습된 모델은 "평균적으로 좋은 응답"을 생성하지만, 특정 task의 특정 constraint를 일관되게 따르는 것은 학습하지 않았다. 이것이 runtime에서 instruction following rate가 task마다 다른 이유의 한 원천이다.

### §2. 인간 없이 스케일하기 — RLAIF

**직관 앵커**: 신입 사원 교육에 선배 사원을 투입한다. 팀장이 모든 피드백을 줄 필요 없이, 선배가 대신 판단하면 스케일이 늘어난다.
**정밀 정의**: AI가 preference를 생성 → reward model 학습. Lee et al.의 핵심 발견: RLAIF와 RLHF의 성능이 거의 동등.
**운영 번역**: 학습 비용 하락의 기술적 메커니즘. 모델 품질이 빠르게 향상되는 이유. 그러나 품질 향상이 runtime 안정성을 보장하지 않는 구조적 이유는 §4에서.

### §3. 스스로 교정하기 — Constitutional AI

**직관 앵커**: 규칙집을 받은 사원이 자기 답을 스스로 검토하고 수정한다. 외부 감독자 없이 내부 비평 루프를 운영하는 것.
**정밀 정의**:
- Constitution = 원칙 목록. 모델이 자기 출력을 constitution 기준으로 평가하고 수정.
- 학습 단계의 self-critique: 출력 생성 → 자기 비평 → 수정 → 수정된 데이터로 재학습
**운영 번역**:
- Constitutional AI는 **학습 단계**의 자기 교정이다. 한 번 학습이 끝나면 루프가 멈춘다.
- Ch.11의 self-immune은 **런타임 단계**의 자기 교정이다. 실행 중에 루프가 계속 돌아간다.
- 이 둘은 같은 계보에 있지만 동일하지 않다. 이 구분선이 학습과 운영의 경계다.

### §4. 학습 정렬이 Runtime 문제를 풀지 못하는 구조적 이유

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

---

## Ch.4 — 도구, 추론, 기억: Agent는 어떻게 행동하는가

**한 줄**: Agent의 세 가지 핵심 능력 — 도구 사용, 추론-행동 통합, 자기 성찰과 기억 — 의 학술적 기원을 이해하고, 각 능력이 runtime에서 어떻게 실패하는지를 연결한다.

**Backbone 논문**:
- Schick et al., *Toolformer: Language Models Can Teach Themselves to Use Tools* (NeurIPS 2023, ~2,600 citations)
- Yao et al., *ReAct: Synergizing Reasoning and Acting in Language Models* (ICLR 2023, ~5,250 citations)
- Shinn et al., *Reflexion: Language Agents with Verbal Reinforcement Learning* (NeurIPS 2023, ~1,400 citations)

**Companion**:
- Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* (NeurIPS 2020, ~7,000 citations)

**이 챕터가 도입하는 개념**: function calling, tool schema, chain-of-thought, reasoning-acting loop, verbal reinforcement, self-reflection, retrieval-augmented generation, episodic memory

**챕터 종료 시 독자 상태**: 도구 사용 정확도, instruction following rate, multi-step reasoning depth의 측정이 왜 필요한지를 각 능력의 실패 메커니즘으로 설명할 수 있다. Reflexion이 Ch.11 self-immune의 선행 좌표임을 이해한다.

### §1. 도구를 사용하는 법을 스스로 배우기 — Toolformer

**직관 앵커**: 계산기를 쓸 줄 아는 사람과 암산만 고집하는 사람. 도구를 쓸 줄 아는 것이 능력이다 — 하지만 잘못된 도구를 쓰는 것은 능력이 아니라 위험이다.
**정밀 정의**:
- 모델이 학습 데이터에서 "여기서 도구를 호출하면 좋겠다"를 스스로 판단하고, 도구 호출을 삽입하여 학습
- API call의 구조: function name, parameters, return value
- Schema validity (구조 통과)와 semantic correctness (의미 정확)의 구분
**운영 번역**:
- 도구 사용 정확도(tool call accuracy)는 이 구분을 포착한다. Schema를 통과하면서 의미적으로 틀린 호출이 가장 위험하다 — harness가 통과 신호를 보내지만 결과는 틀린 상태.
- Ch.6의 도구 사용 정확도 지표가 이 현상을 측정한다.

### §2. 생각하면서 행동하기 — ReAct

**직관 앵커**: 요리할 때 "냉장고를 열어보니 달걀이 있다(관찰) → 오믈렛을 만들자(생각) → 달걀을 꺼낸다(행동)"의 루프. 생각 없이 행동하면 엉뚱한 요리가 되고, 행동 없이 생각만 하면 음식이 나오지 않는다.
**정밀 정의**:
- Thought-Action-Observation 루프. 매 단계에서 reasoning trace를 명시적으로 생성한 후 행동.
- Chain-of-thought만으로는 부족한 이유: 행동의 결과를 관찰하지 않으면 reasoning이 현실과 괴리된다.
- ReAct의 핵심 발견: reasoning과 acting을 interleave하면 hallucination이 감소한다.
**운영 번역**:
- Multi-step task에서 agent가 각 단계의 결과를 관찰하고 다음 추론에 반영하는 것이 multi-step reasoning depth 측정의 기반이다.
- Reasoning trace가 context를 소비한다 — HOR(Harness Overhead Ratio)과 동일한 trade-off. 추론의 깊이와 token 효율 사이의 긴장.

### §3. 실패에서 배우기 — Reflexion

**직관 앵커**: 시험을 보고 오답노트를 쓰는 학생. 같은 실수를 반복하지 않으려면 실패를 기록하고 다음 시도에 반영해야 한다.
**정밀 정의**:
- Verbal reinforcement learning: 수치 보상 대신 언어적 피드백으로 행동 수정
- 3단계 루프: Actor(행동) → Evaluator(평가) → Self-Reflection(언어적 피드백 생성) → 다음 시도에 반영
- 핵심 발견: episodic memory에 과거 실패와 자기 피드백을 저장하면 재시도 성공률이 유의하게 향상
**운영 번역**:
- Reflexion은 **task 간** self-reflection이다. 한 task를 실패하고 다음 시도에서 개선한다.
- Ch.11의 self-immune은 **task 내** self-monitoring이다. 실행 도중에 자신의 상태를 감지한다.
- Reflexion이 task 간 학습이라면, self-immune은 task 내 면역이다. 시간 스케일이 다르다.

**Callout**: "Reflexion이 보여준 것은 '실패를 기억하면 다음에 덜 실패한다'는 직관의 실증이다. 이 책의 self-immune system이 묻는 것은 '실패를 기억하는 것이 아니라, 실패하고 있는 중에 그것을 감지할 수 있는가'이다."

### §4. 외부 기억 장치 — RAG와 그 너머

**직관 앵커**: 오픈북 시험. 모든 것을 기억할 필요 없이, 필요할 때 정확한 자료를 찾아 참조하면 된다. 문제는 "정확한 자료"를 찾는 것 자체가 어렵다는 점이다.
**정밀 정의**:
- RAG: 질문 → 관련 문서 검색(retrieval) → 검색 결과와 질문을 합쳐 모델에 입력 → 생성
- Lewis et al.의 핵심 기여: retriever와 generator를 end-to-end로 학습
- 한계: 텍스트 유사도 기반 검색은 의미적 관련성을 놓칠 수 있다
**운영 번역**:
- 일반 RAG = 텍스트 유사도로 검색. Ontology RAG = 구조화된 스키마로 검증 후 편입.
- Ch.7에서 정의하는 memory structure (semantic firewall, schema validation)는 RAG의 한계를 보완하는 harness component다.
- Agent의 장기 실행에서 memory mutation이 발생할 때, 스키마 없는 RAG는 오염에 취약하다.

### §5. Agent Operations를 위한 시사점: 세 능력의 실패 지도

| 능력 | 학술 기원 | 실패 양상 | 측정 지표 |
|------|----------|----------|----------|
| 도구 사용 | Toolformer | Schema 통과 + 의미 오류 | 도구 사용 정확도 (Ch.6) |
| 추론-행동 통합 | ReAct | Reasoning trace와 현실의 괴리 | Multi-step reasoning depth (Ch.6) |
| 자기 성찰 | Reflexion | 과거 실패 미반영 / 잘못된 자기 평가 | Self-monitoring accuracy (Ch.11) |
| 외부 기억 | RAG | 관련 없는 문서 검색 / memory 오염 | Context 활용 효율 (Ch.6) |

Part I의 네 챕터가 제공하는 개념적 기반 위에서, Part II는 2026년 현장의 관찰을 기록하고 측정 체계를 구축한다.

---

# Part II — 프레임워크: 관찰과 측정

> **Part II의 원칙**: Part I이 역사적 계보를 깔았다면, Part II는 그 계보가 2026년 현장에서 어떤 모습으로 나타나는지를 관찰하고 측정하는 장이다. Part I에서 확립한 개념을 전제하되, 각 개념은 한 문장 재도입으로 충분하다(적층 원칙 §3.2). Part II의 관찰은 Part I의 메커니즘으로 해석 가능해야 하지만, Part I이 Part II를 결정하지는 않는다.

---

## Ch.5 — 왜 다섯 변수인가: 현장에서의 정당화

**한 줄**: Part I이 깔아둔 attention, compression, alignment, tool-use/memory라는 역사적 좌표가 현장의 agent runtime에서 왜 다섯 개 변수로 수렴하는지를 2026년 상반기 관찰로 정당화한다.

**이 챕터의 중심 질문**: "Attention, 압축, 정렬, 도구 사용이라는 네 갈래의 기술적 역사가 현장에서 부딪힐 때, 병목 분석의 최소 단위는 왜 모델·harness·surface·intervention·compute 다섯인가?"

**기반**: 현행 Ch.1 + v4 Ch.3의 5변수 프레임워크 + Agent-1~5 스펙트럼

**v4에서의 변경**: v4에서 Ch.1(생태계 스냅샷)과 Ch.3(5변수 프레임워크)으로 분리되어 있던 내용을 하나로 통합한다. Part I이 개념적 기반을 제공하므로 별도 챕터가 불필요해졌다. 이 챕터는 "생태계 소개"가 아니라 **"왜 5변수인가를 현장에서 정당화하는 장"**이다.

### §1. 2026년 상반기: agent가 깨지는 풍경

직관 앵커 소재: "어제까지 잘 돌던 agent가 오늘 깨졌다"
생태계 스냅샷은 이 질문의 배경으로 기능한다. 풍경 자체가 목적이 아니라, 이 풍경에서 반복적으로 관찰되는 실패 패턴이 왜 단일 변수로 설명되지 않는지를 보이는 것이 목적이다.

### §2. Part I에서 이 현장으로: 네 갈래 기술사가 만나는 지점

Part I의 네 챕터가 다룬 attention(Ch.1), compression(Ch.2), alignment(Ch.3), tool-use/memory(Ch.4)가 현장의 agent runtime에서 어떻게 동시에 작용하는지를 보인다. 한 문장 재도입으로 각 개념을 소환하되, 핵심은 **이 네 갈래가 단일 변수가 아니라 다변수 상호작용으로 나타난다는 관찰**이다.

### §3. 5변수 프레임워크: 병목 분석의 최소 단위

5변수의 조작적 정의. "어떤 조건에서 무엇이 1차 병목이 되는가"를 비교하기 위한 실험 분석 구조. 왜 4도 6도 아닌 5인지: Part I의 기술사에서 빠뜨릴 수 없는 변수(모델)와 Part I이 다루지 않는 현장 변수(surface, intervention, compute)가 만나는 지점.

### §4. 이원론의 거부와 Agent-1~2 스펙트럼

"모델 vs. 나머지"가 아니라, 각 변수가 독립적으로 작용하는 동시에 상호 결합하는 구조. Agent-1 → Agent-2 전환은 이 다섯 변수의 배치가 바뀌는 것이다.

### §5. 이 책의 좌표: AI Engineering 이후의 질문

Chip Huyen의 *AI Engineering*(2025)이 application layer를 다뤘다면, 이 책은 agent runtime의 운영 구조를 다룬다. OpenAI의 harness engineering 연구(2026)가 이상적 환경에서 원칙을 도출했다면, 이 책은 제약 환경에서 동일 원칙을 실험한다.

**학습 결과**: Part I의 역사적 좌표가 현장에서 왜 5변수로 수렴하는지를 설명할 수 있고, 자신의 환경에서 병목을 식별할 수 있다.

---

## Ch.6 — Agent가 모델로부터 무엇을 물려받는가

**한 줄**: 5변수 중 "모델" 변수를 격리하여 관찰한다. 네 가지 관찰 지표(도구 사용 정확도, instruction following rate, multi-step reasoning depth, context 활용 효율)를 정의하고, Capability Cliff의 비선형적 급락을 측정한다.

**기반**: 현행 Ch.2

**Part I 해석 연결** (각 관찰 지표는 이 챕터에서 독립적으로 정의된다. Part I은 학술적 배경을 제공하지만, 지표의 정의 자체를 도출하지 않는다):
- 도구 사용 정확도의 배경: Ch.4 §1 Toolformer — 학술적 기원
- Instruction following rate의 배경: Ch.3 §1 InstructGPT — 학습적 기원
- Multi-step reasoning depth의 배경: Ch.4 §2 ReAct — 학술적 기원
- Context 활용 효율의 배경: Ch.1 §5 Lost in the Middle — 실증적 근거
- Capability Cliff의 해석 렌즈: Ch.2 §3 cross-entropy — 오류 누적을 정보이론적으로 읽는 하나의 방법

### §1. 물려받는 경향: reasoning, tool use, consistency, calibration

직관 앵커 소재: "같은 코드인데 모델 바꾸니까 결과가 다르다"

**변경**: Part I에서 각 경향의 학술적 기원이 이미 확립되었으므로, 여기서는 한 문장 재도입 후 바로 agent runtime에서의 관찰로 진입.

### §2. 모델 관찰 지표 — 네 항목의 정의와 측정

**변경**: 현행 Ch.2 §2에서 4개 지표가 한 섹션에 동시 도입되던 문제(learning curve guideline 위반)를 해소. 도구 사용 정확도 + instruction following rate / multi-step reasoning depth + context 활용 효율로 2+2 분리. ARCC라는 합성 지표는 사용하지 않고, 개별 관찰 지표로 제시한다.

### §3. Capability Cliff — 선형이 아닌 급락이 발생하는 조건

Ch.2 §1의 (1-p)^n 공식은 Ch.2(압축 렌즈)의 cross-entropy 프레임으로 읽을 수 있다. 이 연결은 해석적 유용성이지 정의적 의존은 아니다.

### §4. Quantization Tax Curve

### §5. Distillation Efficiency Frontier

### §6. Mid-run model switching의 context continuity 붕괴

### §7. 모델 변수가 1차 병목이 되는 조건 — 그리고 아닌 조건

**학습 결과**: 네 가지 모델 관찰 지표 기반의 측정을 설계할 수 있다. 모델이 1차 병목인 조건과 아닌 조건을 구분할 수 있다.

---

## Ch.7 — Harness Engineering과 AgentOps

**한 줄**: 5변수 중 "harness"와 "intervention" 변수를 정의한다. Failure Budget Reallocation 프레임워크로 harness의 효과를 재규정하고, Ch.8 실험의 가설을 pre-register한다.

**기반**: 현행 Ch.3

**Part I 해석 연결**:
- Harness 정의의 직관 앵커: Ch.3 §4 "학습 정렬이 runtime 문제를 풀지 못하는 이유"가 harness 필요성의 배경
- Ontology RAG / semantic firewall: Ch.4 §4 RAG의 한계가 구조화된 memory가 필요한 이유를 이해하는 배경
- AgentOps의 관측 체계: Ch.2 §3 KL divergence가 prompt drift를 읽는 하나의 해석 도구

### §1. Harness Engineering이란 무엇인가

**변경**: 현행 Ch.3 §1이 정의로 바로 시작하던 문제 해소. 직관 앵커를 Ch.3 §4에서 자연스럽게 이어받음: "학습이 해결하지 못하는 것을 runtime에서 관리하는 구조"

### §2. Guardrails, Scaffolding, Orchestration과의 구분

### §3. Ontology와 메모리 구조

**변경**: RAG 원논문(Ch.4 §4)이 baseline으로 이미 확립되었으므로, 바로 "일반 RAG와 Ontology RAG의 차이"로 진입 가능.

### §4. Failure Budget Reallocation

**변경**: 직관 앵커 추가 — "harness를 달았는데 왜 실패 횟수가 똑같은가? 횟수가 아니라 종류가 바뀌었기 때문이다."

### §5. AgentOps와 운영 지표 (HOR, MTTR, HER)

### §6. Ch.8 실험 프레임 설정 — 가설과 판단 기준의 Pre-registration

**학습 결과**: Harness와 AgentOps를 정의하고, Failure Budget Reallocation으로 harness 효과를 설명할 수 있다. Ch.8 실험의 가설을 이해한다.

---

# Part III — 실험: 의도적 실패

---

## Ch.8 — 22개 시나리오: 무엇이 어떤 조건에서 깨지는가

**기반**: 현행 Ch.4. 변경 최소 — 이 챕터는 이미 learning curve를 비교적 잘 따르고 있다.

**Part I 연결**: 각 실험의 관찰은 Part I의 메커니즘으로 해석 가능한 사례가 된다. 아래는 인과 확정이 아니라 해석 가설이며, 본문 실험 해석에서 검증 여부를 판단한다.
- E05 memory leakage — Ch.1 attention 메커니즘의 잔류 activation으로 해석 가능한 사례
- E08 자기평가 정확도 급락 — Ch.3 self-critique 루프의 runtime 한계와 관련될 수 있는 관찰
- E09 goal drift — Ch.1 Lost in the Middle과 Ch.4 ReAct 루프의 장기 실행 한계가 겹치는 현상으로 읽을 수 있는 사례

### §1. 실험 설계 원칙: 왜 의도적으로 실패시키는가
### §2. 실험 환경: GCP 무료 티어, OpenRouter, 측정 인프라
### §3. 1막 — 모델·harness·surface 변수 격리 (E01~E07)
### §4. 2막 — 자원 제약 하에서 self-immune의 최소 조건 (E08~E12)
### §5. 3막 — 개입의 반복 가능성과 내재화 (E13~E18)
### §6. 반례 — task design과 compute saturation (E19~E20)

---

## Ch.9 — 실험이 보여준 것

**기반**: 현행 Ch.5 (scaffold → 초고로 끌어올리기 필요)

### §1. 22개 실험 결과 종합: 어떤 변수가 어떤 조건에서 1차 병목이었는가
### §2. Failure Budget Reallocation 정량 분석
### §3. 운영 metric 번역: MTTR과 Human Escalation Rate
### §4. 비용 metric 번역: TotalCost와 optimal HOR
### §5. Component ablation: 무엇이 얼마나 기여하는가
### §6. Token efficiency를 운영 규율로
### §7. Scaling과 temporal stability
### §8. 학술적 확장 가능성 — exploratory 발견 목록

---

# Part IV — 진화: 관찰에서 시스템으로

---

## Ch.10 — Operational Compiler: 관찰에서 도구로

**기반**: 현행 Ch.6. 변경 최소.

### §1. 반복 실패 패턴에서 도구화 후보 식별
### §2. Operational Compiler 설계 원칙
### §3. 점진적 업데이트: Pareto frontier를 따라 이동하는 전략
### §4. Skill로 쓸 수 있는 능력의 극대화
### §5. CLI-Anything 방법론 비교: 독립적 수렴의 의미

---

## Ch.11 — Self-Immune System: Harness에서 Agent로

**기반**: 현행 Ch.7

**Part I 해석 연결 (이 챕터에서 Part I의 투자가 회수된다)**:
- Self-critique의 계보: Ch.3 Constitutional AI는 이 챕터의 runtime self-immune이 놓인 학술적 계보를 제공한다. 같은 메커니즘이 아니라 같은 문제 의식의 연장이다.
- Reflexion과의 구분: Ch.4 §3 Reflexion = task 간 학습 / Self-immune = task 내 감지. 시간 스케일의 차이가 핵심이다.
- 재귀적 한계의 해석 렌즈: Ch.2의 cross-entropy 프레임은 self-monitoring 자체의 bit cost를 생각하는 하나의 방법을 제공한다.

### §1. 실험이 남긴 것
### §2. 현 세대 harness가 아직 풀 수 없는 문제
### §3. AgentOps → Harness → Agent 내재화: 점진적 경로
### §4. Self-immune system 초기 설계
### §5. Model Capability × Harness Value: Scaling 조건
### §6. Temporal Stability: self-immune은 얼마나 오래 유지되는가
### §7. Agent-1 → Agent-2: 전환 조건의 정식화
### §8. 이 책 이후: 미해결 질문들
### §9. 집필 과정의 메타 관찰

---

## Appendices

| Appendix | 내용 |
|----------|------|
| A — 실험 로그 템플릿 | 5변수, 교차검증, pre-registration 포함 |
| B — 용어 사전 | 전체 용어의 조작적 정의 |
| C — Figure 목록과 해석 가이드 | 모든 Figure의 읽는 법과 재현 조건 |
| D — 참조 프로젝트 목록 | GitHub 프로젝트 전체 (stars, URL, 인용 맥락) |
| E — 참고문헌 | 논문, 서적, 기술 블로그 전체 목록 |

---

## v4 → v6 변경 로그

| 항목 | v4 | v6 | 변경 이유 |
|------|----|----|----------|
| Part I | Agent Runtime의 현장 (Ch.1-3) | **기반: Agent를 만든 논문들 (Ch.1-4)** | 핵심 논문을 backbone으로 세워 개념적 기반 확보 |
| 구조 | 9챕터, 4 Parts | **11챕터, 4 Parts** | Part I 4챕터 신설, Part II 이후 기존 7챕터 재배치 |
| v4 Ch.2 (작동 원리) | 별도 챕터 | Part I Ch.4에 흡수 | Toolformer/ReAct/Reflexion이 논문 기반으로 더 풍부하게 커버 |
| v4 Ch.3 (5변수) | 별도 챕터 | v6 Ch.5에 통합 | Part I이 기반을 제공하므로 별도 챕터 불필요 |
| 교육 설계 | 암묵적 | **learning curve 3단계 명시적 적용** | editorial-learning-curve-guideline.md 전 챕터 적용 |
| 문헌 위치 | 본문 내 산발적 인용 | **Part I에서 backbone으로 체계화** | 권위 장식이 아니라 개념적 기반으로 기능 |
| compression lens | 미포함 | **Ch.2로 배치 (Direction A)** | 정보이론이 HOR, prompt 최적화, 모델 관찰 지표의 해석 렌즈 |
| Attention Is All You Need | 기각 (v4에서 "직접 활용도 제한적") | **Ch.1 backbone** | Part I 구조에서는 attention이 context/hallucination 이해의 필수 기반 |
| Lost in the Middle | Ch.1/Ch.3 조건부 | **Ch.1 companion** | Attention과 함께 읽으면 context 활용 효율의 메커니즘이 완결 |
| Constitutional AI | Ch.7 조건부 | **Ch.3 backbone** | 학습-runtime 경계를 구분하는 핵심 좌표 |
| Reflexion | Ch.7 배치 | **Ch.4 backbone + Ch.11 연결** | Self-immune의 선행 좌표로 Part I에서 먼저 확립 |
| RAG | Ch.3 baseline | **Ch.4 companion** | Memory 구조의 baseline으로 Part I에서 확립 |
| InstructGPT/RLAIF | Preface/Ch.1 배경 | **Ch.3 backbone** | 정렬 계보가 "왜 harness가 필요한가"의 구조적 답 |
| Toolformer/ReAct | 기각/조건부 | **Ch.4 backbone** | 도구 사용 정확도와 multi-step reasoning depth의 학술적 기원 — Part I에서 확립 필수 |

---

## 집필 순서 제안

Part I은 기존 원고와 독립적이므로 병렬 집필 가능.

**Phase 1 — Part I 초고 (신규)**
1. Ch.2 (압축 렌즈) — 영어 원고 존재, 한국어 적응 + voice rule 적용
2. Ch.1 (Attention + Lost in the Middle) — prerequisite 개념이 가장 기초적
3. Ch.3 (정렬 계보) — InstructGPT/RLAIF/Constitutional AI 순서가 명확
4. Ch.4 (도구/추론/기억) — Toolformer/ReAct/Reflexion/RAG 통합

**Phase 2 — Part II~IV 기존 원고 재정비**
5. Ch.5 (현행 Ch.1 재작성 — voice rule 위반 수정 + 5변수 통합)
6. Ch.6 (현행 Ch.2 — 모델 관찰 지표 도입부 learning curve 재구성)
7. Ch.7 (현행 Ch.3 — 직관 앵커 추가 + 손상 복구)
8. Ch.8 (현행 Ch.4 — 변경 최소, [X] 데이터 의존)
9. Ch.9 (현행 Ch.5 — scaffold에서 초고로)
10. Ch.10 (현행 Ch.6 — 변경 최소)
11. Ch.11 (현행 Ch.7 — Part I 연결 강화)
