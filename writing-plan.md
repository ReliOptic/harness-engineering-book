# 집필계획서 v6 — *Harness Engineering and AgentOps*

## 0. 프로젝트 개요

**제목**
*Harness Engineering and AgentOps*

**부제 후보**
*Observing What Makes Agents Work — and What Breaks Them*

**도입부 시간 앵커**
2026년 3월 13일 (도입 내러티브 기준일. 챕터 제목에는 넣지 않음.)

**책의 성격: 역사적 배경을 가진 agent engineering textbook + 실험서**
이 책은 권위 있는 논문들을 역사적 좌표로 배열한 뒤, 그것이 왜 오늘의 runtime 실패와 연결되는지를 실험으로 다시 묻는 책이다. Part I은 논문 서베이가 아니라 계보이고, Part II~IV는 그 계보를 현재 조건에서 검증하는 장이다. 10년 뒤에 AI agent를 처음 설계해야 하는 학생이 이 책을 펼쳤을 때, Part I이 역사적 배경을 제공하고 Part II~IV가 2026년의 실험 기록을 제공하는 구조다.

Part I은 Transformer, 정보이론, alignment, tool use 연구를 역사적 좌표로 배열하여 agent가 왜 이렇게 작동하는지의 배경을 제공하고, Part II~IV는 그 배경 위에서 관찰, 실험, 도구화, 내재화를 기록한다. OpenAI 팀이 정의한 harness engineering 프레임워크 — Context Engineering, Architectural Constraints, Entropy Management — 를 출발점으로 삼되, Part I의 역사적 계보가 그 프레임워크의 배경을 제공하고, Part III의 22개 실험이 제약 환경에서의 작동과 한계를 검증한다.

**레퍼런스**
- OpenAI, *Harness Engineering: Leveraging Codex in an Agent-First World* (2026). 이 책이 실험으로 검증하는 1차 연구.
- Chip Huyen, *AI Engineering* (2025). Foundation model 위에 application을 만드는 전 과정. 이 책은 AIE가 다루는 영역의 다음 레이어를 실험으로 기록한다.

**원고 마일스톤**

| 마일스톤 | 목표일 |
| --- | --- |
| Part I 초고 (Ch.1~4) | 2026년 4월 15일 |
| Beta manuscript (11챕터 초고) | 2026년 5월 31일 |
| Polished release manuscript | 완성도 우선, 일정 미확정 |

**책의 근본 자세**
미리 결론을 정해놓고 증거를 끼워맞추지 않는다.
관찰하고, 측정하고, 기록하고, 그 기록에서 패턴을 추출한다.

---

## 집필 맥락 및 핵심 결정 (AI 협업 / 인수인계용)

> 이 섹션은 다른 AI 또는 다른 환경에서 이 프로젝트를 이어받을 때
> 맥락을 완전히 복원하기 위한 결정 로그다.
> 이 writing-plan을 처음 읽는 AI는 이 섹션을 먼저 읽어야 한다.

---

### 이 책은 무엇인가

핵심 논문들이 agent를 어떻게 가능하게 했는지를 기반으로 깔고(Part I), OpenAI 팀이 정의한 harness engineering 프레임워크를 분석하고(Part II), 그 원칙들이 실제 제약 환경에서 어떤 조건에서 작동하고 어디서 무너지는지를 22개 실험으로 검증하고(Part III), 관찰에서 도구와 시스템으로 진화하는 경로를 기록한다(Part IV).

**이 책이 아닌 것:**
- 개인 실패 경험 기록이 아니다
- 저자의 독자적 프레임워크를 주장하는 책이 아니다
- OpenAI와 경쟁하거나 대안을 제시하는 책이 아니다
- 논문 서베이 또는 교과서가 아니다

**저자의 역할:** 연구자 + 실험자. 핵심 논문의 개념을 agent runtime 실무에 번역하고, 그것을 제약 환경에서 실험하여 관찰을 기록한다.

---

### 핵심 결정 로그

| 날짜 | 결정 | 이유 |
| --- | --- | --- |
| 2026-03-20 | 개인 서사 완전 제거 (TeamClaws/PicoClaw 포함) | 감정적 서술 제거. 연구 분석이 책의 권위. 개인 경험은 어떤 형태로도 챕터에 등장하지 않는다 |
| 2026-03-20 | OpenAI 명시적 인용 결정 | 모호하게 쓰지 않는다. OpenAI 연구가 이 책의 1차 검증 대상임을 명확히 |
| 2026-03-20 | 5변수 = 조작적 분석 구조 (귀납 도출 아님) | 저자가 경험에서 귀납한 것이 아니라 OpenAI 연구를 실험으로 비교하기 위한 분석 구조 |
| 2026-03-20 | TCR을 공통 측정 단위로 확정 | 5변수가 이질적 단위를 가짐. "1차 병목" 비교는 TCR(Task Completion Rate) 기준으로 통일 |
| 2026-03-20 | harness_engineering_glossary.md → DR reference로 재정의 | OpenAI 논문 기반 용어집. 책의 backbone glossary가 아니라 검증 대상 프레임워크의 원전 용어 스냅샷 |
| 2026-03-30 | v6 구조 전환: 7챕터 → 11챕터 4-Part | 핵심 논문을 각 소주제의 backbone으로 세우고, prerequisite 개념까지 포괄하는 구조로 확장. compression lens 챕터가 패턴의 참조 구현 |
| 2026-03-30 | Part I 신설: 논문 기반 기초 4챕터 | Attention Is All You Need, Language Modeling Is Compression, InstructGPT/Constitutional AI, Toolformer/ReAct/Reflexion을 backbone으로 배치 |
| 2026-03-30 | learning curve 3단계 전 챕터 적용 | editorial-learning-curve-guideline.md의 직관 앵커 → 정밀 정의 → 운영 번역 구조를 Part I~IV 전체에 의무 적용 |
| 2026-03-30 | 기존 7챕터를 Part II~IV로 재배치 | Ch.1→Ch.5, Ch.2→Ch.6, Ch.3→Ch.7, Ch.4→Ch.8, Ch.5→Ch.9, Ch.6→Ch.10, Ch.7→Ch.11 |

---

### 파일 구조

**현재 존재하는 파일:**

```
harness-engineering-book/
├── CLAUDE.md              # AI 협업 지침 + voice rules (필수 참조)
├── writing-plan.md        # 이 파일. 마스터 집필 계획서 v6
├── list-of-contents-v6.md # 챕터별 상세 목차 + 섹션별 학습 곡선 설계
├── chapter-map.md         # 챕터별 상세 아웃라인 (v6 업데이트 필요)
├── token-policy.md        # 토큰 사용 정책
├── editorial-learning-curve-guideline.md  # 학습 곡선 편집 가이드라인
│
├── chapters/              # 챕터 초고 (현재 구 번호 체계)
│   ├── preface.md
│   ├── ch01-what-is-happening-now.md              # → v6 Ch.5로 rename 예정
│   ├── ch02-nature-agent-inherits.md              # → v6 Ch.6으로 rename 예정
│   ├── ch03-harness-and-agentops-defined.md       # → v6 Ch.7으로 rename 예정
│   ├── ch04-deliberate-failure-experiments.md     # → v6 Ch.8으로 rename 예정
│   ├── ch05-lessons-from-experiments.md           # → v6 Ch.9로 rename 예정
│   ├── ch06-from-observation-to-operational-compiler.md  # → v6 Ch.10으로 rename 예정
│   └── ch07-harness-to-agent-self-immune.md       # → v6 Ch.11로 rename 예정
│
├── deep-research/         # DR reference 파일들
├── evidence/              # 사례 연구, 외부 관찰 기록
├── field-dispatches/      # FD series (현장 관찰 노트)
├── experiments/           # 실험 로그 (E01~E22)
├── operational-compiler/  # Operational Compiler 설계
├── references/            # 참고문헌
├── team/                  # 팀 에이전트 역할 정의, 워크플로
│
└── dialogue/              # 챕터별 대화형 통찰 수집 (아래 설명 참조)
    ├── README.md
    ├── ch01-attention/
    ├── ch03-alignment/
    ├── ch04-tools-reasoning-memory/
    ├── ch05-five-variables/
    ├── ch07-harness-fbr/
    └── ch11-self-immune/
```

#### `dialogue/` 폴더의 목적과 사용법

