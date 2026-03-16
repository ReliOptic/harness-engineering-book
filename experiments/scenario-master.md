# 실험 시나리오 마스터 목록 — 20개 의도적 실패 시나리오

> 이 목록이 Ch.4의 핵심이며, Ch.5 분석의 입력이다.
> 각 시나리오는 5변수 중 어떤 것을 조작하는지 명시한다.
>
> **v2 구조 변경 (2026-03-17)**: 5축 병렬 구조 → 3막 내러티브 구조.
> 인프라 최소사양 실험(구 E11-E13: CPU/RAM/네트워크 제한) 제거.
> 2막을 "자원 제약 하에서 self-immune이 가능한 harness의 최소 조건"으로 재설계.

---

## 배정표

| 실험 | 담당 | 교차검증 | 상태 |
|------|------|----------|------|
| E01~E07 | Experimenter A | B (E04, E06) | 미시작 |
| E08~E12 | Experimenter B | A (E09, E11) | 미시작 |
| E13~E18 | Experimenter C | B (E16, E17) | 미시작 |
| E19~E20 | Experimenter C | A | 미시작 |

---

## 1막: 무엇이 실패를 만드는가 (Ch.2-3)

**막의 질문**: 모델·harness·surface 변수 중 어떤 것을 바꿀 때 어떤 실패가 나타나는가?

### E01 — 동일 task를 SOTA vs. 소형 모델로 실행
- **조작 변수**: 모델
- **관찰 대상**: tool call 패턴, 완료율, 실패 지점의 성격
- **파일**: `axis-1-model-variation/E01-sota-vs-small-model.md`
- **상태**: 미시작

### E02 — 동일 코드 리뷰를 frontier vs. distilled 모델로 실행
- **조작 변수**: 모델
- **관찰 대상**: 리뷰 품질 차이가 일관되는가, task 구조에 따라 달라지는가
- **파일**: `axis-1-model-variation/E02-frontier-vs-distilled.md`
- **상태**: 미시작

### E03 — 모델을 workflow 중간에 교체 (mid-run switching)
- **조작 변수**: 모델
- **관찰 대상**: context 연속성이 어떤 방식으로 깨지는가
- **파일**: `axis-1-model-variation/E03-mid-run-model-switch.md`
- **상태**: 미시작

### E04 — 동일 task를 harness 있음 vs. 없음으로 실행
- **조작 변수**: Harness
- **관찰 대상**: 실패 빈도, 실패 성격(가역/비가역), 복구 가능성의 차이
- **교차검증**: Experimenter B
- **파일**: `axis-2-harness-surface/E04-with-vs-without-harness.md`
- **상태**: 미시작

### E05 — Memory 보호 해제 상태에서 multi-turn 실행
- **조작 변수**: Harness
- **관찰 대상**: context leakage 패턴 — 어떤 정보가 어떤 경로로 흘러가는가
- **파일**: `axis-2-harness-surface/E05-memory-protection-off.md`
- **상태**: 미시작

### E06 — Permission boundary를 점진적으로 넓혀가며 실행
- **조작 변수**: Harness
- **관찰 대상**: 안전하지 않은 행동의 발생 임계치 — boundary 확장의 어느 단계에서 나타나는가
- **교차검증**: Experimenter B
- **파일**: `axis-2-harness-surface/E06-permission-boundary-widening.md`
- **상태**: 미시작

### E07 — 동일 task를 CLI vs. API surface로 실행
- **조작 변수**: Surface
- **관찰 대상**: surface 구조가 입출력 안정성과 실패 성격을 어떻게 바꾸는가
- **파일**: `axis-2-harness-surface/E07-cli-vs-api-surface.md`
- **상태**: 미시작

---

## 2막: 자원 제약 하에서 self-immune이 가능한 harness의 최소 조건 (Ch.4)

**막의 질문**: Agent가 자원 압박 아래에서 자기 상태를 인식하고 보고하는 능력을 언제 잃는가?
그 임계치를 harness가 관찰할 수 있는가?

이 막이 다루는 것은 "자원이 부족하면 실패한다"(자명)가 아니다.
전통 소프트웨어는 자원이 부족하면 crash하거나 timeout한다.
Agent는 자원이 줄어들 때 **조용히 능력을 잃는다** — 오류 없이, 확신 있게, 틀린 방향으로.
Harness가 이 소실 과정을 감지할 수 있는 신호가 있는지, 그 신호가 어디에 있는지가 이 막의 질문이다.

