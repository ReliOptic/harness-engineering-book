# Ch.4 — 도구 호출, 추론, 기억의 실패 경로

> **Part I — Agent Runtime의 기술적 전제**

**한 줄**: Agent의 세 가지 핵심 능력 — 도구 사용, 추론-행동 통합, 자기 성찰과 기억 — 의 학술적 기원을 이해하고, 각 능력이 runtime에서 어떻게 실패하는지를 연결한다.

**Backbone 논문**:
- Schick et al., *Toolformer: Language Models Can Teach Themselves to Use Tools* (NeurIPS 2023, ~2,600 citations)
- Yao et al., *ReAct: Synergizing Reasoning and Acting in Language Models* (ICLR 2023, ~5,250 citations)
- Shinn et al., *Reflexion: Language Agents with Verbal Reinforcement Learning* (NeurIPS 2023, ~1,400 citations)

**Companion**:
- Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* (NeurIPS 2020, ~7,000 citations)

**이 챕터가 도입하는 개념**: function calling, tool schema, chain-of-thought, reasoning-acting loop, verbal reinforcement, self-reflection, retrieval-augmented generation, episodic memory

**챕터 종료 시 독자 상태**: 도구 사용 정확도, instruction following rate, multi-step reasoning depth의 측정이 왜 필요한지를 각 능력의 실패 메커니즘으로 설명할 수 있다. Reflexion이 Ch.11 self-immune의 선행 좌표임을 이해한다.

---

## §1. 도구를 사용하는 법을 스스로 배우기 — Toolformer

**직관 앵커**: 계산기를 쓸 줄 아는 사람과 암산만 고집하는 사람. 도구를 쓸 줄 아는 것이 능력이다 — 하지만 잘못된 도구를 쓰는 것은 능력이 아니라 위험이다.

**정밀 정의**:
- 모델이 학습 데이터에서 "여기서 도구를 호출하면 좋겠다"를 스스로 판단하고, 도구 호출을 삽입하여 학습
- API call의 구조: function name, parameters, return value
- Schema validity (구조 통과)와 semantic correctness (의미 정확)의 구분

**운영 번역**:
- 도구 사용 정확도(tool call accuracy)는 이 구분을 포착한다. Schema를 통과하면서 의미적으로 틀린 호출이 가장 위험하다 — harness가 통과 신호를 보내지만 결과는 틀린 상태.
- Ch.6의 도구 사용 정확도 지표가 이 현상을 측정한다.

**탐구 질문**: schema validity와 semantic correctness 사이의 gap을 자동으로 탐지하는 harness component는 어떤 형태여야 하는가?

<!-- TODO: 본문 집필 -->

---

## §2. 생각하면서 행동하기 — ReAct

**직관 앵커**: 요리할 때 "냉장고를 열어보니 달걀이 있다(관찰) → 오믈렛을 만들자(생각) → 달걀을 꺼낸다(행동)"의 루프. 생각 없이 행동하면 엉뚱한 요리가 되고, 행동 없이 생각만 하면 음식이 나오지 않는다.

**정밀 정의**:
- Thought-Action-Observation 루프. 매 단계에서 reasoning trace를 명시적으로 생성한 후 행동.
- Chain-of-thought만으로는 부족한 이유: 행동의 결과를 관찰하지 않으면 reasoning이 현실과 괴리된다.
- ReAct의 핵심 발견: reasoning과 acting을 interleave하면 hallucination이 감소한다.

**운영 번역**:
- Multi-step task에서 agent가 각 단계의 결과를 관찰하고 다음 추론에 반영하는 것이 multi-step reasoning depth 측정의 기반이다.
- Reasoning trace가 context를 소비한다 — harness overhead와 동일한 trade-off. 추론의 깊이와 token 효율 사이의 긴장.

**탐구 질문**: reasoning trace의 길이와 task completion rate 사이에 최적점이 존재하는가? 그 최적점이 task 복잡도에 따라 이동하는가?

<!-- TODO: 본문 집필 -->

---

## §3. 실패에서 배우기 — Reflexion

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

**탐구 질문**: Reflexion의 episodic memory가 무한히 누적될 때, 유용한 기억과 노이즈를 구분하는 메커니즘은 무엇인가? 이것이 agent의 장기 실행에서 memory management 문제와 어떻게 연결되는가?

<!-- TODO: 본문 집필 -->

---

## §4. 외부 기억 장치 — RAG와 그 너머

**직관 앵커**: 오픈북 시험. 모든 것을 기억할 필요 없이, 필요할 때 정확한 자료를 찾아 참조하면 된다. 문제는 "정확한 자료"를 찾는 것 자체가 어렵다는 점이다.

**정밀 정의**:
- RAG: 질문 → 관련 문서 검색(retrieval) → 검색 결과와 질문을 합쳐 모델에 입력 → 생성
- Lewis et al.의 핵심 기여: retriever와 generator를 end-to-end로 학습
- 한계: 텍스트 유사도 기반 검색은 의미적 관련성을 놓칠 수 있다

**운영 번역**:
- 일반 RAG = 텍스트 유사도로 검색. Ontology RAG = 구조화된 스키마로 검증 후 편입.
- Ch.7에서 정의하는 memory structure (semantic firewall, schema validation)는 RAG의 한계를 보완하는 harness component다.
- Agent의 장기 실행에서 memory mutation이 발생할 때, 스키마 없는 RAG는 오염에 취약하다.

**탐구 질문**: ontology 기반 RAG가 텍스트 유사도 기반 RAG 대비 agent task completion rate에서 측정 가능한 차이를 만드는 조건은 무엇인가?

<!-- TODO: 본문 집필 -->

---

## §5. Agent Operations를 위한 시사점: 세 능력의 실패 지도

| 능력 | 학술 기원 | 실패 양상 | 측정 지표 |
|------|----------|----------|----------|
| 도구 사용 | Toolformer | Schema 통과 + 의미 오류 | 도구 사용 정확도 (Ch.6) |
| 추론-행동 통합 | ReAct | Reasoning trace와 현실의 괴리 | Multi-step reasoning depth (Ch.6) |
| 자기 성찰 | Reflexion | 과거 실패 미반영 / 잘못된 자기 평가 | Self-monitoring accuracy (Ch.11) |
| 외부 기억 | RAG | 관련 없는 문서 검색 / memory 오염 | Context 활용 효율 (Ch.6) |

Part I의 네 챕터가 제공하는 개념적 기반 위에서, Part II는 2026년 현장의 관찰을 기록하고 측정 체계를 구축한다.

**탐구 질문**: 네 가지 능력의 실패가 동시에 발생할 때, 어떤 실패를 먼저 해결하는 것이 전체 task completion rate에 가장 큰 영향을 미치는가? 이 우선순위가 task 유형에 따라 달라지는가?

<!-- TODO: 본문 집필 -->
