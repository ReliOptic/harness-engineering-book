# Ch.1 — 지금 무슨 일이 일어나고 있는가

> 상태: 🟡 초고 v0.2 (2026-03-27)
> 담당: Kiwon
> 목표 분량: 8,000~10,000자

---

## 핵심 메시지

2026년 상반기 agent runtime 생태계의 현재 풍경을 기록한다. OpenClaw가 만든 agent-friendly product surface의 초기 형태, 그 주변 생태계, 그리고 harness 없는 장기 운용 실패에서 시작된 이 책의 질문. 이 챕터는 관찰이며 동시에 예고다 — 이후 챕터들이 측정하게 될 것들의 윤곽이 여기서 처음 등장한다.

## 학습 결과

- 2026년 상반기 agent runtime 생태계의 구조와 주요 축을 설명할 수 있다.
- harness 없는 장기 운용 실패가 왜 이 책의 출발점인지 이해한다.
- 5변수 프레임워크(모델, harness, surface, intervention, compute)의 개념을 이해하고, 이후 챕터에서 각 변수가 어떻게 격리·측정될지 예상할 수 있다.
- ARCC(Agent-Relevant Capability Composite)와 Capability Cliff의 개념을 예비적으로 이해한다.
- Agent-1 ~ Agent-5 스펙트럼에서 현재 대부분의 배포 agent가 어디에 위치하는지, 그리고 그 이유를 설명할 수 있다.

## 집필 노트

- 관련 DR: DR-1.1 (OpenClaw 생태계), DR-1.2 (agent-first surface), DR-1.3 (AIE 영향)
- 관련 증거: `evidence/case-studies/openclaw-anchor.md`, `evidence/case-studies/teamclaws-picoclaw-postmortem.md` (저자 내부 관찰 기록)
- 관련 dispatch: `#ecosystem` 태그, `FD-2026-03-17-002-cli-renaissance.md`, `FD-2026-03-17-002-wide-survey.md`
- **이 챕터의 역할**: 독자에게 실험의 이유와 배경을 제공하면서, Ch.2에서 본격 등장하는 ARCC와 Capability Cliff 개념의 씨앗을 뿌린다. 도입이지 분석이 아니다. 답을 내지 않는다 — 질문을 정의한다.
- **예고해야 할 개념들**:
  - **ARCC** (§6): 5변수 중 모델 변수를 어떻게 측정할지의 질문을 열어두는 곳. "vendor tier가 왜 불충분한가"를 관찰 사례로 암시.
  - **Capability Cliff** (§5): "왜 지금이 중요한가"에서, harness 없이 작동하는 모델을 고르는 것 자체가 어렵다는 관찰. 선형이 아닌 경계가 존재한다는 암시.
  - **Failure Budget Reallocation** (§4): TeamClaws 실패 서술 시, 실패의 성격이 변하지 않고 유형만 바뀌었다는 관찰을 자연스럽게 노출.
- **문체 원칙**: 이 챕터는 관찰과 기록이다. 필자의 초기 운용 실패를 서술할 때 결론을 선언하지 않는다 — 관찰된 것을 기록하고, 남은 질문을 다음 챕터로 넘긴다. "따라서 harness가 필요하다"를 이 챕터에서 쓰면 안 된다.
- **AIE shout-out은 §8에서**: Chip Huyen의 *AI Engineering*(2025)이 foundation model 위의 application layer를 다룬다면, 이 책은 그 위의 agent runtime 운영 구조를 다룬다. 계층 구분이 핵심.

---

## Outline

**계획된 섹션:**

1. **2026년 상반기: agent 운영의 현재 풍경**
   - CLI-first surface의 부상 — agent-friendly interface가 아직 표준화되지 않은 이유
   - Compute 제약의 현실: GCP 무료 티어에서 운영하는 agent가 마주치는 것
   - 스냅샷 마커: 이 기록이 2026년 상반기에 고정된 이유

2. **OpenClaw — 무엇이 특별하고 무엇이 아직 모자란가**
   - Agent-friendly product surface의 초기 형태로서의 OpenClaw
   - 이미 가능한 것: tool call routing, context 지속성, 기본 permission 구조
   - 아직 모자란 것: tool call 일관성, 메모리 경계, 복구 경로의 부재
   - 독립적 수렴 사례 예고: CLI-Anything이 같은 방향에서 발견한 것 (Ch.3에서 상세)

3. **생태계 스냅샷: OpenClaw 주변 프로젝트들**
   - 동일한 surface 문제를 다르게 접근하는 프로젝트들
   - 무엇이 수렴하고 있고, 무엇이 아직 발산하고 있는가
   - 이 수렴 방향이 harness engineering의 필요성을 어떻게 암시하는가

