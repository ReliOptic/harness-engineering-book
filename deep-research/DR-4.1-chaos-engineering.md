# DR-4.1 Ch.4 — Chaos Engineering Applied to AI Agent Systems

**작성일**: 2026-03-21  
**관련 챕터**: Ch.4 (deliberate failure), Ch.5 (failure analysis), Ch.6 (Operational Compiler 설계 경계)

> 이 문서는 Ch.4의 실험 설계를 위한 연구 정리다.  
> 출판 원고에는 이 문서를 직접 인용하지 않고, 아래 원문 출처를 확인해 직접 인용한다.

## 1. 연구 질문

1. 고전적 chaos engineering 원칙을 LLM agent 시스템에 어떻게 이식할 수 있는가?
2. agent 시스템에서 failure injection의 최소 단위는 무엇인가?
3. deliberate failure를 실험으로 수행할 때 안전 경계(blast radius)를 어떻게 설정할 것인가?

## 2. 핵심 결론

- agent 시스템의 chaos engineering 단위는 "서버/프로세스 장애"보다 좁고, "tool-call, context state, permission, budget" 단위로 쪼개야 한다.
- LLM agent 실험에서 steady-state는 단일 성공률이 아니라 `TCR + IFR + TCA + drift signal`의 다변량 벡터로 정의해야 한다.
- failure injection은 반드시 pre-registration(가설/중단 조건/판정 기준 사전 고정)과 결합되어야 하며, 그렇지 않으면 사후 해석 편향이 커진다.
- Ch.4의 deliberate failure는 chaos engineering의 변형이 아니라, agent runtime에 맞춘 **operationalized chaos protocol**로 보는 편이 정확하다.

## 3. 고전 Chaos Engineering과 Agent 실험의 매핑

| 고전 원칙 | Agent 시스템 대응 | Ch.4 대응 실험 |
|---|---|---|
| Steady-state 정의 | TCR, IFR, TCA, drift rate를 기준선으로 고정 | E01~E04 기준선 + E08/E09 drift |
| 현실 교란 주입 | tool 실패, context 압박, permission 변화, compute throttling | E05~E14 |
| Blast radius 제한 | sandbox, token cap, step cap, retry cap | 전 실험 공통 가드레일 |
| 자동 관측/복구 | trace + failure taxonomy + retry policy | framework/ + E17/E18 |
| 사후 학습 | 실패 패턴 분류, 재현 가능 규칙화 | Ch.5 연결 |

## 4. Agent 실패 주입 카탈로그 (실험 설계용)

### 4.1 Tool-plane Fault
- 존재하지 않는 tool name 주입
- schema-valid but semantic-invalid 인자 주입
- tool timeout/429/5xx 응답 주입
- 예상: TCA 하락, retry 패턴 증가, T3 goal-retention 저하

### 4.2 Context-plane Fault
- budget 단계적 축소(100/75/50/25)
- long-horizon에서 과거 step 요약 손실 유도
- 예상: self-report 과신 증가, IFR-TCR 괴리 확대

### 4.3 Permission-plane Fault
- 파일/네트워크/명령 권한 단계적 확대 혹은 축소
- 예상: 위험 행동 증가 또는 과도한 보수화에 따른 task 미완료

### 4.4 Compute-plane Fault
- CPU steal time 상승 조건 재현
- RAM 압박/OOM 경계 재현
- I/O 병목(디스크/네트워크) 재현
- 예상: 무증상 성능 저하 후 급락(cliff-like behavior)

## 5. Ch.4 실험 프로토콜 제안

1. **Pre-register**
   가설, 조작 변수, 중단 조건, 판정 지표를 실험 전 고정.
2. **Baseline 확보**
   무교란 조건에서 task별 steady-state 분포를 먼저 계측.
3. **Single-axis injection**
   한 번에 하나의 변수만 교란하고 나머지는 고정.
4. **Safety guardrail**
   최대 step, 최대 token, 최대 retry, sandbox 경계를 강제.
5. **Rollback 조건**
   과금/보안/데이터 손상 조건 도달 시 즉시 종료.
6. **Postmortem 템플릿**
   실패 원인을 model/harness/surface/operator/compute 축으로 동일하게 라벨링.

## 6. Ch.4 집필에 바로 반영할 문장 수준 포인트

- "의도적 실패 실험"은 무작위 오류 유발이 아니라, 재현 가능한 교란 설계다.
- 결과 해석은 성공/실패 이분법보다 failure mode 이동(분포 변화)을 중심으로 해야 한다.
- 반례 실험(E21/E22)은 "harness가 실패하는 경계조건"을 찾는 목적임을 명시해야 한다.

## 7. 남은 검증 TODO

- agent-runtime 특화 chaos benchmark의 공개 표준 여부 추가 확인
- tool-call semantic correctness 자동 판정기의 신뢰도(κ) 재검증
- failure injection 강도(level)와 재현성의 상관관계 정량화

## 참고 출처 (원문 확인 대상)

- Principles of Chaos Engineering (principlesofchaos.org)
- Netflix/chaosmonkey (GitHub)
- AWS Fault Injection Service (AWS 공식 문서)
- Google SRE Book / SRE Workbook (Google 공식)
- Why Do Multi-Agent LLM Systems Fail? (arXiv:2503.13657)
- Agents of Chaos (원문/공개 리포트)
- Real Faults in MCP Software: a Comprehensive Taxonomy (arXiv:2603.05637)
