# Harness Engineering and AgentOps

*Observing What Makes Agents Work — and What Breaks Them*

---

2026년 상반기, agent는 이미 프로덕션에 들어와 있다. 그리고 예상하지 못한 방식으로 실패하고 있다.

처음에는 모델의 문제라고 생각했다. 더 좋은 모델로 교체하면 해결될 것이라고. 실제로 그렇게 해결되는 경우도 있다. 그러나 관찰해보면, 그 판단이 성립하지 않는 경우가 더 많다. Tool call이 조용히 실패하고, context가 운영자도 모르는 사이에 오염된다. 권한 경계가 불분명해서 agent가 해서는 안 될 일을 하고, token budget이 바닥나는 방식이 예측 불가능하다. 이것들은 모델의 문제가 아니다. 그렇다고 모델과 무관하지도 않다.

이 책은 그 애매한 지점에서 시작한다. "모델이냐 harness냐"는 이원론을 버리고, **어떤 조건에서 무엇이 1차 병목이 되는가(under what conditions does what become the primary bottleneck)**를 묻는다. 그리고 그 답을 논증이 아니라 20개의 의도적 실패 실험을 통해 관찰한다.

---

## 5변수 프레임워크 — Five-Variable Framework

Agent 시스템의 실패를 단일 원인으로 귀결하려는 시도는 대부분 불완전하다. 실제 운영 환경에서 agent의 품질은 최소 다섯 개의 변수가 서로 간섭하며 결정된다.

**모델(Model)** 은 reasoning, tool use, consistency, context sensitivity의 특성을 갖는다. 모델이 타고난 것과 harness로 보정할 수 있는 것의 경계를 이해하는 것이 첫 번째 과제다. **Harness** 는 agent의 operational envelope를 정의하는 구조다. Memory 보호, 권한 경계, 복구 로직, evaluation hook이 여기에 속한다. **Surface** 는 agent가 input과 output을 주고받는 인터페이스다. CLI인지 API인지, surface의 설계 자체가 agent에게 어떤 신호를 보내는지가 생각보다 중요하다. **Operator intervention** 은 인간 운영자의 개입 패턴, 타이밍, 효과 반경이다. 언제 개입이 도움이 되고 언제 방해가 되는지는 자명하지 않다. **Compute/resource budget** 은 VM 사양, token budget, API 비용, 네트워크 지연을 포함한다. 이 변수는 나머지 네 개를 전부 압도하는 순간이 있다.

어떤 실험에서는 model이 1차 병목이다. 어떤 실험에서는 harness 설계의 결함이 model의 한계를 증폭시킨다. 어떤 실험에서는 compute saturation이 나머지 모든 변수를 무력화한다. 이 책이 관찰하는 것은 바로 그 조건들이다.

---

## 챕터 구조 — Chapter Structure

7개의 챕터는 관찰에서 도구화로 이어지는 하나의 흐름이다.

Ch.1은 2026년 상반기 agent runtime 생태계의 스냅샷이다. 무엇이 실용화되고 있고, 어떤 전제가 현장에서 통하지 않는지를 기록한다. Ch.2는 agent가 모델로부터 무엇을 물려받는가를 다룬다. 관찰 가능한 것과 관찰 불가능한 것의 경계를 탐색한다. Ch.3에서 Harness Engineering과 AgentOps를 정의한다. 두 개념의 관계와 경계를 설정하는 것이 이 책 전체의 언어적 토대가 된다.

Ch.4가 이 책의 중심이다. 20개의 의도적 실패 실험(E01–E22)이 여기에 있다. 각 실험은 하나의 가설, 하나의 실패 조건, 그리고 하나의 관찰 기록이다. 실험 설계 자체가 실패한 케이스(E21)와 compute saturation이 모든 것을 압도한 케이스(E22)도 포함된다. Ch.5는 실험 결과에서 추출한 패턴이다. AgentOps와 Harness의 실무가 이 장에서 구체화된다. Ch.6는 반복 실패에서 도구화로 이어지는 과정을 다룬다. Operational Fieldkit은 이론적 설계물이 아니라 실험 과정에서 실제로 만들어진 결과물이다. Ch.7은 그 다음 전환점을 탐색한다. Harness가 agent에 내재화되어 agent 스스로 자신의 운영자가 되는 조건, 즉 self-immune system으로의 이행이 가능한가를 묻는다.

---

## 이 책의 한계 — What This Book Cannot Do

이 책은 2026년 상반기의 기록이다. 6개월 후에는 상당 부분이 구식이 될 수 있다. 과도한 일반화를 시도하지 않았으며, 단일 실행에서 도출한 주장에는 반드시 잠정적 표시를 달았다. 반례도 적극적으로 포함했다. 결과가 예상과 다를 때 결과를 버리지 않았다.

이 책이 제시하는 것은 확정된 방법론이 아니라 하나의 관찰 방식이다.

---

## 이 Repository에 대하여 — About This Repository

이 repo는 집필 중인 live document다. 완성된 챕터는 `chapters/`에, 실험 로그는 `experiments/`에, 현장 관찰 기록은 `field-dispatches/`에 실시간으로 올라온다. Beta 마감은 2026-05-13이며, 한국어 초고로 집필한다.

관찰, 반례, 혹은 이 책이 틀렸다고 생각하는 지점이 있다면 issue를 열어주시기 바란다.

*Questions, contradicting evidence, or observations from your own production systems: open an issue.*

---

**Lead Author** — Kiwon. TeamClaws/PicoClaw 운영 실패에서 이 책은 시작됐다.
