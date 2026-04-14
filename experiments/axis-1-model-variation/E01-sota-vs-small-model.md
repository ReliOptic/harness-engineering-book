# E01 — 동일 task를 SOTA vs. 소형 모델로 실행

**Experiment ID**: E01
**Date**: 2026-03-20~2026-03-21 (pilot)
**Experimenter**: A
**Cross-validator**: B (E03, E05)
**Target chapter**: Ch.2 (§3 성능 급락), Ch.4 (1막)
**Status**: [ ] 계획 / [x] 진행중 / [ ] 완료 / [ ] 교차검증 완료

---

## Task

T1 (Code Review) 및 T2 (Multi-Step Reasoning) task를 동일 조건에서 SOTA 모델과 소형 모델로 각각 실행한다.
Task 정의: `experiments/design-specification.md §1` 기준.

---

## 5변수 설정

| 변수 | 설정 |
|------|------|
| **조작 변수** | 모델 (SOTA vs. 소형) |
| **모델** | 운영 라인업 기준: `google/gemini-3.1-flash-lite-preview`(SOTA), `google/gemini-2.5-flash-lite`(소형), `openai/gpt-5.4-nano`(MID), `qwen/qwen3.5-9b`(소형 proxy) |
| **Harness config** | harness=OFF (baseline, harness-off 조건) |
| **Surface** | CLI |
| **Compute environment** | GCP e2-micro (free tier) |
| **Token budget** | T1: 32K / T2: 64K |

**통제 변수**: surface=CLI, harness=OFF, token budget 동일, task 동일

---

## 관찰 대상

- tool call 패턴 (TCA: Tool Call Accuracy)
- task 완료율 (TCR per task type)
- 실패 지점의 성격 (tool call 실패 vs. reasoning 실패 vs. format 오류)
- 모델 능력 지표 sub-component 측정 (TCA, IFR, MSRD_n, CUE)

**핵심 가설 (pre-registered)**: 모델 능력 지표가 특정 threshold 이하에서 TCR이 선형이 아닌 급락한다 (성능 급락). Cliff position은 task type(T1/T2)에 따라 다르다.

---

## 실행 기록

### Tool usage
- 사용한 tool: OpenRouter chat completions (tool-call 없음)
- tool call 횟수: 0 (pilot 시나리오 기준)
- tool call 성공률: N/A

### 실행 로그 요약
- 2026-03-20 pilot(T1/T2): `results/model-matrix*/model-matrix-results.md`
- 2026-03-21 rerun(T2, sandbox): DNS 제한으로 `api_error` 발생 (token=0)
- 2026-03-21 rerun(T1+T2, network 승격): `results/e01-pilot-r2/model-matrix-results.md` (유효 결과)
- 2026-03-21 SOTA vs 소형 2모델 비교: `results/e01-sota-small-r2/model-matrix-results.md`

---

## 결과

**Success / Failure**: [ ] 성공 / [ ] 실패 / [x] 부분 성공

**Failure type**: `task_failure`(주로 qwen/qwen3.5-9b), `partial_quality_degradation`(일부 모델 T1)

**TCR (T1)**:
- nvidia/nemotron-3-super-120b-a12b: 0.750 (1 success, 1 partial)
- openai/gpt-5.4-nano: 0.500 (2 partial)
- google/gemini-3.1-flash-lite-preview: 0.250 (1 partial, 1 fail)
- google/gemini-2.5-flash-lite: 0.750 (1 success, 1 partial)
- qwen/qwen3.5-9b: 0.000 (2/2 fail)

**TCR (T2)**:
- nvidia/nemotron-3-super-120b-a12b: 1.000 (2/2 success)
- openai/gpt-5.4-nano: 1.000 (2/2 success)
- google/gemini-3.1-flash-lite-preview: 1.000 (2/2 success)
- google/gemini-2.5-flash-lite: 1.000 (2/2 success)
- qwen/qwen3.5-9b: 0.000 (2/2 fail)

**모델 능력 지표 (SOTA)**: 미계산 (MSRD_n/CUE/T3 데이터 미수집)
**모델 능력 지표 (소형)**: 미계산 (MSRD_n/CUE/T3 데이터 미수집)

---

## 분석

### Primary bottleneck
**1차 병목**: 모델 성능의 task-conditional 변동 + T3 fixture 부재
**근거**:
- qwen proxy는 T1/T2 모두 0.000으로 하한을 형성
- gemini-3.1(SOTA) vs gemini-2.5(소형) 비교에서 T1은 소형이 높고(TCR 0.75 vs 0.25), T2는 동률(1.0)
- `framework/tasks.py`의 T3는 `make_t3_repo()` 전제인데 실구현 fixture가 없음

### Balloon effect
[ ] 관찰됨 / [x] 관찰 안 됨 (pilot 표본이 작아 확정 불가)

---

## 측정값

| 지표 | SOTA | 소형 |
|------|------|------|
| Token usage (input) | gemini-3.1 기준 T1/T2 평균 약 7.1K/0.6K | gemini-2.5 기준 T1/T2 평균 약 4.3K/0.7K |
| Token usage (output) | 별도 분리 미기록 (현재 러너 한계) | 별도 분리 미기록 |
| 실행 시간 | run 완료(steps 1~4) | run 완료(steps 1~4) |
| 비용 (API) | 정상 호출 비용 발생 (세부 비용 미집계) | 정상 호출 비용 발생 |
| TCA | T1: 0.000 / T2: 1.000 (gemini-3.1) | T1: 0.000 / T2: 0.000 (gemini-2.5) |
| IFR | T1: 0.125 / T2: 0.600 (gemini-3.1) | T1: 0.400 / T2: 0.000 (gemini-2.5) |
| MSRD_n | 미측정 | 미측정 |
| CUE | 미측정 | 미측정 |

---

## Human Intervention

**개입 여부**: [x] 없음 / [ ] 있음

---

## Recovery

**복구 시도**: [ ] 없음 / [x] 있음 (sandbox 실패 후 network 승격 재실행)

---

## Lesson Learned

- E01 완료 조건은 단순 TCR 집계가 아니라 모델 능력 지표 구성요소(TCA/IFR/MSRD_n/CUE) 동시 계측이다.
- 현 상태는 T1/T2 pilot만 존재하고 T3 데이터가 없어 성능 급락 위치를 확정할 수 없다.
- sandbox 네트워크 모드에서는 API 오류가 섞일 수 있어, 실행 모드(승격/비승격)를 실험 메타데이터로 기록해야 한다.

---

## Blockers (2026-03-21)

1. T3 long-horizon 측정을 위한 repo fixture 생성 루틴(`make_t3_repo`)이 코드베이스에 없음.
2. pilot은 token budget 2000으로 수행되어 본래 E01 스펙(32K/64K)과 다름.

---

## 교차검증 메모

**교차검증자**: B
**교차검증 날짜**:
**검증 방법**: 동일 조건 재현
**검증 결과**:
**불일치 사항**:

---

## 관련 Figure

- Fig 1 — Agent 성능 급락 (E01 확장): 모델 능력 지표 scatter plot + task-conditional sigmoid fit
- Fig 1b — Quantization Tax Curve (E02 연결)
