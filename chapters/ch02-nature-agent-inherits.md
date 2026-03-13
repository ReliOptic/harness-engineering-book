# Ch.2 — Agent가 모델로부터 무엇을 물려받는가

> 상태: 🔲 skeleton only
> 담당: TBD (Experimenter A primary)
> 목표 분량: 8,000~10,000자

---

## 핵심 메시지

Agent는 중립적이지 않다. 모델별 행동 차이를 정량적으로 측정하고 스냅샷으로 기록한다.

## 학습 결과

- 모델 원인의 취약성을 식별하고, 자신의 환경에서 유사한 측정을 설계할 수 있다.

## 집필 노트

- 관련 DR: DR-2.1 (agent 벤치마크), DR-2.2 (OpenRouter routing), DR-2.3 (distillation/quantization)
- 관련 실험: E01 (issue triage), E02 (코드 리뷰), E03 (multi-step quantized), E04 (mid-run switch)
- 스냅샷 마커: "2026년 3월 기준으로 측정한 모델별 tool call 성공률"

---

## Outline

<!-- /outline ch02 실행 후 여기에 삽입 -->

**계획된 섹션:**

1. 물려받는 경향: reasoning, tool use, consistency, confidence
2. OpenRouter 기반 모델 교체 실험 — SOTA, mid-tier, open-source, distilled, quantized
3. 정량 측정 결과: 동일 task에서의 행동 차이
4. Edge 조건과 전문화 문제
5. 5변수 중 "모델" 변수가 1차 병목이 되는 조건

---

<!-- 섹션별 초고는 /draft ch02 N 으로 작성 -->

## 참조

- `deep-research/DR-2.1-agent-benchmarks.md`
- `deep-research/DR-2.2-openrouter-routing.md`
- `deep-research/DR-2.3-distillation-tool-use.md`
- `experiments/axis-1-model-variation/E01-issue-triage-model-compare.md`
- `experiments/axis-1-model-variation/E02-code-review-distilled.md`
- `experiments/axis-1-model-variation/E03-multistep-quantized.md`
- `experiments/axis-1-model-variation/E04-mid-run-model-switch.md`
