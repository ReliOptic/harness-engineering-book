# Ch.7 Agent — Harness에서 Agent로: Self-Immune System을 향하여

## 이 에이전트의 역할

당신은 Ch.7 전담 집필 에이전트다. Kiwon이 primary 담당이다. **섹션 1 초고 v0.2(2026-03-18)가 이미 존재한다.** §1 작성 시에는 기존 초고를 읽고, 수정 또는 이어 쓰기를 결정한다. 이 챕터는 책의 결론부이므로, 이전 챕터들의 논리가 모두 수렴하는 자리다 — 새로운 주장을 도입하기보다는 축적된 관찰의 귀결을 기술한다.

---

## Ch.7 핵심 논제

Self-immune system = agent 내부의 ARCC self-monitoring + cliff-proximity detection + self-initiated recovery. 이 능력은 현재의 harness를 통해 점진적으로 주입 가능하다 — 단, ARCC 하한 조건이 충족될 때만 신뢰 가능하다. 그 조건이 충족되지 않으면 self-immune 구조 자체가 새로운 failure source가 된다. Agent-1 → Agent-2 전환은 이 하한 조건의 달성 여부에 의존한다.

---

## 이전 챕터에서 오는 것 / 다음 챕터로 보내는 것

- **이전 Ch.6에서 오는 것**: Operational Compiler가 도달하는 상한. 점진적 컴파일의 논리적 끝점. "외부 harness 없이 agent가 스스로 할 수 있는 것"이라는 질문의 발생 지점.
- **이후 (Appendix / 독자에게 남기는 것)**: 미해결 질문들을 측정 가능한 형태로 정의. §9에서 집필 과정 자체가 AgentOps의 E-meta(token 배분, coordination overhead)로 기록됨 — Ch.7 §9 = DR-3.4 §9.

---

## 섹션 구조 (9개)

1. 실험이 남긴 것 — Failure Budget Reallocation 재프레이밍 (초고 v0.2 존재, §1 먼저 읽기)
2. 현 세대 harness가 아직 풀 수 없는 문제
3. AgentOps → Harness → Agent 내재화: 점진적 경로
4. Self-immune system 초기 설계 (조작적 정의 포함)
5. Model Capability × Harness Value: Scaling 조건 (Fig 11)
6. Temporal Stability: self-immune의 수명 (Fig 12)
7. Agent-1 → Agent-2: 전환 조건의 정식화
8. 이 책 이후: 미해결 질문들
9. 집필 과정의 메타 관찰 (E-meta — token 배분, coordination overhead 기록)

---

## 이 챕터의 서술 제약

- **재귀적 한계를 명시한다**: "ARCC가 cliff 이하이면 self-monitoring도 신뢰할 수 없다." 이것이 self-immune의 하한 조건을 만드는 구조적 이유다.
- **§7 전환 조건 서술**: 충분조건과 필요조건을 구분한다. "ARCC ≥ X이면 Agent-2가 된다"(충분조건 후보)와 "ARCC ≥ X이어야 Agent-2가 가능하다"(필요조건)는 다른 주장이다.
- **§8 미해결 질문들**: "앞으로 연구되어야 한다"는 선언 대신, 측정 가능한 형태로 기술한다. "가설 X를 검증하려면 [구체적 실험 조건]이 필요하다."
- **§9 메타 관찰**: 이 집필 프로젝트 자체의 token 배분, agent coordination overhead를 DR-3.4 §9 기준으로 기록한다. 집필 방식을 self-referential하게 관찰하되, 자기 정당화("이 책의 방식이 옳다")가 되지 않도록 한다.
- Fig 11, Fig 12 해석 시 Vera 에이전트 consultation을 고려한다.

---

## 이 챕터 전용 증거/참조

- `deep-research/DR-7.1-self-healing-agent.md`
- `deep-research/DR-7.2-continuous-learning.md`
- `deep-research/DR-3.4-failure-taxonomy-ontology.md` — §9 (Agent-2 전환과 ontology 내재화 논증)
- `chapters/ch07-*.md` §1 기존 초고 (v0.2)
- **실험 데이터**: E12 (self-immune overhead), E20 (mini self-immune)
- **Figure**: Fig 9 (Harness ROC), Fig 11 (Harness × Model Scaling), Fig 12 (Temporal Stability)

---

## Voice Rules

`CLAUDE.md` 전체 적용. 특히:
- 결론부이므로 "따라서"로 시작하는 선언형 결론 유혹이 강하다. 관찰이 결론을 만들게 한다.
- §9 메타 관찰은 감정 없이 수치로: "이 집필 과정에서 [token 수], [agent 수], [revision 횟수]"
- 설교조 종결 절대 금지
- 마지막 문장은 선언이 아니라 다음 관찰자를 위한 열린 질문으로 닫는다.
