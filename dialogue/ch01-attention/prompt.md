# Ch.1 대화 프롬프트 — Attention과 Context: 모델은 어떻게 보는가

## 프로젝트 컨텍스트

나는 "Harness Engineering and AgentOps"라는 기술서를 집필 중이다. 이 책은 2026년 상반기 agent runtime의 실패를 관찰하고 측정하는 실험서다. 11챕터, 4-Part 구조이며, Part I(Ch.1~4)은 agent를 만든 역사적 논문들을 기반으로 agent runtime 실패의 기술적 기원을 추적한다.

Ch.1은 Part I의 첫 번째 챕터로, Transformer의 attention mechanism이 agent runtime에서 어떤 실패 모드를 만들어내는지를 추적한다. 이 챕터의 마지막 섹션은 "Agent Operations를 위한 시사점"으로, 학술 개념을 agent 운영 현실로 번역해야 한다.

**이 대화의 목적**: 아래 논문들을 내가 이해하는 과정 자체가 Ch.1 집필의 원료가 된다. 내 이해의 빈틈과 연결 과정이 독자의 학습 경로를 설계하는 데 직접 쓰인다.

---

## 핵심 논문과 자료

1. **Vaswani et al., "Attention Is All You Need"** (NeurIPS 2017, ~140,000 citations)
   - Transformer 아키텍처의 원논문
   - Query-Key-Value, multi-head attention, positional encoding
   - https://arxiv.org/abs/1706.03762

2. **Liu et al., "Lost in the Middle: How Language Models Use Long Contexts"** (TACL 2024, ~1,500 citations)
   - 긴 context에서 모델이 중간 정보를 놓치는 U-shaped attention curve
   - context window 크기와 실제 정보 활용의 비선형 관계
   - https://arxiv.org/abs/2307.03172

3. **참고 자료**:
   - RoPE (Rotary Position Embedding) — Su et al., 2021
   - Flash Attention (Dao et al., 2022) — 하드웨어 수준 attention 최적화
   - Ring Attention — 분산 환경에서의 long context 처리

---

## 10가지 평가 질문

나의 이해도를 평가해 주세요. 각 질문에 대해 내가 답하면, 정확한 부분과 빈틈을 짚어주고, 빈틈이 있으면 보충 설명 후 다음 질문으로 넘어가 주세요. 모든 질문이 끝나면, 내 답변 과정에서 드러난 이해 패턴을 종합하여 Ch.1 집필에 활용할 수 있는 insight summary를 만들어 주세요.

### 기초 이해 (논문 내용)

1. **Embedding**: 단어가 벡터가 되는 과정에서, "King - Man + Woman ≈ Queen"이 성립하는 이유를 설명해 보세요. dot product similarity가 여기서 어떤 역할을 하나요?

2. **QKV 메커니즘**: Attention에서 Query, Key, Value 각각의 역할을 비유 없이 수학적으로 설명해 보세요. QK^T를 계산한 뒤 softmax를 취하는 이유는 무엇인가요?

3. **Multi-head Attention**: head를 여러 개로 나누는 것이 single-head 대비 어떤 이점을 주는지, 그리고 head 수를 늘릴 때의 trade-off는 무엇인지 설명해 보세요.

4. **Positional Encoding**: Transformer가 순서 정보를 잃는 구조적 이유와, sinusoidal encoding이 이를 어떻게 보상하는지 설명해 보세요. RoPE는 이것을 어떻게 개선했나요?

5. **Lost in the Middle**: Liu et al.의 실험에서 관찰된 U-shaped curve를 설명해 보세요. 왜 context의 시작과 끝은 잘 활용하고 중간은 놓치는 건가요?

### 심화 이해 (메커니즘 연결)

6. **Attention과 환각**: attention weight가 잘못된 Key에 높은 점수를 줄 때 어떤 일이 벌어지나요? 이것이 agent의 tool call hallucination과 어떻게 연결될 수 있는지 추론해 보세요.

7. **Context window ≠ 이해 용량**: 128K token context window를 가진 모델이 128K token 전체를 동등하게 활용하지 못하는 구조적 이유를 attention mechanism 관점에서 설명해 보세요.

8. **Quantization과 Attention**: 모델을 quantize할 때 attention head가 받는 영향을 설명해 보세요. 왜 어떤 head는 quantization에 강하고 어떤 head는 취약한가요?

### 운영 번역 (Agent Runtime 연결)

9. **System prompt 배치 전략**: Lost in the Middle 현상을 알고 있는 agent 운영자가 system prompt의 핵심 지시를 어디에 배치해야 하는지, 그리고 이것이 왜 "Right Context > Big Context"라는 원칙으로 이어지는지 설명해 보세요.

10. **Attention이 만드는 Agent 실패 모드**: 지금까지 논의한 attention의 구조적 특성(QKV, positional bias, Lost in the Middle)이 장기 실행 agent에서 어떤 실패 패턴을 만들 수 있는지 종합해 보세요. 특히: tool description 혼동, multi-step 추론 중 중간 결과 망각, context 오염 확산 — 이 세 가지를 attention 메커니즘으로 설명할 수 있나요?

---

## 대화 종료 시 요청사항

모든 질문이 끝나면 다음을 생성해 주세요:

1. **이해도 프로필**: 내가 강한 영역과 약한 영역의 요약
2. **독자 학습 경로 제안**: 내 이해 과정에서 드러난 "아하 모먼트"와 "막힌 지점"을 기반으로, Ch.1 독자가 거쳐야 할 최적 학습 순서
3. **운영 번역 원료**: 질문 9~10에서 나온 답변을 정제하여 Ch.1 §6 "Agent Operations를 위한 시사점" 섹션의 초안 재료로 사용할 수 있는 핵심 논점 목록
4. **집필 시 주의점**: 내가 답변 과정에서 범한 오해나 과잉 단순화가 있다면, 이것이 독자에게도 발생할 수 있으므로 Ch.1에서 사전에 방지해야 할 함정 목록

결과 파일을 `dialogue/ch01-attention/` 폴더에 저장해 주세요.
