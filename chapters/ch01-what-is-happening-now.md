# Ch.1 — 지금 무슨 일이 일어나고 있는가

> 상태: 🔲 skeleton only
> 담당: Kiwon
> 목표 분량: 8,000~10,000자

---

## 핵심 메시지

2026년 상반기 agent runtime 생태계의 현재 풍경을 기록한다. OpenClaw가 만든 agent-friendly product surface의 초기 형태, 그 주변 생태계, 그리고 TeamClaws/PicoClaw 실패에서 시작된 이 책의 질문. 이 챕터는 관찰이며 동시에 예고다 — 이후 챕터들이 측정하게 될 것들의 윤곽이 여기서 처음 등장한다.

## 학습 결과

- 2026년 상반기 agent runtime 생태계의 구조와 주요 축을 설명할 수 있다.
- TeamClaws/PicoClaw 실패가 왜 이 책의 출발점인지 이해한다.
- 5변수 프레임워크(모델, harness, surface, intervention, compute)의 개념을 이해하고, 이후 챕터에서 각 변수가 어떻게 격리·측정될지 예상할 수 있다.
- ARCC(Agent-Relevant Capability Composite)와 Capability Cliff의 개념을 예비적으로 이해한다.
- Agent-1 ~ Agent-5 스펙트럼에서 현재 대부분의 배포 agent가 어디에 위치하는지, 그리고 그 이유를 설명할 수 있다.

## 집필 노트

- 관련 DR: DR-1.1 (OpenClaw 생태계), DR-1.2 (agent-first surface), DR-1.3 (AIE 영향)
- 관련 증거: `evidence/case-studies/openclaw-anchor.md`, `evidence/case-studies/teamclaws-picoclaw-postmortem.md`
- 관련 dispatch: `#ecosystem` 태그, `FD-2026-03-17-002-cli-renaissance.md`, `FD-2026-03-17-002-wide-survey.md`
- **이 챕터의 역할**: 독자에게 실험의 이유와 배경을 제공하면서, Ch.2에서 본격 등장하는 ARCC와 Capability Cliff 개념의 씨앗을 뿌린다. 도입이지 분석이 아니다. 답을 내지 않는다 — 질문을 정의한다.
- **예고해야 할 개념들**:
  - **ARCC** (§6): 5변수 중 모델 변수를 어떻게 측정할지의 질문을 열어두는 곳. "vendor tier가 왜 불충분한가"를 관찰 사례로 암시.
  - **Capability Cliff** (§5): "왜 지금이 중요한가"에서, harness 없이 작동하는 모델을 고르는 것 자체가 어렵다는 관찰. 선형이 아닌 경계가 존재한다는 암시.
  - **Failure Budget Reallocation** (§4): TeamClaws 실패 서술 시, 실패의 성격이 변하지 않고 유형만 바뀌었다는 관찰을 자연스럽게 노출.
- **문체 원칙**: 이 챕터는 관찰과 기록이다. TeamClaws/PicoClaw 실패를 서술할 때 결론을 선언하지 않는다 — 관찰된 것을 기록하고, 남은 질문을 다음 챕터로 넘긴다. "따라서 harness가 필요하다"를 이 챕터에서 쓰면 안 된다.
- **AIE shout-out은 §8에서**: Chip Huyen의 *AI Engineering*(2025)이 foundation model 위의 application layer를 다룬다면, 이 책은 그 위의 agent runtime 운영 구조를 다룬다. 계층 구분이 핵심.

---

## Outline

**계획된 섹션:**

1. **2026년 상반기: agent 운영의 현재 풍경**
   - CLI-first surface의 부상 — agent-friendly interface가 아직 표준화되지 않은 이유
   - Compute 제약의 현실: GCP 무료 티어에서 운영하는 agent가 마주치는 것
   - 스냅샷 마커: 이 기록이 2026년 상반기에 고정된 이유

2. **OpenClaw — 무엇이 특별하고 무엇이 아직 모자란가**
   - Agent-friendly product surface의 초기 형태로서의 OpenClaw
   - 이미 가능한 것: tool call routing, context 지속성, 기본 permission 구조
   - 아직 모자란 것: tool call 일관성, 메모리 경계, 복구 경로의 부재
   - 독립적 수렴 사례 예고: CLI-Anything이 같은 방향에서 발견한 것 (Ch.3에서 상세)

