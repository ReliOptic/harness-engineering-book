# DR-4.3 Ch.4 — Token Budget Optimization Strategies for Agent Systems

**작성일**: 2026-03-21  
**관련 챕터**: Ch.4 (E08/E12/E20), Ch.5 (cost-reliability frontier), Ch.6 (Operational Compiler의 오버헤드 제어)

> 이 문서는 Ch.4 실험 설계를 위한 연구 정리다.  
> 출판 원고에는 이 문서를 직접 인용하지 않고, 원문 출처를 확인해 직접 인용한다.

## 1. 연구 질문

1. token budget을 단순 상한값이 아니라 실험 변수로 어떻게 조작할 것인가?
2. budget 감소가 agent의 "실행 품질"과 "자기평가 정확도"에 미치는 효과를 어떻게 분리 측정할 것인가?
3. budget 최적화 기법(압축/캐싱/라우팅)을 어떤 순서로 적용해야 재현성이 높은가?

## 2. 핵심 결론

- token budget은 비용 변수이자 reliability 변수다. 예산 축소는 성능만 떨어뜨리는 것이 아니라 failure mode 자체를 바꾼다.
- agent 실험에서는 총 token보다 **실효 budget(Effective Task Budget)** 이 중요하다.
- harness가 강화될수록 안전성은 오르지만 overhead가 늘어, 특정 임계점 이후 TCR이 역전될 수 있다.
- budget 최적화는 "프롬프트 단순화" 한 가지로 끝나지 않고, 라우팅·캐싱·압축·재시도 정책을 결합해야 한다.

## 3. 실험용 조작적 정의

### 3.1 실효 budget

- `Total Budget` = run 전체 허용 token
- `Harness Overhead` = 검증/모니터링/복구 로직에 쓰인 token
- `Effective Task Budget (ETB)` = `Total Budget - Harness Overhead`

Ch.4에서는 ETB를 task 단위로 기록해야 budget 효과를 정확히 비교할 수 있다.

### 3.2 분석 지표

- TCR (Task Completion Rate)
- IFR (Instruction-Following Rate)
- TCA (Tool-Call Accuracy)
- Overconfidence Gap = `Self-assessment - Actual outcome`
- HOR (Harness Overhead Ratio) = `Harness Overhead / Total Budget`

## 4. Ch.4 실험 설계로의 직접 매핑

| 실험 | budget 관련 조작 | 기대 관찰 |
|---|---|---|
| E08 | 100%→75%→50%→25% 단계 감소 | calibration cliff 지점 확인 |
| E12 | self-immune monitoring 강도 증가 | HOR 임계치 및 순효과 역전 확인 |
| E20 | 극단 budget 제약 + harness=ON/OFF 비교 | "보호 비용 > 실행 비용" 구간 확인 |

## 5. 최적화 전략 계층 (실험 설계 관점)

### 5.1 Prompt/Context 압축
- LLMLingua 계열, 요약 기반 context compaction
- 목적: input token 절감 + 핵심 제약 보존

### 5.2 Semantic Caching
- 의미 유사 질의 재사용으로 중복 호출 제거
- 목적: 호출 횟수와 대기시간 동시 절감

### 5.3 Routing/Cascading
- 쉬운 질의는 저비용 모델, 복잡 질의만 고성능 모델
- 목적: 평균 token 비용 하향 + 품질 하한 유지

### 5.4 Retry/Verification 정책
- 무한 재시도 방지, semantic-invalid 반복 차단
- 목적: "실패한 호출의 토큰 누수" 억제

## 6. 보고 규약 (원고 반영용)

- 각 실험에서 `Total Budget`, `ETB`, `HOR`, `TCR`, `IFR`, `TCA`를 함께 보고.
- "성능 저하" 서술은 반드시 임계 구간(예: 50% 이하)과 함께 제시.
- 자기평가 지표는 실제 성능과 분리해 보고하고, 괴리(Overconfidence Gap)를 별도 표로 제시.

## 7. 남은 검증 TODO

- task 난이도별 ETB 민감도 모델링(선형/비선형) 비교
- budget 절감 기법 간 상호작용(압축+캐싱+라우팅) 교호효과 분리
- T3 long-horizon에서 "응답 길이 축소"가 drift의 선행지표인지 재검증

## 참고 출처 (원문 확인 대상)

- LLMLingua-2: Data Distillation for Efficient Prompt Compression
- RouteLLM: Learning to Route LLMs with Preference Data
- Dynamic Model Routing and Cascading for Efficient LLM Inference (survey)
- AWS ElastiCache semantic caching 공식 기술 문서/블로그
- Redis prompt caching vs semantic caching 공식 문서
- OpenAI Structured Outputs / function calling 관련 공식 문서
