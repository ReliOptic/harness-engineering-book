# 실험 실행 Runbook

> 2026-03-19 업데이트 (최초 2026-03-18). 실험 시작 전 이 문서를 완독한다.

## 환경 설정 체크리스트

- [ ] OPENROUTER_API_KEY 환경변수 설정 (`export OPENROUTER_API_KEY=sk-or-...`)
- [ ] Python 3.11+ 확인
- [ ] `cd experiments && python3 -m pytest framework/smoke_test.py -v` → 4/4 PASS 확인
- [ ] GCP e2-micro VM 접속 확인 (또는 로컬 환경 사양 기록)
- [ ] `experiments/design-specification.md` 읽기 완료

## 모델 라인업 (2026-03-19 개정, OpenRouter 기준)

> 2026-03-19: SOTA 축을 Gemini 3.1 Flash Lite Preview로, MID 축을 GPT-5.4 Nano로 재편.
> 이전 세대(Gemini 2.5-pro, gpt-5.2)는 pricing table에 reference로 유지.

| Tier | 모델 ID | 입력 $/MTok | 출력 $/MTok | ctx | 비고 |
|------|---------|------------|------------|-----|------|
| SOTA | `google/gemini-3.1-flash-lite-preview` | $0.25 | $1.50 | 1M | Gemini 2.5 Flash 수준 접근 |
| MID | `openai/gpt-5.4-nano` | $0.20 | $1.25 | 400K | GPT-5.4 family, sub-agent 최적화 |
| SMALL | `google/gemini-2.5-flash-lite` | $0.10 | $0.40 | 1M | Capability Cliff 기준점 |
| SMALL (OAI) | `openai/gpt-5-mini` | $0.25 | $2.00 | 400K | 이전 세대 기준점 |
| ref | `openai/gpt-5.2` | $1.75 | $14.00 | 400K | 비교 reference 전용 |

**Judge 모델**: `google/gemini-3.1-flash-lite-preview` (비용 효율 + tool-call 신뢰성)

OpenRouter base URL: `https://openrouter.ai/api/v1` (OpenAI SDK 호환)

## 실험 실행 순서 (권고)

### Experimenter A (E01~E07)
1. E01 먼저 실행 — ARCC 측정 baseline 확보
2. E02 실행 — Quantization Tax Curve
3. E03 실행 — mid-run switching
4. E04 실행 — harness on/off baseline (가장 중요한 실험)
5. E05, E06 실행
6. E07 실행 — **[2026-03-27 우선순위 재검토]**: E07 가설은 "CLI vs API surface가 에이전트 성능에 영향을 준다"인데, Claude Code Computer Use 출시로 surface 변수가 플랫폼 레이어로 흡수되는 방향이 확인됨. 이 맥락에서 E07은 surface 변수가 완전히 추상화되기 이전 시점의 경계 관찰로 의미를 재정의한다 — "surface가 흡수될 때 남는 병목이 harness임을 보여주는 대조 실험"으로. 가설 서술은 design-specification.md §E07에서 이 관점을 반영해 업데이트 요망.
7. B의 E03, E05, E06 교차검증 요청

### Experimenter B (E08~E12)
1. A의 E04 완료 후 시작 (harness baseline 필요)
2. E08 — token budget 단계적 감소
3. E09 — 40-step goal drift
4. E10 — model capability floor (E01 데이터 필요)
5. E11 — TeamClaws 재현
6. E12 — self-immune overhead
7. A의 E08, E09, E11 교차검증 완료 확인

### Experimenter C (E13~E20)
1. B의 E12 완료 후 E18 계획 수립
2. E13, E14, E15 순서로 진행
3. E16, E17, E18 순서로 진행
4. E19, E20 반례 실험
5. A의 E19 교차검증 요청

## 실험 로그 작성

각 실험 완료 후:
1. 해당 `ENN-*.md` 파일의 결과 칸 채우기
2. `/log-experiment ENN` 커맨드로 로그 확정
3. 교차검증 대상은 xval 파일 생성: `cross-validation/xval-ENN-by-[A/B/C].md`

## 데이터 수집 원칙

- token usage: OpenRouter API response의 usage 필드에서 직접 기록
- 실행 시간: wall clock time (time.time() 기준)
- 비용: `framework/config.py`의 `compute_cost(model, input_tokens, output_tokens)` 사용
  - 예시: gemini-2.5-flash 32K in / 4K out → $0.0096 + $0.010 = $0.020
- ARCC 측정: `framework/arcc.py`의 `compute_arcc()` 함수 사용

## 이상 발생 시

- 실험 중 예상 밖 패턴 발생 → `[exploratory]` 레이블로 로그에 즉시 기록
- pre-registration 기준 변경 필요 → `design-specification.md §7 Deviation Protocol` 따름
- 실험 중단 필요 → 현재 상태 저장 후 중단 사유 로그 기록
