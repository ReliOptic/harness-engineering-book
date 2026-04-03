# DR-6.1 — CLI Design Patterns

> 원본: `CLI 도구 설계 패턴 조사.md` (동일 디렉토리)
> 보조: `CLI 도구 설계 패턴 조사.docx`, `Agent-first CLI 툴 최신 정보.docx`

## 요약

현대 CLI 도구의 3대 설계 기둥:
1. **자가 서술적(Self-Describing) 인터페이스** — --help가 기계 파싱 가능한 API 명세로 작동
2. **조합 가능성(Composability)** — stdout/stderr 엄격 분리, 역압(backpressure) 처리, 의미론적 종료 코드
3. **구조화된 출력(Structured Output)** — JSON 출력 모드, 인간/기계 이중 인터페이스

## Ch.10 연결

- Operational Compiler의 CLI 구현 시 이 세 기둥이 설계 제약으로 작용
- Agent가 CLI 도구를 자율적으로 사용할 때, 자가 서술성이 tool description의 역할을 대행
- §5 산업적 수렴: CLAUDE.md, AGENTS.md 등 공개 harness 패턴이 CLI-first 구조를 공유하는 이유

## 핵심 참조

- CLIG.dev (Command Line Interface Guidelines)
- kubectl, gh CLI, Cobra 프레임워크
- Raftt CLI의 비동기 상태 캐싱 패턴
