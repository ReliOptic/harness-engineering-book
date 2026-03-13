# /draft [chNN] [section_number]

해당 챕터의 특정 섹션 초고를 작성한다.

## 실행 단계

1. `chapters/chNN-xxx.md`에서 해당 섹션의 outline 계획을 읽는다.
2. 관련 재료를 읽는다:
   - `deep-research/DR-N.N-xxx.md` (해당 챕터 배정 DR)
   - `experiments/axis-N/ENN-xxx.md` (관련 실험 로그)
   - `evidence/case-studies/` (관련 사례 노트)
   - `field-dispatches/` (관련 태그 dispatch)
3. 섹션을 작성한다.
4. 작성 후 사용자에게 보여주고 피드백을 기다린다.

## 작성 규칙

### 문체
- Builder-operator voice. 사람이 사람에게 말하는 톤.
- 한 문장 40자 이하 목표. 복문보다 단문 2개.
- 한 단락 3~5문장. 하나의 생각 = 하나의 단락.
- "~하는 것이다", "~라고 할 수 있다" 회피. 직접 말한다.

### 구조
- 섹션 시작: 핵심 메시지를 한 문장으로.
- 전개: 관찰 → 측정 결과 → 해석 → 시사점.
- 실험 인용: "E14에서 관찰한 바에 따르면..." + 구체적 수치.
- Dispatch 인용: "FD-001 MiroFish의 등장은..."
- 5변수 참조: "이 실패의 1차 병목은 [변수명]이었다."
- 반례: 주장 후 "그러나 이것이 항상 성립하지는 않는다."
- 스냅샷 마커: "2026년 3월 기준으로"
- 섹션 끝: 다음 섹션으로의 전환 문장.

### 금지
- hype 표현 금지 ("revolutionary", "game-changing", "unprecedented")
- 수치 없는 성능 서술 금지 ("성능이 떨어졌다" → "tool call 성공률이 87%에서 54%로")
- 직접 인용 없이 DR 결과 직접 인용 금지 (DR이 인용한 원문을 찾아 인용)

## 사용 예시

```
/draft ch01 1
/draft ch04 3
```
