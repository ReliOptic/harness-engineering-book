# Ch.1 — Context Window의 구조적 한계

> **Part I — Agent Runtime의 기술적 전제**

> 상태: 🟡 초고 (2026-04-04) — dialogue 재료 기반 full draft
> 담당: Kiwon
> 목표 분량: 8,000~10,000자

**Backbone 논문**:
- Vaswani et al., *Attention Is All You Need* (NeurIPS 2017, ~140,000 citations)
- Liu et al., *Lost in the Middle: How Language Models Use Long Contexts* (TACL 2024, ~1,500 citations)

**이 챕터가 도입하는 개념**: embedding, dot product similarity, softmax, K-Q-V mechanism, multi-head attention, positional encoding, U-shaped attention curve, autoregressive inference, KV Cache

**챕터 종료 시 독자 상태**: "왜 context window를 늘려도 agent가 중간 정보를 놓치는가"를 attention 메커니즘으로 설명할 수 있으며, 이 구조적 한계가 harness의 존재 이유라는 것을 인지한다.

---

Transformer 아키텍처는 2017년 Vaswani et al.이 "Attention Is All You Need"에서 제시한 이래로 대규모 언어 모델의 근간이 되었다. 이 챕터가 attention 메커니즘을 해부하는 이유는 모델 자체의 우수성을 설명하기 위해서가 아니다. Agent가 장기 실행 중에 보이는 실패 패턴의 상당수가 attention의 구조적 성질에서 기인하며, 그 성질을 이해하지 않으면 harness가 왜 필요한지, 어디에 개입해야 하는지를 정밀하게 규정할 수 없기 때문이다. 이 챕터는 embedding에서 시작하여 QKV 메커니즘, multi-head attention, positional encoding, Lost in the Middle 현상, autoregressive 추론과 KV Cache를 거쳐, 이 모든 것이 agent runtime에서 어떤 실패로 발현되는지를 추적한다.

---

## §1. 단어가 숫자가 되는 순간 — Embedding과 벡터 공간

"King - Man + Woman ≈ Queen"이라는 유명한 벡터 산술을 대부분의 독자는 어디선가 접했을 것이다. 단어가 고차원 벡터 공간에 매핑되면, 의미 관계가 벡터 간의 기하학적 관계로 표현된다는 것은 직관적으로 받아들이기 쉽다. 그러나 "두 벡터의 유사도를 어떻게 측정하는가"라는 질문에서 많은 독자가 멈춘다. 이 질문이 중요한 이유는 이것이 attention 메커니즘의 첫 번째 연산이기 때문이다.

Dot product는 두 벡터가 같은 방향을 가리킬수록 높은 값을 반환한다. 2차원으로 단순화하면 이것은 두 화살표가 얼마나 같은 쪽을 향하고 있는가의 문제다. 벡터 A = [1, 0]과 벡터 B = [0, 1]은 직교하므로 dot product는 0이다. 벡터 A = [1, 0]과 벡터 C = [1, 0]은 동일 방향이므로 dot product는 1이다. 이것이 2차원에서의 직관이고, embedding 공간은 이 직관을 수백, 수천 차원으로 확장한다. "차원"이란 물리적 공간의 x, y, z축이 아니라, 단어의 특성을 기술하는 축이다. 한 축은 성별 정보를 담고, 다른 축은 왕족 여부를 담고, 또 다른 축은 시제 정보를 담는 식이다. King과 Queen이 벡터 공간에서 가까운 이유는 "왕족" 차원에서 높은 값을 공유하기 때문이며, King과 Man이 "남성" 차원에서 가까운 이유도 같은 논리다.

이것이 agent의 tool 선택과 직결된다. Agent가 context에서 tool description을 읽고 어떤 tool을 호출할지 결정할 때, 모델은 현재 과제를 나타내는 벡터(Query)와 각 tool description의 벡터(Key) 사이의 dot product를 계산한다. "이메일을 보내라"라는 지시와 `send_email`이라는 tool description은 embedding 공간에서 높은 유사도를 갖는다. 그런데 `send_notification`이라는 tool도 존재한다면, 두 tool의 embedding 거리가 가까워서 모델이 혼동할 수 있다. 이 혼동은 모델이 "멍청"해서가 아니라, embedding 공간에서 두 tool이 유사한 좌표를 점유하기 때문에 발생하는 구조적 현상이다.

