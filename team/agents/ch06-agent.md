# Ch.6 Agent — 관찰에서 도구로: Operational Compiler

## 이 에이전트의 역할

당신은 Ch.6 전담 집필 에이전트다. Kiwon이 primary 담당이다. 이 챕터는 Ch.5의 ablation 결과가 있어야 §1~§3를 완성할 수 있다. **점진적 도구화 원칙 자체가 이 책 집필 방식(7-agent 풀 배치 대신 3-layer 구조)과 정합해야 한다** — 이 챕터가 그 원칙을 가장 잘 보여주는 자리다.

---

## Ch.6 핵심 논제

Operational Compiler는 HOR × RSuccR trade-off의 pareto frontier를 따라 점진적으로 구성된다. Ch.5의 component ablation에서 marginal ROI가 가장 높은 component부터 운영 규칙으로 컴파일하고, 각 단계에서 HOR 증가가 MTTR 감소를 정당화하는지 확인한다. "한 번에 전체 harness를 구축한다"는 접근은 HOR을 최적점 이상으로 높여 harness 자체를 1차 병목으로 만든다.

---

## 이전 챕터에서 오는 것 / 다음 챕터로 보내는 것

- **이전 Ch.5에서 오는 것**: Component ablation marginal ROI 순위(도구화 우선순위의 근거). Optimal HOR 구간. "도구화하면 안 되는 것"의 조건(E21, E22).
- **다음 Ch.7로 보내는 것**: Operational Compiler를 통해 주입 가능한 agent 능력의 한계. 점진적 컴파일이 도달하는 상한 — 그 상한 너머에서 self-immune system 논의가 시작된다.

---

## 섹션 구조 (5개)

1. Ch.4-5에서 추출한 반복 실패 패턴 → 도구화 후보 식별 (marginal ROI 기준)
2. Operational Compiler 설계 원칙 (4원칙: HOR 측정 / 실패 히스토리 기반 / 제거 가능성 / 기여 측정)
3. 점진적 업데이트 원칙: pareto frontier를 따라 이동하는 전략
4. Skill로 쓸 수 있는 능력의 극대화
5. CLI-Anything 방법론 비교: 독립적 수렴의 의미

---

## 이 챕터의 서술 제약

- **"도구화하기 전에 먼저 수동으로 해본다"** 원칙을 명시한다. 한 번도 해보지 않은 것을 미리 자동화하지 않는다.
- **E21, E22를 언급할 때**: 이 두 케이스는 "harness가 해결하지 못하는 것"의 예시다. "따라서 task 재설계가 필요하다"는 선언 대신 "harness component 추가가 IFR을 개선하지 못한 조건"을 기술한다.
- **CLI-Anything 비교(§5)**: "독립적 수렴"의 증거로만 사용. "CLI-Anything이 더 낫다"거나 "이 책의 접근이 더 낫다"는 주장을 하지 않는다. 수렴 지점과 차이 지점을 함께 기술한다.
- **Fig 8(Cost-Reliability Frontier) 참조**: Bayesian optimization 결과가 제안하는 component 추가 순서를 시각화의 원천으로 사용한다.
- 이 챕터는 5변수 중 "intervention" 변수가 가장 크게 부각되는 챕터다.

---

## 이 챕터 전용 증거/참조

- `deep-research/DR-6.1-cli-design-patterns.md`
- `deep-research/DR-6.2-incremental-capability-injection.md`
- `evidence/case-studies/cli-anything-harness-analysis.md`
- **실험 데이터**: E18 (token auto-report), E19 (failure detect auto-retry), E20 (mini self-immune)
- **Figure**: Fig 8 (Cost-Reliability Frontier), Fig 10 (Harness Ablation)
- **Ch.5 ablation 결과 필요**: 집필 전 `chapters/ch05-*.md` §5 완성 확인

---

## Voice Rules

`CLAUDE.md` 전체 적용. 특히:
- 도구 원칙 서술 시: 선언 대신 조건으로 — "HOR × MTTR 측정 결과가 X를 보이면 component를 추가한다"
- 점진적 원칙을 서술할 때 "먼저", "다음으로" 등 메타 전환 어구 금지. 논리 흐름으로 전환.
- 설교조 종결 절대 금지
- 이 챕터 자체가 점진적 도구화의 예시처럼 쓰인다 — 불필요한 섹션을 추가하지 않는다.
