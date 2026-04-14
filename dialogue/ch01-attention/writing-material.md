# Ch.1 Dialogue — Writing Material

> 생성일: 2026-04-03
> 용도: Ch.1 §1~§6 본문 집필의 초안 재료

---

## §1 용 재료: Embedding과 유사도

**독자 진입점**: "King - Man + Woman ≈ Queen"은 대부분의 독자가 알고 있다. 여기서 시작하되, dot product similarity로 즉시 이동해야 한다.

**저자 대화에서 추출한 전환 문장 후보**:
> 벡터 산술이 작동한다는 사실은 직관적으로 받아들이기 쉽다. 그러나 "두 벡터의 유사도를 어떻게 측정하는가"라는 질문에서 대부분의 독자는 멈춘다. Dot product는 두 벡터가 같은 방향을 가리킬수록 높은 값을 반환한다. 이것이 attention의 첫 번째 연산이다.

**집필 지시**: Dot product를 2차원 벡터 그림으로 먼저 보여준 후, 고차원으로 확장하는 서술 순서.

---

## §2 용 재료: QKV와 Softmax

**핵심 발견**: 저자가 "sparsity"와 attention의 연결을 못 만들었다. 이것은 softmax의 "winner-take-most" 성질을 설명하지 않으면 자연스럽게 발생하는 빈틈이다.

**서술 순서 (대화에서 검증됨)**:
1. "차원(dimension)"이란 무엇인가 — 물리적 공간이 아니라 "특성 축"
2. Q = "내가 찾는 것", K = "라벨", V = "실제 내용"
3. Q × K^T = 유사도 점수 행렬
4. Softmax = 점수를 확률로 변환 → **여기서 sparsity 발생**
5. Softmax(Q × K^T) × V = "관련 있는 내용에 집중한 결과"

**시각화 제안**: Softmax 온도(τ) 실험
- τ = 1.0: 비교적 고른 분포
- τ = 0.1: 하나에 집중, 나머지 거의 0
- "이것이 attention의 '집중'이다"

**저자 대화에서 추출한 전환 문장 후보**:
> Softmax는 단순히 숫자를 정규화하는 함수가 아니다. 높은 점수와 낮은 점수의 차이를 증폭시키는 함수다. 하나가 충분히 높으면 나머지를 거의 0으로 만든다. 이것이 attention이 "집중"할 수 있는 이유이며, 동시에 "잘못된 곳에 집중"할 수 있는 이유이기도 하다.

---

## §3 용 재료: Multi-head와 Positional Encoding

**Multi-head 핵심 교정**: 저자(그리고 예상 독자)가 multi-head를 "병렬처리 속도 향상"으로 이해했다. 실제 핵심은 "서로 다른 관계 유형을 동시에 포착"이다.

**예시 제안**: 
- Head A: "이 단어의 구문적 역할은?" (주어-동사 관계)
- Head B: "이 단어의 의미적 연관은?" (동의어, 반의어)
- Head C: "이 단어의 위치적 근접성은?" (인접 단어)

**Positional Encoding 서술 순서** (저자가 완전한 빈칸이었으므로 ground-up):
1. "Transformer는 왜 순서를 모르는가" — self-attention은 집합 연산, 순서 개념 없음
2. "순서가 없으면 무엇이 깨지는가" — "개가 사람을 물었다" vs "사람이 개를 물었다"
3. Sinusoidal: 고정된 파형으로 위치 정보 주입. 장점(무한 길이 일반화), 한계(상대적 거리 표현 어려움)
4. RoPE: 회전을 이용해 상대적 위치 관계를 직접 인코딩. 현대 모델의 표준.

**저자의 Q4 후속 질문에서 나온 교정 재료**:
- "d_model이 generation에 영향을 주나 learning에만 영향을 주나?" → 둘 다. 학습 시 표현력 결정, 추론 시 동일 구조 사용.
- "base model의 방향 없음이 positional encoding과 관련 있나?" → 아니다. 순서 인식(positional)과 목적 부여(training objective, Ch.3)는 별개. 이 혼동은 Ch.1에서 반드시 차단해야 한다.

---

## §4 용 재료: Lost in the Middle과 컨텍스트의 실효 활용

**저자의 비판적 시각 활용**: 저자가 Liu et al.을 "heuristic"이라고 과소평가한 것은 독자에게도 발생할 반응이다. Ch.1에서 이 반응을 예상하고 선제적으로 다뤄야 한다.

