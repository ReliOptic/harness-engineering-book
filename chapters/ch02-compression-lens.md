# Ch.2 — 압축 렌즈: 모든 언어 모델은 압축기다

> **Part I — 기반: Agent를 만든 논문들**

**한 줄**: 언어 모델이 확률적 텍스트 생성기인 동시에 압축 알고리즘이라는 사실을 정보이론으로 보이고, 이 등가성이 agent runtime 현상을 읽는 하나의 해석 렌즈가 됨을 보여준다. 이 챕터는 HOR이나 모델 관찰 지표의 직접 근거를 세우는 것이 아니라, Part II 이후에서 사용할 정보이론적 어휘를 제공한다.

**Backbone 논문**:
- Delétang et al., *Language Modeling Is Compression* (ICLR 2024)
- Shannon, *A Mathematical Theory of Communication* (1948)

**이 챕터가 도입하는 개념**: information content, entropy, cross-entropy, KL divergence, arithmetic coding, autoregressive chain rule, bits-per-byte, compression ratio

**챕터 종료 시 독자 상태**: "왜 더 좋은 모델이 더 잘 압축하는가"를 수식으로 설명할 수 있고, 이것을 prompt 최적화와 모델 비교에 적용할 수 있다.

> **참조 구현**: `compression lens 챕터 -learning curve reference.docx`의 한국어 적응 + 확장. 영어 원고의 7개 섹션 구조를 유지하되, 한국어 voice rule 적용 및 이 책의 5변수 프레임워크와의 연결을 강화한다.

---

## §1. 정보량: 놀라움을 측정하는 방법

**직관 앵커**: "오늘 아침 해가 떴다" vs. "7월 서울에 3미터 눈이 내렸다" — 놀라운 사건이 더 많은 정보를 담는다.

**정밀 정의**: I(x) = −log₂(p), bit 단위, Shannon의 세 가지 필요조건(연속, 단조, 가법성)

**운영 번역**: 모델이 다음 토큰을 95% 확신으로 예측하면 ~0.07 bits, 1% 확신이면 ~6.6 bits. 예측 능력이 곧 비용이다.

**탐구 질문**: agent가 tool call을 생성할 때, 각 토큰의 정보량 분포는 자연어 생성과 어떻게 다른가?

<!-- TODO: 본문 집필 -->

---

## §2. 엔트로피: 놀라움의 평균 비용

**직관 앵커**: 공정한 동전 vs. 편향된 동전(앞면 90%). 편향된 동전은 예측 가능하므로 기록에 필요한 비트가 적다.

**정밀 정의**: H(P) = −Σ p(x) · log₂ p(x), Shannon의 소스 코딩 정리 — 엔트로피가 압축의 이론적 하한

**운영 번역**: 모델의 엔트로피가 낮다 = 예측이 정확하다 = 데이터가 잘 압축된다. Temperature가 이 엔트로피를 조절하는 운영 파라미터.

**탐구 질문**: temperature 조절이 agent의 tool call accuracy와 creativity 사이의 trade-off를 어떤 곡선으로 만드는가?

<!-- TODO: 본문 집필 -->

---

## §3. Cross-Entropy와 KL Divergence: 틀린 모델의 대가

**직관 앵커**: 편향된 동전(90:10)을 공정한 동전이라고 가정하면 기록에 0.53 bits/flip을 낭비한다. 이 낭비가 "모델이 틀린 정도"다.

**정밀 정의**: H(P,Q) = −Σ p(x) · log₂ q(x), D_KL(P‖Q) = H(P,Q) − H(P)
- Cross-entropy = 진짜 엔트로피 + 모델 오차에 대한 벌금
- 학습 loss = cross-entropy loss. 학습 = cross-entropy 최소화 = KL divergence 최소화

**운영 번역**: prompt drift를 KL divergence의 언어로 읽을 수 있다 — 의도한 행동 분포와 실제 출력 분포 사이의 괴리를 정보량으로 표현하는 하나의 방법.

**탐구 질문**: 장기 실행 agent에서 prompt drift가 누적될 때, KL divergence의 증가 곡선은 선형인가 비선형인가?

<!-- TODO: 본문 집필 -->

---

## §4. Arithmetic Coding: 확률이 압축된 파일이 되는 과정

**직관 앵커**: 숫자 선 [0, 1)을 확률에 비례하여 쪼개는 과정. 높은 확률의 토큰은 넓은 구간 = 적은 비트, 낮은 확률의 토큰은 좁은 구간 = 많은 비트.

**정밀 정의**: interval narrowing, 압축 크기 ≈ cross-entropy

**운영 번역**: 좋은 예측 = 좋은 압축. 이 등가성이 모델 비교의 보편 척도를 제공한다.

**탐구 질문**: arithmetic coding의 구조와 autoregressive generation의 구조가 동형이라는 사실이 모델 평가 방법론에 어떤 함의를 갖는가?

<!-- TODO: 본문 집필 -->

---

## §5. Autoregressive 구조: 언어 모델은 태생적 압축기다

**정밀 정의**: P(x_t | x_1,...,x_{t-1}), chain rule, arithmetic coding과의 구조적 동일성
- 생성(generation)과 압축(compression)은 같은 연산의 다른 사용
- 생성: 분포에서 sampling → 새 텍스트 생성
- 압축: 실제 토큰의 bit cost 기록 → 기존 텍스트 인코딩

**운영 번역**: 토큰별 bit cost가 균일하지 않다. "The capital of France is Paris"에서 "Paris"는 ~0.1 bits, "The"는 ~8 bits. 예측 가능한 토큰은 거의 무료.

**탐구 질문**: agent의 structured output(JSON, function call)에서 예측 가능한 토큰(괄호, 키 이름)과 예측 불가능한 토큰(값)의 bit cost 분포는 어떤 형태인가?

<!-- TODO: 본문 집필 -->

---

## §6. Bits-per-Byte: 모델을 비교하는 보편 척도

**정밀 정의**: bits-per-byte = 압축 후 총 비트 ÷ 원본 바이트 수. Tokenizer에 무관한 비교 가능.
- Compression ratio = 압축 크기 ÷ 원본 크기. Black-box 모델에도 적용 가능.
- 두 척도의 관계: bits-per-byte ≈ 8 × compression ratio

**운영 번역**: 어떤 모델이 더 나은가의 보편 답: 더 잘 압축하는 모델이 더 나은 모델이다.

**탐구 질문**: bits-per-byte가 agent task completion rate과 어떤 상관을 보이는가? 이 상관이 task 복잡도에 따라 달라지는가?

<!-- TODO: 본문 집필 -->

---

## §7. Agent Operations를 위한 시사점

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

**탐구 질문**: CLAUDE.md를 lossy compression artifact로 본다면, 압축률과 agent performance 사이의 최적점은 어디에 있는가?

<!-- TODO: 본문 집필 -->