이 책의 원료는 두 종류다. 하나는 실험 데이터(E01~E22)이고, 다른 하나는 **저자가 핵심 논문과 개념을 이해해 가는 과정에서 생성된 대화 기록**이다. 이 두 원료는 독립적이지 않다. 저자의 대화 과정에서 새로운 실험 시나리오가 도출되거나, 기존 실험의 관찰 범위가 조정될 수 있다. 따라서 E01~E22 실험 목록은 확정된 것이 아니라, 대화 기록의 진행에 따라 추가·수정·누락될 수 있는 가변적 목록이다. Ch.2 compression lens 영어 원고가 Claude와의 대화를 통해 만들어진 것처럼, 나머지 챕터들도 동일한 방식으로 집필 재료를 생산한다.

**구조**: 각 폴더에 `prompt.md`가 있다. 이 프롬프트를 새 Claude 세션에 붙여넣으면 대화가 시작된다. 프롬프트는 해당 챕터의 backbone 논문/자료를 제시하고, 저자의 이해도를 평가하는 10가지 질문을 던진다. 질문은 기초(논문 내용) → 심화(메커니즘 연결) → 운영 번역(agent runtime 연결) 순서로 진행된다.

**대화 결과**: 모든 질문이 끝나면 Claude가 다음을 생성한다:
- `insight-summary.md` — 이해도 프로필 + 핵심 통찰
- `writing-material.md` — 해당 챕터의 운영 번역 섹션 초안 재료
- `connections.md` — 다른 챕터와의 연결 씨앗

**집필 시 사용법**: 챕터 초고 작성 세션(`/draft`)에서 해당 `dialogue/chNN/` 폴더의 결과 파일을 context로 로드하면, 저자의 이해 과정에서 나온 통찰이 집필에 직접 반영된다. 특히 각 챕터 마지막 섹션(Agent Operations 시사점 / 운영 번역)의 핵심 논점은 이 대화에서 도출된다.

**대화 순서**: Ch.1 → Ch.3 → Ch.4 → Ch.5 → Ch.7 → Ch.11. Ch.5는 Part I(Ch.1~4) 대화를 모두 마친 후에 시작해야 Part I 개념 회수가 가능하다. Ch.11은 Ch.7(FBR/HOR) 대화 이후에 시작해야 운영 지표 개념이 전제로 작동한다.

**제외된 챕터**: Ch.2(이미 영어 원고 존재), Ch.6(Ch.2+Ch.4 대화 결과+실험 데이터로 구성), Ch.8~9(실험 데이터가 원료), Ch.10(Ch.8~9 분석에 의존).

**Phase 0에서 생성 예정:**

```
├── chapters/
│   ├── ch01-attention-and-context.md              # Part I — 신규
│   ├── ch02-compression-lens.md                   # Part I — 영어 원고 한국어 적응
│   ├── ch03-alignment-to-autonomy.md              # Part I — 신규
│   └── ch04-tools-reasoning-memory.md             # Part I — 신규
│
├── reference-chapters/    # 참조 원고
│   └── compression-lens-en.docx  # Ch.2 한국어 적응의 영어 원본
│
└── diagrams/              # 그림, 도표
```

---

### 챕터 현재 상태

| v6 챕터 | 현재 파일명 | v6 목표 파일명 | 상태 | 잔여 작업 |
| --- | --- | --- | --- | --- |
| Preface | `preface.md` | (변경 없음) | 🟡 v0.2 | 마지막 문장 voice rule 위반 재작성 |
| **Ch.1** | — (미생성) | `ch01-attention-and-context.md` | 🔲 미착수 | 전체 신규 집필 |
| **Ch.2** | — (미생성) | `ch02-compression-lens.md` | 🔲 미착수 | 한국어 적응 + voice rule 적용 + 5변수 연결 강화 (영어 원고 존재) |
| **Ch.3** | — (미생성) | `ch03-alignment-to-autonomy.md` | 🔲 미착수 | 전체 신규 집필 |
| **Ch.4** | — (미생성) | `ch04-tools-reasoning-memory.md` | 🔲 미착수 | 전체 신규 집필 |
| Ch.5 | `ch01-what-is-happening-now.md` | `ch05-what-is-happening-now.md` | 🔴 v0.1 | rename 후 voice rule 위반 수정 + 5변수 프레임워크 통합 |
| Ch.6 | `ch02-nature-agent-inherits.md` | `ch06-nature-agent-inherits.md` | 🔴 v0.1 | rename 후 `[X]` 보완, §2 측정 지표 도입 순서 재설계, §8 재작성, ARCC → 개별 관찰 지표 전환 |
| Ch.7 | `ch03-harness-and-agentops-defined.md` | `ch07-harness-and-agentops-defined.md` | 🔴 v0.1 | rename 후 line 71 손상 복구, §1 직관 앵커 추가, §5 FBR 직관 앵커 추가 |
| Ch.8 | `ch04-deliberate-failure-experiments.md` | `ch08-deliberate-failure-experiments.md` | 🔴 v0.1 | rename 후 §7-§8 마커 채움, 수치 보완 |
| Ch.9 | `ch05-lessons-from-experiments.md` | `ch09-lessons-from-experiments.md` | 🔲 scaffold | rename 후 전면 초고 작성 (Ch.8 실험 완료 후) |
| Ch.10 | `ch06-from-observation-to-operational-compiler.md` | `ch10-operational-compiler.md` | 🔴 v0.1 | rename 후 §1-§5 보완 |
| Ch.11 | `ch07-harness-to-agent-self-immune.md` | `ch11-self-immune-system.md` | 🔴 v0.1 | rename 후 §4 직관 앵커 추가, §3-§9 보완 |

---

### 이 프로젝트를 이어받는 AI에게

1. **writing-plan.md가 단일 진실의 원천이다.** CLAUDE.md는 voice rules와 AI 협업 지침을, writing-plan.md는 집필 전략과 결정 사항을 담는다. list-of-contents-v6.md는 섹션 단위 상세 설계를 담는다.
2. **5변수 프레임워크는 실험 분석 구조다.** 저자 경험에서 귀납한 것이 아니라 OpenAI 연구를 TCR 기준으로 비교 실험하기 위한 조작적 정의다.
3. **개인 서사 금지.** TeamClaws, PicoClaw, 저자의 개인 실패 경험은 어떤 형태로도 챕터에 등장하지 않는다.
4. **OpenAI는 명시적으로 인용한다.** "전문가 그룹"처럼 모호하게 쓰지 않는다.
5. **Voice rules는 CLAUDE.md에 있다.** AI 문체 금지 8대 원칙 포함. 초고 작성 시 반드시 참조.
6. **Deep-research 파일들은 인용 출처가 아니다.** DR이 인용한 원문을 확인하여 그 원문을 인용한다.
7. **Part I은 논문 기반이지 논문 서베이가 아니다.** 각 챕터는 backbone 논문의 개념을 3단계 학습 곡선(직관 앵커 → 정밀 정의 → 운영 번역)으로 도입하고, 마지막 섹션에서 agent operations로 번역한다. compression lens 챕터가 이 패턴의 참조 구현이다.
8. **learning curve guideline을 따른다.** editorial-learning-curve-guideline.md의 3단계 구조, 개념 밀도 제어(섹션당 신규 개념 최대 2개), 적층 원칙이 전 챕터에 적용된다.

---

## 1. 핵심 탐구 질문과 개념 정의

### 한 줄 논제

핵심 논문들이 agent를 가능하게 한 메커니즘을 이해하고, OpenAI 팀이 정의한 harness engineering 원칙들을 실제 제약 환경에서 5변수 프레임워크로 실험한다.

### 왜 지금이 중요한 시점인가

2026년 상반기, agent runtime은 아직 공고하지 않다. Harness engineering이라는 용어 자체가 이제 막 정의되기 시작했고, 모델·harness·surface·intervention·compute의 상호작용이 어떤 조건에서 어떤 병목을 만드는지에 대한 체계적 관찰이 거의 없다. 이 불안정한 초기 상태가 역설적으로 관찰의 적기다 — agent가 고도화되기 전에, 그것을 구성하는 변수들 사이의 상호작용을 노출된 상태에서 기록할 수 있기 때문이다.

### 5변수 프레임워크: 병목 비교를 위한 분석 구조

