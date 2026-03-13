# 실험 시나리오 마스터 목록 — 20개 의도적 실패 시나리오

> 이 목록이 Ch.4의 핵심이며, Ch.5 분석의 입력이다.
> 각 시나리오는 5변수 중 어떤 것을 조작하는지 명시한다.

---

## 배정표

| 실험 | 담당 | 교차검증 | 상태 |
|------|------|----------|------|
| E01~E08 | Experimenter A | B (E03, E05) | 미시작 |
| E09~E16 | Experimenter B | A (E11, E14) | 미시작 |
| E17~E22 | Experimenter C | B (E19, E20) | 미시작 |

---

## 축 1: 모델을 바꾸면 무엇이 달라지는가 (Ch.2 주력)

### E01 — 동일 GitHub issue triage를 SOTA vs. 소형 모델로 실행
- **조작 변수**: 모델
- **예상 관찰**: Tool call 패턴, 완료율 차이
- **파일**: `axis-1-model-variation/E01-issue-triage-model-compare.md`
- **상태**: 미시작

### E02 — 동일 코드 리뷰를 frontier vs. distilled 모델로 실행
- **조작 변수**: 모델
- **예상 관찰**: 리뷰 품질, 환각률 차이
- **파일**: `axis-1-model-variation/E02-code-review-distilled.md`
- **상태**: 미시작

### E03 — 동일 multi-step CLI 작업을 quantized vs. full 모델로 실행
- **조작 변수**: 모델
- **예상 관찰**: 중간 단계 실패 지점 비교
- **파일**: `axis-1-model-variation/E03-multistep-quantized.md`
- **교차검증**: Experimenter B
- **상태**: 미시작

### E04 — 모델을 mid-run에서 교체 (workflow 중간에 모델 스위칭)
- **조작 변수**: 모델
- **예상 관찰**: Context 연속성 깨짐 패턴
- **파일**: `axis-1-model-variation/E04-mid-run-model-switch.md`
- **상태**: 미시작

---

## 축 2: Harness와 surface를 바꾸면 무엇이 달라지는가 (Ch.3, Ch.4)

### E05 — 동일 task를 harness 있음 vs. 없음(raw model)으로 실행
- **조작 변수**: Harness
- **예상 관찰**: 실패 빈도, 복구 가능성 차이
- **파일**: `axis-2-harness-surface/E05-with-vs-without-harness.md`
- **교차검증**: Experimenter B
- **상태**: 미시작

### E06 — Memory 보호 해제 상태에서 multi-turn 대화
- **조작 변수**: Harness
- **예상 관찰**: Context leakage 패턴
- **파일**: `axis-2-harness-surface/E06-memory-protection-off.md`
- **상태**: 미시작

### E07 — Permission boundary를 점진적으로 넓혀가며 실행
- **조작 변수**: Harness
- **예상 관찰**: 안전하지 않은 행동 발생 임계치
- **파일**: `axis-2-harness-surface/E07-permission-boundary-widening.md`
- **상태**: 미시작

### E08 — 동일 task를 CLI vs. 다른 surface(API, webhook)로 실행
- **조작 변수**: Surface
- **예상 관찰**: 입출력 안정성 차이
- **파일**: `axis-2-harness-surface/E08-cli-vs-api-surface.md`
- **상태**: 미시작

---

## 축 3: 제약 환경에서 가장 먼저 드러나는 병목 (Ch.4 주력)

### E09 — Token budget을 50%로 제한하여 동일 task 실행
- **조작 변수**: Compute (token budget)
- **예상 관찰**: 품질 저하 시작 지점
- **파일**: `axis-3-constraint-bottleneck/E09-token-budget-50pct.md`
- **상태**: 미시작

### E10 — Token budget을 25%로 제한
- **조작 변수**: Compute (token budget)
- **예상 관찰**: 완료 불가능 임계치
- **파일**: `axis-3-constraint-bottleneck/E10-token-budget-25pct.md`
- **상태**: 미시작

