# DR-7.1 — Self-Healing Agents

> 원본: `하네스 엔지니어링과 자율적 AI의 진화_ 안드레 카파티의 오토리서치와 지속적 학습 에이전트를 위한 구조적 비평.md` (동일 디렉토리)
> 보조: DR-7.2 (continuous learning), DR-6.2 (incremental capability injection)

## 요약

Self-healing agent = runtime 중 자기 상태를 감지하고, 실패를 탐지하며, 외부 개입 없이 복구를 시도하는 agent 능력.

핵심 구조:
1. **Self-monitoring** — ARCC 지표 기반 자기 상태 추정 (cliff-proximity detection)
2. **Failure detection** — 실행 궤적에서 비정상 패턴 식별 (hallucination, loop, drift)
3. **Self-initiated recovery** — 재시도, 롤백, 도구 전환, 인간 에스컬레이션 판단

## 학술적 선행 좌표

- **Reflexion** (Shinn et al., 2023): task 간 verbal self-reflection → 재시도 성공률 향상. 그러나 task 간 학습이지 task 내 실시간 감지는 아님.
- **Constitutional AI** (Bai et al., 2022): 학습 단계 self-critique. Runtime에서는 루프 정지.
- **Autoresearch** (Karpathy): 자율적 연구 루프. 실패 시 자동 재설계. 그러나 harness 없이 운영하면 drift 위험.

## Ch.11 연결

- Self-immune system = self-healing의 harness 내재화 버전
- 재귀적 한계: self-monitoring 자체가 ARCC를 소비 → monitoring overhead가 cliff를 당길 수 있음
- Agent-1 → Agent-2 전환 조건: self-healing이 신뢰 가능한 ARCC 하한이 존재하는가?

## 미정리 질문 (DR 단계)

- [ ] Self-healing의 false positive rate 측정 방법론
- [ ] Healing 시도가 상황을 악화시키는 조건 (healing loop)
- [ ] Model capability 증가에 따른 self-healing 신뢰도 곡선