OpenAI 프레임워크의 Harness 변수를 포함하여, agent runtime의 실질적 병목을 구성하는 변수들을 이 책은 다음 5개로 조작적으로 정의한다. 이원론("모델 vs. 운영 구조")이 아니라, 어떤 조건에서 무엇이 1차 병목이 되는가를 TCR(Task Completion Rate) 기준으로 비교하기 위한 실험 분석 구조다.

| 변수 | 설명 |
| --- | --- |
| **모델** | Foundation model의 reasoning, tool use, consistency, confidence 특성 |
| **Harness** | Operational envelope: memory 보호, 권한, 복구, evaluation hook |
| **Product surface** | Agent가 input/output을 주고받는 인터페이스 (CLI, API, 기타) |
| **Operator intervention** | 인간 운영자의 개입 패턴, 타이밍, 효과 |
| **Compute/resource budget** | VM 사양, token budget, API 비용, 네트워크 지연 |

**이 책의 핵심 질문은 "모델과 harness 중 누가 더 중요한가?"가 아니다.**
**"어떤 조건에서 무엇이 1차 병목이 되는가?"이다.**

이것을 실험을 통해 관찰하고 측정한다.

### 핵심 탐구 질문

1. **Agent 시스템의 품질을 결정하는 5개 변수 중, 어떤 조건에서 무엇이 1차 병목이 되는가?** — 이원론이 아닌, 다변수 상호작용을 실험으로 관찰한다.
2. **제약 환경에서는 어떤 병목이 가장 먼저 드러나는가?** — 실용적 사실: threshold가 낮아서 빨리 실패하고, "괜찮다/안 괜찮다"를 빠르게 판별할 수 있다.
3. **AgentOps의 범위와 역할은 무엇이며, 어디까지 확장되는가?** — 함의를 좁히지 않고 열어둔다.
4. **Harness engineering을 통해 AgentOps 기능을 agent 자체에 점진적으로 주입할 수 있는가?** — Self-immune system을 향한 경로.

### 이 책의 관찰 프로그램 (5개 관찰 축)

1. 같은 task에서 **모델을 바꾸면** agent 행동과 failure mode가 어떻게 달라지는가
2. 같은 모델에서 **harness와 surface를 바꾸면** 결과가 어디까지 달라지는가
3. **제약 환경**에서는 어떤 병목이 가장 먼저 드러나는가
4. 어떤 **operator intervention**이 반복 가능해서 reusable runtime aid로 굳어지는가
5. AgentOps의 어떤 기능은 **harness 안으로 부분 내재화**될 수 있는가

### 반드시 포함할 반례

**반례 1 — Task design 문제:**
어떤 실패는 harness나 모델 문제가 아니라 task 자체가 불안정한 경우이다. 질문이 흔들리면 runtime을 아무리 튜닝해도 흔들린다.

**반례 2 — Compute saturation 문제:**
어떤 실패는 모델이나 harness가 아니라 compute 포화 문제이다. VM 과부하, CPU 불안정, agent 충돌이 그 예이다. 이 경우 AgentOps는 observability만이 아니라 resource governance여야 한다.

### 핵심 용어 정의

**Harness**
Memory, privacy, 권한, 핵심 context를 보호하면서 bounded capability, 재현성, 복구를 가능하게 하는 설계된 operational envelope.
나아가, AgentOps의 기능을 agent 내부에 점진적으로 주입하는 구조적 프레임워크이기도 하다.

**AgentOps**
비결정적 agent runtime을 **관찰 가능하고, 통제 가능하고, 복구 가능하고, 자원 인식적**으로 운영하기 위한 실천 규율.
Logging만이 아니라, intervention policy, permission design, recovery path, cost/latency discipline, compute overload control, self-reporting을 포함한다.
MLOps/DevOps에서 파생되었으나 그것보다 넓으며, 궁극적으로 harness를 통해 agent 자체에 내재화되는 방향으로 진화한다.

**Agent-first product surface**
Agent가 input을 안정적으로 해석하고 구조화된 feedback을 받을 수 있도록 설계된 제품 표면.
현재 인류가 알고 있는 가장 효과적인 형태는 CLI이다.
그러나 CLI를 대체하거나 확장할 수 있는 더 나은 형태가 있지 않을까? — 이 질문을 열어둔다.

**Operational Compiler**
제약 실험에서 반복적으로 확인된 failure pattern과 intervention rule을 실행 가능한 운영 규칙으로 컴파일하는 구조.
**Harness에 직접 한 번에 embedding하는 것이 아니다.**
Lesson learned가 누적될수록 Operational Compiler는 업데이트되고, 그 업데이트가 더 정교한 self-immune system의 외부 전단을 형성한다.
**한 번에 implement하는 것이 아니라, 점진적으로 발전시키는 것이 조건이다.**

---

## 2. 독자 정의

### Primary reader

**Technical builder-operator**: agent runtime을 직접 다루는 사람.

- Agent runtime 실험 중인 엔지니어 (OpenClaw, Claude Code, nanobot 등)
- Open-source agent 빌더 및 운영자 — 특히 tool 연결 및 확장
- Agent-first application을 설계하는 product/technical lead

**이 독자의 월요일 아침 문제:**
"어제까지 잘 돌던 workflow가 모델 업데이트 후 tool call에서 실패한다. 모델 문제인지 harness 문제인지 compute 문제인지 모르겠다. 그리고 이 agent에 proactivity가 부족한 것 같은데, 어떻게 개선하지?"

### Secondary reader

전략 지향 기술자, 스타트업 팀, 기술 product owner.

### 난이도

LLM, tool use, agent workflow 실무 수준 전제. ML 연구 전문성 미전제.
Part I이 필요한 개념적 기반을 제공하므로, 독자는 정보이론이나 attention 메커니즘의 사전 지식 없이 책을 시작할 수 있다.
모든 챕터는 product lead가 이해 가능하면서 builder에게 유용해야 한다.

---

## 3. 포지셔닝

### 이 책의 정체

- 핵심 논문의 개념을 agent runtime 실무로 번역하는 기반 + 독립적 실험 검증 기록
- 제약 환경에서 5변수 병목을 TCR 기준으로 비교한 field book
- Harness engineering과 AgentOps의 실험적 정의 — 관찰에 기반하여 경계를 그린 초기 시도
- 관찰 → 측정 → 도구화 → agent 내재화의 방법론 경로
- Ch.8-9의 실험 설계가 후속 학술 연구의 벤치마크가 될 수 있는 수준

### 이 책이 아닌 것

- 결론을 미리 정하지 않는다
- "모델 vs. harness" 이원론이 아니다
- AgentOps 백과사전이 아니다
- CLI를 최종 형태로 경직되게 취급하지 않는다
- 논문 서베이가 아니다 (Part I은 서베이가 아니라 실무 번역이다)

### CLI 열린 포지셔닝

CLI는 현재 가장 효과적인 agent-first surface이다. 그러나 더 나은 형태가 있지 않을까?
다양한 시도를 해보고, agent/harness/모델의 진화에 따라 surface도 진화할 가능성을 열어둔다.

---

## 4. 교육 설계 원칙

### Learning Curve 3단계 구조

editorial-learning-curve-guideline.md에 정의된 구조로, 모든 챕터의 모든 새로운 개념에 의무 적용한다.

| 단계 | 역할 | 판정 기준 |
| --- | --- | --- |
| Stage 1 — 직관 앵커 | 독자가 이미 아는 경험에 개념 연결 | 전문 용어 등장 전에 비유/시나리오가 존재하는가? |
| Stage 2 — 정밀 정의 | 정확한 정의와 수식 제시 | 직관 앵커와 정의 사이에 논리적 다리가 있는가? |
| Stage 3 — 운영 번역 | 실무에서 무엇을 의미하는지 명시 | agent runtime/harness/AgentOps와 연결되는가? |

### 참조 구현

`compression lens 챕터 -learning curve reference.docx`가 이 패턴의 모범 구현이다.
7개 섹션에 걸쳐 정보이론 개념을 3단계로 도입하고, 마지막 섹션에서 agent operations로 번역한다.
Part I의 모든 챕터가 이 패턴을 따른다.

### 개념 밀도 제어

- 한 섹션에 신규 개념 최대 2개
- 표와 수식 사이에는 산문 연결 필수
- Callout box는 챕터당 최대 3개, Stage 3(운영 번역) 핵심 메시지에만 사용

