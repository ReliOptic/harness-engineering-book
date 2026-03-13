# Ch.3 — Harness Engineering과 AgentOps: 정의와 프레임워크

> 상태: 🔲 skeleton only
> 담당: Kiwon
> 목표 분량: 8,000~10,000자

---

## 핵심 메시지

Ch.4-5의 실험을 위해, harness engineering과 AgentOps를 먼저 정의하고 실험 프레임을 설정한다.

## 학습 결과

- Harness와 AgentOps를 정의하고, Ch.4 실험의 프레임을 이해한다.

## 집필 노트

- 관련 DR: DR-3.1 (용어), DR-3.2 (CLI-Anything), DR-3.3 (AgentOps 도구), DR-3.4 (실패 taxonomy)
- 관련 실험: E05 (harness 있음/없음), E06 (memory 보호), E07 (permission), E08 (surface)
- 관련 증거: `evidence/case-studies/teamclaws-picoclaw-postmortem.md`, `evidence/case-studies/cli-anything-harness-analysis.md`
- 이 챕터 끝에서 Ch.4의 실험 설계를 announce한다

---

## Outline

<!-- /outline ch03 실행 후 여기에 삽입 -->

**계획된 섹션:**

1. Harness engineering이란 무엇인가 — operational envelope 정의
2. 보호와 enablement의 이중 구조
3. Harness를 guardrails, scaffolding, orchestration과 구분
4. AgentOps란 무엇인가 — profession으로서의 정의
5. 5변수 프레임워크에서 harness와 AgentOps의 위치
6. Harness 부재의 비용: TeamClaws/PicoClaw 사후 분석 (반례 2)
7. CLI-Anything HARNESS.md — 독립적 수렴 사례
8. Ch.4-5에서 실험할 것에 대한 프레임 설정

---

<!-- 섹션별 초고는 /draft ch03 N 으로 작성 -->

## 참조

- `deep-research/DR-3.1-harness-terminology.md`
- `deep-research/DR-3.2-cli-anything-harness.md`
- `deep-research/DR-3.3-agentops-landscape.md`
- `deep-research/DR-3.4-failure-taxonomies.md`
- `evidence/case-studies/teamclaws-picoclaw-postmortem.md`
- `evidence/case-studies/cli-anything-harness-analysis.md`
