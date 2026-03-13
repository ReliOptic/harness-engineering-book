# Ch.6 — 관찰에서 도구로: Operational Fieldkit

> 상태: 🔲 skeleton only
> 담당: Kiwon
> 목표 분량: 8,000~10,000자

---

## 핵심 메시지

먼저 직접 써보고, 실패하고, 기록하고, 그 히스토리를 점진적으로 도구로 만든다.

## 학습 결과

- 실험 로그에서 도구화 후보를 식별하고, 점진적 Fieldkit 업데이트 전략을 설계할 수 있다.

## 집필 노트

- 관련 DR: DR-6.1 (CLI 설계 패턴), DR-6.2 (점진적 capability injection)
- 관련 실험: E18 (token auto-report), E19 (failure detect auto-retry), E20 (mini self-immune)
- 핵심 원칙: Fieldkit은 harness에 한 번에 embedding되지 않는다. 점진적으로.
- `fieldkit/README.md` 와 연계

---

## Outline

<!-- /outline ch06 실행 후 여기에 삽입 -->

**계획된 섹션:**

1. Ch.4-5에서 추출한 반복 실패 패턴 → 도구 후보 식별
2. Operational Fieldkit 설계 원칙
3. 점진적 업데이트 원칙: Fieldkit은 harness에 한 번에 embedding되는 것이 아니다
4. Skill로 쓸 수 있는 능력의 극대화 — harness engineering으로 탐색
5. CLI-Anything 방법론 비교

---

<!-- 섹션별 초고는 /draft ch06 N 으로 작성 -->

## 참조

- `deep-research/DR-6.1-cli-design-patterns.md`
- `deep-research/DR-6.2-incremental-capability-injection.md`
- `experiments/axis-5-harness-internalization/E18-token-auto-report.md`
- `experiments/axis-5-harness-internalization/E19-failure-detect-auto-retry.md`
- `experiments/axis-5-harness-internalization/E20-mini-self-immune.md`
- `fieldkit/README.md`
- `fieldkit/failure-to-tool-map.md`