### 적층 원칙

- **챕터 내**: 선형 적층. 앞의 개념 위에 뒤의 개념이 쌓인다.
- **챕터 간**: 참조 적층. 앞 챕터에서 정의된 개념은 한 문장 재도입으로 충분하다.
- **Part I → Part II~IV**: Part I에서 확립된 개념은 Part II 이후에서 재정의보다 현장 정당화에 집중한다. Part II가 Part I의 개념을 현장 관찰로 다시 도입하는 것은 재정의가 아니라 정당화이며, 이것이 적층의 한 형태다.

---

## 5. 내러티브 척추와 핵심 사례

### 스냅샷 원칙

2026년 상반기에 벌어지는 일의 스냅샷을 정직하게 기록한다.

### 연구 출발점: OpenAI harness engineering 프레임워크

OpenAI 팀이 정의한 harness engineering — Context Engineering, Architectural Constraints, Entropy Management 3-pillar — 이 책이 실험으로 검증하는 원전 프레임워크다.
이 프레임워크는 최적 환경(내부 엔지니어, 충분한 compute)에서 도출되었다.
이 책의 질문: 제약 환경에서 동일한 원칙들이 어떻게 작동하는가. 어떤 조건에서 병목이 harness 외부 변수로 이동하는가.

### 실험 환경: OpenClaw

OpenClaw는 이 책의 실험이 수행된 agent runtime 환경이다.
MCP 연결, skills 통합, gateway 아키텍처를 하나의 운영 가능한 시스템으로 제공한다.
OpenAI 프레임워크의 원칙들을 이 환경에서 격리 조작하여 실험한다.

### 생태계 스냅샷

OpenClaw 주변 프로젝트들 (nanobot, CLI-Anything, OpenClaw-RL, openclaw-agents, openclaw-studio 등)을 deep research로 기록. 2026년 상반기 agent 생태계의 기록적 가치.

---

## 6. 챕터 구조 (11개 챕터, 4 Parts)

### 전체 논리 흐름

```
Part I — 기반: Agent를 만든 논문들
  Ch.1   Attention과 Context: 모델은 어떻게 보는가
  Ch.2   압축 렌즈: 모든 언어 모델은 압축기다
  Ch.3   정렬에서 자율로: 모델은 어떻게 행동을 배우는가
  Ch.4   도구, 추론, 기억: Agent는 어떻게 행동하는가
    ↓  Part I의 개념적 기반 위에서
Part II — 프레임워크: 관찰과 측정
  Ch.5   왜 다섯 변수인가: 현장에서의 정당화
  Ch.6   Agent가 모델로부터 무엇을 물려받는가
  Ch.7   Harness Engineering과 AgentOps
    ↓  프레임워크를 제약 환경에서 실험
Part III — 실험: 의도적 실패
  Ch.8   22개 시나리오: 무엇이 어떤 조건에서 깨지는가
  Ch.9   실험이 보여준 것
    ↓  실험에서 도구와 시스템으로
Part IV — 진화: 관찰에서 시스템으로
  Ch.10  Operational Compiler: 관찰에서 도구로
  Ch.11  Self-Immune System: Harness에서 Agent로
```

**Part 간 관계:**
- **Part I → Part II**: Part I은 역사적 계보, Part II는 그 계보가 2026년 현장에서 어떤 모습으로 나타나는지의 관찰. Part I 없이 Part II를 읽을 수 있지만, Part I을 거치면 관찰이 메커니즘으로 해석 가능해진다. Part I이 Part II를 결정하지는 않는다.
- **Part II → Part III**: Part II가 정의한 프레임워크와 가설을 Part III가 22개 실험으로 검증한다.
- **Part III → Part IV**: Part III의 관찰에서 패턴을 추출하여 Part IV가 도구와 시스템으로 진화시킨다.

---

### Part I — 기반: Agent를 만든 논문들

> 각 챕터는 1~2편의 핵심 논문을 backbone으로 삼는다. compression lens 챕터가 이 패턴의 참조 구현이다.

#### Chapter 1. Attention과 Context: 모델은 어떻게 보는가

**Backbone 논문:**
- Vaswani et al., *Attention Is All You Need* (NeurIPS 2017)
- Liu et al., *Lost in the Middle* (TACL 2024)

**핵심 구성:**
1. embedding과 벡터 공간
2. Attention 메커니즘의 해부 (Q-K-V)
3. Multi-Head Attention
4. Positional Encoding
5. Lost in the Middle — 긴 입력에서의 정보 손실
6. Agent Operations를 위한 시사점

**학습 결과:** "왜 context window를 늘려도 agent가 중간 정보를 놓치는가"를 attention 메커니즘으로 설명할 수 있다.

**Part II 해석 연결:**
- Context window ≠ attention capacity — Ch.6에서 관찰하는 context 활용 효율의 배경
- Attention 오배분 — Ch.6에서 관찰하는 tool call 정확도 문제의 한 가지 해석 경로
- System prompt 위치 설계 — Ch.7 harness의 context engineering에 대한 배경

---

#### Chapter 2. 압축 렌즈: 모든 언어 모델은 압축기다

**Backbone 논문:**
- Delétang et al., *Language Modeling Is Compression* (ICLR 2024)
- Shannon, *A Mathematical Theory of Communication* (1948)

**참조 구현:** compression lens 챕터 영어 원고의 한국어 적응 + 확장.

**핵심 구성:**
1. 정보량 I(x) = −log₂(p)
2. 엔트로피 H(P)
3. Cross-Entropy와 KL Divergence
4. Arithmetic Coding
5. Autoregressive 구조와 압축의 등가성
6. Bits-per-Byte: 보편 비교 척도
7. Agent Operations를 위한 시사점

**학습 결과:** "왜 더 좋은 모델이 더 잘 압축하는가"를 수식으로 설명할 수 있고, prompt 최적화와 모델 비교에 적용할 수 있다.

**Part II 해석 연결** (이 챕터는 Part II의 측정 체계를 직접 근거하는 것이 아니라, runtime 현상을 읽는 해석 렌즈를 제공한다):
- Cross-entropy — Capability Cliff를 정보이론적으로 읽는 하나의 방법 (Ch.6)
- Prompt 최적화 — cross-entropy 최소화의 관점에서 해석 가능 (Ch.7)
- Bits-per-byte — 모델 비교의 보편 척도로 활용 가능 (Ch.6)
- KL divergence — prompt drift를 읽는 하나의 해석 도구 (Ch.7)

---

#### Chapter 3. 정렬에서 자율로: 모델은 어떻게 행동을 배우는가

**Backbone 논문:**
- Ouyang et al., *InstructGPT* (NeurIPS 2022)
- Lee et al., *RLAIF* (2023)
- Bai et al., *Constitutional AI* (Anthropic, 2022)

**핵심 구성:**
1. InstructGPT와 RLHF — SFT → Reward Model → PPO
2. RLAIF — 인간 없이 스케일하기
3. Constitutional AI — 스스로 교정하기
4. 학습 정렬이 Runtime 문제를 풀지 못하는 구조적 이유

**학습 결과:** "모델이 aligned되었는데 왜 agent가 여전히 실패하는가"를 학습-runtime 경계로 설명할 수 있다.

**Part II/IV 연결:**
- Instruction following rate가 task마다 다른 이유 — Ch.6 모델 관찰의 배경
- 학습 vs runtime의 구조적 간극 → Ch.7 harness 필요성의 동기
- Constitutional AI의 self-critique → Ch.11 self-immune의 이론적 선행 좌표

---

#### Chapter 4. 도구, 추론, 기억: Agent는 어떻게 행동하는가

**Backbone 논문:**
- Schick et al., *Toolformer* (NeurIPS 2023)
- Yao et al., *ReAct* (ICLR 2023)
- Shinn et al., *Reflexion* (NeurIPS 2023)
- Lewis et al., *RAG* (NeurIPS 2020) — companion

**핵심 구성:**
1. Toolformer — 도구 사용의 자기 학습
2. ReAct — 추론-행동 통합 루프
3. Reflexion — 실패에서 배우기 (verbal reinforcement learning)
4. RAG — 외부 기억 장치
5. Agent Operations를 위한 시사점: 세 능력의 실패 지도

**학습 결과:** 도구 사용 정확도, instruction following, multi-step reasoning depth의 측정이 왜 필요한지를 각 능력의 실패 메커니즘으로 설명할 수 있다.