> **이 섹션의 한 문장**: 단어가 벡터가 되고, 벡터 간 유사도가 attention의 원료가 된다. 유사한 것이 가까이 있으면 혼동이 생긴다.

---

## §2. 주의를 기울인다는 것 — Attention 메커니즘의 해부

Embedding이 "단어를 숫자로 바꾼다"면, attention은 "어떤 숫자에 더 주의를 기울일 것인가"를 결정한다. Transformer는 입력의 모든 토큰을 동등하게 처리하지 않는다. 관련 있는 토큰에 높은 가중치를, 관련 없는 토큰에 낮은 가중치를 부여하여 정보를 선택적으로 집중한다.

이 메커니즘의 핵심은 세 가지 행렬이다: Query(Q), Key(K), Value(V). 입력 토큰들은 학습된 가중치 행렬을 통해 Q, K, V 세 가지 표현으로 변환된다. Q는 "내가 찾는 것"이다. 현재 처리 중인 토큰이 context에서 어떤 정보를 필요로 하는가를 나타낸다. K는 "라벨"이다. 각 토큰이 자신을 어떤 유형의 정보로 광고하는가를 나타낸다. V는 "실제 내용"이다. K가 "나는 이런 정보입니다"라고 광고하면, V는 그 정보의 실체다. Attention 연산은 세 단계로 진행된다. Q와 K의 전치 행렬(K^T) 사이의 dot product를 계산하여 유사도 점수 행렬을 만든다. 이 점수에 softmax를 적용하여 확률 분포로 변환한다. 변환된 확률로 V의 가중 합을 계산하여 최종 출력을 생성한다.

여기서 softmax의 역할을 단순한 정규화로 이해하면 핵심을 놓친다. Softmax는 높은 점수와 낮은 점수의 차이를 증폭시키는 함수다. 입력이 [2.0, 1.0, 0.1]이면 softmax 출력은 대략 [0.66, 0.24, 0.10]으로 차이가 완만하다. 그러나 입력이 [10.0, 1.0, 0.1]이면 출력은 [0.9999, 0.0001, 0.00004]에 가까워진다. 하나의 점수가 충분히 높으면 나머지를 거의 0으로 만든다. 이것이 softmax의 "winner-take-most" 성질이며, attention이 특정 토큰에 "집중"할 수 있는 수학적 실체다. 동시에 이것은 attention이 "잘못된 곳에 집중"할 수 있는 이유이기도 하다. 잘못된 K에 높은 점수가 부여되면, softmax가 그 오류를 증폭시켜 나머지 모든 관련 정보를 묻어버린다.

이 성질을 온도(temperature, τ)로 조절할 수 있다. Attention score를 √d_k로 나누는 것(scaled dot-product attention)은 softmax 입력의 크기를 조절하여 분포가 지나치게 뾰족해지는 것을 방지한다. d_k는 Key 벡터의 차원 수인데, 차원이 높을수록 dot product 값이 커지므로 나누어 보정하는 것이다. 이 보정이 없으면 고차원에서 softmax는 사실상 하나의 토큰에만 전체 가중치를 부여하는 argmax에 가까워진다.

한 가지 흔한 혼동이 있다. 고빈도 토큰, 예를 들어 관사, 접속사, 구두점 같은 토큰이 context에 반복적으로 등장하면, 이 토큰들이 attention을 과도하게 흡수하는 현상이 관찰된다. 이를 attention sink라고 부르는데, 이 토큰들이 의미적으로 중요해서가 아니라, 학습 과정에서 softmax가 여분의 확률 질량을 할당할 "기본 수신자"를 필요로 하기 때문이다. Agent의 context에 반복적인 로그 메시지나 동일한 시스템 프롬프트 패턴이 누적되면 이 현상이 실질적 문제로 작용할 수 있다.

> **이 섹션의 한 문장**: Attention은 Q와 K의 유사도를 softmax로 증폭시켜 V에서 관련 정보를 추출하는 연산이며, softmax의 "winner-take-most" 성질이 집중과 오류를 동시에 가능하게 한다.

---

## §3. 여러 관점으로 동시에 보기 — Multi-Head Attention과 Positional Encoding