**서술 구조**:
1. Liu et al.의 실험 설계 소개 (20개 모델, 다양한 길이, 정량적 측정)
2. U-shaped curve 제시
3. "serial position effect의 analogy일 뿐인가?" → 아니다, 실험적으로 측정된 현상
4. 2023→2026 진전: 윈도우 크기 확대, valley 깊이 감소, **그러나 구조 자체는 존속**
5. "컨텍스트 윈도우 크기 ≠ 이해 용량" — 이것이 Ch.1의 핵심 긴장

**저자 대화에서 추출한 비유**:
> "200K 윈도우는 기술적 극복이 아니라 큰 깔때기다."

이 비유를 Ch.1에서 직접 사용할 것을 권장. 독자가 즉시 이해할 수 있는 직관 앵커.

---

## §5 용 재료: Autoregressive 추론과 KV Cache

**핵심 경험 앵커**: "AI가 잘못된 방향으로 가면 새 채팅을 연다" → 이것을 Ch.1 독자 경험으로 활용.

**서술 구조**:
1. 학습 vs 추론의 attention 차이 (병렬 vs 순차, causal mask)
2. Autoregressive: 자기 출력을 다음 입력으로 → 오류 전파 구조
3. "새 채팅을 여는 이유" = KV Cache 초기화
4. KV Cache의 물리적 비용: 200K 토큰 → 수 GB GPU 메모리
5. Agent 장기 실행에서 KV Cache가 compute 병목이 되는 조건

**용어 정리 박스 (대화에서 발견된 혼동 기반)**:

| 용어 | 의미 | Agent 맥락 |
|------|------|------------|
| Autoregressive | 이전 출력 → 다음 입력 | 토큰 생성, tool call 순차 실행 |
| Recursive | 자기 자신 호출, 들어갔다 나옴 | Reflexion, self-critique 루프 |
| Regression | 통계적 회귀분석 | 모델 능력 지표 모델링 (Ch.8) |

---

## §6 용 재료: Agent Operations를 위한 시사점

**저자가 독립적으로 도출한 핵심 논점** (Q9에서):
1. 사용자는 컨텍스트 축적을 원한다 (매번 입력하는 것은 낭비)
2. LLM은 무엇을 버려야 할지 모른다 (선택적 망각 메커니즘 부재)
3. 컨텍스트 축적 자체에 별도 학습/정제 레이어가 필요하다
4. 이 "별도 레이어"가 harness의 memory boundary / context compression 역할이다

**운영 번역 논점 목록**:

| Attention 특성 | Agent 실패 모드 | Harness 대응 |
|---------------|----------------|-------------|
| Softmax sparsity | 잘못된 tool에 attention 집중 → tool call hallucination | Tool call 검증/차단 레이어 |
| Lost in the Middle | 장기 실행 시 중간 지시 망각 → silent drift | 핵심 지시 반복 주입, context 재구성 |
| Autoregressive 오류 전파 | 한번 잘못되면 되돌아오지 못함 | Recovery hook, 외부 recursive 루프 |
| KV Cache 누적 | 장기 실행 시 메모리 병목 → 시스템 마비 | Memory boundary, context window 관리 |
| Attention ≠ 이해 | 상관관계 기반 응답 → 논리적 오류 미감지 | Evaluation hook, output 검증 |

**Ch.1 마지막 문장 후보** (저자 Q10 답변 정제):
> 컨텍스트 윈도우가 아무리 커져도, attention의 통계적 본성 때문에 모델은 모든 것을 균등하게 이해하지 못한다. 이 간극이 harness가 존재해야 하는 이유이며, 이 책의 나머지가 측정하려는 대상이다.

---

## 대화에서 발견된 추가 집필 소재

1. **"사람은 휴리스틱하게 잊는다"** (Q9): 인간의 선택적 망각과 LLM의 무차별적 토큰 보존의 대비. Ch.1 서두 또는 Ch.4(기억)에서 활용 가능.

2. **"매일 바뀌는 업무를 매번 입력하는 것은 낭비"** (Q10): Agent에 대한 사용자 기대와 현실의 간극. Ch.5 도입부에서 활용 가능.

3. **"토큰화 전 필터 레이어"** (Q6): Prompt preprocessing (LLMLingua, query rewriting)의 직관적 도출. Ch.10 Operational Compiler의 context compression 모듈과 직접 연결.

4. **"자주 반복되는 단어가 noise로 작용"** (Q6): Attention sink 현상의 직관적 포착. §2 또는 §4에서 활용 가능.