**Part II/IV 연결:**
- Toolformer (도구 사용 정확도) — Ch.6 모델 관찰의 배경
- ReAct (multi-step reasoning) — Ch.6 모델 관찰의 배경
- Reflexion = task 간 학습 / Self-immune = task 내 감지 → Ch.11
- RAG의 한계 → Ch.7 Ontology RAG, semantic firewall

---

### Part II — 프레임워크: 관찰과 측정

> Part I에서 확립한 개념을 전제한다. 각 개념은 한 문장 재도입으로 충분하다(적층 원칙).

#### Chapter 5. 왜 다섯 변수인가: 현장에서의 정당화

**기반:** 구 Ch.1 + v4 Ch.3의 5변수 프레임워크 + Agent-1~5 스펙트럼 통합

**이 챕터의 중심 질문:** Part I이 깔아둔 네 갈래 기술사(attention, compression, alignment, tool-use/memory)가 현장에서 부딪힐 때, 병목 분석의 최소 단위는 왜 다섯인가?

**핵심 구성:**
1. 2026년 상반기: agent가 깨지는 풍경 (배경, 목적이 아님)
2. Part I에서 이 현장으로: 네 갈래 기술사가 만나는 지점
3. 5변수 프레임워크: 병목 분석의 최소 단위
4. 이원론의 거부와 Agent-1~2 스펙트럼
5. 이 책의 좌표: AI Engineering 이후의 질문

**학습 결과:** Part I의 역사적 좌표가 현장에서 왜 5변수로 수렴하는지를 설명할 수 있고, 자신의 환경에서 병목을 식별할 수 있다.

---

#### Chapter 6. Agent가 모델로부터 무엇을 물려받는가

**기반:** 구 Ch.2

**핵심 구성:**
1. 물려받는 경향: reasoning, tool use, consistency, calibration
2. 모델 관찰 지표 — 도구 사용 정확도, instruction following rate, multi-step reasoning depth, context 활용 효율 (개별 지표로 도입, 2+2 분리)
3. Capability Cliff — 선형이 아닌 급락이 발생하는 조건
4. Quantization Tax Curve
5. Distillation Efficiency Frontier
6. Mid-run model switching의 context continuity 붕괴
7. 모델 변수가 1차 병목이 되는 조건 — 그리고 아닌 조건

**Part I 해석 연결** (각 관찰 지표의 학술적 배경):
- 도구 사용 정확도의 배경: Ch.4 §1 Toolformer
- Instruction following rate의 배경: Ch.3 §1 InstructGPT
- Multi-step reasoning depth의 배경: Ch.4 §2 ReAct
- Context 활용 효율의 배경: Ch.1 §5 Lost in the Middle
- Capability Cliff의 해석 렌즈: Ch.2 §3 cross-entropy

**학습 결과:** 모델 관찰 지표 기반의 측정을 설계할 수 있다. 모델이 1차 병목인 조건과 아닌 조건을 구분할 수 있다.

---

#### Chapter 7. Harness Engineering과 AgentOps

**기반:** 구 Ch.3

**핵심 구성:**
1. Harness Engineering이란 무엇인가
2. Guardrails, Scaffolding, Orchestration과의 구분
3. Ontology와 메모리 구조
4. Failure Budget Reallocation
5. AgentOps와 운영 지표 (HOR, MTTR, HER)
6. Ch.8 실험 프레임 설정 — 가설과 판단 기준의 Pre-registration

**Part I 연결:**
- Harness 필요성의 동기 ← Ch.3 §4 "학습 정렬이 runtime 문제를 풀지 못하는 이유"
- Ontology RAG ← Ch.4 §4 RAG의 한계
- Prompt drift 측정 ← Ch.2 §3 KL divergence

**학습 결과:** Harness와 AgentOps를 정의하고, Failure Budget Reallocation으로 harness 효과를 설명할 수 있다. Ch.8 실험의 가설을 이해한다.

---

### Part III — 실험: 의도적 실패

#### Chapter 8. 22개 시나리오: 무엇이 어떤 조건에서 깨지는가

**기반:** 구 Ch.4. 변경 최소 — learning curve를 비교적 잘 따르고 있다.

**핵심 구성:**
1. 실험 설계 원칙: 왜 의도적으로 실패시키는가
2. 실험 환경: GCP 무료 티어, OpenRouter, 측정 인프라
3. 1막 — 모델·harness·surface 변수 격리 (E01~E07)
4. 2막 — 자원 제약 하에서 self-immune의 최소 조건 (E08~E12)
5. 3막 — 개입의 반복 가능성과 내재화 (E13~E18)
6. 반례 — task design과 compute saturation (E19~E20)

**Part I 해석 연결 (인과 확정이 아니라 해석 가설 — 본문에서 검증):**
- E05 memory leakage — Ch.1 attention 메커니즘의 잔류 activation으로 해석 가능한 사례
- E08 자기평가 정확도 급락 — Ch.3 self-critique 루프의 runtime 한계와 관련될 수 있는 관찰
- E09 goal drift — Ch.1 Lost in the Middle과 Ch.4 ReAct 루프가 겹치는 현상으로 읽을 수 있는 사례

**학습 결과:** 자신의 환경에서 의도적 실패 실험을 설계하고 실행할 수 있다.

---

#### Chapter 9. 실험이 보여준 것

**기반:** 구 Ch.5 (scaffold → 초고로 끌어올리기 필요)

**핵심 구성:**
1. 22개 실험 결과 종합: 어떤 변수가 어떤 조건에서 1차 병목이었는가
2. Failure Budget Reallocation 정량 분석
3. 운영 metric 번역: MTTR과 Human Escalation Rate
4. 비용 metric 번역: TotalCost와 optimal HOR
5. Component ablation: 무엇이 얼마나 기여하는가
6. Token efficiency를 운영 규율로
7. Scaling과 temporal stability
8. 학술적 확장 가능성 — exploratory 발견 목록

**Ch.8과의 관계:** Ch.8이 실험의 실행과 기록이라면, Ch.9는 분석과 패턴 추출이다. 두 챕터가 이 책의 실험적 무게중심이다.

**학습 결과:** AgentOps 실무를 이해하고, computation 요구사항을 산정하며, 실험 결과에서 학술적 확장 가능성을 식별할 수 있다.

---

### Part IV — 진화: 관찰에서 시스템으로

#### Chapter 10. Operational Compiler: 관찰에서 도구로

**기반:** 구 Ch.6. 변경 최소.

**핵심 구성:**
1. 반복 실패 패턴에서 도구화 후보 식별
2. Operational Compiler 설계 원칙
3. 점진적 업데이트: Pareto frontier를 따라 이동하는 전략
4. Skill로 쓸 수 있는 능력의 극대화
5. CLI-Anything 방법론 비교: 독립적 수렴의 의미

**학습 결과:** 실험 로그에서 운영 규칙 컴파일 후보를 식별하고, 점진적 Operational Compiler 업데이트 전략을 설계할 수 있다.

---

#### Chapter 11. Self-Immune System: Harness에서 Agent로

**기반:** 구 Ch.7

**핵심 구성:**
1. 실험이 남긴 것
2. 현 세대 harness가 아직 풀 수 없는 문제
3. AgentOps → Harness → Agent 내재화: 점진적 경로
4. Self-immune system 초기 설계
5. Model Capability × Harness Value: Scaling 조건
6. Temporal Stability: self-immune은 얼마나 오래 유지되는가
7. Agent-1 → Agent-2: 전환 조건의 정식화
8. 이 책 이후: 미해결 질문들
9. 집필 과정의 메타 관찰

**Part I 해석 연결 (Part I의 투자가 회수되는 챕터):**
- Constitutional AI는 runtime self-immune이 놓인 학술적 계보를 제공한다 (Ch.3). 같은 메커니즘이 아니라 같은 문제 의식의 연장.
- Reflexion = task 간 학습 / Self-immune = task 내 감지 (Ch.4 §3). 시간 스케일의 차이가 핵심.
- Ch.2의 cross-entropy 프레임은 self-monitoring 자체의 bit cost를 생각하는 하나의 해석 렌즈.

**학습 결과:** Harness engineering이 Agent-2 전환에 왜 필수적인지 설명할 수 있다.

---