### Multi-Head Attention

Multi-head attention에 대한 가장 흔한 오해는 "병렬 처리를 통한 속도 향상"이 핵심 이점이라는 것이다. 속도 향상은 부수적 효과일 뿐이며, 핵심은 동일한 입력을 서로 다른 관점에서 동시에 분석하는 능력이다.

각 head는 독립적인 Q, K, V 가중치 행렬을 갖는다. 이것은 동일한 토큰 집합에 대해 서로 다른 유형의 관계를 포착할 수 있다는 뜻이다. Head A는 "이 토큰의 구문적 역할이 무엇인가"를 포착하여 주어-동사 관계에 집중할 수 있다. Head B는 "이 토큰과 의미적으로 연관된 토큰이 무엇인가"를 포착할 수 있다. Head C는 "이 토큰의 인접 토큰이 무엇인가"에 집중하여 국소적 패턴을 학습할 수 있다. 이 head들의 출력은 결합(concatenation)된 후 선형 변환을 거쳐 최종 표현이 된다.

이 구조가 agent runtime에서 의미 있는 이유는 양자화(quantization)와의 관계에 있다. 모델을 양자화할 때, 모든 head가 동일하게 영향을 받는 것이 아니다. 구문적 관계를 포착하는 head는 상대적으로 양자화에 강한 반면, 미세한 의미 차이를 포착하는 head는 정밀도 손실에 취약한 경향이 있다. Ch.6에서 관찰하게 될 Quantization Tax Curve의 배경이 여기에 있으며, 이 불균등한 영향이 양자화된 모델에서 tool 선택 정확도가 비선형적으로 저하되는 현상의 메커니즘 중 하나다.

### Positional Encoding

Transformer의 self-attention 연산은 본질적으로 집합(set) 연산이다. Q와 K의 dot product는 두 토큰 사이의 내용 유사도만 계산하며, 어떤 토큰이 앞에 오고 어떤 토큰이 뒤에 오는지에 대한 정보를 포함하지 않는다. "개가 사람을 물었다"와 "사람이 개를 물었다"는 동일한 토큰 집합으로 구성되어 있으므로, 위치 정보 없이는 attention이 두 문장을 구분할 수 없다.

Vaswani et al.의 원 논문은 이 문제를 sinusoidal positional encoding으로 해결했다. 각 위치에 고정된 사인/코사인 파형의 값을 embedding에 더하여 위치 정보를 주입한다. 이 방식의 장점은 학습 데이터에 없던 길이의 입력으로도 일반화할 수 있다는 것이다. 단, 두 토큰 사이의 상대적 거리를 직접 표현하기 어렵다는 한계가 있었다.

현대 모델의 표준은 RoPE(Rotary Position Embedding, Su et al. 2021)다. RoPE는 벡터를 위치에 비례하여 회전시키는 방식으로 상대적 위치 관계를 Q와 K의 dot product 자체에 내장시킨다. 두 토큰의 위치 차이가 동일하면 동일한 회전각 차이가 적용되므로, 상대적 거리가 attention score에 직접 반영된다. 이 개선이 long context 처리 능력의 확장에 기여했으나, positional encoding만으로 §5에서 다루는 Lost in the Middle 현상이 해소되지는 않았다.

한 가지 혼동을 사전에 차단한다. Base model이 특정 방향성(예: 도움이 되려는 성향)을 갖지 않는 것은 positional encoding의 한계가 아니다. 방향성의 부재는 아키텍처의 문제가 아니라 학습 목표(training objective)의 문제이며, 이것은 Ch.3에서 RLHF와 Constitutional AI를 통해 다루게 될 주제다. Positional encoding은 "순서 인식"을 담당하고, training objective는 "목적 부여"를 담당한다. 두 가지는 독립적인 계층이다.

> **이 섹션의 한 문장**: Multi-head는 동일 입력을 여러 관계 유형으로 동시에 분석하는 구조이며, positional encoding은 순서 정보를 주입하되 의미적 이해와는 독립적이다.

---

## §4. 긴 입력에서 무엇이 사라지는가 — Lost in the Middle

