# Ch.4 대화 프롬프트 — 도구, 추론, 기억: Agent는 어떻게 행동하는가

## 프로젝트 컨텍스트

나는 "Harness Engineering and AgentOps"라는 기술서를 집필 중이다. 이 책은 2026년 상반기 agent runtime의 실패를 관찰하고 측정하는 실험서다. 11챕터, 4-Part 구조이며, Part I(Ch.1~4)은 agent를 만든 역사적 논문들을 기반으로 agent runtime 실패의 기술적 기원을 추적한다.

Ch.4는 Part I의 마지막 챕터로, agent가 실제로 "행동"하는 네 가지 능력(도구 사용, 추론-행동 통합, 자기 반성, 외부 기억)의 학술적 기원을 추적한다. 이 챕터의 마지막 섹션은 "실패 지도"로, 각 능력의 실패 모드와 그것을 측정할 지표를 매핑한다. 이 실패 지도가 Part II Ch.6의 4개 관찰 지표(도구 사용 정확도, instruction following rate, multi-step reasoning depth, context 활용 효율)의 직접적 근거가 된다.

**이 대화의 목적**: 각 논문이 보여주는 "능력"과 그 능력의 "실패 모드"를 동시에 이해한다. 특히 Reflexion과 Ch.11 self-immune의 시간 척도 차이(task 간 학습 vs. task 내 감지)가 핵심 통찰.

---

## 핵심 논문과 자료

1. **Schick et al., "Toolformer: Language Models Can Teach Themselves to Use Tools"** (NeurIPS 2023, ~2,600 citations)
   - 모델이 데이터에서 "여기서 도구를 쓰면 좋다"를 스스로 학습
   - API 호출 구조: name, parameters, return
   - https://arxiv.org/abs/2302.04761

2. **Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models"** (ICLR 2023, ~5,250 citations)
   - Thought-Action-Observation 루프: 추론과 행동의 교차 실행
   - chain-of-thought만으로는 부족한 이유(현실 확인 없음)
   - https://arxiv.org/abs/2210.03629

3. **Shinn et al., "Reflexion: Language Agents with Verbal Reinforcement Learning"** (NeurIPS 2023, ~1,400 citations)
   - Actor → Evaluator → Self-Reflection → 다음 시도
   - 과거 실패를 언어 피드백으로 저장하여 재시도 성공률 향상
   - https://arxiv.org/abs/2303.11366

4. **Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"** (NeurIPS 2020, ~7,000 citations)
   - Query → 관련 문서 검색 → 입력과 결합 → 생성
   - https://arxiv.org/abs/2005.11401

5. **참고 자료**:
   - Function Calling (OpenAI, 2023) — Toolformer의 상용화
   - LATS (Language Agent Tree Search) — Zhou et al., 2023
   - Tree of Thoughts — Yao et al., 2023

---

## 10가지 평가 질문

나의 이해도를 평가해 주세요. 각 질문에 대해 내가 답하면, 정확한 부분과 빈틈을 짚어주고, 빈틈이 있으면 보충 설명 후 다음 질문으로 넘어가 주세요. 모든 질문이 끝나면, 내 답변 과정에서 드러난 이해 패턴을 종합하여 Ch.4 집필에 활용할 수 있는 insight summary를 만들어 주세요.

### 기초 이해 (논문 내용)

1. **Toolformer의 자기 학습**: Toolformer가 "여기서 도구를 쓰면 좋다"를 스스로 학습하는 메커니즘을 설명해 보세요. perplexity 감소를 기준으로 API 호출 삽입 여부를 결정하는 과정이 왜 중요한가요?

2. **Schema validity vs. Semantic correctness**: tool call에서 "형식은 맞지만 의미가 틀린" 호출이 "형식 자체가 틀린" 호출보다 왜 더 위험한가요? 구체적 예시를 들어 설명해 보세요.

3. **ReAct의 Thought-Action-Observation**: 이 루프가 chain-of-thought만의 추론보다 나은 이유를 설명해 보세요. "현실 확인"이 없는 순수 추론이 왜 hallucination에 취약한가요?

4. **Reflexion의 verbal reinforcement**: 수치적 reward 대신 언어 피드백으로 학습하는 것의 장점과 한계를 설명해 보세요. episodic memory에 과거 실패를 저장하는 것이 왜 효과적인가요?

5. **RAG의 작동 원리와 한계**: 텍스트 유사도 검색이 의미적 관련성을 놓치는 구조적 이유를 설명해 보세요. "비슷한 단어를 쓰지만 다른 맥락"의 문서가 검색되면 어떤 문제가 생기나요?

### 심화 이해 (실패 모드 분석)

6. **도구 사용의 연쇄 실패**: agent가 5-step tool chain을 실행할 때, step 2에서 schema는 맞지만 의미가 틀린 호출을 했다면, step 3~5에 어떤 영향이 전파되나요? 이 전파를 중간에 끊으려면 어떤 메커니즘이 필요한가요?

7. **ReAct 장기 실행의 한계**: Thought-Action-Observation 루프를 20회 이상 반복할 때, 초기 Thought의 맥락이 유지되지 않는 현상이 발생합니다. 이것을 Ch.1에서 다룬 attention mechanism과 Lost in the Middle 관점에서 설명해 보세요.

8. **Reflexion vs. Self-immune — 시간 척도의 차이**: Reflexion은 "task A 실패 → 반성 → task A 재시도"입니다. 만약 "task A 실행 중 step 15에서 실패를 감지"해야 한다면, Reflexion의 구조로는 왜 불가능한가요? 이 차이가 왜 중요한가요?

### 운영 번역 (Agent Runtime 연결)

9. **실패 지도 구성**: 지금까지 논의한 네 가지 능력(도구 사용, 추론-행동 통합, 자기 반성, 외부 기억)의 실패 모드를 표로 정리해 보세요. 각 실패 모드를 "측정할 수 있는 지표"와 연결할 수 있나요?

   | 능력 | 학술적 기원 | 실패 모드 | 측정 지표 |
   |------|-----------|----------|----------|
   | 도구 사용 | Toolformer | ? | ? |
   | 추론-행동 | ReAct | ? | ? |
   | 자기 반성 | Reflexion | ? | ? |
   | 외부 기억 | RAG | ? | ? |

10. **Part I 종합 — 네 갈래 기술사의 합류**: Ch.1(attention), Ch.2(compression), Ch.3(alignment), Ch.4(tools/reasoning/memory)를 모두 거쳤습니다. 이 네 갈래가 agent runtime이라는 현장에서 만날 때, 왜 단일 변수로는 실패를 설명할 수 없고 최소한 여러 변수의 상호작용으로 봐야 하는지 종합해 보세요.

---

## 대화 종료 시 요청사항

모든 질문이 끝나면 다음을 생성해 주세요:

1. **이해도 프로필**: 내가 강한 영역과 약한 영역의 요약
2. **실패 지도 완성본**: 질문 9의 표를 대화 내용 기반으로 완성
3. **Reflexion-Self-immune 경계 분석**: 질문 8에서 도출된 시간 척도 차이를 Ch.11 집필용 연결 씨앗으로 정리
4. **Part I → Part II 다리**: 질문 10의 종합 답변을 정제하여 Ch.5 "왜 다섯 변수인가"의 논증 재료로 사용할 수 있는 핵심 논점
5. **집필 시 주의점**: 대화에서 드러난 과잉 단순화나 오해 패턴 → Ch.4에서 독자를 위해 사전 방지할 함정 목록

결과 파일을 `dialogue/ch04-tools-reasoning-memory/` 폴더에 저장해 주세요.
