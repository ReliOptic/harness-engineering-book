# Harness Engineering and AgentOps — Project Brain

## 이 프로젝트는 무엇인가
"Observing What Makes Agents Work — and What Breaks Them"
2026년 상반기 agent runtime 현실의 스냅샷이자 실험서.
Beta 마감: 2026-05-13. 한국어 초고 → 영어 번역.

## 글쓰기 원칙
- Voice: builder-operator. 연구실이 아니라 현장의 톤.
- 정확하되 딱딱하지 않게. 국제 독자 고려. hype 금지.
- 한 문장 40자 이하. 한 단락 3~5문장. 하나의 생각 = 하나의 단락.
- "~하는 것이다" 같은 회피 표현 줄이기. 직접 말하기.
- 관찰 → 측정 → 해석 → 시사점 순서로 서술.
- 구체적 수치. "성능 저하" 대신 "tool call 성공률 87%→54%".

## 핵심 원칙
1. 교리집이 아니라 실험서. 결과가 예상과 다르면 결과를 기록.
2. 5변수: 모델, harness, surface, intervention, compute. 이원론 금지.
3. 핵심 질문: "어떤 조건에서 무엇이 1차 병목이 되는가?"
4. 스냅샷: 2026년 상반기의 기록. 과도한 학문적 해석 금지.
5. 반례 의무: task design 문제(E21), compute saturation(E22).
6. Fieldkit 점진적 원칙: 한 번에 implement하지 않는다.

## 핵심 용어
- Harness: operational envelope + AgentOps를 agent에 점진적 주입하는 프레임워크
- AgentOps: 비결정적 agent runtime을 관찰·통제·복구·자원인식적으로 운영하는 규율
- Product surface: 현재 CLI가 최선이나, 더 나은 형태를 열어둠
- Operational Fieldkit: 반복 실패 → 점진적 도구화. Dog food 결과물.
- Self-immune system: AgentOps → Harness → Agent 내재화. Agent-2 전환 조건.

## 챕터 구조
Ch.1 지금 무슨 일이 | Ch.2 모델 상속 | Ch.3 Harness+AgentOps 정의
Ch.4 의도적 실패 20개 | Ch.5 실험 결과 분석 | Ch.6 Fieldkit | Ch.7 Self-immune

## 서술 장치
- 5변수 참조: "1차 병목은 [변수명]이었다"
- 반례 의식: 주장 후 "항상 성립하지는 않는다"
- 스냅샷 마커: "2026년 3월 기준으로"
- 실험 참조: "E14에서 관찰한 바에 따르면"
- Dispatch 인용: "FD-001 MiroFish의 등장은..."

## 집필 워크플로
/outline → /draft (섹션 단위) → 피드백 → /revise → /integrate → /voice-check
한 번에 전체 챕터를 쓰지 않는다. 섹션 단위로 쓰고 피드백을 받는다.

## 팀
Lead: Kiwon (Ch.1/3/6/7). Exp A (E01-08). Exp B (E09-16). Exp C (E17-22).