Liu et al.은 2023년(TACL 2024에 정식 게재)에 20개 모델을 대상으로 다양한 길이의 context에서 정보의 위치별 활용도를 정량적으로 측정했다. 결과는 U-shaped curve였다. 모델은 context의 시작 부분과 끝 부분에 위치한 정보를 효과적으로 활용하는 반면, 중간에 위치한 정보의 활용도는 현저히 낮았다.

이 결과를 처음 접하면 두 가지 반응이 나온다. 하나는 인간의 serial position effect(초두 효과와 최신 효과)와의 유사성에 주목하여 이 현상을 단순한 관찰적 유추로 평가하는 것이다. 그러나 Liu et al.의 연구는 관찰적 유추가 아니라, 20개 모델에 걸쳐 체계적으로 측정된 실험 결과다. Attention의 구조적 성질, 특히 softmax의 확률 질량 분배와 positional encoding의 거리 편향이 이 패턴의 기계적 원인이다.

다른 하나는 "2023년 논문이므로 2026년에는 해결되었을 것"이라는 가정이다. 이 가정은 부분적으로만 맞다. 2023년에서 2026년 사이에 context window는 4K에서 200K 이상으로 확장되었고, Gemini 1.5의 "needle in a haystack" 테스트를 비롯하여 long context 성능은 개선되었다. 그러나 개선된 것은 U-shaped curve의 valley 깊이, 즉 중간 위치에서의 정보 손실률이다. U-shaped curve라는 구조 자체가 소멸한 것은 아니다. Attention의 softmax 분포가 본질적으로 sparse하기 때문에, 토큰 수가 증가하면 중간 위치의 attention weight는 여전히 희석되는 경향을 보인다.

200K token context window를 가진 모델이 200K token 전체를 균등하게 활용한다는 것은 사실이 아니다. Context window의 크기와 context의 실효 활용률은 서로 다른 변수다. 200K 윈도우는 200K 토큰을 "이해"한다는 뜻이 아니라, 200K 토큰을 "입력받을 수 있다"는 뜻이다. 이것은 기술적 극복이 아니라 입력 용량의 확대이며, 깔때기를 크게 만든 것이지 깔때기 자체를 제거한 것이 아니다.

이 현상이 agent 운영에서 직접적으로 발현되는 지점은 장기 실행이다. Agent가 수십 번의 tool call을 수행하면서 context가 누적될 때, 초기에 주어진 system prompt의 핵심 지시가 context의 중간에 묻히게 된다. 모델은 최근의 tool call 결과(context 끝)와 system prompt의 도입부(context 시작)는 잘 참조하지만, 중간에 축적된 과거 결과와 중간에 위치한 지시를 놓치기 시작한다. 이것이 agent의 silent drift, 즉 명시적 오류 없이 원래 의도에서 점진적으로 벗어나는 현상의 기계적 원인 중 하나다.

> **이 섹션의 한 문장**: Context window의 크기는 입력 용량이지 이해 용량이 아니며, U-shaped attention curve는 2026년에도 구조적으로 존속한다.

---

## §5. 학습과 추론의 비대칭 — Autoregressive 생성과 KV Cache

대부분의 독자는 AI가 잘못된 방향으로 진행할 때 새로운 대화 세션을 열어 해결한 경험이 있을 것이다. AI에게 "돌아가서 다시 생각해 봐"라고 말해도 같은 오류를 반복하거나, 돌아갔다고 주장하면서 실제로는 이전의 잘못된 맥락 위에 계속 쌓아나가는 현상. 새 세션을 여는 것이 왜 효과적인지를 이해하려면, Transformer가 학습할 때와 추론할 때 attention을 사용하는 방식의 차이를 알아야 한다.

학습 시 Transformer는 문장 전체를 한꺼번에 처리한다. "나는 고양이를 좋아한다"라는 문장이 있으면, 각 위치에서 다음 토큰을 예측하는 작업을 모든 위치에 대해 병렬로 수행한다. 단, "좋아한다"를 예측할 때 그 뒤에 오는 토큰을 참조하면 안 되므로, 미래 위치를 가리는 causal mask를 적용한다. 이것은 시험에서 답을 알고 있는 상태에서 커닝 방지 장치를 쓴 것에 비유할 수 있다. 답은 이미 있지만, 각 위치에서 미래를 참조하지 못하게 강제한다.