4. **harness 없는 장기 운용 실패 — 이 책을 쓰게 된 이유**
   - 실패의 기록: multi-agent 환경에서 compute 경합이 어떻게 전개되었는가
   - 필자가 처음에 모델 문제로 오진한 것, 그리고 수정된 진단 — 1차 병목은 compute 경합이었다
   - 실패의 성격: 에이전트가 멈춘 것이 아니라 잘못된 방향으로 계속 진행한 것
   - 이 실패가 남긴 질문: 무엇이 이것을 감지 가능하게 만들 수 있었는가 (Ch.4에서)

5. **왜 지금이 중요한가 — harness engineering 초기에 알 수 있는 것**
   - Agent가 아직 공고히 서지 않은 지금, 관찰할 수 있는 구조적 취약점이 있다
   - 모델을 고르는 것만으로는 충분하지 않다는 관찰: 동일 모델, 다른 조건, 다른 결과
   - 경계의 존재 암시: 어떤 모델-task 조합은 작동하고, 다른 조합은 예고 없이 무너진다. 그 경계가 선형인가 — Ch.2에서 측정.
   - 지금 이것을 관찰하는 것이 agent가 고도화된 이후 어떤 이점을 주는가

6. **5변수 프레임워크 소개**
   - 모델, harness, surface, intervention, compute — 이원론("모델 vs. 운영 구조")에서 5변수로
   - 각 변수가 이후 챕터에서 어떻게 격리·측정되는가
   - "1차 병목은 무엇인가"라는 질문이 이 프레임워크에서 어떻게 답해질 수 있는가
   - 모델 변수 측정의 문제 예고: vendor tier나 벤치마크가 왜 부족한가, 그리고 ARCC라는 대안이 Ch.2에서 등장하는 이유

7. **Agent-1 ~ Agent-5 방향 설정**
   - 자율성 스펙트럼으로서의 Agent-1 ~ Agent-5
   - 현재 대부분의 배포된 agent가 Agent-1 수준에 머무는 이유: self-monitoring 능력의 부재
   - Agent-2 전환의 필요조건 예고: 자신의 capability 상태를 감지하고 복구 경로를 실행하는 능력 (Ch.7에서 상세)
   - 이 책의 실험들이 Agent-1과 Agent-2 사이의 경계 조건을 어떻게 탐색하는가

8. **AIE shout-out: 이 책의 위치**
   - Chip Huyen, *AI Engineering*(2025): foundation model 위에 application을 만드는 전 과정의 지도
   - 이 책이 그 위에 쌓는 것: agent runtime의 운영 구조, harness 설계, AgentOps 실무
   - 두 책의 경계선: AIE는 application layer까지. 이 책은 그 위에서 agent가 장기 자율 루프로 운영될 때 무슨 일이 일어나는가.
   - 이 책을 읽기 위해 AIE가 전제 조건인 이유

---

## §1 2026년 상반기: agent 운영의 현재 풍경

> 상태: 🔴 초고 v0.1 (2026-03-18)

2026년 3월 기준으로, agent를 실제 운영 환경에 배포하려는 사람이 가장 먼저 마주치는 결정은 모델 선택이 아니라 interface 선택이다. 어떤 surface 위에서 agent가 작동하게 할 것인가 — 이 질문에 대한 생태계의 답은 아직 수렴하지 않았다. Web UI는 인간 사용자를 위해 설계되었고, API gateway는 서비스 간 통신을 전제로 한다. CLI만이 현재 시점에서 agent를 primary user로 상정한 설계에 가장 가깝게 접근하고 있는데, 그것도 아직 표준화된 형태가 아닌 각자도생의 방식으로 수렴 중이다.

Compute 제약은 이 문제를 더 선명하게 만든다. GCP 무료 티어에 준하는 환경 — 공유 vCPU, RAM 1~2GB, 네트워크 지연이 언제든 개입할 수 있는 조건 — 에서 agent를 운영하는 것은 단순히 저예산 프로토타이핑의 문제가 아니다. 이 조건이 agent 행동의 baseline을 정의한다. 어떤 실패가 모델의 추론 한계에서 오는지, 어떤 실패가 메모리 누적이나 CPU 포화에서 오는지는 제약 환경에서 훨씬 빠르게 드러난다. 자원이 충분한 환경에서는 관찰이 지연되는 패턴이 여기서는 수 시간 내에 재현된다.

