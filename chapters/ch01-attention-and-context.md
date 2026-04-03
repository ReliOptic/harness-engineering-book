# Ch.1 — Attention과 Context: 모델은 어떻게 보는가

> **Part I — 기반: Agent를 만든 논문들**

**한 줄**: Transformer의 attention 메커니즘이 정보를 처리하는 방식을 이해하고, 그 구조적 한계가 agent runtime에서 어떤 실패로 나타나는지를 연결한다.

**Backbone 논문**:
- Vaswani et al., *Attention Is All You Need* (NeurIPS 2017, ~140,000 citations)
- Liu et al., *Lost in the Middle: How Language Models Use Long Contexts* (TACL 2024, ~1,500 citations)

**이 챕터가 도입하는 개념**: embedding, dot product similarity, softmax, K-Q-V mechanism, multi-head attention, positional encoding, U-shaped attention curve

**챕터 종료 시 독자 상태**: "왜 context window를 늘려도 agent가 중간 정보를 놓치는가"를 attention 메커니즘으로 설명할 수 있다.

---

## §1. 단어가 숫자가 되는 순간 — embedding과 벡터 공간

**직관 앵커**: "왕 - 남자 + 여자 = 여왕"이라는 유명한 예시. 단어가 숫자 벡터가 되면 의미의 산술이 가능해진다.

**정밀 정의**: embedding, 벡터 공간, 차원, dot product similarity, cosine similarity

**운영 번역**: agent가 tool description을 "이해"하는 것은 embedding 공간에서의 유사도 계산이다. 유사한 tool description이 혼동을 만드는 구조적 이유.

**탐구 질문**: embedding 공간에서 의미가 가까운 두 tool description이 있을 때, agent는 어떤 기준으로 선택하는가? 그 선택이 실패하는 조건은 무엇인가?

<!-- TODO: 본문 집필 -->

---

## §2. 주의를 기울인다는 것 — Attention 메커니즘의 해부

**직관 앵커**: 시끄러운 파티에서 자기 이름이 불리면 들린다. 모든 소리를 동일하게 처리하는 것이 아니라, 관련 있는 정보에 가중치를 부여하는 것이 attention이다.

**정밀 정의**: Query-Key-Value, attention score = softmax(QK^T / √d_k), weighted sum of Values

**운영 번역**: agent가 context window에서 "어떤 정보에 주의를 기울이는가"는 Q와 K의 dot product가 결정한다. 이것이 확률적이라는 사실이 agent 출력의 비결정성의 한 원천이다.

**탐구 질문**: attention score 분포가 uniform에 가까워지는 조건은 무엇인가? 그 조건이 agent의 어떤 실패 양상과 연결되는가?

<!-- TODO: 본문 집필 -->

---

## §3. 여러 관점으로 동시에 보기 — Multi-Head Attention

**직관 앵커**: 같은 문서를 법무팀과 재무팀이 다르게 읽는다. Multi-head attention은 동일한 입력을 여러 관점에서 동시에 분석한다.

**정밀 정의**: head 분할, 독립적 Q/K/V projection, concatenation + linear projection

**운영 번역**: head 수가 많을수록 양자화 저항성이 높아지는 경향 — Ch.6 Quantization Tax Curve의 배경.

**탐구 질문**: 양자화가 head별 attention pattern을 균일하게 훼손하는가, 특정 head에 집중적으로 영향을 미치는가?

<!-- TODO: 본문 집필 -->

---

## §4. 순서를 기억하는 방법 — Positional Encoding

**직관 앵커**: "개가 사람을 물었다"와 "사람이 개를 물었다" — 같은 단어, 다른 순서, 다른 의미.

**정밀 정의**: sinusoidal positional encoding, 상대적 위치 표현, RoPE

**운영 번역**: positional encoding의 한계가 long context에서 위치 편향을 만든다. 이것이 §5의 Lost in the Middle 현상으로 이어진다.

**탐구 질문**: RoPE 계열 위치 인코딩이 context window 확장에서 기존 sinusoidal 대비 어떤 trade-off를 만드는가?

<!-- TODO: 본문 집필 -->

---

## §5. 긴 입력에서 무엇이 사라지는가 — Lost in the Middle

**직관 앵커**: 20페이지 보고서를 읽을 때, 첫 페이지와 마지막 페이지는 기억하지만 중간은 흐릿해진다.

**정밀 정의**: Liu et al.의 실험 — 문서를 입력 위치별로 배치했을 때 정보 활용도의 U-shaped curve. 중간 위치 정보의 활용도가 시작/끝 대비 현저히 낮다.

**운영 번역**:
- Context window를 늘리는 것이 만능이 아닌 이유: "Right Context > Big Context"
- Agent의 context 활용 효율이 context 길이에 따라 비선형적으로 감소하는 메커니즘
- Ch.6에서 관찰하는 context 활용 효율 지표가 이 현상을 포착한다

**탐구 질문**: U-shaped curve의 trough 깊이가 모델 크기나 학습 데이터에 따라 달라지는가? 이 차이가 agent runtime에서 관찰 가능한가?

<!-- TODO: 본문 집필 -->

---

## §6. Agent Operations를 위한 시사점

**이 섹션은 Stage 3(운영 번역)의 종합이다.**

- **Context window = attention capacity**: 토큰 수가 아니라, 모델이 실제로 활용할 수 있는 정보량이 진정한 한계
- **Attention 오배분 → Hallucination 경로**: K-Q-V에서 Query가 잘못된 Key에 높은 점수를 부여하면, 관련 없는 Value가 출력에 혼입된다. 이것이 tool call hallucination의 구조적 기원 중 하나
- **System prompt 설계 원칙**: 중요한 instruction은 context의 시작과 끝에 배치한다 (Lost in the Middle 대응)
- **Ch.6 연결**: 도구 사용 정확도의 semantic 차원, context 활용 효율의 측정 근거가 이 챕터에서 확립된다

**Callout**: "Context window 128K는 128K 토큰을 '이해'한다는 뜻이 아니다. Attention이 실제로 활용하는 정보량은 위치와 관련성에 따라 비선형적으로 감소한다."

**탐구 질문**: system prompt의 위치 전략(시작/끝 배치)이 실제 agent task completion rate에 측정 가능한 차이를 만드는가?

<!-- TODO: 본문 집필 -->