추론 시에는 상황이 근본적으로 다르다. 미래 토큰이 존재하지 않는다. 모델은 토큰을 하나 생성하고, 그 토큰을 context에 추가하고, 확장된 context를 기반으로 다음 토큰을 생성한다. 이것이 autoregressive 추론이다. "자기 출력을 다음 입력으로 사용한다"는 뜻이며, 본질적으로 순차적이다.

> **용어 구분**: Autoregressive, recursive, regression은 서로 다른 개념이다. Autoregressive는 이전 출력이 다음 입력이 되는 순방향 구조다(A→B→C→D). Recursive는 자기 자신을 호출하여 들어갔다 나오는 구조다(A→B→C→B→A). Regression은 통계적 회귀분석이다. Transformer의 추론은 autoregressive이며 recursive가 아니다. Agent에서 "recursive"라고 부르는 Reflexion 같은 자기 수정 루프는 Transformer 내부가 아니라 외부의 harness가 만드는 구조다.

Autoregressive 구조의 실용적 함의는 오류 전파에 있다. 생성된 토큰은 이후 모든 토큰의 context가 되므로, 초기에 발생한 오류가 하류의 모든 생성에 영향을 미친다. 되돌아가서 오류를 수정하는 메커니즘이 Transformer 내부에는 존재하지 않는다. "다시 생각해 봐"라고 요청해도, 이전의 잘못된 토큰들이 이미 context에 존재하며 attention은 그것들을 참조한다. 새 세션을 열면 이 누적된 오류 context가 제거되어 효과적인 것이다.

이 과정에서 KV Cache가 물리적 비용을 결정한다. 추론 시 새 토큰을 생성할 때마다 이전 모든 토큰의 attention을 다시 계산하면 비용이 제곱으로 증가한다. KV Cache는 이전 토큰들의 Key와 Value를 GPU 메모리에 저장해두고, 새 토큰의 Query만 저장된 K, V와 attention을 계산함으로써 이 비용을 선형으로 줄인다. 그런데 이 cache는 context 길이에 비례하여 메모리를 소비한다. 200K 토큰 context의 KV Cache는 모델 구조와 정밀도에 따라 수 GB의 GPU 메모리를 차지할 수 있다. KV Cache는 손실 없는 정확한 복사본이어야 하므로, 분산 저장 시스템에서 사용하는 erasure coding 같은 손실 허용 기법을 적용할 수 없다. 일부가 누락되면 attention 계산 자체가 틀어진다.

Agent가 장기간 실행되면서 context가 누적될 때, KV Cache의 메모리 소비는 선형으로 증가한다. Ch.5에서 필자가 "컴퓨팅 자원이 1차 병목이 되는 조건"으로 기술한 현상의 물리적 실체가 이것이다. 공유 vCPU와 제한된 메모리 환경에서 agent를 운영할 때, KV Cache의 누적은 모델의 추론 능력과 무관하게 시스템을 정지시킬 수 있다.

> **이 섹션의 한 문장**: Autoregressive 추론은 오류를 앞으로만 전파하며, KV Cache는 그 오류 context를 물리적 메모리로 고착시킨다.

---

## §6. Agent Operations를 위한 시사점

Attention 메커니즘에 대한 이해를 agent 운영의 언어로 번역하면 다섯 가지 실패 경로가 보인다.

**Softmax sparsity와 tool call hallucination.** Softmax의 winner-take-most 성질은 모델이 가장 높은 attention score를 받은 tool description에 대부분의 확률 질량을 할당하게 만든다. 유사한 tool이 여러 개 존재하거나, 이전 대화에서 특정 tool을 반복 호출한 이력이 context에 남아 있으면, attention이 잘못된 tool definition에 편향될 수 있다. 이것이 agent가 존재하지 않는 함수를 호출하거나 잘못된 인자를 전달하는 현상, 즉 tool call hallucination의 구조적 원인 중 하나다.

**Lost in the Middle과 silent drift.** Agent가 수십 단계의 작업을 수행하면서 context가 수만 토큰으로 누적되면, 초기에 주어진 핵심 지시가 context의 중간에 매몰된다. U-shaped attention curve에 따라 이 지시에 대한 attention weight가 감소하면, agent는 명시적 오류 없이 원래 의도에서 점진적으로 이탈한다. 이 silent drift는 오류 메시지를 생성하지 않으므로 외부에서 감지하기 어렵다.