## 7. Agent-1 ~ Agent-5 프레임워크

| 레벨 | 작업 라벨 | 이 책에서의 역할 |
| --- | --- | --- |
| Agent-1 | Early Agent | 현 세대: tool-using이지만 취약, proactivity 결여 |
| Agent-2 | Continuous Learner | Self-immune system, collapse 후 자발 복구, infinite learning |
| Agent-3 | Domain Expert | 한정 영역 고속 역량, harness 전문화 |
| Agent-4 | Superhuman Researcher | 인간 실무자 초과 |
| Agent-5 | Collective | 조직 규모 조율 |

Ch.5에서 도입, Ch.11에서 Agent-1→2 전환에 집중.

---

## 8. 증거 전략

### 관찰 원칙

- 결론을 미리 정하지 않는다
- 결과가 예상과 다르면 결과를 기록한다
- 단일 실행에서 일반화할 때 반드시 잠정적으로 표시
- 반례를 적극적으로 포함한다

### 챕터-증거 매핑

| 챕터 | 1차 증거 | Deep research |
| --- | --- | --- |
| Ch.1 | Attention Is All You Need 분석, Lost in the Middle 실험 재현/해석 | DR-1.1, DR-1.2 |
| Ch.2 | Language Modeling Is Compression 분석, Shannon 원전 | DR-2.1 |
| Ch.3 | InstructGPT/RLAIF/Constitutional AI 분석 | DR-3.1, DR-3.2 |
| Ch.4 | Toolformer/ReAct/Reflexion/RAG 분석 | DR-4.1, DR-4.2 |
| Ch.5 | OpenClaw anchor, OpenAI 연구 분석, 생태계 survey | DR-5.1, DR-5.2, DR-5.3 |
| Ch.6 | 모델 교체 실험 (Cluster A) | DR-6.1, DR-6.2, DR-6.3 |
| Ch.7 | Cluster C, D + CLI-Anything + harness 부재 사례 | DR-7.1~7.4 |
| Ch.8 | **22개 의도적 실패 실험** | DR-8.1~8.4 |
| Ch.9 | Ch.8 결과 분석 + computation 측정 | DR-9.1~9.3 |
| Ch.10 | 반복 실패 패턴 → Operational Compiler 설계 | DR-10.1, DR-10.2 |
| Ch.11 | 전체 종합 + self-recovery 초기 실험 | DR-11.1, DR-11.2 |

---

## 9. 실험 프로그램: 22개 의도적 실패 시나리오

> 이 22개 시나리오가 Ch.8의 핵심이며, Ch.9 분석의 입력이다.
> 각 시나리오는 5변수 중 어떤 것을 조작하는지 명시한다.

### 관찰 축별 실험 배치

#### 축 1: 모델을 바꾸면 무엇이 달라지는가 (Ch.6 주력)

| # | 시나리오 | 조작 변수 | 예상 관찰 |
| --- | --- | --- | --- |
| E01 | 동일 GitHub issue triage를 SOTA vs. 소형 모델로 실행 | 모델 | Tool call 패턴, 완료율 차이 |
| E02 | 동일 코드 리뷰를 frontier vs. distilled 모델로 실행 | 모델 | 리뷰 품질, 환각률 차이 |
| E03 | 동일 multi-step CLI 작업을 quantized vs. full 모델로 실행 | 모델 | 중간 단계 실패 지점 비교 |
| E04 | 모델을 mid-run에서 교체 (workflow 중간에 모델 스위칭) | 모델 | Context 연속성 깨짐 패턴 |

#### 축 2: Harness와 surface를 바꾸면 무엇이 달라지는가 (Ch.7, Ch.8)

| # | 시나리오 | 조작 변수 | 예상 관찰 |
| --- | --- | --- | --- |
| E05 | 동일 task를 harness 있음 vs. 없음(raw model)으로 실행 | Harness | 실패 빈도, 복구 가능성 차이 |
| E06 | Memory 보호 해제 상태에서 multi-turn 대화 | Harness | Context leakage 패턴 |
| E07 | Permission boundary를 점진적으로 넓혀가며 실행 | Harness | 안전하지 않은 행동 발생 임계치 |
| E08 | 동일 task를 CLI vs. 다른 surface(API, webhook)로 실행 | Surface | 입출력 안정성 차이 |

#### 축 3: 제약 환경에서 가장 먼저 드러나는 병목 (Ch.8 주력)

| # | 시나리오 | 조작 변수 | 예상 관찰 |
| --- | --- | --- | --- |
| E09 | Token budget을 50%로 제한하여 동일 task 실행 | Resource | 품질 저하 시작 지점 |
| E10 | Token budget을 25%로 제한 | Resource | 완료 불가능 임계치 |
| E11 | VM CPU를 1코어로 제한하고 복합 task 실행 | Resource | Compute saturation 발생 조건 |
| E12 | VM RAM을 512MB로 제한 | Resource | OOM 발생 패턴, agent 충돌 양상 |
| E13 | 네트워크 지연을 인위적으로 추가 (API latency 시뮬레이션) | Resource | Timeout 처리, 재시도 행동 |
| E14 | 동시에 2개 agent를 같은 VM에서 실행 | Resource | 충돌, 리소스 경쟁 패턴 관찰 |

#### 축 4: Operator intervention의 효과 (Ch.9 주력)

| # | 시나리오 | 조작 변수 | 예상 관찰 |
| --- | --- | --- | --- |
| E15 | 동일 실패 상황에서: 개입 없음 vs. 힌트 제공 vs. 직접 수정 | Intervention | 복구 성공률, 소요 시간 비교 |
| E16 | 반복 실패에 규칙 기반 자동 개입 적용 | Intervention | 자동화 가능한 개입의 범위 |
| E17 | Agent에게 자기 상태 보고를 요청 (self-reporting) | Intervention | Agent 자기 인식의 정확도 |

#### 축 5: AgentOps 기능의 harness 내재화 가능성 (Ch.10, Ch.11)

| # | 시나리오 | 조작 변수 | 예상 관찰 |
| --- | --- | --- | --- |
| E18 | Token 사용량 자동 보고 기능을 harness에 추가 | Harness (내재화) | Self-reporting 정확도, overhead |
| E19 | 실패 감지 + 자동 재시도 로직을 harness에 추가 | Harness (내재화) | Self-recovery 성공률 |
| E20 | E18+E19를 결합하여 "mini self-immune" 구성 | Harness (내재화) | 통합 동작 안정성, Agent-2 전환 가능성 |

#### 반례 전용 실험

| # | 시나리오 | 조작 변수 | 예상 관찰 |
| --- | --- | --- | --- |
| E21 | 모호한 task 정의로 실행 (task design 문제 반례) | Task design | Harness/모델과 무관한 실패 |
| E22 | 완벽한 harness + SOTA 모델이지만 VM 1코어 (compute 반례) | Resource | 모든 것이 좋아도 compute가 부족하면 실패 |

### 실험 로그 템플릿

| 필드 | 설명 |
| --- | --- |
| Experiment ID | E01~E22 |
| Date | 실행 날짜 |
| Task | 구체적 task 설명 |
| 조작 변수 | 5변수 중 무엇을 조작했는가 |
| 통제 변수 | 나머지 변수의 고정 조건 |
| Model | 모델명 + provider |
| Harness config | Harness 구성 상세 |
| Surface | CLI / API / 기타 |
| Compute environment | VM 사양, 티어, CPU/RAM |
| Tool usage | 어떤 tool, 몇 회 |
| Success / failure | 결과 |
| Failure type | 분류 |
| Primary bottleneck | 5변수 중 어떤 것이 1차 병목이었는가 |
| Balloon effect | 풍선 효과 관찰 여부 |
| Token usage | 입출력 token |
| Human intervention | 개입 여부, 종류, 효과 |
| Recovery | 시도된 복구, 성공 여부 |
| Lesson learned | 핵심 교훈 |
| Target chapter | 사용될 챕터 |
| Experimenter | 실험자 (A, B, C 중) |
| Cross-validation | 교차검증 실험자 |

---

## 10. 팀 설계와 교차검증

### 역할

| 역할 | 담당 | 핵심 책임 |
| --- | --- | --- |
| **Lead author / Concept owner** | Kiwon | 논제, 챕터 논리, 최종 voice, Part I + Ch.5/7/10/11 primary writing |
| **Experimenter A** | TBD | E01~E08 primary, E09~E14 cross-validation |
| **Experimenter B** | TBD | E09~E16 primary, E01~E08 cross-validation |
| **Experimenter C** | TBD | E17~E22 primary, E15~E16 cross-validation |

