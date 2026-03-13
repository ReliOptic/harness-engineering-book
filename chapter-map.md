# Chapter Map — Harness Engineering and AgentOps

> 각 챕터의 제목, 탐구 질문, 핵심 메시지, 학습 결과, 관련 DR/실험 목록.
> 집필 시 이 문서를 기준으로 방향 확인. writing-plan.md의 요약본.

---

## Preface

**핵심 메시지**: 왜 이 책이 필요한가. 누구를 위한 책인가.
**학습 결과**: 독자가 이 책에서 무엇을 얻을 수 있는지 명확히 이해한다.

---

## Ch.1 — 지금 무슨 일이 일어나고 있는가

**파일**: `chapters/ch01-what-is-happening-now.md`
**핵심 메시지**: Agent-friendly product surface의 초기 형태가 부상하는 시점을 기록한다.

**탐구 질문**:
- 2026년 상반기 agent runtime 현장은 어떤 상태인가?
- OpenClaw는 무엇을 가능하게 했고 무엇이 아직 모자란가?
- TeamClaws/PicoClaw 실패는 무엇을 보여주는가?

**핵심 구성**:
1. 2026년 상반기: agent 운영의 현재 풍경
2. OpenClaw — 무엇이 특별하고 무엇이 아직 모자란가
3. 생태계 스냅샷: OpenClaw 주변 프로젝트들
4. TeamClaws/PicoClaw — 이 책을 쓰게 된 이유
5. 왜 지금이 중요한가 — harness engineering 초기에 알 수 있는 것
6. 5변수 프레임워크 소개
7. Agent-1 ~ Agent-5 방향 설정
8. AIE shout-out (Chip Huyen, AI Engineering, 2025)

**학습 결과**:
- 현재 agent 생태계를 파악하고, 왜 이 시점에서 harness engineering이 필요한지 설명할 수 있다.
- 5변수 프레임워크의 기본 개념을 이해한다.

**관련 DR**: DR-1.1, DR-1.2, DR-1.3
**관련 실험**: (없음 — 관찰 및 사례 중심)
**관련 증거**: `evidence/case-studies/openclaw-anchor.md`, `evidence/case-studies/teamclaws-picoclaw-postmortem.md`

---

## Ch.2 — Agent가 모델로부터 무엇을 물려받는가

**파일**: `chapters/ch02-nature-agent-inherits.md`
**핵심 메시지**: Agent는 중립적이지 않다. 모델별 행동 차이를 정량적으로 측정하고 스냅샷으로 기록한다.

**탐구 질문**:
- 동일한 task에서 모델을 바꾸면 무엇이 어떻게 달라지는가?
- 모델 변수가 1차 병목이 되는 조건은 무엇인가?

**핵심 구성**:
1. 물려받는 경향: reasoning, tool use, consistency, confidence
2. OpenRouter 기반 모델 교체 실험 — SOTA, mid-tier, open-source, distilled, quantized
3. 정량 측정 결과: 동일 task에서의 행동 차이
4. Edge 조건과 전문화 문제
5. 5변수 중 "모델" 변수가 1차 병목이 되는 조건

**학습 결과**:
- 모델 원인의 취약성을 식별하고, 자신의 환경에서 유사한 측정을 설계할 수 있다.

**관련 DR**: DR-2.1, DR-2.2, DR-2.3
**관련 실험**: E01, E02, E03, E04

---

## Ch.3 — Harness Engineering과 AgentOps: 정의와 프레임워크

**파일**: `chapters/ch03-harness-and-agentops-defined.md`
**핵심 메시지**: Ch.4-5의 실험을 위해, harness engineering과 AgentOps를 먼저 정의하고 실험 프레임을 설정한다.

**탐구 질문**:
- Harness engineering은 guardrails, scaffolding과 어떻게 다른가?
- AgentOps는 MLOps, DevOps와 어떻게 다른가?
- 무엇을 의도적으로 실패시킬 것인가?

**핵심 구성**:
1. Harness engineering이란 무엇인가 — operational envelope 정의
2. 보호와 enablement의 이중 구조
3. Harness를 guardrails, scaffolding, orchestration과 구분
4. AgentOps란 무엇인가 — profession으로서의 정의
5. 5변수 프레임워크에서 harness와 AgentOps의 위치
6. Harness 부재의 비용: TeamClaws/PicoClaw 사후 분석 (반례 2)
7. CLI-Anything HARNESS.md — 독립적 수렴 사례
8. Ch.4-5에서 실험할 것에 대한 프레임 설정

**학습 결과**:
- Harness와 AgentOps를 정의하고, Ch.4 실험의 프레임을 이해한다.

**관련 DR**: DR-3.1, DR-3.2, DR-3.3, DR-3.4
**관련 실험**: E05, E06, E07, E08

---

## Ch.4 — 의도적 실패 실험: 20개 시나리오

**파일**: `chapters/ch04-deliberate-failure-experiments.md`
**핵심 메시지**: 의도적으로 실패시키고, 무엇이 어떤 조건에서 깨지는지를 체계적으로 기록한다.

**탐구 질문**:
- 5변수 중 어느 것을 조작하면 어떤 실패가 나타나는가?
- 제약 환경에서 가장 먼저 드러나는 병목은 무엇인가?
- 풍선 효과는 어떤 패턴으로 나타나는가?

