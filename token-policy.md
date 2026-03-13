# 토큰 절약 정책 (Token Policy)

이 문서는 harness-engineering-book 집필 전 모든 팀원이 읽는다.
집필은 약 50회의 `/draft` 호출로 완성된다. 토큰 관리 없이는 후반부로 갈수록 비용이 기하급수적으로 증가한다.

---

## 왜 섹션 단위인가

Claude Code는 대화 히스토리 전체를 매 턴 input으로 받는다. 챕터 전체를 한 세션에서 쓰면:
- 1섹션 완료 시점: input ~5K tokens
- 7섹션 완료 시점: input ~35K tokens (누적 7배)

섹션 단위로 나누고 챕터 전환 시 `/clear`를 쓰면 누적 증가를 차단한다.

---

## 캐싱 자동 작동 원리

Claude Code는 API 레벨에서 prompt caching을 자동 적용한다.
- cache hit: 0.1× 비용 (90% 절감)
- 캐시 대상: 대화 초반의 안정적인 context (CLAUDE.md, 자주 읽는 파일)
- **CLAUDE.md를 200줄 이하로 유지하는 이유**: 안정적인 파일일수록 캐시 효과 극대화

캐싱이 작동하는지 확인: `/cost` 실행 후 `cache_read_input_tokens`가 있으면 작동 중.

---

## 세션 시작/종료 의식

### 챕터 시작 (새 세션)
```
/begin chNN 1
```
- 챕터 파일에서 섹션 1 outline만 읽는다
- CLAUDE.md는 이미 세션에 로드됨 — 재읽기 없음

### 섹션 완료 후
- 피드백 주고 승인 → `/draft chNN N+1`
- 다음 섹션으로 넘어가기 전 반드시 멈춘다

### 대화가 10턴 이상이면
```
/compact "voice rules, chapter outline, current section progress 유지"
```

### 챕터 전환 시
```
/clear
```
다음 챕터는 무조건 새 세션에서 시작.

---

## 최소 읽기 원칙

| 단계 | 읽는 것 | 읽지 않는 것 |
|------|---------|------------|
| `/begin` | 해당 섹션 outline 블록 | 챕터 파일 전체 |
| `/outline` | chapter-map 해당 항목, writing-plan 해당 섹션, DR README (목록만) | DR 파일 내용 |
| `/draft` | outline에 명시된 DR/실험만 | 명시되지 않은 파일 |

**추측으로 파일 읽기 금지.** outline에 "DR-1.2"가 적혀 있을 때만 DR-1.2를 읽는다.

---

## 모니터링

- `/cost`: 누적 토큰 현황. `cache_read_input_tokens` 확인.
- 세션당 input token이 20K를 넘으면 `/compact` 또는 `/clear` 고려.
- 챕터 완료 후 항상 `/clear`로 초기화.
