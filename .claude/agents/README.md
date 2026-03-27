# Project Agents: Harness Engineering Book

이 디렉터리는 `/root/harness-engineering-book` 전용 서브에이전트를 담는다.

## Agents

- `book-ghostwriter`
  - 역할: 섹션 초고 작성 + 주장-근거 매핑
  - 권장 사용: 챕터 집필 라운드

- `book-evidence-checker`
  - 역할: 주장/수치/날짜/실험 ID 검증
  - 권장 사용: 초고 완료 직후 검증 라운드

- `book-style-editor`
  - 역할: CLAUDE.md voice rules 기준 문체/용어 교정
  - 권장 사용: 검증 통과 후 편집 라운드

- `book-managing-editor`
  - 역할: 당일 작업 배치, 우선순위, 범위 통제
  - 권장 사용: 세션 시작 시 작업 오더 생성

## Recommended Workflow

1. `book-managing-editor`로 오늘 작업 오더를 만든다.
2. `book-ghostwriter`로 지정 섹션 초고를 작성한다.
3. `book-evidence-checker`로 검증 리포트를 만든다.
4. `book-style-editor`로 최종 문체/용어를 정리한다.

## Example Prompts

- `book-managing-editor로 오늘 ch04 집필 작업 오더 만들어줘`
- `book-ghostwriter로 ch04 섹션 3 초고 작성해줘`
- `book-evidence-checker로 방금 초고 검증해줘`
- `book-style-editor로 voice rules 기준 편집해줘`