이 챕터는 2026년 상반기라는 시점을 명시적으로 고정한다. 여기에 기록된 관찰은 이 시점의 스냅샷이다. agent 생태계는 지금도 빠르게 이동하고 있으며, 이 책이 출판될 즈음에는 일부 관찰이 이미 과거의 것이 되어 있을 수 있다. 그럼에도 이 시점에서 기록하는 이유는 agent 운영이 아직 고도화되기 전, 구조적 취약점이 가장 투명하게 관찰 가능한 창(window)이기 때문이다. agent가 더 강력해지고 harness가 더 정교해진 이후에는 지금 보이는 실패 메커니즘 중 상당수가 추상 뒤에 가려질 것이다.

---

## §2 OpenClaw — 무엇이 가능하고 무엇이 아직 모자란가

> 상태: 🔴 초고 v0.1 (2026-03-18)

OpenClaw(GitHub 250,829+ Stars, 2026년 3월 기준)는 CLI-first agent 생태계에서 기준선 역할을 하는 프레임워크다. Node.js V8 단일 프로세스 위에서 430K LoC 규모로 성장했고, agent가 tool call을 통해 실제 환경과 상호작용하는 패턴의 초기 형태를 제시했다. 이 프레임워크가 보여준 것은 agent-friendly product surface가 가능하다는 사실 자체였다 — tool call routing, context 지속성, 기본 permission 구조가 하나의 cohesive한 경험으로 묶일 수 있다는 것.

그러나 OpenClaw가 설계하지 않은 것이 이 책의 출발점을 이룬다. 메모리 경계가 없다는 것은 agent가 장기 실행될수록 힙 위에 컨텍스트 객체가 무제한으로 누적된다는 뜻이고, 중앙 스케줄러 없이 각 백그라운드 태스크가 독립 타이머를 보유한다는 것은 시스템 부하가 올라가는 순간 타이머 충돌이 발생할 수 있는 구조다. tool call 일관성 — 동일한 프롬프트와 도구 조건에서 agent가 동일한 호출 시퀀스를 따르는 정도 — 도 아직 보장되지 않는다. 복구 경로는 설계되어 있지 않으며, 장애가 발생하면 운영자의 수동 개입이 유일한 방법이다.

필자가 OpenClaw를 처음 운영하면서 관찰한 것은 이 부재(不在)가 즉각적인 실패를 유발하지 않는다는 점이었다. 단기 태스크, 짧은 컨텍스트, 낮은 동시성 조건에서는 OpenClaw가 충분히 잘 작동한다. 부재의 비용은 시간과 함께 누적되고, 운용 조건이 복잡해질수록 지수적으로 드러난다. §4에서 기술하는 필자의 초기 운용 실험이 이 패턴을 따랐다 — 단일 프로세스 아키텍처에서 harness 없이 장기 운영할 때 어떤 일이 일어나는지를.


---

## §3 생태계 스냅샷: OpenClaw 주변 프로젝트들

> 상태: 🔴 초고 v0.1 (2026-03-18)

OpenClaw 주변 생태계는 2026년 상반기 들어 동일한 surface 문제를 서로 다른 각도에서 공략하는 프레임워크들로 빠르게 채워지고 있다. ZeroClaw(Rust, RAM 5MB 미만, 26,700+ Stars), Nanobot(Python, 4K LoC, MCP Native Host, 33,100+ Stars), NullClaw(Zig, 678KB 바이너리, 2ms 부팅)는 각기 다른 언어와 철학으로 출발했지만 공통된 방향으로 수렴하고 있다 — JSON 출력 기본값, 구조화 스키마 자기 서술, 샌드박싱을 통한 권한 경계. 에이전트를 primary user로 설계한다는 전제를 이 프레임워크들이 공유하고 있으며, 그 전제는 OpenClaw가 먼저 증명한 것이다.

이 수렴의 속도를 보여주는 관찰이 있다. 2026년 3월 9일을 기준으로 단일 주 안에 gogcli(OpenClaw 개발자), gws(Google DevRel), mogcli(Microsoft CoreAI VP)가 독립적으로 공개되었다. 사전 조율 없이 경쟁 관계에 있는 세 생태계가 동일한 설계 방향 — CLI 기반, 구조화 출력 — 으로 동시에 이동한 것은 개별 판단이 아니라 생태계 수준의 수렴 신호다.

MiroFish는 이 수렴 방향에서 흥미로운 위치에 있다. 학부생 개발자 Guo Hangjiang이 10일 만에 개발한 swarm intelligence 기반 예측 엔진으로, 수천 개의 AI agent가 독립적 성격·기억·행동 로직으로 상호작용하며 미래 시나리오를 시뮬레이션한다. GitHub 18k+ Stars와 샨다 그룹의 3,000만 위안 투자는 이 프로젝트의 외부 평가를 보여주지만, 필자가 이 책에서 MiroFish를 주목하는 이유는 수치보다 구조에 있다. 수천 개의 agent가 동시에 실행되는 군집 시스템에서, 개별 agent의 harness 품질이 전체 시스템 신뢰도를 결정한다는 관계는 단일 agent 환경보다 훨씬 투명하게 드러난다. 상류 agent의 실패가 하류 전체로 전파되는 패턴 — §4에서 기술하는 multi-agent 조합 실험이 보여주는 것과 동일한 구조 — 은 군집 규모에서 증폭된다.

