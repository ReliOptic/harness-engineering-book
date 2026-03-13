# Ch.4 — 의도적 실패 실험: 20개 시나리오

> 상태: 🔲 skeleton only
> 담당: Kiwon (narrative) + Experimenter A/B/C (실험)
> 목표 분량: 12,000~15,000자

---

## 핵심 메시지

의도적으로 실패시키고, 무엇이 어떤 조건에서 깨지는지를 체계적으로 기록한다.

## 학습 결과

- 자신의 환경에서 의도적 실패 실험을 설계하고 실행할 수 있다.
- 이 챕터의 실험 설계를 벤치마크하여 학술적 실험을 구축할 수 있다.

## 집필 노트

- 관련 DR: DR-4.1 (chaos engineering), DR-4.2 (GCP 무료 티어), DR-4.3 (token budget), DR-4.4 (compute benchmarks)
- 관련 실험: E01~E22 전체
- 이 챕터는 실험 실행 완료 후 작성 가능. 실험 로그를 먼저 쌓는다.
- 풍선 효과 관찰 기록 중요

---

## Outline

<!-- /outline ch04 실행 후 여기에 삽입 -->

**계획된 섹션:**

1. 실험 설계 원칙: 왜 의도적으로 실패시키는가
2. 실험 환경: GCP 무료 티어, OpenRouter 설정
3. 축 1 결과: 모델을 바꾸면 (E01~E04)
4. 축 2 결과: Harness와 surface를 바꾸면 (E05~E08)
5. 축 3 결과: 제약 환경의 병목 (E09~E14)
6. 축 4 결과: Operator intervention의 효과 (E15~E17)
7. 축 5 결과: AgentOps 내재화 (E18~E20)
8. 반례 실험: Task design과 compute saturation (E21~E22)

---

<!-- 섹션별 초고는 /draft ch04 N 으로 작성 -->
<!-- 실험 완료 전: 실험 로그를 먼저 채운 후 작성 시작 -->

## 참조

- `experiments/scenario-master.md`
- `experiments/axis-1-model-variation/` (E01~E04)
- `experiments/axis-2-harness-surface/` (E05~E08)
- `experiments/axis-3-constraint-bottleneck/` (E09~E14)
- `experiments/axis-4-operator-intervention/` (E15~E17)
- `experiments/axis-5-harness-internalization/` (E18~E20)
- `experiments/counterexamples/` (E21~E22)
- `evidence/tables/bottleneck-by-condition.md`