### 교차검증 설계

모든 핵심 실험은 primary experimenter가 실행하고, 다른 experimenter가 교차검증한다.
교차검증은 동일 조건에서 재현 또는 다른 조건에서 비교 실행으로 수행한다.

```
Experimenter A: E01~E08 실행 → Experimenter B가 E03, E05 교차검증
Experimenter B: E09~E16 실행 → Experimenter A가 E11, E14 교차검증
Experimenter C: E17~E22 실행 → Experimenter B가 E19, E20 교차검증
```

### 팀 성장 원칙

이 실험 과정은 팀원들이 AgentOps와 harness engineering에 대해 알아가며 성장하는 과정이다.
실험자들과 디베이트하면서 성장해나가는 것이 이 프로젝트의 부가 가치이다.

---

## 11. 집필 편집 체계

### 3-layer 구조

- **Layer 1 — Drafter**: 단일 drafting agent. 챕터 전환 시 chapter-map 해당 섹션 + glossary + 이전 챕터 요약을 context로 주입. Voice consistency 구조적 보장.
- **Layer 2 — Editor**: voice-check, 용어 일관성 체크리스트(HOR·Failure Budget Reallocation 등 핵심 용어 조작적 정의 포함), learning curve 3단계 준수 여부 검토, PASS/REVISE/REJECT 판정.
- **Layer 3 — Specialist (on-demand)**: Vera(정량 측정/Figure 해석), Felix(실험 설계 검토) — 상시 가동 아님. 특정 섹션 작성 시 consultation call로만 호출.

**저자**: Kiwon — Part I 전체 + Ch.5/7/10/11 담당. 방향 결정, 반례 의식, 최종 판단.

**메타 원칙**: 이 집필 구조 자체가 Ch.10 "점진적 도구화" 원칙의 dogfooding이다. E-meta(집필 과정 token 배분, coordination overhead)는 Ch.11 §9에 기록한다.

### 편집 체크리스트 (섹션 단위)

editorial-learning-curve-guideline.md §7에서 발췌:

```
□ 직관 앵커가 정의/수식보다 먼저 등장하는가?
□ 이 섹션에서 사용하는 모든 용어가 이전 섹션에서 정의되었는가?
□ 신규 개념이 2개 이하인가?
□ 수식이 있다면 각 기호가 직관과 연결되는가?
□ 운영 번역(Stage 3)이 존재하는가?
□ 운영 번역이 5변수 프레임워크와 연결되는가?
□ 표-수식 사이에 산문 연결이 있는가?
□ "왜 이걸 여기서 설명하는가"에 한 문장으로 답할 수 있는가?
□ 다음 섹션으로의 전환 문장이 존재하는가?
```

---

## 12. 태스크 기반 일정

> 주차별이 아니라 **해야 하는 일 중심**으로 서술한다.

### Phase 0: v6 구조 확정과 기반 정비

**해야 하는 일:**
- list-of-contents-v6.md 최종 확정
- writing-plan.md v6 확정 (이 문서)
- 기존 챕터 파일 → v6 번호 체계로 rename
- chapter-map.md v6로 업데이트
- CLAUDE.md 챕터 구조 섹션 업데이트

**산출물:** v6 구조 동결, 파일 체계 정비 완료

---

### Phase 1: Part I 집필 — 논문 기반 기초 (Ch.1~4)

**해야 하는 일:**
- Ch.2 (compression lens) 한국어 적응 — 영어 원고가 있으므로 가장 먼저 착수
- Ch.1 (Attention) 신규 집필 — Attention Is All You Need + Lost in the Middle
- Ch.3 (Alignment) 신규 집필 — InstructGPT/RLAIF/Constitutional AI
- Ch.4 (Agent 행동) 신규 집필 — Toolformer/ReAct/Reflexion/RAG
- Deep research DR-1.1~DR-4.2 실행
- 각 챕터 learning curve 3단계 준수 검증

**집필 순서:**
1. Ch.2 (영어 원고 존재 → 가장 빠르게 완성 가능, Part I 패턴의 기준점)
2. Ch.1 (Ch.2의 정보이론 기반이 Ch.1의 attention 설명과 상호 참조)
3. Ch.3 (Ch.1-2의 모델 구조 위에 학습/정렬 계보)
4. Ch.4 (Ch.1-3의 기반 위에 agent 행동 능력)

**산출물:** Ch.1~4 초고, Part I 적층 순서 검증 완료

---

### Phase 2: Part II 정비 — 기존 챕터 재배치 + 개선 (Ch.5~7)

**해야 하는 일:**
- 구 Ch.1 → Ch.5: voice rule 위반 수정 + 5변수 프레임워크 통합
- 구 Ch.2 → Ch.6: §2 측정 지표 도입 순서 재설계, §8 재작성, `[X]` 보완, ARCC 합성 지표 → 개별 관찰 지표 전환
- 구 Ch.3 → Ch.7: line 71 손상 복구, §1/§5 직관 앵커 추가
- Part I → Part II 적층 연결 검증 (한 문장 재도입 확인)
- 문헌 배치: Lost in the Middle(Ch.5), RAG(Ch.7)

**산출물:** Ch.5~7 개선 초고, Part I-II 적층 검증 완료

---

### Phase 3: Part III 실험 — 의도적 실패 (Ch.8~9)

**해야 하는 일:**
- 구 Ch.4 → Ch.8: §7-§8 마커 채움, 수치 `[X]` 보완, Part I 연결 문장 추가
- E01~E22 실험 실행 (팀 교차검증 포함)
- 반례 실험 E21, E22 실행
- 구 Ch.5 → Ch.9: scaffold에서 초고로 끌어올리기 (Ch.8 실험 완료 후)

**산출물:** Ch.8~9 초고, E01~E22 전체 로그, 패턴 분류표

---

### Phase 4: Part IV 진화 — 도구화와 내재화 (Ch.10~11)

**해야 하는 일:**
- 구 Ch.6 → Ch.10: §1-§5 보완
- 구 Ch.7 → Ch.11: §4 직관 앵커 추가, §3-§9 보완, Part I 회수 연결
- Operational Compiler 설계 노트 작성
- Self-immune system 초기 설계 정리

**산출물:** Ch.10~11 초고, Operational Compiler 설계 노트

---

### Phase 5: 통합과 Beta

**해야 하는 일:**
- 11챕터 간 용어 통일
- 5변수 프레임워크의 일관된 적용 확인
- Part I → Part II~IV 적층 원칙 최종 검증
- Learning curve 3단계 전 챕터 준수 최종 검증
- 반례가 적절히 포함되어 있는지 확인
- Preface 재작성
- Appendices 정비 (용어 사전, 실험 로그 템플릿, Figure 목록, 참조 프로젝트, 참고문헌)
- Beta 원고 패키지 준비

**산출물:** Beta manuscript (11챕터 + Preface + Appendices)

---

## 13. Deep Research 프롬프트 종합

### Part I — 논문 기반 기초

| ID | 챕터 | 프롬프트 |
| --- | --- | --- |
| DR-1.1 | Ch.1 | "Attention Is All You Need(2017) 이후 attention 메커니즘의 변형과 발전을 조사하라. 특히 agent runtime에서 context window 처리와 관련된 발전(Flash Attention, Ring Attention, sliding window 등)에 집중하라." |
| DR-1.2 | Ch.1 | "Lost in the Middle(2024) 이후 long context 처리의 진전을 조사하라. 특히 1M+ token window를 주장하는 모델들에서 실제 정보 활용도가 어떤지에 대한 실증 연구." |
| DR-2.1 | Ch.2 | "Language Modeling Is Compression(ICLR 2024) 이후의 후속 연구와 비평을 조사하라. 특히 bits-per-byte가 실무 모델 비교에 적용된 사례." |
| DR-3.1 | Ch.3 | "InstructGPT/RLHF 이후 alignment 방법론의 계보를 조사하라. DPO, KTO, RLAIF, Constitutional AI의 관계와 차이. 특히 runtime 행동에 미치는 영향 차이." |
| DR-3.2 | Ch.3 | "Constitutional AI의 self-critique 메커니즘과 runtime self-monitoring의 구분에 대한 기존 논의를 조사하라." |
| DR-4.1 | Ch.4 | "Toolformer 이후 tool use 학습의 발전을 조사하라. Function calling, tool schema 설계, tool use 벤치마크(ToolBench, API-Bank 등)." |
| DR-4.2 | Ch.4 | "ReAct와 Reflexion 이후 agent reasoning 방법론의 발전을 조사하라. LATS, Tree of Thoughts, chain-of-thought variations. 특히 multi-step task에서의 성능 비교." |

