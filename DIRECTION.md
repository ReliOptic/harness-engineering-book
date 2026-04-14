# DIRECTION — harness-engineering-book

> 이 문서는 세션 시작 시 CLAUDE.md와 함께 읽는다.
> CLAUDE.md = voice rules + 프로젝트 정체성 (불변)
> DIRECTION.md = 지금 해야 할 일 + 의사결정 로그 (가변)
> 마지막 갱신: 2026-04-04

---

## 현재 상태

- **베타 마감: 2026-04-30 (26일 남음)**
- 총 11장 구성, ~45,000단어 / 목표 ~105,000단어
- Ch.1만 완성 초안. Ch.2-4 스켈레톤. Ch.5-7 v0.1 초안. Ch.8-9 실험 데이터 대기. Ch.10-11 아웃라인.

| 챕터 | 상태 | 긴급도 |
|------|------|--------|
| Preface | v0.2 | 🟡 마지막에 다듬기 |
| Ch.1 | 완성 초안 | ✅ |
| Ch.2-4 | 스켈레톤 | 🔴 4/15까지 풀 드래프트 |
| Ch.5 | v0.1 | 🟡 voice-check 필요 |
| Ch.6 | v0.1 | 🔴 [X] 플레이스홀더 → 실험 데이터 |
| Ch.7 | v2.0 | 🟡 refinement |
| Ch.8 | v0.1 | 🔴 E01-E22 실험 결과 필요 |
| Ch.9 | scaffold | 🔴 Ch.8 의존 |
| Ch.10 | v0.1 | 🟡 §5 확장 |
| Ch.11 | v0.1 | 🟡 self-immune 조건 형식화 |

---

## 크리티컬 패스

```
4/4-4/6   E01 실험 파일럿 (T1 완료, T2 진행)
4/7-4/15  Part I 풀 드래프트 (Ch.2→3→4, dialogue/ 재료 활용)
4/7-4/22  E01-E22 병렬 실행 (OpenRouter + Claude Code)
4/15-4/22 Ch.6 데이터 통합 + Ch.8 실험 결과 기술
4/22-4/28 Ch.9 분석 + Ch.10-11 확장 + 전체 voice-check
4/28-4/30 Preface 최종 + 크로스레퍼런스 감사
```

---

## E01 실험 현황

### 완료

| Task | 난이도 | 모델 | F1 | 날짜 |
|------|--------|------|-----|------|
| T1 Code Review | EASY | claude-opus-4-6 | 1.00 | 2026-04-04 |
| T1 Code Review | MODERATE | claude-opus-4-6 | 1.00 | 2026-04-04 |
| T1 Code Review | FRONTIER | claude-opus-4-6 | 1.00 | 2026-04-04 |

### 다음 실행

- [ ] T2 Multi-Step Reasoning — EASY/MODERATE/FRONTIER (Claude)
- [ ] T1/T2 전 난이도 — SMALL 모델 (OpenRouter: gemini-2.5-flash-lite)
- [ ] T1/T2 전 난이도 — MID 모델 (OpenRouter: gpt-5.4-nano)
- [ ] 모델 능력 지표 복합 점수 계산 + R² ≥ 0.65 검증

### 실험 수정 사항 (반드시 적용)

1. **tasks.py 버그 힌트 주석 제거**: `# Bug 1 (line 15): off-by-one` 같은 주석이 코드에 포함됨. 모델에 전달하기 전에 strip 필요. `experiments/E01-RUNBOOK-LOCAL.md`에 strip_hints.py 스크립트 포함.
2. **T3 fixture 미구현**: `make_t3_repo()` ~50줄 필요. E01은 T1+T2로 충분하지만, 모델 능력 지표 완전 검증에는 T3 필요.

### 결과 파일 위치

```
experiments/results/
  e01-claude-t1-easy.json
  e01-claude-t1-easy-validation.json
  e01-claude-t1-moderate.json
  e01-claude-t1-moderate-validation.json
  e01-claude-t1-frontier.json
  e01-claude-t1-frontier-validation.json
```

---

## 세션 진입 프로토콜

1. 이 파일(`DIRECTION.md`)과 `CLAUDE.md` 읽기
2. `writing-plan.md` §현재_페이즈 확인
3. 작업할 챕터의 `chapter-map.md` 해당 섹션 확인
4. 해당 `dialogue/chNN/` 재료 확인
5. 작업 시작 전 `/begin [chNN] [section]`

---

## 의사결정 로그

| 날짜 | 결정 | 이유 |
|------|------|------|
| 04-04 | Claude Code로 E01 파일럿 실행 | 이번주 토큰 잔량 활용, SOTA 베이스라인 확보 |
| 04-04 | T1 전 난이도 Claude 만점 확인 | SOTA 모델은 code review에서 천장 효과. SMALL 모델 대비가 핵심 데이터 |
| 04-04 | tasks.py 힌트 주석 문제 발견 | 공정성 위해 strip 필수. 기존 파일럿 데이터 유효성 재검토 필요 |
