# CONTEXT — Harness Engineering and AgentOps
> **세션 시작 시 이 파일을 먼저 읽는다.**
> 작업 종료 시 "## 마지막 세션" 섹션을 업데이트한다.

---

## 이 책은 무엇인가

OpenAI 팀이 정의한 harness engineering 프레임워크(Context Engineering, Architectural Constraints, Entropy Management)를 분석하고, 그 원칙들이 실제 제약 환경에서 어떻게 작동하는지를 22개 실험으로 검증한 기록.

**저자 역할:** 연구자 + 실험자 (개인 실패 서사 없음)
**Beta 마감:** 2026-04-30 / Polished: 완성도 우선, 일정 미확정

---

## 절대 금지

- TeamClaws, PicoClaw, 저자 개인 실패 경험 → 어떤 형태로도 챕터에 등장 금지
- OpenAI를 "전문가 그룹" 같은 모호한 표현으로 대체 금지
- 네 영역을 "저자가 귀납적으로 도출한 프레임워크"로 서술 금지
- voice rules 위반 (CLAUDE.md 참조)

---

## 핵심 구조

**Harness 중심 분석 구조** (TCR 기준 병목 비교)
Harness가 주어. 모델 능력(inbound), 실행 환경 제약(boundary), 사용자 접점(outbound), 피드백 루프(return).

→ 핵심 질문: "어떤 조건에서 무엇이 1차 병목이 되는가?"

**주요 측정 지표**
- TCR (Task Completion Rate) — 병목 비교 공통 단위
- harness overhead — harness가 소비하는 토큰·시간 비용
- MTTR — 운영 복구 시간

---

## 파일 구조 요약

```
chapters/          preface + ch01~ch04 (Part I 스켈레톤) + ch05~ch11 (Part II~IV 초고)
deep-research/     DR reference 파일 (정의 출처 아님, 인용 전 원문 확인)
  └ harness_engineering_glossary.md  [DR reference, backbone 아님]
evidence/          외부 사례 기록
experiments/       E01~E22 실험 로그
CLAUDE.md          voice rules + AI 지침 (필수)
writing-plan.md    마스터 계획서 v6 (핵심 결정 로그 포함)
chapter-map.md     챕터별 상세 아웃라인
```

---

## 챕터 상태

| 챕터 | 상태 | 잔여 작업 |
| --- | --- | --- |
| Preface | 🟡 v0.2 | 포지셔닝 재정초 완료 |
| Ch.1 | 🟡 수정 필요 | PicoClaw 참조 잔존 — 익명화 재작성 필요 |
| Ch.2 | 🟢 초고 완성 | §1~§7 완성, [X] 플레이스홀더 = 실험 데이터 대기 |
| Ch.3 | 🟢 초고 완성 | TeamClaws 참조 제거 완료 |
| Ch.4 | 🟡 초고 | TeamClaws 제거 완료, §7~§8 마커, [X] 데이터 대기 |
| Ch.5 | 🟡 초고 | |
| Ch.6 | 🟡 초고 | |
| Ch.7 | 🟡 초고 | |

---

## 참조 우선순위

1. `CONTEXT.md` (이 파일) — 세션 브리핑
2. `CLAUDE.md` — voice rules, AI 협업 지침
3. `writing-plan.md` — 전략, 결정 로그, 실험 설계 전체
4. `chapter-map.md` — 챕터별 상세 구성

---

## 마지막 세션

**날짜:** 2026-03-29
**작업 내용:**
- 거버넌스 파일 전체 리팩토링 (구조 불일치 해소)
- writing-plan.md: "20개"→"22개" 통일, 마감일 Beta 2026-04-30으로 변경
- CONTEXT.md: 마감일 통일, Ch.1 상태 정정 (PicoClaw 잔존 확인)
- chapter-map.md: TeamClaws/PicoClaw 제거, Ch.3 중복 블록 삭제
- CLAUDE.md: 마감일·실험 수 정합
- to-do.md: 실험 번호 오류 수정
- list-of-contents-final.md: v4 9챕터 구조는 향후 목표로 주석 처리
- 7챕터 구조 유지 확인 (writing-plan.md v5 기준)

**다음 작업 후보 (우선순위순):**
1. Ch.1 PicoClaw 본문 익명화 재작성
2. E01~E22 실험 실행 → [X] 플레이스홀더 채우기
3. Ch.7 §7~§9 작성 (Agent-1→Agent-2, 미해결 질문, E-meta)
4. Ch.5 분석 프레임 초고
5. Ch.6 §5 (CLI-Anything 수렴 섹션)
6. Ch.4 §7~§8
