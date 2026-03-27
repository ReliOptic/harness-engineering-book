# Field Dispatch System — 현장 기록 시스템

> 집필 60일 동안 빠르게 전개되는 상황을 스냅샷으로 잡아두는 시스템.
> 팀원 누구나 5분 안에 기록할 수 있어야 한다.
> 이 기록 자체가 책의 일부가 된다 — "스냅샷 안의 스냅샷".

---

## Field Dispatch란 무엇인가

전쟁터의 전문(戰文)처럼, 현장에서 일어나는 일을 짧고 정확하게 기록한다.

**Field Dispatch는 분석이 아니다.** 기록이다.
"이런 일이 일어났다. 우리 책과 이렇게 연결된다." — 이것만 적는다.
분석은 나중에 챕터에서 한다.

---

## Dispatch 한 건의 구조

```markdown
# FD-YYYY-MM-DD-NNN: [한 줄 제목]

**Date:** YYYY-MM-DD
**Reporter:** [팀원 이름]
**Source:** [URL 또는 출처]
**Category:** [카테고리]

## 무슨 일이 일어났는가 (3문장 이내)

[사실만. 의견 없이.]

## 우리 책과 어떻게 연결되는가 (3문장 이내)

[5변수 중 어떤 것과 관련되는지, 어떤 챕터에 영향을 주는지]

## 즉시 행동이 필요한가

- [ ] Deep research 필요 → DR-ID 부여
- [ ] 실험 설계 변경 필요
- [ ] 챕터 내용 수정 필요
- [x] 기록만 해두면 됨 (대부분 이것)

## Tags

`#태그1` `#태그2`
```

---

## 카테고리

| 카테고리 | 설명 |
|----------|------|
| `NEW_PROJECT` | 새로운 agent 관련 프로젝트 등장 |
| `MODEL_RELEASE` | 새 모델 출시 또는 주요 업데이트 |
| `FRAMEWORK_CHANGE` | Agent 프레임워크의 주요 변경 |
| `RESEARCH_PAPER` | 관련 논문 또는 벤치마크 발표 |
| `INDUSTRY_MOVE` | 투자, 인수, 전략적 발표 |
| `TOOLING` | Agent 관련 도구 출시/업데이트 |
| `INCIDENT` | Agent 시스템의 주요 실패/사건 |
| `CONCEPT` | 새로운 개념이나 용어의 부상 |

---

## Dispatch → 챕터 연결 태그

| 태그 | 관련 챕터 |
|------|----------|
| `#ecosystem` | Ch.1 (생태계 스냅샷) |
| `#model` | Ch.2 (모델 상속) |
| `#harness` | Ch.3 (harness 정의) |
| `#compute` `#constraint` | Ch.4 (제약 실험) |
| `#agentops` `#tooling` | Ch.5 (AgentOps 실무) |
| `#operational-compiler` | Ch.6 (Operational Compiler) |
| `#swarm` `#self-immune` `#future` | Ch.7 (self-immune, 미래) |

---

## 팀 운영 규칙

- **누가 쓰는가**: 팀원 4명 모두. 뉴스를 발견하면 바로 적는다.
- **최소**: 주 2건 (팀 전체 합산). **목표**: 60일간 30~50건.
- **작성 시간 제한**: 1건당 5분 이내.
- **리뷰**: Lead author가 주 1회 `index.md`를 업데이트하며 전체를 훑는다.

---

## Claude Code Skill

`/dispatch [url] "[한 줄 설명]"` 으로 실행.
자세한 내용: `.claude/commands/dispatch.md`