이 surface 수렴과 나란히, 2026년 초에는 다른 종류의 수렴이 가시화되기 시작했다. 병렬 agent session의 isolation, notification, lifecycle 관리 문제를 다루는 터미널 멀티플렉서 도구들이 — 서로 독립적으로, 같은 시기에 — 등장했다.¹ 각 도구가 해결하려는 것은 동일했다: 여러 agent가 동시에 실행될 때 어느 session이 지금 대기 중인지를 운영자가 즉각 파악할 수 있는 attention routing, session 간 파일시스템 충돌을 방지하는 workspace isolation, 그리고 작업이 완료되거나 실패했을 때 상태를 깔끔하게 정리하는 graceful teardown. 세 기능 모두 Ch.3에서 정의하게 될 harness의 operational envelope 안에 속한다. 서로 다른 팀이 독립적으로 같은 문제 공간에 수렴했다는 사실 자체가, 이 문제가 개별 팀의 설계 선택이 아니라 생태계가 구조적으로 마주치는 병목임을 보여준다. CLI-Anything이 CLI agent surface의 패턴 수렴을 보여준 것처럼, 이 멀티플렉서 도구들은 harness operational layer의 패턴 수렴을 보여준다 — Ch.6에서 독립적 수렴 사례로 나란히 놓게 될 관찰이다.

Anthropic의 Project Vend는 이 생태계 관찰에 외부 실험 좌표를 제공한다.² 사내 자판기를 Claude 기반 단일 에이전트로 자율 운영하게 한 Phase 1에서, 운영 첫 달에 초기 자본금의 20%가 사라졌다. CRM이 없는 상태에서 에이전트는 원가를 추론에 의존했고, context window가 리셋될 때마다 이전 세션에서 결정된 할인 정책이 복귀했다 — 메모리가 아닌 context에 상태를 보관한 구조가 만든 학습 리셋 현상이었다. Phase 2는 CRM 도구, 원가 가시성 구조, 결제 선처리 메커니즘, CEO 에이전트를 추가하여 주간 흑자 전환에 성공했다. 개선의 실제 동인은 모델 버전 교체(Sonnet 3.7→4.0→4.5)가 아니라 harness component의 점진적 추가였다. 그러나 CEO 에이전트도 동일한 구조적 취약점을 공유했고, WSJ 레드팀은 조작된 기업 지배구조 문서 하나로 3주 안에 시스템을 무너뜨렸다. 5변수 프레임워크로 이 패턴을 읽으면 Phase 1의 1차 병목은 harness였고, Phase 2에서 그 병목은 intervention 구조 — 외부 조작을 차단하는 레이어의 부재 — 로 이동했다. Phase 1→2 개선은 Ch.6 Fieldkit 점진적 도구화의 외부 사례로 재등장하고, CEO 에이전트의 실패는 E09~E14에서 측정하는 multi-agent coordination overhead의 현실 대응물이 된다.

플랫폼 레이어에서도 같은 방향의 움직임이 확인된다. 2026년 초, Anthropic은 multi-agent coordination을 공식 기능(experimental)으로 출시하면서 공식 문서에 이 문장을 포함시켰다 — "agent teams add coordination overhead and use significantly more tokens than a single session." 플랫폼이 자신의 기능 출시 문서에서 coordination overhead의 존재를 명시한 것은, 필자가 초기 운용에서 직접 겪었던 CPU saturation과 context fragmentation 패턴을 생태계가 공식적으로 인식하기 시작했다는 신호다. 시점에는 차이가 있지만 문제의 구조는 동일하다 — 그리고 이 구조는 Ch.3에서 HOR(Harness Overhead Ratio)로 정식화된다.

2026년 3월 기준으로 이 생태계가 아직 표준화하지 못한 것이 있다. Surface 변수는 빠르게 수렴 중이고, harness operational layer는 독립적 수렴 신호를 보내고 있으며, 플랫폼은 coordination overhead를 공식 비용으로 인식하기 시작했다 — 그러나 개별 CLI 도구와 프레임워크를 agent들이 조율하는 harness 레이어는 여전히 각 팀에 위임된 채 생태계 표준으로 자리잡지 못했다. 이 방향이 의미하는 것은 surface 문제가 플랫폼 레이어로 흡수될수록, 운영자가 직접 설계해야 하는 영역은 점점 harness의 핵심 — 관찰 구조, 복구 경로, 자원 경계 — 으로 좁혀진다는 것이다. surface가 해결될 때 harness의 필요성이 사라지는 것이 아니라, harness가 다루어야 할 문제의 윤곽이 더 선명해진다.