3. **생태계 스냅샷: OpenClaw 주변 프로젝트들**
   - 동일한 surface 문제를 다르게 접근하는 프로젝트들
   - 무엇이 수렴하고 있고, 무엇이 아직 발산하고 있는가
   - 이 수렴 방향이 harness engineering의 필요성을 어떻게 암시하는가

4. **TeamClaws/PicoClaw — 이 책을 쓰게 된 이유**
   - 실패의 기록: multi-agent 환경에서 compute 경합이 어떻게 전개되었는가
   - 필자가 처음에 모델 문제로 오진한 것, 그리고 수정된 진단 — 1차 병목은 compute 경합이었다
   - 실패의 성격: 에이전트가 멈춘 것이 아니라 잘못된 방향으로 계속 진행한 것
   - 이 실패가 남긴 질문: 무엇이 이것을 감지 가능하게 만들 수 있었는가 (Ch.4에서)

5. **왜 지금이 중요한가 — harness engineering 초기에 알 수 있는 것**
   - Agent가 아직 공고히 서지 않은 지금, 관찰할 수 있는 구조적 취약점이 있다
   - 모델을 고르는 것만으로는 충분하지 않다는 관찰: 동일 모델, 다른 조건, 다른 결과
   - 경계의 존재 암시: 어떤 모델-task 조합은 작동하고, 다른 조합은 예고 없이 무너진다. 그 경계가 선형인가 — Ch.2에서 측정.
   - 지금 이것을 관찰하는 것이 agent가 고도화된 이후 어떤 이점을 주는가

6. **5변수 프레임워크 소개**
   - 모델, harness, surface, intervention, compute — 이원론("모델 vs. 운영 구조")에서 5변수로
   - 각 변수가 이후 챕터에서 어떻게 격리·측정되는가
   - "1차 병목은 무엇인가"라는 질문이 이 프레임워크에서 어떻게 답해질 수 있는가
   - 모델 변수 측정의 문제 예고: vendor tier나 벤치마크가 왜 부족한가, 그리고 ARCC라는 대안이 Ch.2에서 등장하는 이유

7. **Agent-1 ~ Agent-5 방향 설정**
   - 자율성 스펙트럼으로서의 Agent-1 ~ Agent-5
   - 현재 대부분의 배포된 agent가 Agent-1 수준에 머무는 이유: self-monitoring 능력의 부재
   - Agent-2 전환의 필요조건 예고: 자신의 capability 상태를 감지하고 복구 경로를 실행하는 능력 (Ch.7에서 상세)
   - 이 책의 실험들이 Agent-1과 Agent-2 사이의 경계 조건을 어떻게 탐색하는가

8. **AIE shout-out: 이 책의 위치**
   - Chip Huyen, *AI Engineering*(2025): foundation model 위에 application을 만드는 전 과정의 지도
   - 이 책이 그 위에 쌓는 것: agent runtime의 운영 구조, harness 설계, AgentOps 실무
   - 두 책의 경계선: AIE는 application layer까지. 이 책은 그 위에서 agent가 장기 자율 루프로 운영될 때 무슨 일이 일어나는가.
   - 이 책을 읽기 위해 AIE가 전제 조건인 이유

---

<!-- 섹션별 초고는 /draft ch01 N 으로 작성 -->

## 참조

- `deep-research/DR-1.1-openclaw-ecosystem.md`
- `deep-research/DR-1.2-agent-first-surfaces.md`
- `deep-research/DR-1.3-aie-book-impact.md`
- `evidence/case-studies/openclaw-anchor.md`
- `evidence/case-studies/teamclaws-picoclaw-postmortem.md`
- `evidence/case-studies/openclaw-ecosystem-snapshot.md`
- `field-dispatches/2026-03/FD-2026-03-17-002-cli-renaissance.md`
- `field-dispatches/2026-03/FD-2026-03-17-002-wide-survey.md`
