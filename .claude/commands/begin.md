# /begin [chNN] [section_N]

새 챕터 세션을 시작할 때 실행한다. 현재 위치를 확인하고 다음 작업을 명확히 한다.

## 실행 단계

1. `chapters/chNN-xxx.md`에서 **섹션 N의 outline 블록만** 읽는다.
   - 파일 전체를 읽지 않는다. 해당 섹션 항목만 읽는다.
   - section_N을 생략하면 완성되지 않은 첫 섹션을 찾아 거기서 시작한다.
2. 챕터 파일에서 **완성된 섹션 수**를 확인한다 (헤더나 체크 표시 기준).
3. 다음 작업을 제안한다:
   - "현재: ch0N 섹션 M까지 완성. 다음: 섹션 M+1. `/draft chNN M+1` 로 시작합니다."

## 규칙

- CLAUDE.md는 세션 시작 시 이미 로드됨 — 재읽기 없음.
- `chapter-map.md`, `writing-plan.md` 등 전체 파일을 읽지 않는다.
- 단순 현황 파악이 목적이다. 분량 최소화.

## 사용 예시

```
/begin ch01 1       # ch01 섹션 1부터 시작
/begin ch03         # ch03 미완성 섹션 자동 탐지
/begin ch04 3       # ch04 섹션 3 이어 쓰기
```

## 세션 관리 안내

- 섹션 하나 완료마다 피드백 대기 → 승인 후 다음 섹션
- 10턴 이상: `/compact "voice rules, chapter outline, current section progress 유지"`
- 챕터 완료: `/clear` 후 다음 챕터를 새 세션에서 시작