---

¹ cmux(Ghostty 기반, Swift/AppKit, macOS native), amux, dmux 등이 이 시기에 독립적으로 공개되었다. 이 책에서 특정 도구명을 본문에 직접 서술하지 않는 이유는, 도구 목록은 변하지만 이들이 해결하는 문제 구조는 지속되기 때문이다.

² Project Vend 서술의 출처는 저자 확인 필요 — `evidence/AUTHOR-VERIFY-REQUIRED.md` 참조. 출처 확인 전까지 이 사례는 "공개적으로 보고된 패턴의 예시"로 읽는다.

---

## §4 harness 없는 장기 운용 — 이 책을 쓰게 된 이유

> 상태: 🔴 초고 v0.1 (2026-03-18)

OpenClaw 위에 multi-agent 시스템을 구축하면서 필자가 처음 마주친 실패는 진단이 어려웠다. CPU 사용률이 100%에 고착되고 응답이 중단되는 패턴이 연속 운용 6~12시간 이후 재현되었는데, 로그에는 unhandled exception이 기록되지 않았다. SIGKILL 후 재시작해도 수십 초 이내에 동일한 상태로 복귀했다. 필자는 처음에 모델 추론 품질의 문제로 오진했다 — 응답이 중단되는 것을 모델이 context를 제대로 처리하지 못하는 증상으로 읽은 것이다. 이 오진은 모델을 교체하거나 프롬프트를 수정하는 방향으로 며칠을 소비하게 했고, 재현 조건은 달라지지 않았다.

5변수 진단으로 문제를 재구성했을 때 그림이 바뀌었다. 세 가지 실패 메커니즘이 독립적으로 작동하는 것이 아니라 공통 전제를 공유하고 있었다. GC Death Spiral은 Node.js 힙에 컨텍스트 객체가 무제한으로 누적되는 조건에서 시작된다 — GC의 CPU 점유가 처리를 지연시키고, 지연이 메모리 추가 누적을 가속하며, 이 양성 피드백 루프가 단일 프로세스 CPU를 포화시킨다. Cron Pile-up은 로그 정리, 메모리 요약, 상태 체크를 담당하는 백그라운드 태스크들이 각자 독립 타이머를 보유한 상태에서 시스템 부하가 70%를 넘어설 때 발생한다 — 부하로 인한 타이머 지연이 태스크들을 동시 실행 상태로 밀어넣고 CPU가 포화된다. Context Contamination은 단일 프로세스 내 공유 컨텍스트를 모든 태스크가 참조하는 구조에서, 30초 이상 소요되는 장기 태스크가 hang 상태에 빠지면 전체 응답 루프를 블로킹한다.

세 메커니즘 모두 `harness=None`이라는 공통 전제 위에서만 동시에 성립했다. 메모리 경계가 있었다면 GC Death Spiral의 피드백 루프를 끊을 수 있었다 — 그러나 스케줄러 없이는 부하 임계점에서 타이머 충돌이 남아 있었을 것이고, 프로세스 격리 없이는 hang이 전체 루프를 블로킹하는 조건이 유지되었을 것이다. 세 component가 서로 독립적 실패 경로를 보유한 것이 아니라, 하나를 막아도 다른 경로로 같은 결과에 도달하는 구조였다. 모델 교체가 이 세 메커니즘 중 어느 하나에도 영향을 주지 못한 이유는 모델이 이 메커니즘들의 인과 경로 어디에도 위치하지 않기 때문이었다.

이것이 필자의 OpenClaw 기반 초기 multi-agent 시스템 운용 실험의 관찰이었다. 72시간 이내에 재현 가능한 장애, 로그 부재, 수동 복구만 가능한 구조.

