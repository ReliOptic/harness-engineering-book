# Ch.7 대화 프롬프트 — Harness Engineering과 AgentOps: FBR 정량 프레임

## 프로젝트 컨텍스트

나는 "Harness Engineering and AgentOps"라는 기술서를 집필 중이다. 이 책은 2026년 상반기 agent runtime의 실패를 관찰하고 측정하는 실험서다. 11챕터, 4-Part 구조이며, Part II(Ch.5~7)는 관찰과 측정의 프레임워크를 세운다.

Ch.7은 harness engineering과 AgentOps를 조작적으로 정의하고, **실패 재분류(FBR)** 개념을 통해 harness의 효과를 측정하는 프레임을 제시한다. FBR의 핵심 관찰: "harness를 추가하면 실패가 줄어드는 게 아니라, 실패의 유형이 바뀐다." 이 관찰을 정량적으로 포착하는 프레임이 이 챕터의 독창적 기여다.

**이 대화의 목적**: FBR 개념을 정량화할 수 있는 측정 프레임을 설계한다. "좋은 재배분"과 "나쁜 재배분"을 구분하는 기준, harness overhead(harness overhead)와의 trade-off, 그리고 Ch.8 실험의 사전 등록 가설을 구체화한다.

---

## 핵심 자료

1. **OpenAI, "Harness Engineering"** (2026)
   - Operational envelope 개념
   - Codex + terminal 결합의 신뢰도 향상 사례

2. **이 책의 기존 정의 (chapters/ch03-harness-and-agentops-defined.md)**:
   - Harness: 런타임에서 메모리 보호, 권한 관리, 복구 메커니즘, 평가 hook을 제공하는 운영적 포위망
   - AgentOps: 관찰 가능성, 통제 가능성, 복구 가능성, 자원 인식을 갖춘 운영 규율
   - harness overhead(Harness Overhead Ratio), MTTR(Mean Time To Resolution), HER(Human Escalation Rate)

3. **관련 학술 자료**:
   - Chaos Engineering (Netflix, Principles of Chaos) — 의도적 장애 주입의 방법론
   - SRE(Site Reliability Engineering) — Error Budget 개념의 원조
   - Lewis et al., RAG (2020) — Ch.7에서 Ontology RAG로 확장

4. **Part I 연결점**:
   - Ch.3 §4: 학습-런타임 경계 → harness 필요성의 구조적 근거
   - Ch.4 §4: RAG 한계 → Ontology RAG 필요성
   - Ch.2: KL divergence → prompt drift 측정 도구

---

## 10가지 평가 질문

나의 이해도를 평가해 주세요. 각 질문에 대해 내가 답하면, 논리적 빈틈을 짚어주고, 정량화가 부족하면 "이걸 어떻게 숫자로 표현할 수 있나?"라고 추가 질문을 던져 주세요.

### Harness와 AgentOps 정의 (개념 이해)

1. **Harness vs. Guardrails vs. Scaffolding vs. Orchestration**: 이 네 용어가 현재 업계에서 혼용되고 있습니다. 각각의 차이를 정의하고, harness가 나머지 셋과 구분되는 핵심 속성을 설명해 보세요.

2. **AgentOps의 4가지 속성**: 관찰 가능성(observability), 통제 가능성(controllability), 복구 가능성(recoverability), 자원 인식(resource-awareness)을 각각 agent runtime 맥락에서 설명해 보세요. SRE의 observability/reliability와 어떤 점에서 다른가요?

3. **Ontology RAG vs. 일반 RAG**: Ch.4에서 RAG의 한계(텍스트 유사도 ≠ 의미적 관련성)를 확인했습니다. Ontology RAG가 이 한계를 어떻게 보완하는지, 스키마 검증이 왜 필요한지 설명해 보세요.

### 실패 재분류 (핵심 개념)

4. **FBR의 직관**: "harness를 추가했는데 실패 횟수가 같다"는 관찰을 어떻게 해석해야 하나요? "harness가 효과가 없다"와 "실패 유형이 바뀌었다"를 어떻게 구분할 수 있나요?

5. **실패 유형 분류**: agent runtime에서 발생하는 실패를 유형별로 분류해 보세요. 예를 들어: 치명적 중단(crash) / 잘못된 방향 진행(silent drift) / 품질 저하(degradation) / 자원 소진(exhaustion). harness가 추가되면 이 유형 간의 비율이 어떻게 바뀌나요?

6. **"좋은 재배분" vs. "나쁜 재배분"**: 치명적 중단이 줄고 품질 저하가 늘었다면, 이것은 좋은 재배분인가요? 반대로, 잘못된 방향 진행(silent drift)이 늘었다면? 좋고 나쁨을 판단하는 기준을 제안해 보세요.

7. **FBR을 숫자로 표현하기**: 실패 유형별 비율의 변화를 정량적으로 포착하는 방법을 설계해 보세요. harness-on과 harness-off 조건에서의 실패 유형 분포를 비교하려면 어떤 측정이 필요한가요?

### 운영 지표와 실험 설계

8. **harness overhead(Harness Overhead Ratio)의 최적점**: harness가 소비하는 token overhead가 전체 token budget의 몇 %일 때 가장 효율적인가요? overhead가 너무 낮으면 어떤 문제가 생기고, 너무 높으면 어떤 문제가 생기나요? 최적점을 찾는 방법을 제안해 보세요.

9. **MTTR과 HER의 관계**: Mean Time To Resolution이 줄면 Human Escalation Rate도 줄어야 할 것 같지만, 실제로는 어떤 조건에서 MTTR이 줄어도 HER이 늘어나는 역설이 발생할 수 있나요?

10. **Ch.8 실험 가설 사전 등록**: FBR, harness overhead, MTTR, HER를 사용하여 Ch.8의 22개 실험에서 검증할 핵심 가설 3개를 작성해 보세요. 각 가설은 "조건 X에서 변수 Y를 조작하면 지표 Z가 [방향]으로 변할 것이다" 형식으로 작성하세요.

---

## 대화 종료 시 요청사항

모든 질문이 끝나면 다음을 생성해 주세요:

1. **이해도 프로필**: 내가 강한 영역과 약한 영역의 요약
2. **FBR 정량 프레임 설계서**: 대화에서 도출된 실패 유형 분류 + 좋은/나쁜 재배분 판단 기준 + 측정 방법론을 Ch.7 §4 초안 재료로 정리
3. **harness overhead 최적점 탐색 프레임**: 질문 8에서 도출된 overhead trade-off 분석을 Ch.9(실험 결과)에서 검증 가능한 형태로 정리
4. **실험 가설 목록**: 질문 10에서 작성한 가설을 Ch.7 §6(실험 프레임 사전 등록)에 직접 삽입할 수 있는 형태로 정리
5. **용어 정합성 점검**: 대화에서 사용된 harness/AgentOps/FBR/harness overhead/MTTR/HER의 정의가 glossary.md와 일치하는지 확인할 수 있는 대조표

결과 파일을 `dialogue/ch07-harness-fbr/` 폴더에 저장해 주세요.
