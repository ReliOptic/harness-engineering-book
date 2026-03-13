# Harness Engineering and AgentOps

**부제**: Observing What Makes Agents Work — and What Breaks Them

2026년 상반기 agent runtime 현실의 스냅샷이자 실험서.
Beta 마감: 2026-05-13.

---

## 이 책의 핵심 질문

"모델과 harness 중 누가 더 중요한가?" — 이 이원론을 넘어선다.

**핵심 질문: "어떤 조건에서 무엇이 1차 병목이 되는가?"**

이것을 20개의 의도적 실패 실험을 통해 관찰하고 측정한다.

---

## 5변수 프레임워크

Agent 시스템의 실용적 품질은 최소 5개 변수의 상호작용으로 결정된다:

| 변수 | 설명 |
|------|------|
| **모델** | reasoning, tool use, consistency, confidence 특성 |
| **Harness** | Operational envelope: memory 보호, 권한, 복구, evaluation hook |
| **Product surface** | CLI, API 등 agent가 input/output을 주고받는 인터페이스 |
| **Operator intervention** | 인간 운영자의 개입 패턴, 타이밍, 효과 |
| **Compute/resource budget** | VM 사양, token budget, API 비용, 네트워크 지연 |

---

## 챕터 구조

```
Ch.1  지금 무슨 일이 일어나고 있는가 (스냅샷, 생태계)
  ↓
Ch.2  Agent는 모델로부터 무엇을 물려받는가 (관찰, 측정)
  ↓
Ch.3  Harness engineering이란 무엇인가 + AgentOps란 무엇인가
  ↓
Ch.4  의도적 실패 실험: 20개 시나리오
  ↓
Ch.5  실험 결과에서 배운 것: AgentOps와 Harness의 실무
  ↓
Ch.6  관찰에서 도구로: Operational Fieldkit
  ↓
Ch.7  Harness → Agent 내재화 → Self-Immune System
```

---

## 관찰 원칙

1. 결론을 미리 정하지 않는다.
2. 결과가 예상과 다르면 결과를 기록한다.
3. 단일 실행에서 일반화할 때 반드시 잠정적으로 표시.
4. 반례를 적극적으로 포함한다.

---

## 팀

| 역할 | 담당 | 핵심 책임 |
|------|------|----------|
| Lead author | Kiwon | 논제, 챕터 논리, Ch.1/3/6/7 집필 |
| Experimenter A | TBD | E01~E08 primary |
| Experimenter B | TBD | E09~E16 primary |
| Experimenter C | TBD | E17~E22 primary |

---

## 집필 도구 (Claude Code Custom Skills)

| Skill | 용도 |
|-------|------|
| `/outline [chNN]` | 챕터 section outline 생성 |
| `/draft [chNN] [N]` | 섹션 초고 작성 |
| `/revise [chNN] [N] "[피드백]"` | 피드백 반영 수정 |
| `/integrate [chNN]` | 섹션 통합 → 완성 챕터 |
| `/voice-check [chNN]` | 문체 점검 |
| `/dispatch [url] "[설명]"` | Field Dispatch 작성 |
| `/log-experiment [ENN]` | 실험 로그 작성 |
| `/status` | 프로젝트 현황 보고 |