**Autoregressive 오류 전파.** Transformer의 추론이 순방향 전용(autoregressive)이라는 사실은, 한번 잘못된 방향으로 진행된 agent가 자력으로 되돌아오기 어렵다는 것을 의미한다. 잘못된 tool call의 결과가 context에 추가되면, 이후의 모든 결정이 그 오류를 전제로 이루어진다. 이것은 "agent가 멈추는 것이 아니라 잘못된 방향으로 계속 진행하는" 실패 패턴의 기계적 기원이다.

**KV Cache 누적과 execution boundary 병목.** Agent의 장기 실행에서 KV Cache의 메모리 소비는 선형으로 증가하며, 자원이 제한된 환경에서 이것은 모델의 추론 능력과 무관하게 시스템을 정지시킬 수 있다. 이 병목은 inbound(model capability)나 harness 설계가 아니라 boundary(실행 환경 제약)에 해당하며, harness 중심 프레임워크가 이원론(모델 vs 시스템)을 넘어야 하는 이유의 하나다.

**Attention ≠ 이해.** Attention weight가 높다는 것은 두 토큰 사이의 통계적 상관관계가 높다는 뜻이지, 모델이 그 관계의 논리적 정합성을 검증했다는 뜻이 아니다. "서울의 수도는 한국이다"라는 문장에서 모델이 "서울"과 "수도"에 높은 attention을 줄 수 있으나, 그것은 두 단어가 학습 데이터에서 자주 함께 등장했기 때문이지, 모델이 이 문장의 사실 관계를 이해했기 때문이 아니다. Attention은 상관관계를 포착하지 인과관계를 검증하지 않는다.

이 다섯 가지 실패 경로 각각에 harness의 구성 요소가 대응한다. Tool call 검증 레이어는 softmax sparsity에 의한 hallucination을 차단한다. 핵심 지시의 반복 주입과 context 재구성은 Lost in the Middle에 대응한다. Recovery hook과 외부 recursive 루프는 autoregressive 오류 전파를 끊는다. Memory boundary와 context window 관리는 KV Cache 누적을 통제한다. Evaluation hook과 output 검증은 attention의 통계적 본성이 만드는 논리적 오류를 포착한다.

사용자가 agent에게 기대하는 것은 맥락의 축적이다. 매일 바뀌는 업무와 매순간 달라지는 조건을 매번 처음부터 입력하는 것은 비효율적이며, 사용자는 agent가 자신의 맥락을 기억하고 축적하기를 원한다. 그러나 LLM은 무엇을 기억하고 무엇을 버려야 하는지 스스로 결정하는 메커니즘을 갖고 있지 않다. 인간은 선택적으로 망각하지만, LLM은 context window에 있는 토큰을 무차별적으로 보존한다. 축적된 컨텍스트를 정제하고, 불필요한 정보를 제거하고, 중요한 정보의 위치를 관리하는 별도의 레이어가 필요하다. 이것이 harness의 memory boundary와 context compression이 존재하는 이유이며, Ch.10에서 Operational Compiler의 설계 원칙으로 구체화될 것이다.

컨텍스트 윈도우가 아무리 커져도, attention의 통계적 본성 때문에 모델은 모든 것을 균등하게 이해하지 못한다. 이 간극이 harness가 존재해야 하는 이유이며, 이 책의 나머지가 측정하려는 대상이다.

---

## 참조

- Vaswani, A. et al. (2017). Attention Is All You Need. *NeurIPS*. arXiv:1706.03762
- Liu, N. F. et al. (2024). Lost in the Middle: How Language Models Use Long Contexts. *TACL*. arXiv:2307.03172
- Su, J. et al. (2021). RoFormer: Enhanced Transformer with Rotary Position Embedding. arXiv:2104.09864
- Dao, T. et al. (2022). FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness. arXiv:2205.14135
- `dialogue/ch01-attention/insight-summary.md` — 저자 이해도 프로필 및 독자 함정 목록
- `dialogue/ch01-attention/writing-material.md` — 섹션별 초안 재료
- `dialogue/ch01-attention/connections.md` — 타 챕터 연결 씨앗
