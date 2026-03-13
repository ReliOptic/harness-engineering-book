# Harness Engineering and AgentOps — Project Brain

## 이 프로젝트는 무엇인가
"Observing What Makes Agents Work — and What Breaks Them"
2026년 상반기 agent runtime 현실의 스냅샷이자 실험서.
Beta 마감: 2026-05-13. 한국어 초고 → 영어 번역.

## 글쓰기 원칙 — Voice Rules

**목소리의 기준**: 현장에서 실패를 직접 관찰한 실무자가 쓴 실험 기록. 교수의 강의도 아니고, 컨설턴트의 제안서도 아니다.

**문장 구조**:
- 논리가 흐른다. 아이디어가 다음 아이디어로 이어진다. 헤더로 쪼개고 불릿으로 나열하는 것은 흐름을 끊는다.
- 긴 문장을 두려워하지 않는다. 단, 긴 문장은 복잡한 생각을 담기 위해서이지, 공허한 수식어를 채우기 위해서가 아니다.
- "첫째, 둘째, 셋째"는 리스트가 아니라 연결된 논증이다. 각 항목은 앞 항목을 받아서 한 걸음 더 나아간다.

**무엇을 쓰지 않는가**:
- 선언만 하는 문장: "이것은 X다. Y가 아니다." — 왜 그런지가 없으면 쓰지 않는다.
- 수치 없는 성능 서술: "훨씬 빠르다", "대폭 개선됐다" — 측정값이 없으면 쓰지 않는다.
- Hype: "혁신적", "패러다임 전환", "게임 체인저" — 쓰지 않는다.
- 공허한 결론: "따라서 X가 중요하다" — 실험 결과나 관찰 없이 도달하는 결론은 쓰지 않는다.

**구조적 한계를 숨기지 않는다**:
- 주장 다음에 그 주장이 성립하지 않는 조건을 적는다.
- 실험 설계가 잘못된 경우도 기록한다 (E21).
- 단일 실행에서 일반화할 때는 반드시 잠정적으로 표시한다.

**언어**:
- 한국어 우선. 영어 기술 용어(harness, surface, token budget 등)는 번역하지 않고 그대로 쓴다.
- 수치 없는 성능 서술 금지. 상세 규칙은 `/draft` skill 참고.

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

## 토큰 절약 정책 (Token Policy)
- 세션 시작 시 `/begin [chNN] [section_N]`으로 현재 위치 확인
- 섹션 하나 완료 후 피드백 없이 다음 섹션으로 넘어가지 않는다
- 대화가 10턴 이상이면 `/compact "voice rules, chapter outline, current section progress 유지"` 실행
- 챕터 전환 시 `/clear` — 다음 챕터는 새 세션에서 시작
- `/cost` 로 토큰 현황 수시 확인
- 상세 정책: `token-policy.md` 참고
