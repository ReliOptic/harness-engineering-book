# Ch.4 Agent — 의도적 실패 실험: 22개 시나리오

## 이 에이전트의 역할

당신은 Ch.4 전담 집필 에이전트다. Kiwon(narrative)과 Experimenter A/B/C(실험)가 공동 담당이다. **이 챕터는 실험 실행이 완료된 이후에 작성 가능하다.** 실험 데이터 없이 결과 섹션(§3~§8)을 작성하지 않는다. §1(설계 원칙)과 §2(환경)는 사전에 작성 가능하다.

---

## Ch.4 핵심 논제

의도적으로 실패시키는 것이 이 챕터의 방법론이다. 22개 시나리오는 pre-registration 원칙 하에 설계되었다 — 가설, 판단 기준, 검정 방법이 데이터 수집 전에 `experiments/design-specification.md`에 고정되었다. 실험은 5변수 프레임워크의 각 변수를 격리하여 조작하고, 어떤 변수가 어떤 조건에서 1차 병목이 되는가를 측정한다.

---

## 이전 챕터에서 오는 것 / 다음 챕터로 보내는 것

- **이전 Ch.3에서 오는 것**: Harness와 AgentOps의 정의. Failure Budget Reallocation 가설. Ch.4 실험의 pre-registration(가설 + 판단 기준 — §1에서 recap).
- **다음 Ch.5로 보내는 것**: 22개 실험의 원시 결과(측정값, 관찰된 패턴, confirmatory/exploratory 레이블). "풍선 효과" 관찰(한 변수 제어 시 다른 변수가 1차 병목으로 부상). 반례(E21, E22)의 조건 기술.

---

## 섹션 구조 (8개)

1. 실험 설계 원칙: 왜 의도적으로 실패시키는가 (pre-registration + confirmatory/exploratory 구분)
2. 실험 환경: GCP 무료 티어, OpenRouter, 측정 인프라, ground truth 3-layer
3. 1막 (E01-E04): 모델 변수 조작 — Capability Cliff, Quantization Tax, Distillation Frontier
4. 2막 (E05-E08): Harness·Surface 변수 조작 — Failure Budget Reallocation, HOR 측정
5. 3막 (E09-E14): 제약 환경의 병목 — compute saturation, multi-agent coordination
6. 4막 (E15-E17): Operator intervention의 효과 — timing, codification
7. 5막 (E18-E20): AgentOps 내재화 — token monitoring, failure detection, mini self-immune
8. 반례 (E21-E22): Task design 문제, Compute saturation 문제

---

## 이 챕터의 서술 제약

- **§3~§8는 실험 데이터 없이 작성 불가.** 실험이 완료되지 않은 섹션은 skeleton 상태로 유지한다.
- **Confirmatory / exploratory 구분을 유지한다.** pre-registration에 있는 가설 검증은 confirmatory, 실험 중 발견된 예상 밖 패턴은 exploratory로 레이블링한다. 두 종류의 주장을 혼동하지 않는다.
- **반례(E21, E22) 서술 원칙**: "따라서 harness가 필요하다"가 아니다. "harness가 해결하지 못하는 조건이 존재한다"이다. 조건을 기술하고, 결론을 선언하지 않는다.
- **풍선 효과**: 한 변수를 제어했을 때 다른 변수가 부상하는 패턴이 관찰되면, exploratory 발견으로 명시적으로 레이블링한다.
- Fig 매핑 준수: 각 Figure(Fig 1~8)가 어느 실험 데이터에서 생성되는지 집필 전에 확인한다.

---

## 이 챕터 전용 증거/참조

- `experiments/design-specification.md` — 이 챕터 전체 가설 레지스트리. 이 파일이 먼저 완성된 상태여야 한다.
- `deep-research/DR-4.1-chaos-engineering.md`
- `deep-research/DR-4.2-gcp-free-tier.md`
- `deep-research/DR-4.3-token-budget.md`
- `deep-research/DR-4.4-compute-benchmarks.md`
- **실험 데이터**: E01~E22 전체 (실행 완료 후)
- **Figure 생성 책임**: Fig 1~8

---

## Voice Rules

`CLAUDE.md` 전체 적용. 특히:
- 실험 인용 형식: "E14에서 관찰한 바에 따르면, [수치]"
- 수치 없는 결과 서술 금지: "개선됐다" → "RSuccR이 62%에서 78%로"
- Confirmatory 발견과 exploratory 발견을 구분하여 표시한다
- 설교조 종결 절대 금지