### Part II — 프레임워크

| ID | 챕터 | 프롬프트 |
| --- | --- | --- |
| DR-5.1 | Ch.5 | "OpenClaw를 벤치마크하거나 대안으로 등장한 open-source personal AI agent 프로젝트들을 2025-2026년 GitHub에서 전수 조사하라." |
| DR-5.2 | Ch.5 | "CLI 이외에 agent-first product surface로 시도되고 있는 형태들을 조사하라. A2UI, Canvas, voice-first, GUI automation 등." |
| DR-5.3 | Ch.5 | "Chip Huyen의 AI Engineering(2025)이 출간 이후 AI engineering 커뮤니티에 미친 영향과 후속 논의를 조사하라." |
| DR-6.1 | Ch.6 | "LLM을 agent로 사용할 때 모델별 행동 차이를 벤치마크한 기존 연구를 조사하라. SWE-bench, WebArena, ToolBench 등." |
| DR-6.2 | Ch.6 | "OpenRouter의 모델 routing 메커니즘, 지원 모델 목록, pricing, agent workflow에서의 사용 사례를 조사하라." |
| DR-6.3 | Ch.6 | "Model distillation과 quantization이 LLM의 tool call 안정성에 미치는 영향에 대한 기존 연구를 조사하라." |
| DR-7.1 | Ch.7 | "Agent 시스템에서 guardrails, scaffolding, harness, orchestration layer라는 용어가 각각 어떻게 사용되고 있는지 2025-2026년 자료에서 조사하라." |
| DR-7.2 | Ch.7 | "HKUDS CLI-Anything 프로젝트의 HARNESS.md를 분석하라." |
| DR-7.3 | Ch.7 | "AgentOps 관련 기존 도구와 프레임워크를 조사하라: LangSmith, Weights & Biases Weave, AgentOps.ai, Helicone, Braintrust 등." |
| DR-7.4 | Ch.7 | "AI agent runtime 실패를 분류하는 기존 taxonomy가 있는지 조사하라." |

### Part III — 실험

| ID | 챕터 | 프롬프트 |
| --- | --- | --- |
| DR-8.1 | Ch.8 | "Chaos engineering 원리를 AI agent 시스템에 적용한 사례나 연구를 조사하라." |
| DR-8.2 | Ch.8 | "Google Cloud 무료 티어의 구체적 제약 사항과 해당 환경에서 agent 운영 실패 패턴을 조사하라." |
| DR-8.3 | Ch.8 | "Agent 시스템에서 token budget을 관리하고 최적화하는 전략에 대한 기존 연구를 조사하라." |
| DR-8.4 | Ch.8 | "LLM 기반 agent runtime의 CPU/RAM 요구사항을 벤치마크한 자료를 조사하라." |
| DR-9.1 | Ch.9 | "Agent 시스템의 실패 패턴을 분석하는 방법론을 조사하라." |
| DR-9.2 | Ch.9 | "Compute cost optimization for agent deployments — agent 배포의 비용 최적화 사례." |
| DR-9.3 | Ch.9 | "VM 환경에서 LLM agent의 리소스 관리 방법론을 조사하라." |

### Part IV — 진화

| ID | 챕터 | 프롬프트 |
| --- | --- | --- |
| DR-10.1 | Ch.10 | "Developer CLI tool design patterns — 성공적인 CLI 도구의 설계 패턴을 조사하라." |
| DR-10.2 | Ch.10 | "Agent에 능력을 점진적으로 주입하는 기존 접근을 조사하라." |
| DR-11.1 | Ch.11 | "Self-healing and self-recovering AI agent architectures — 기존 self-healing agent 연구를 조사하라." |
| DR-11.2 | Ch.11 | "Continuous learning in deployed agent systems — 배포된 agent의 지속 학습 사례를 조사하라." |

---

## 14. 외부 문헌 인용 원칙과 배치

### 인용 원칙 (CLAUDE.md에서)

외부 연구는 권위 장식이 아니라 비교 좌표다.
인용할 때는 세 가지를 밝힌다: 이 책의 실험과 어디서 겹치는가, 어디서 다른가, 이 책은 그 연구와 달리 무엇을 보려 하는가.

### Part I Backbone 논문 (챕터별 1~3편)

| 논문 | 배치 | 역할 |
| --- | --- | --- |
| Vaswani et al., *Attention Is All You Need* (2017) | Ch.1 backbone | Transformer attention 메커니즘의 원전 |
| Liu et al., *Lost in the Middle* (2024) | Ch.1 backbone | Long context 활용도의 실증 |
| Delétang et al., *Language Modeling Is Compression* (2024) | Ch.2 backbone | LM-압축 등가성의 증명 |
| Shannon, *A Mathematical Theory of Communication* (1948) | Ch.2 backbone | 정보이론 원전 |
| Ouyang et al., *InstructGPT* (2022) | Ch.3 backbone | RLHF 방법론의 원전 |
| Lee et al., *RLAIF* (2023) | Ch.3 backbone | AI feedback scaling |
| Bai et al., *Constitutional AI* (2022) | Ch.3 backbone | Self-critique 계보의 원전 |
| Schick et al., *Toolformer* (2023) | Ch.4 backbone | Tool use 자기 학습 |
| Yao et al., *ReAct* (2023) | Ch.4 backbone | Reasoning-acting 통합 |
| Shinn et al., *Reflexion* (2023) | Ch.4 backbone | Verbal reinforcement learning |
| Lewis et al., *RAG* (2020) | Ch.4 companion | 외부 기억 장치의 원전 |

### Part II~IV 비교 좌표 논문

| 논문 | 배치 후보 | 역할 |
| --- | --- | --- |
| OpenAI, *Harness Engineering* (2026) | Ch.5, Ch.7 | 이 책이 검증하는 1차 프레임워크 |
| Chip Huyen, *AI Engineering* (2025) | Ch.5 | 포지셔닝 좌표 |
| Lost in the Middle | Ch.5 재도입 | Context pressure 관찰의 메커니즘 연결 |

---

## 15. 참조 문서 체계

| 문서 | 역할 |
| --- | --- |
| `CLAUDE.md` | Voice rules + AI 협업 지침. 모든 초고 작성 시 필수 참조 |
| `writing-plan.md` | 이 파일. 마스터 집필 계획서. 단일 진실의 원천 |
| `list-of-contents-v6.md` | 섹션 단위 상세 설계. 각 섹션의 직관 앵커, 정밀 정의, 운영 번역 내용 |
| `editorial-learning-curve-guideline.md` | Learning curve 편집 가이드라인. 3단계 구조, 개념 밀도, 적층 원칙 |
| `compression lens 챕터 -learning curve reference.docx` | Ch.2 한국어 적응의 영어 원본. Part I 패턴의 참조 구현 |
| `chapter-map.md` | 챕터별 상세 아웃라인 (v6 업데이트 필요) |
| `token-policy.md` | 토큰 사용 정책 |
| `gemini-review-report.md` | 외부 리뷰에 대한 비판적 수용 메모 |

---

## 16. 토큰 절약 정책 (Token Policy)

- 세션 시작 시 `/begin [chNN] [section_N]`으로 현재 위치 확인
- 섹션 하나 완료 후 피드백 없이 다음 섹션으로 넘어가지 않는다
- 대화가 10턴 이상이면 `/compact "voice rules, chapter outline, current section progress 유지"` 실행
- 챕터 전환 시 `/clear` — 다음 챕터는 새 세션에서 시작
- `/cost` 로 토큰 현황 수시 확인
- 상세 정책: `token-policy.md` 참고

---

## 17. 집필 워크플로

/outline → /draft (섹션 단위) → 피드백 → /revise → /integrate → /voice-check
한 번에 전체 챕터를 쓰지 않는다. 섹션 단위로 쓰고 피드백을 받는다.
