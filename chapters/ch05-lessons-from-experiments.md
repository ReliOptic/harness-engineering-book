# Ch.5 — 실험 결과에서 배운 것: AgentOps와 Harness의 실무

> 상태: 🔲 skeleton only
> 담당: Kiwon
> 목표 분량: 10,000~12,000자

---

## 핵심 메시지

Ch.4의 20개 실험에서 패턴을 추출하고, AgentOps와 harness engineering의 구체적 실무로 전환한다.

## 학습 결과

- AgentOps 실무를 이해하고, computation 요구사항을 산정하며, 실험 결과에서 학술적 확장 가능성을 식별할 수 있다.

## 집필 노트

- 관련 DR: DR-5.1 (실패 패턴 분석), DR-5.2 (compute cost 최적화), DR-5.3 (VM 리소스 관리)
- 관련 실험: E01~E22 분석 (Ch.4 실험 완료 후 작성)
- Ch.4와의 관계: Ch.4가 실행과 기록이라면, 이 챕터는 분석과 패턴 추출
- `evidence/tables/bottleneck-by-condition.md` 를 핵심 표로 활용

---

## Outline

<!-- /outline ch05 실행 후 여기에 삽입 -->

**계획된 섹션:**

1. 20개 실험 결과 종합: 어떤 변수가 어떤 조건에서 1차 병목이었는가
2. 패턴 추출: 반복되는 실패 유형 분류
3. Computation 요구사항: harness에 요구되는 능력 수준별 필요 사양
4. Token efficiency를 운영 규율로
5. Operator intervention 패턴: 어떤 개입이 반복 가능한 runtime aid가 되는가
6. 무료 티어 → 유료 티어: 무엇이 개선되고 무엇이 변하지 않는가
7. Harness engineering에 필요한 skill set 정리
8. 학술적 확장 가능성

---

<!-- 섹션별 초고는 /draft ch05 N 으로 작성 -->

## 참조

- `deep-research/DR-5.1-failure-analysis-methods.md`
- `deep-research/DR-5.2-compute-cost-optimization.md`
- `deep-research/DR-5.3-vm-resource-management.md`
- `evidence/tables/bottleneck-by-condition.md`
- `evidence/tables/computation-requirements.md`
- `evidence/tables/academic-extension-candidates.md`
