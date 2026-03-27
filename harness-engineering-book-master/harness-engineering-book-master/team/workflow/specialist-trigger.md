# Specialist 호출 조건표

> Vera(정량) 또는 Felix(실험설계) consultation이 필요한 섹션 목록.
> 해당 섹션 작성 전 이 표를 확인한다.

---

## Vera 호출 조건 (정량 분석)

| 챕터·섹션 | 트리거 조건 | consultation 핵심 질문 |
|-----------|------------|----------------------|
| Ch.2 §2 | ARCC composite 작성 시 | Weight 결정 방법, sensitivity analysis 설계 |
| Ch.2 §3 | Capability Cliff 서술 시 | Sigmoid vs. piecewise linear AIC 비교 해석 |
| Ch.2 §4 | Quantization Tax Curve 서술 시 | Adaptive sampling 전략 (FP16/Q4 먼저, cliff 근처 촘촘히) |
| Ch.4 §1 | Statistical analysis plan 언급 시 | Pre-registration §4 검토 |
| Ch.4 §3~§8 | 각 막(幕) 결과 수치 서술 시 | 95% CI 계산, 유의성 기준 확인 |
| Ch.5 §2 | Failure Budget Reallocation 정량화 시 | 6축 taxonomy 비율 계산 방법 |
| Ch.5 §3 | MTTR, HER 번역 시 | Level 1 → Level 2 파생 공식 |
| Ch.5 §4 | TotalCost, CostIndex 계산 시 | Cost Model 3 scenario 수치 검증 |
| Ch.5 §7 | Fig 11, Fig 12 해석 시 | Scaling threshold 추정, degradation 곡선 해석 |
| Ch.7 §5 | Fig 11 재해석 시 | Ch.7 맥락에서 ARCC threshold 해석 |
| Ch.7 §6 | Fig 12 재해석 시 | Self-immune fatigue 메커니즘 수치 |

---

## Felix 호출 조건 (실험 설계)

| 챕터·섹션 | 트리거 조건 | consultation 핵심 질문 |
|-----------|------------|----------------------|
| Ch.3 §8 | Pre-registration announce 작성 시 | 가설 명확성, 판단 기준 구체성 검토 |
| Ch.4 §1 | Confirmatory/exploratory 구분 서술 시 | 구분 기준 명확화 |
| Ch.4 §2 | Ground truth 3-layer 서술 시 | κ ≥ 0.70 달성 방법, LLM judge 설정 |
| Ch.4 §3 | E01-E04 실험 방법 서술 시 | 모델 변수 격리 조건 검토 |
| Ch.4 §4 | E05-E08 실험 방법 서술 시 | Harness on/off 격리, HOR 측정 방법 |
| Ch.4 §8 | E21, E22 반례 서술 시 | 반례 설계 강도 — 어떤 조건이 가장 강한 반례인가 |
| Ch.5 §8 | Exploratory 발견 분류 시 | 학술적 확장 후보로 분류하는 기준 |

---

## 호출 불필요 확인

아래 섹션은 Specialist 없이 Drafter 단독 작성 가능:

- Ch.1 전체 (관찰 및 사례 중심, 정량 없음)
- Ch.3 §1~§7 (정의 및 프레임워크, Pre-registration §8 제외)
- Ch.6 §1~§5 (Ch.5 결과를 받아 서술, 새 통계 분석 없음)
- Ch.7 §1~§4, §7~§9 (개념 정의 및 논증)
- Preface 전체

---

## Specialist 호출 절차

1. Drafter가 해당 섹션 outline을 확인하고 이 표를 조회한다
2. 해당 항목이 있으면: consultation 질문을 구체적으로 작성한 후 호출한다
3. Vera/Felix는 consultation 출력을 반환한다 (각 에이전트 파일의 형식 준수)
4. Drafter가 결과를 섹션 산문에 통합한다
5. **Specialist 결과는 인용 수준으로** — 챕터 논리 구조는 Drafter가 유지한다