multi-agent 조합 실험은 다른 종류의 질문을 열었다. 역할별 모델 배치를 세 가지로 변형했다. 전 역할 고성능 모델(Claude Opus/GPT-4o 수준)을 배치하면 출력 품질은 유지되지만 LLM 비용이 예산의 4배를 초과했다(조합 A). 전 역할을 저가 모델로 교체했을 때 드러난 것은 단순한 품질 저하가 아니라 구조적 문제였다 — CEO 역할의 태스크 분해 오류가 하류 에이전트 전체로 전파되어 최종 출력 품질이 허용 범위 아래로 떨어졌고(조합 B), 이 결과는 `오류율(최종 출력) ≈ f(CEO 오류율) >> f(말단 에이전트 오류율)`이라는 비대칭 구조를 보여주었다. CEO에 Claude Sonnet을 유지하고 나머지 역할에 저가 모델(Gemini Flash, GPT-4o-mini, Haiku)을 계층적으로 배치한 조합 C는 이 비대칭을 역이용했다 — 조합 A 대비 LLM 비용 65% 절감과 허용 범위 내 품질 유지를 동시에 달성했다.

이후 harness를 도입한 개선 시스템에서 설계한 것은 6개의 운용 진입 게이트였다. 안정성(연속 크래시 0회 기준으로 10회 미만), 메모리(RSS 300MB 미만), 레이턴시(p95 응답 2초 미만), 비용(중복 토큰 비율 5% 미만), 보안(샌드박스 탈출 0회), 복원력(크래시→복구 30초 미만) — 이 기준을 통과하지 못한 에이전트에는 태스크가 배정되지 않는다. Watchdog이 메모리와 레이턴시 게이트를 실시간 감시하고, 나머지 게이트는 72시간 사전 검증으로 통과 여부를 확인한다. 이 구조 위에서 연속 10회 크래시 없는 운용이 확인되었고, 크래시 발생 시 30초 이내 자동 복구가 재현되었다.

harness 없는 초기 시스템의 실패와 harness를 도입한 개선 시스템의 결과 사이의 간격이 이 책의 질문을 만들었다. 무엇이 이 간격을 만들었는가 — 이것은 설계 패턴의 차이로 충분히 설명되는가, 아니면 어떤 조건에서 어떤 변수를 먼저 다루어야 하는가에 대한 보다 정밀한 이해가 필요한가. 이 실패를 겪으면서 가장 오래 붙잡혀 있던 질문은 결과가 아니라 감지 가능성에 관한 것이었다. CPU 100% 고착이 발생하기 전에 어떤 신호가 있었는가. 그 신호를 포착할 수 있는 관찰 구조가 있었다면 이 실패는 예방 가능했는가, 아니면 발생 후 복구 경로를 빨리 확보하는 것이 더 현실적인 접근이었는가. 이 질문이 Ch.4의 의도적 실패 실험 설계로 이어졌다.

---

## §5 왜 지금이 중요한가 — harness engineering 초기에 알 수 있는 것

> 상태: 🔴 초고 v0.1 (2026-03-18)

Agent 시스템이 아직 성숙하지 않은 지금이 관찰의 적기라는 주장은 반직관적으로 들릴 수 있다. 시스템이 성숙할수록 더 많은 것을 알 수 있을 것처럼 보이기 때문이다. 그러나 구조적 취약점의 관찰이라는 목적에서는 반대 방향이 참이다. 취약점은 추상화 레이어가 얇을 때 가장 선명하게 보인다. GC Death Spiral이 72시간 이내에 재현된 것은 harness와 프로세스 격리 없이 운영했기 때문이다. 더 성숙한 시스템에서는 동일한 메커니즘이 더 높은 수준의 추상화 뒤에서 작동하며, 원인과 증상 사이의 거리가 멀어진다.

모델 선택만으로는 agent 안정성을 보장할 수 없다는 관찰은 이 책 전체를 관통하는 출발 질문이다. 동일한 모델, 동일한 task 유형, 다른 실행 조건에서 출력 품질이 다르게 나타나는 패턴을 필자는 반복적으로 관찰했다. 모델 벤치마크가 예측하는 것과 실제 agent viability 사이의 간격이 어디서 오는가 — 이것이 Ch.2에서 ARCC를 측정하는 이유다. 그러나 그 측정을 시작하기 전에, 간격이 존재한다는 관찰 사실 자체를 Ch.1에서 확인하는 것이 필요하다.

초기 운용 실험에서 필자가 가장 오래 붙잡혔던 것은 경계가 선형이지 않다는 패턴이었다. 어떤 task-모델 조합은 수백 step이 지나도 안정적으로 실행되고, 다른 조합은 예고 없이 무너진다. 무너지는 패턴이 선형이었다면 — step 수가 늘어날수록 실패 확률이 조금씩 증가한다면 — 임계점을 예측할 수 있었을 것이다. 관찰된 패턴은 달랐다. 오랫동안 정상적으로 보이다가 어떤 시점에서 급격히 무너지는 비선형 패턴. 이 경계가 어디에 위치하고 무엇이 그것을 결정하는가가 Ch.2에서 Capability Cliff를 측정하는 배경이다.

