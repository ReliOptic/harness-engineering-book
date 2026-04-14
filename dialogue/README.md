# Dialogue Prompts — 챕터별 대화형 통찰 수집

## 사용법

각 폴더의 `prompt.md`를 새 Claude 세션에 붙여넣고 대화를 시작합니다.
대화가 끝나면 Claude가 생성한 결과 파일을 해당 폴더에 저장합니다.

## 폴더 구조

| 폴더 | 챕터 | 핵심 논문/자료 | 대화 목적 |
|------|------|---------------|----------|
| `ch01-attention/` | Ch.1 Attention과 Context | Vaswani 2017, Liu 2024 | QKV→agent 실패 모드 연결 |
| `ch03-alignment/` | Ch.3 정렬에서 자율로 | InstructGPT, RLAIF, Constitutional AI | 학습-런타임 경계 논증 |
| `ch04-tools-reasoning-memory/` | Ch.4 도구, 추론, 기억 | Toolformer, ReAct, Reflexion, RAG | 실패 지도 + Reflexion-Self-immune 경계 |
| `ch05-five-variables/` | Ch.5 왜 다섯 변수인가 | 현장 관찰 + Part I 종합 | 5변수 필연성 논증 |
| `ch07-harness-fbr/` | Ch.7 Harness/AgentOps | Chaos Eng, SRE Error Budget | FBR 정량 프레임 설계 |
| `ch11-self-immune/` | Ch.11 Self-Immune System | Constitutional AI, Reflexion, Cross-entropy | 재귀적 한계 + 전환 조건 정식화 |

## 제외된 챕터

| 챕터 | 이유 |
|------|------|
| Ch.2 | compression lens 영어 원고가 이미 대화를 통해 생성됨 (`reference-chapters/`) |
| Ch.6 | Ch.2 + Ch.4 대화 결과 + 실험 데이터로 구성. 독립 대화 불필요. |
| Ch.8~9 | 실험 실행 결과에 의존. 대화가 아닌 데이터가 원료. |
| Ch.10 | Ch.8~9 결과 분석에 의존. 독립 대화 불필요. |

## 대화 순서 권장

1. **Ch.1** (attention) → 2. **Ch.3** (alignment) → 3. **Ch.4** (tools) → 4. **Ch.5** (5변수) → 5. **Ch.7** (FBR) → 6. **Ch.11** (self-immune)

Ch.5는 Ch.1~4 대화를 모두 마친 후에 시작해야 Part I 회수가 가능합니다.
Ch.11은 Ch.7 대화 이후에 시작해야 FBR/harness overhead 개념이 전제로 작동합니다.

## 결과 파일 네이밍 규칙

대화 결과를 저장할 때:
- `insight-summary.md` — 이해도 프로필 + 핵심 통찰
- `writing-material.md` — 운영 번역 원료 / 초안 재료
- `connections.md` — 다른 챕터 연결 씨앗