**핵심 구성**:
- 축 1 (E01-E04): 모델을 바꾸면 무엇이 달라지는가
- 축 2 (E05-E08): Harness와 surface를 바꾸면 무엇이 달라지는가
- 축 3 (E09-E14): 제약 환경에서 가장 먼저 드러나는 병목
- 축 4 (E15-E17): Operator intervention의 효과
- 축 5 (E18-E20): AgentOps 기능의 harness 내재화 가능성
- 반례 (E21-E22): Task design 문제, Compute saturation 문제

**학습 결과**:
- 자신의 환경에서 의도적 실패 실험을 설계하고 실행할 수 있다.
- 이 챕터의 실험 설계를 벤치마크하여 학술적 실험을 구축할 수 있다.

**관련 DR**: DR-4.1, DR-4.2, DR-4.3, DR-4.4
**관련 실험**: E01~E22 전체

---

## Ch.5 — 실험 결과에서 배운 것: AgentOps와 Harness의 실무

**파일**: `chapters/ch05-lessons-from-experiments.md`
**핵심 메시지**: Ch.4의 20개 실험에서 패턴을 추출하고, AgentOps와 harness engineering의 구체적 실무로 전환한다.

**탐구 질문**:
- 어떤 변수가 어떤 조건에서 1차 병목이었는가?
- 반복되는 실패 유형은 무엇인가?
- Harness engineering에 필요한 skill set은 무엇인가?

**핵심 구성**:
1. 20개 실험 결과 종합: 어떤 변수가 어떤 조건에서 1차 병목이었는가
2. 패턴 추출: 반복되는 실패 유형 분류
3. Computation 요구사항: harness에 요구되는 능력 수준별 필요 사양
4. Token efficiency를 운영 규율로
5. Operator intervention 패턴: 어떤 개입이 반복 가능한 runtime aid가 되는가
6. 무료 티어 → 유료 티어: 무엇이 개선되고 무엇이 변하지 않는가
7. Harness engineering에 필요한 skill set 정리
8. 학술적 확장 가능성

**학습 결과**:
- AgentOps 실무를 이해하고, computation 요구사항을 산정하며, 실험 결과에서 학술적 확장 가능성을 식별할 수 있다.

**관련 DR**: DR-5.1, DR-5.2, DR-5.3
**관련 실험**: E01~E22 분석

---

## Ch.6 — 관찰에서 도구로: Operational Fieldkit

**파일**: `chapters/ch06-from-observation-to-fieldkit.md`
**핵심 메시지**: 먼저 직접 써보고, 실패하고, 기록하고, 그 히스토리를 점진적으로 도구로 만든다.

**탐구 질문**:
- 어떤 실패 패턴이 도구화 후보인가?
- 점진적 Fieldkit 업데이트 전략은 무엇인가?
- Skill로 쓸 수 있는 능력을 어떻게 극대화하는가?

**핵심 구성**:
1. Ch.4-5에서 추출한 반복 실패 패턴 → 도구 후보 식별
2. Operational Fieldkit 설계 원칙
3. 점진적 업데이트 원칙: Fieldkit은 harness에 한 번에 embedding되지 않는다
4. Skill로 쓸 수 있는 능력의 극대화 — harness engineering으로 탐색
5. CLI-Anything 방법론 비교

**학습 결과**:
- 실험 로그에서 도구화 후보를 식별하고, 점진적 Fieldkit 업데이트 전략을 설계할 수 있다.

**관련 DR**: DR-6.1, DR-6.2
**관련 실험**: E18, E19, E20

---

## Ch.7 — Harness에서 Agent로: Self-Immune System을 향하여

**파일**: `chapters/ch07-harness-to-agent-self-immune.md`
**핵심 메시지**: AgentOps 기능을 harness를 통해 agent에 점진적으로 주입하여, agent가 스스로 복구하고 학습하는 self-immune system을 갖게 하는 것이 Agent-2 전환의 핵심 조건이다.

**탐구 질문**:
- 어떤 AgentOps 기능이 harness 내재화가 가능한가?
- Agent-1 → Agent-2 전환의 조건은 무엇인가?

**핵심 구성**:
1. 이 책의 실험들이 보여준 유의미한 결과 종합
2. 현 세대 harness가 아직 풀 수 없는 문제
3. AgentOps → Harness → Agent 내재화: 점진적 경로
4. Self-immune system 초기 설계
5. Agent-1 → Agent-2: infinite learning이 가능해지는 조건
6. 이 책 이후: AI agent가 연구와 기록을 자율적으로 수행하는 미래
7. 집필 과정 자체가 agent와의 협업이었다는 메타 관찰

**학습 결과**:
- Harness engineering이 Agent-2 전환에 왜 필수적인지 설명할 수 있다.

**관련 DR**: DR-7.1, DR-7.2
**관련 실험**: E20 (mini self-immune)

---

## Appendices

| Appendix | 파일 | 내용 |
|----------|------|------|
| A | `appendix-a-experiment-log-template.md` | 실험 로그 템플릿 (v4: 5변수, 교차검증 포함) |
| B | `appendix-b-glossary.md` | 용어 사전 |
| C | `appendix-c-diagrams.md` | 다이어그램 모음 |
| D | `appendix-d-reference-projects.md` | 참조 프로젝트 목록 |
| E | `appendix-e-deep-research-prompts.md` | Deep research 프롬프트 전체 목록 |