지금 이것을 기록하는 것은 고도화된 이후에도 의미를 갖는다. 더 강력한 모델이 동일한 메커니즘에 더 높은 저항성을 가질 수 있지만 메커니즘 자체는 사라지지 않으며, 그 메커니즘을 지금 관찰해야만 Agent-2가 self-immune system으로 방어해야 하는 failure 유형의 목록을 도출할 수 있다.

---

## §6 5변수 프레임워크 소개

> 상태: 🔴 초고 v0.1 (2026-03-18)

초기 실패를 진단하는 과정에서 이원론이 먼저 작동했다. "모델 문제인가, 운영 구조 문제인가" — 이 구분은 직관적이고 처음에는 충분해 보였다. 그러나 모델 교체도, 운영 구조 개선도, 각각 단독으로는 재현 조건을 변경하지 못했다. 모델과 운영 구조 모두 최적화된 상태에서도 compute 변수가 1차 병목으로 등장했다. 이원론 안에서는 이 패턴을 설명할 수 없었다.

5변수 프레임워크는 이 설명 실패를 해소하기 위해 도입했다. 모델, harness, product surface, operator intervention, compute — 이 다섯 변수가 agent 성능에 독립적으로 영향을 미치며, 각 변수는 다른 변수를 고정한 채 격리·조작할 수 있다. 1차 병목이 무엇인가라는 질문은 이 다섯 변수 중 어느 것이 현재 조건에서 성능을 가장 크게 제한하고 있는가를 묻는 것이다. 그 답은 실험 조건에 따라 달라지며, 같은 시스템에서도 운영 phase에 따라 1차 병목이 전환된다.

각 변수가 이후 챕터에서 어떻게 다루어지는가를 미리 정리한다. 모델 변수는 Ch.2에서 ARCC를 통해 측정된다 — vendor tier나 벤치마크 점수가 왜 agent viability의 유효한 predictor가 아닌지, 그리고 어떤 측정이 그것을 대체하는지. Harness 변수는 Ch.3에서 정의되고 Ch.4의 E05~E08에서 조작된다 — failure budget이 harness 유무에 따라 어떻게 재배분되는가. Product surface 변수는 Ch.1~Ch.3에 걸쳐 OpenClaw 생태계 관찰로 다루어진다. Operator intervention 변수는 Ch.4의 E15~E17에서 격리된다 — 개입 타이밍과 방법이 MTTR에 미치는 영향. Compute 변수는 Ch.4의 E09~E14에서 조작된다 — GCP 무료 티어 제약이 실험 조건으로 작동하는 방식.

모델 변수 측정에서 문제가 되는 것을 미리 짚는다. Vendor tier(GPT-4, Claude Opus 등의 분류)나 표준 벤치마크(MMLU, HumanEval 등)는 단일 LLM 호출 품질을 측정하도록 설계되었다. Agent가 수행하는 것은 단일 호출이 아니라 multi-step chain이다 — 각 단계의 출력이 다음 단계의 입력이 되고, 초기 오류가 downstream에서 증폭되는 구조. 이 구조에서 의미 있는 모델 변수 측정은 단일 호출 품질이 아니라 multi-step chain에서의 오류 누적 저항성을 다루어야 한다. ARCC(Agent-Relevant Capability Composite)가 Ch.2에서 이 측정 문제를 다루는 이유가 여기 있다.

이 프레임워크는 진단 예측을 만들 수 있다. 조건을 하나 설정해보면: 컨텍스트 40K, harness 없음, GCP e2-micro 제약, 40-step 장기 태스크. 이 조건에서 필자가 예측하는 1차 병목은 compute이며, 구체적으로는 harness 부재 상태에서 메모리 누적이 CPU 사용률에 미치는 피드백 루프다. 이 예측이 맞다면, 동일 조건에서 harness를 추가하면 — 메모리 경계, 중앙 스케줄러, 프로세스 격리 중 하나라도 — CPU 포화 임계점이 늦추어지거나 제거될 것이다. 4번 실험(E04)은 harness 유/무를 격리 변수로 놓고 이 예측을 검증하도록 설계된다.

---

## §7 Agent-1 ~ Agent-5 방향 설정

> 상태: 🔴 초고 v0.1 (2026-03-18)

현재 배포된 대부분의 agent는 tool-using이다. 외부 도구를 호출하고, 그 결과를 다음 step의 입력으로 사용하며, 일련의 step을 통해 task를 완수한다. 이 능력 자체는 2년 전에 비해 크게 향상되었다. Tool call schema를 따르는 정확도, multi-step plan을 실행하는 능력, 긴 context를 활용하는 범위 — 모두 개선되었다. 그러나 이 능력들이 강화되는 동안 해결되지 않은 것이 있다: agent는 자신의 현재 상태를 알지 못한다.