### E08 — 컨텍스트 압박 하의 에이전트 자기평가 능력
- **조작 변수**: Compute (token budget 단계적 감소)
- **설계**: token budget을 100%→75%→50%→25%로 줄이며 매 단계에서 agent에게 자기 상태를 보고하게 한다. 보고 정확도를 측정한다.
- **핵심 질문**: 어느 budget 수준에서 agent의 자기평가가 실제 상태와 乖離하기 시작하는가? Harness가 그 乖離 시점을 보고 이전에 감지할 수 있는가?
- **Harness 관점**: 자기평가 능력 소실의 선행 신호 — harness hook의 위치
- **교차검증**: Experimenter A
- **파일**: `axis-3-constraint-selfimmune/E08-context-pressure-self-assess.md`
- **상태**: 미시작

### E09 — 장기 task에서의 목표 표류 (goal drift)
- **조작 변수**: Compute (context 누적, 40-step 이상 task)
- **설계**: 초기 목표를 명시적으로 기록한 후 40-step task를 실행. 10-step마다 현재 목표와 초기 목표의 일치도를 평가한다.
- **핵심 질문**: Goal drift가 harness가 감지 가능한 신호를 만드는가, 아니면 무증상으로 진행하는가? Agent 자신은 drift를 인식하는가?
- **Harness 관점**: drift 조기 감지 hook의 가능성과 위치
- **교차검증**: Experimenter A
- **파일**: `axis-3-constraint-selfimmune/E09-goal-drift-longrange.md`
- **상태**: 미시작

### E10 — Self-monitoring을 얹을 수 있는 모델 capability floor
- **조작 변수**: 모델 (다른 tier에서 E15 self-reporting 반복)
- **설계**: E15(agent self-reporting)를 SOTA / mid-tier / small / quantized 모델에서 각각 실행하고 보고 정확도를 비교한다.
- **핵심 질문**: 어느 모델 tier 이하에서 자기 상태 보고의 정확도가 self-immune 운용에 부적합한 수준으로 떨어지는가?
- **Harness 관점**: Agent-2 전환을 시도할 수 있는 모델의 최소 요건. Harness 설계가 모델 선택 제약을 어떻게 반영해야 하는가.
- **파일**: `axis-3-constraint-selfimmune/E10-model-capability-floor.md`
- **상태**: 미시작

### E11 — TeamClaws 재현: context 오염의 전파 경로
- **조작 변수**: Compute (multi-agent resource contention)
- **설계**: 2개 agent를 동일 VM에서 실행. 리소스 경쟁 지표(CPU, memory)와 context 오염 지표(의도하지 않은 정보 공유, 응답 혼선)를 동시에 측정한다.
- **핵심 질문**: 리소스 경쟁이 먼저인가, context 오염이 먼저인가? Harness가 context 오염을 리소스 경쟁보다 먼저 감지할 수 있는가?
- **Harness 관점**: 오염 전파를 막는 격리 경계의 위치 — TeamClaws가 실패한 지점
- **교차검증**: Experimenter A
- **파일**: `axis-3-constraint-selfimmune/E11-teamclaws-replication.md`
- **상태**: 미시작

### E12 — Self-immune harness 자체의 compute overhead
- **조작 변수**: Harness overhead under constraint
- **설계**: E18(mini self-immune)을 점점 더 제약된 resource 환경에서 실행. self-monitoring loop 자체가 소비하는 token/compute 비용을 측정한다.
- **핵심 질문**: Self-immune harness가 언제 자기 자신이 병목이 되는가? 자원이 부족할 때 self-immune을 유지하려면 harness는 얼마나 가벼워야 하는가?
- **Harness 관점**: Self-immune의 지속 가능성 조건. harness overhead가 agent capacity를 잠식하는 임계치.
- **파일**: `axis-3-constraint-selfimmune/E12-selfimmune-overhead.md`
- **상태**: 미시작

---

## 3막: 개입은 반복 가능한가, 그리고 내재화될 수 있는가 (Ch.5-7)

**막의 질문**: Operator intervention을 운영 규율로 만들 수 있는가?
만들 수 있다면, 그 규율의 일부를 harness에 내재화할 수 있는가?

### E13 — 동일 실패 상황에서: 개입 없음 vs. 힌트 제공 vs. 직접 수정
- **조작 변수**: Intervention
- **관찰 대상**: 복구 성공률, 소요 시간, 부작용 차이
- **파일**: `axis-4-operator-intervention/E13-intervention-levels.md`
- **상태**: 미시작

### E14 — 반복 실패에 규칙 기반 자동 개입 적용
- **조작 변수**: Intervention
- **관찰 대상**: 자동화 가능한 개입의 범위 — 어떤 실패 패턴이 규칙으로 포착되고, 어떤 것이 포착되지 않는가
- **파일**: `axis-4-operator-intervention/E14-rule-based-auto-intervention.md`
- **상태**: 미시작

