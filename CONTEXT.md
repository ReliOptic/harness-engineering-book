# CONTEXT — Harness Engineering and AgentOps
> **세션 시작 시 이 파일을 먼저 읽는다.**
> 작업 종료 시 "## 마지막 세션" 섹션을 업데이트한다.

---

## 이 책은 무엇인가

OpenAI 팀이 정의한 harness engineering 프레임워크(Context Engineering, Architectural Constraints, Entropy Management)를 분석하고, 그 원칙들이 실제 제약 환경에서 어떻게 작동하는지를 22개 실험으로 검증한 기록.

**저자 역할:** 연구자 + 실험자 (개인 실패 서사 없음)
**Beta 마감:** 2026-03-25 / Polished: 2026-03-30

---

## 절대 금지

- TeamClaws, PicoClaw, 저자 개인 실패 경험 → 어떤 형태로도 챕터에 등장 금지
- OpenAI를 "전문가 그룹" 같은 모호한 표현으로 대체 금지
- 5변수를 "저자가 귀납적으로 도출한 프레임워크"로 서술 금지
- voice rules 위반 (CLAUDE.md 참조)

---

## 핵심 구조

**5변수 프레임워크** (조작적 분석 구조, TCR 기준 병목 비교)
모델 / Harness / Product surface / Operator intervention / Compute

→ OpenAI 3-pillar = Harness 변수의 내부 구조
→ 핵심 질문: "어떤 조건에서 무엇이 1차 병목이 되는가?"

**주요 측정 지표**
- TCR (Task Completion Rate) — 변수 간 병목 비교 공통 단위
- ARCC — 모델 변수 측정 (TCA, IFR, MSRD_n, CUE composite)
- HOR (Harness Overhead Ratio) — harness 비용 측정
- MTTR — 운영 복구 시간

---

## 파일 구조 요약

```
chapters/          preface + ch01~ch07 (초고 존재)
deep-research/     DR reference 파일 (정의 출처 아님, 인용 전 원문 확인)
  └ harness_engineering_glossary.md  [DR reference, backbone 아님]
evidence/          외부 사례 기록
experiments/       E01~E22 실험 로그
CLAUDE.md          voice rules + AI 지침 (필수)
writing-plan.md    마스터 계획서 v5 (핵심 결정 로그 포함)
chapter-map.md     챕터별 상세 아웃라인
```

---

## 챕터 상태

| 챕터 | 상태 | 잔여 작업 |
| --- | --- | --- |
| Preface | 🟡 v0.2 | 포지셔닝 재정초 완료 |
| Ch.1 | 🟢 초고 완성 | TeamClaws 참조 제거 완료 |
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

**날짜:** 2026-03-20
**작업 내용:**
- writing-plan.md v4 → v5 리팩토링 (포지셔닝 전환, TeamClaws 제거)
- preface.md 개인 서사 제거
- ch01, ch03, ch04 내 TeamClaws/PicoClaw 참조 전체 제거 완료
- CONTEXT.md 신설, 메모리 시스템 업데이트
- **Ch.2 §2~§7 초고 완성** (ARCC, Capability Cliff, Quantization Tax, Distillation Frontier, Mid-run switching, 모델 1차 병목 조건)

**다음 작업 후보 (우선순위순):**
1. E01~E22 실험 실행 → [X] 플레이스홀더 채우기
2. Ch.7 §7~§9 작성 (Agent-1→Agent-2, 미해결 질문, E-meta)
3. Ch.5 분석 프레임 초고
4. Ch.6 §5 (CLI-Anything 수렴 섹션)
5. Ch.4 §7~§8
6. chapter-map.md TeamClaws 참조 정합성 확인
7. CLAUDE.md 포지셔닝 업데이트