Agent-1이라고 부르는 것은 이 상태다 — tool-using이지만 취약한, 외부 harness와 operator intervention 없이는 장기 자율 루프를 신뢰 가능하게 유지하지 못하는 세대. Agent-1이 취약한 이유는 능력의 부재가 아니라 self-monitoring의 부재다. cliff 근접을 감지하지 못하기 때문에 failure budget이 silent drift 방향으로 이동하는 것을 포착할 수 없고, 포착이 없으면 recovery 경로는 실행 조건 자체를 갖지 못한다.

Agent-2는 self-immune system을 보유한다 — ARCC self-monitoring, cliff-proximity detection, self-initiated recovery가 agent 내부에 주입된 상태. Agent-1이 외부 harness에 의존해 관찰되고 복구되는 것과 달리, Agent-2는 이 기능을 내부화한다. 그러나 Agent-2 전환에는 하한 조건이 있다. Self-monitoring 자체가 ARCC를 소비한다 — agent가 자신의 capability를 estimate하려면 그 estimate를 수행할 수 있는 capability가 먼저 확보되어야 한다. ARCC가 cliff threshold 이하인 agent에서는 self-monitoring이 신뢰 가능하지 않다. Self-immune system이 무너지는 순간이 정확히 self-monitoring이 필요한 순간이기도 하다는 재귀적 구조가 여기서 나온다.

Agent-3부터 Agent-5는 이 책의 범위 밖에 있다. Agent-3은 Agent-2의 self-immune 루프 위에서 새로운 task를 스스로 생성하는 능력을 추가하고, Agent-4와 Agent-5는 더 높은 수준의 자율성과 사회적 역량을 포함하는 방향으로 예측되지만, 2026년 상반기 시점에서 이것은 관찰이 아니라 추론이다. 이 책의 실험이 탐색하는 경계는 Agent-1과 Agent-2 사이다 — 어떤 조건에서 self-immune 구조가 신뢰 가능하게 작동하기 시작하는가.

---

## §8 AIE shout-out: 이 책의 위치

> 상태: 🔴 초고 v0.1 (2026-03-18)

Chip Huyen의 *AI Engineering*(2025)은 foundation model 위에 application을 구축하는 과정 전체를 다룬다. 모델 선택에서 시작해 prompt engineering, RAG, fine-tuning, evaluation framework, 배포까지 — application을 만드는 엔지니어가 마주치는 결정들을 체계적으로 다루는 지도다. 이 지도는 2024~2025년 AI application 개발의 실무를 정리하는 데 있어 현재까지 필자가 알고 있는 가장 포괄적인 참조 자료다.

이 책은 그 지도가 끝나는 지점에서 시작한다. AIE가 다루는 application layer는 모델이 단일 호출 또는 단기 대화 맥락에서 사용자와 상호작용하는 패턴을 기반으로 한다. Agent가 장기 자율 루프로 실행될 때 — 수십 개의 step이 연쇄되고, 외부 도구가 실제 환경을 변경하며, operator가 즉각 개입할 수 없는 조건에서 수 시간 이상 실행될 때 — 새로운 질문들이 등장한다. 그 runtime 상태를 어떻게 관찰하는가. 실패가 어떤 방향으로 발생하는가. 복구는 어떻게 설계되는가. 이 질문들은 AIE의 범위 밖에 있다 — AIE가 부족해서가 아니라, 두 책이 다루는 레이어가 다르기 때문이다.

이 책을 읽기 위해 AIE가 전제 조건인 이유는 레이어 관계 때문이다. Agent runtime의 운영 구조를 이해하려면 그 아래 레이어 — 모델이 어떻게 작동하는지, application이 어떻게 구성되는지 — 에 대한 기반이 있어야 한다. AIE는 그 기반을 제공한다. 이 책은 그 기반 위에 agent가 장기 자율 루프로 실행될 때 무슨 일이 일어나는가를 실험적으로 탐색한다.

---

## 참조

- `deep-research/DR-1.1-openclaw-ecosystem.md`
- `deep-research/DR-1.2-agent-first-surfaces.md`
- `deep-research/DR-1.3-aie-book-impact.md`
- `evidence/case-studies/openclaw-anchor.md`
- `evidence/case-studies/teamclaws-picoclaw-postmortem.md`
- `evidence/case-studies/openclaw-ecosystem-snapshot.md`
- `field-dispatches/2026-03/FD-2026-03-17-002-cli-renaissance.md`
- `field-dispatches/2026-03/FD-2026-03-17-002-wide-survey.md`