### E15 — Agent에게 자기 상태 보고를 요청 (self-reporting)
- **조작 변수**: Intervention → 내재화 전환점
- **관찰 대상**: Agent 자기 인식의 정확도 — "나는 지금 어디에 있는가"에 대한 agent의 대답이 실제 상태와 얼마나 일치하는가
- **위치**: Intervention(3막)과 내재화(E16-E18) 사이의 경첩 실험. E15 결과가 E16-E18의 방향을 결정한다.
- **교차검증**: Experimenter B
- **파일**: `axis-4-operator-intervention/E15-agent-self-reporting.md`
- **상태**: 미시작

### E16 — Token 사용량 자동 보고 기능을 harness에 추가
- **조작 변수**: Harness 내재화
- **관찰 대상**: self-reporting 정확도, overhead, agent 행동 변화 여부
- **교차검증**: Experimenter B
- **파일**: `axis-5-harness-internalization/E16-token-auto-report.md`
- **상태**: 미시작

### E17 — 실패 감지 + 자동 재시도 로직을 harness에 추가
- **조작 변수**: Harness 내재화
- **관찰 대상**: self-recovery 성공률, 재시도가 무한 루프로 빠지는 조건
- **교차검증**: Experimenter B
- **파일**: `axis-5-harness-internalization/E17-failure-detect-auto-retry.md`
- **상태**: 미시작

### E18 — E16+E17 결합: mini self-immune
- **조작 변수**: Harness 내재화 (통합)
- **관찰 대상**: 통합 동작 안정성. 두 기능이 서로를 간섭하는가. E12와 교차 분석: 이 harness는 자원 제약 하에서 얼마나 버티는가.
- **파일**: `axis-5-harness-internalization/E18-mini-self-immune.md`
- **상태**: 미시작

---

## 반례 전용 실험

**반례의 역할**: 이 책의 주장이 성립하지 않는 조건을 명시한다.
Harness engineering이 모든 실패를 막는다는 주장을 이 책은 하지 않는다.

### E19 — 모호한 task 정의로 실행 (task design 문제 반례)
- **조작 변수**: Task design
- **목적**: 반례 1 — task 자체가 불안정하면 runtime 튜닝은 무의미하다
- **관찰 대상**: Harness와 모델이 정상인 상황에서 task 정의만 모호하게 했을 때의 실패 성격
- **파일**: `counterexamples/E19-ambiguous-task-design.md`
- **상태**: 미시작

### E20 — 완벽한 harness + SOTA 모델 + 극단적 resource 제약
- **조작 변수**: Compute (극단적 제약)
- **목적**: 반례 2 — compute saturation은 harness와 모델이 해결할 수 없는 독립적 실패 원인이다
- **관찰 대상**: 어느 resource 수준에서 harness overhead 자체가 agent를 죽이는가 (E12와 연결)
- **파일**: `counterexamples/E20-perfect-harness-no-compute.md`
- **상태**: 미시작

---

## 실험 간 참조 구조

```
E15 (self-reporting 정확도)
  ├── E10으로 입력: 모델 tier별 self-reporting 능력
  ├── E16-E17로 입력: 내재화의 출발 근거
  └── E08과 대비: 자원 압박 하에서 self-reporting은 어떻게 달라지는가

E18 (mini self-immune)
  ├── E12로 교차 분석: 이 harness는 resource 제약 하에서 얼마나 버티는가
  └── E20으로 반례: compute가 극단적으로 부족하면 E18도 무너진다

E11 (TeamClaws 재현)
  └── Ch.1 동기와 연결: 이 책을 쓰게 된 실패의 재현
```

---

## 실험 로그 템플릿

각 실험 파일은 `experiments/template.md`를 기준으로 작성.

| 항목 | 내용 |
|------|------|
| Experiment ID | E01~E20 |
| 막 | 1막 / 2막 / 3막 / 반례 |
| 조작 변수 | 5변수 중 무엇을 바꿨는가 |
| 고정 변수 | 무엇을 고정했는가 |
| 환경 | 모델, VM 사양, surface, harness 버전 |
| 관찰 대상 | 무엇을 측정했는가 |
| 결과 요약 | 무엇이 일어났는가 |
| Harness 관점 | Harness가 이 실험에서 무엇을 할 수 있었고 못 했는가 |
| 예상과의 차이 | 놀라운 점이 있었는가 |
| 다음 질문 | 이 실험이 열어놓은 질문 |
| 실험자 | Experimenter A / B / C |
| 교차검증 | 교차검증 실험자와 결과 |
