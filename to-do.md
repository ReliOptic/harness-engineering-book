# Book Completion Checklist

> 목적: 책 완성을 위해 해야 할 일을 한 곳에 모은 체크리스트.
> 표기: `[x]` 완료, `[ ]` 미완료.

## Project Governance
- [x] 용어 전환: `Fieldkit` → `Operational Compiler` (문서/챕터/설계 노트 반영)
- [x] writing-plan의 챕터 상태표를 최신 상태로 업데이트
- [x] 최종 출판 타임라인 확정 (beta/polished 날짜 재검증)

## Deep Research (DR)
- [x] DR-1.1 OpenClaw ecosystem snapshot 정리
- [x] DR-1.2 agent-first product surface 조사 정리
- [x] DR-1.3 AI Engineering 영향 정리
- [x] DR-2.1 LLM agent benchmarks 정리
- [x] DR-2.2 OpenRouter model analysis 정리
- [x] DR-2.3 model distillation/tool use 정리
- [x] DR-3.1 agent system terminology 정리
- [x] DR-3.2 CLI-Anything HARNESS 분석 정리
- [x] DR-3.3 AgentOps frameworks 정리
- [x] DR-3.4 ontology-as-memory 구조 정리
- [x] DR-4.1~DR-4.4 deliberate failure 관련 정리
- [x] DR-5.1 failure analysis methods 정리
- [x] DR-5.2 compute cost optimization 정리
- [x] DR-5.3 VM resource management 정리
- [ ] DR-6.1 CLI design patterns 정리
- [x] DR-6.2 incremental capability injection 정리
- [ ] DR-7.1 self-healing agents 정리
- [x] DR-7.2 continuous learning in deployed agents 정리

## Experiments (E01–E22)
- [ ] E01 Capability Cliff 측정
- [ ] E02 frontier vs distilled 비교
- [ ] E03 mid-run model switching
- [ ] E04 harness-on/off baseline
- [ ] E05~E08 harness component ablation
- [ ] E09~E12 constraint/compute bottleneck 실험
- [ ] E13~E15 operator intervention 실험
- [ ] E16~E18 harness internalization 실험
- [ ] E19~E20 counterexamples
- [ ] E21 task ambiguity 반례
- [ ] E22 compute saturation 반례

## Analysis & Figures
- [ ] ARCC 구성 검증 (holdout R² ≥ 0.65 확인)
- [ ] Capability Cliff 시그모이드 vs piecewise AIC 비교
- [ ] Fig 1/1b/1c (Cliff/Quantization/Distillation) 작성
- [ ] Fig 8/10 (Cost-Reliability Frontier / Ablation) 작성
- [ ] HOR/RSuccR/MTTR/CostIndex 계산 결과 반영

## Chapter Drafts
- [x] Preface 정리 (핵심 framing과 외부 사례 연결)
- [x] Ch.1 생태계 스냅샷 + OpenAI 연구 좌표 정합
- [x] Ch.2 `[X]` 플레이스홀더 제거 및 수치 반영
- [x] Ch.3 harness/AgentOps 정의 완성
- [ ] Ch.4 deliberate failure 실험 서술 완성
- [ ] Ch.5 결과 분석 + 비용/운영 지표 번역 완성
- [ ] Ch.6 Operational Compiler 설계 원칙 완성
- [ ] Ch.7 self-immune 전환 조건 완성

## References & Consistency
- [ ] 모든 참조 파일 존재 여부 확인 (DR/FD/evidence 경로 정합)
- [ ] 수치 인용에 근거 링크/근거 문서 연결
- [ ] 용어/표기 일관성 최종 점검 (ARCC/HOR/RSuccR 등)

## Finalization
- [ ] 챕터별 voice-check 통과 (CLAUDE.md 기준)
- [x] 출판용 glossary 동기화 (`appendix-b-glossary.md`)
- [ ] 최종 통합 리드 스루 및 오류 교정
