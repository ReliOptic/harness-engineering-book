# Harness Engineering and AgentOps

### Observing What Makes Agents Work — and What Breaks Them

---

> "더 좋은 모델을 쓰면 해결된다."
> 현장에서 이 말을 믿었다가 실패한 사람들을 위한 책.

---

## 이 책이 생긴 이유

Agent가 프로덕션에 들어가기 시작했다. 그리고 예상치 못한 방식으로 무너지기 시작했다.

모델 탓이 아니었다. 적어도 항상 그런 건 아니었다.
Tool call이 조용히 실패했고, context가 모르는 사이에 오염됐고, 운영자는 어디에 개입해야 할지 몰랐다. Budget이 바닥났고, surface는 agent에게 맞지 않는 신호를 보냈다.

이 책은 그 실패들을 의도적으로 재현하고, 관찰하고, 기록한 결과다.

---

## 핵심 질문

**"어떤 조건에서 무엇이 1차 병목이 되는가?"**

"모델 vs harness" 이원론을 버린다. Agent 시스템의 실패는 단일 변수로 귀결되지 않는다.
이 책은 5개의 변수가 어떻게 상호작용하며 병목을 만드는지를 실험을 통해 관찰한다.

---

## 5변수 프레임워크

Agent 시스템의 품질은 이 다섯 변수의 조합으로 결정된다.

```
MODEL         reasoning, tool use, consistency, context sensitivity
HARNESS       memory 보호, 권한 경계, 복구 로직, evaluation hook
SURFACE       CLI / API — agent가 input·output을 주고받는 인터페이스
INTERVENTION  운영자의 개입 패턴, 타이밍, 효과 반경
COMPUTE       VM 사양, token budget, API 비용, 네트워크 지연
```

어떤 실험에서는 model이 1차 병목이다.
어떤 실험에서는 harness 설계 결함이 model의 한계를 증폭시킨다.
어떤 실험에서는 compute saturation이 둘 다 압도한다.

---

## 무엇을 읽게 되는가

```
Ch.1  지금 무슨 일이 일어나고 있는가
      2026년 상반기 agent runtime 생태계의 스냅샷

Ch.2  Agent는 모델로부터 무엇을 물려받는가
      관찰 가능한 것과 관찰 불가능한 것

Ch.3  Harness Engineering이란 무엇인가 / AgentOps란 무엇인가
      정의, 경계, 그리고 두 개념의 관계

Ch.4  의도적 실패 실험 — 20개 시나리오
      각 실험은 하나의 가설, 하나의 실패 조건, 하나의 관찰

Ch.5  실험 결과에서 배운 것
      AgentOps와 Harness의 실무 패턴

Ch.6  관찰에서 도구로 — Operational Fieldkit
      반복 실패에서 추출한 점진적 tooling

Ch.7  Harness → Agent 내재화 → Self-Immune System
      다음 전환점: agent가 자신의 운영자가 되는 조건
```

---

## 이 책의 성격

**실험서다. 교리집이 아니다.**

- 결론을 미리 정하지 않았다. 결과가 예상과 다르면 결과를 기록했다.
- 반례를 포함한다. 실험 설계 자체가 실패한 케이스(E21)도 실린다.
- 단일 실행에서 일반화하지 않는다. 잠정적 주장엔 반드시 표시한다.
- 2026년 상반기의 스냅샷이다. 과도한 일반화는 시도하지 않는다.

---

## 현재 상태

| 항목 | 현황 |
|------|------|
| Beta 마감 | 2026-05-13 |
| 집필 언어 | 한국어 초고 |
| 실험 설계 | 20개 확정 |
| 진행 챕터 | Ch.1 집필 중 |

이 repo는 집필 중인 live document다.
챕터가 완성되면 `chapters/` 에 올라온다. 실험 로그는 `experiments/` 에 실시간으로 쌓인다.

---

## Lead Author

**Kiwon** — Ch.1, Ch.3, Ch.6, Ch.7 집필 및 전체 논제 설계.
TeamClaws/PicoClaw 운영 실패에서 이 책은 시작됐다.

---

*Questions, observations, or contradicting evidence: open an issue.*