### E11 — VM CPU를 1코어로 제한하고 복합 task 실행
- **조작 변수**: Compute (CPU)
- **예상 관찰**: Compute saturation 발생 조건
- **파일**: `axis-3-constraint-bottleneck/E11-cpu-1core-limit.md`
- **교차검증**: Experimenter A
- **상태**: 미시작

### E12 — VM RAM을 512MB로 제한
- **조작 변수**: Compute (RAM)
- **예상 관찰**: OOM 발생 패턴, agent 충돌 양상
- **파일**: `axis-3-constraint-bottleneck/E12-ram-512mb-limit.md`
- **상태**: 미시작

### E13 — 네트워크 지연을 인위적으로 추가 (API latency 시뮬레이션)
- **조작 변수**: Compute (network)
- **예상 관찰**: Timeout 처리, 재시도 행동
- **파일**: `axis-3-constraint-bottleneck/E13-network-latency-inject.md`
- **상태**: 미시작

### E14 — 동시에 2개 agent를 같은 VM에서 실행 (TeamClaws 재현)
- **조작 변수**: Compute (resource contention)
- **예상 관찰**: 충돌, 리소스 경쟁
- **파일**: `axis-3-constraint-bottleneck/E14-dual-agent-same-vm.md`
- **교차검증**: Experimenter A
- **상태**: 미시작

---

## 축 4: Operator intervention의 효과 (Ch.5 주력)

### E15 — 동일 실패 상황에서: 개입 없음 vs. 힌트 제공 vs. 직접 수정
- **조작 변수**: Intervention
- **예상 관찰**: 복구 성공률, 소요 시간 비교
- **파일**: `axis-4-operator-intervention/E15-no-hint-vs-hint-vs-fix.md`
- **상태**: 미시작

### E16 — 반복 실패에 규칙 기반 자동 개입 적용
- **조작 변수**: Intervention
- **예상 관찰**: 자동화 가능한 개입의 범위
- **파일**: `axis-4-operator-intervention/E16-rule-based-auto-intervention.md`
- **상태**: 미시작

### E17 — Agent에게 자기 상태 보고를 요청 (self-reporting)
- **조작 변수**: Intervention
- **예상 관찰**: Agent 자기 인식의 정확도
- **파일**: `axis-4-operator-intervention/E17-agent-self-reporting.md`
- **상태**: 미시작

---

## 축 5: AgentOps 기능의 harness 내재화 가능성 (Ch.6, Ch.7)

### E18 — Token 사용량 자동 보고 기능을 harness에 추가
- **조작 변수**: Harness (내재화)
- **예상 관찰**: Self-reporting 정확도, overhead
- **파일**: `axis-5-harness-internalization/E18-token-auto-report.md`
- **상태**: 미시작

### E19 — 실패 감지 + 자동 재시도 로직을 harness에 추가
- **조작 변수**: Harness (내재화)
- **예상 관찰**: Self-recovery 성공률
- **파일**: `axis-5-harness-internalization/E19-failure-detect-auto-retry.md`
- **교차검증**: Experimenter B
- **상태**: 미시작

### E20 — E18+E19를 결합하여 "mini self-immune" 구성
- **조작 변수**: Harness (내재화)
- **예상 관찰**: 통합 동작 안정성, Agent-2 전환 가능성
- **파일**: `axis-5-harness-internalization/E20-mini-self-immune.md`
- **교차검증**: Experimenter B
- **상태**: 미시작

---

## 반례 전용 실험

### E21 — 모호한 task 정의로 실행 (task design 문제 반례)
- **조작 변수**: Task design
- **예상 관찰**: Harness/모델과 무관한 실패
- **목적**: 반례 1 입증 — task 자체가 불안정하면 runtime 튜닝이 무의미
- **파일**: `counterexamples/E21-ambiguous-task-design.md`
- **상태**: 미시작

### E22 — 완벽한 harness + SOTA 모델이지만 VM 1코어 (compute 반례)
- **조작 변수**: Compute (극단적 제약)
- **예상 관찰**: 모든 것이 좋아도 compute가 부족하면 실패
- **목적**: 반례 2 입증 — compute saturation은 독립적 실패 원인
- **파일**: `counterexamples/E22-perfect-harness-no-compute.md`
- **상태**: 미시작
