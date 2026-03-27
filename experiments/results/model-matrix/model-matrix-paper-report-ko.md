# 모델 매트릭스 파일럿 결과보고서 (논문형 초안)

## 제목
**Agent-Targeted LLM의 벤더/모델 크기별 성능 차이: OpenRouter 기반 T1/T2 파일럿 비교 실험**

## 초록
본 보고서는 2026년 3월 공개된 agent-targeted 모델군을 대상으로, 벤더 및 모델 크기 차이가 실제 agent 작업 성능에 유의미한 차이를 만드는지 탐색한 파일럿 실험 결과를 제시한다. 비교 대상은 `nvidia/nemotron-3-super-120b-a12b`, `openai/gpt-5.4-nano`, `qwen/qwen3.5-9b`, `google/gemini-3.1-flash-lite-preview`이며, 과제는 T1(Code Review)와 T2(Multi-step Planning)로 구성했다. T1은 모델당 2회, T2는 모델당 1회 반복 실행하였다. 주 지표는 strict success rate, 연속형 TCR(TCR_cont), IFR, TCA이며, 모델 간 성공률 차이는 two-proportion z-test와 Holm 보정으로 평가했다. 결과적으로 T1에서 `gpt-5.4-nano`가 strict success 2/2를 기록한 반면 일부 모델은 partial/failure 중심 분포를 보였다. 다만 다중비교 보정 후 모든 쌍에서 유의수준 0.05를 충족하지 못했다(Holm 보정 p ≥ 0.273). T2 파일럿에서는 4개 모델 중 3개가 성공, 1개가 실패를 보였으나 표본 수가 1회로 해석력이 제한적이다. 본 파일럿은 “차이 신호 존재 가능성”을 확인했으나, “통계적 확정”을 위해선 모델당 반복 수 확장이 필수적이다.

## 1. 연구 배경 및 목적
Agent 운영 관점에서 벤더-사이즈 조합은 단순 벤치마크 점수보다 중요한 의사결정 변수다. 실제 현장에서는 다음 두 질문이 핵심이다.

1. 동일 agent task에서 벤더/모델 크기 차이가 **재현 가능한 성공률 차이**를 만드는가  
2. 그 차이가 다중비교를 고려해도 **유의수준에서 유지**되는가

본 실험은 위 질문에 대해 “원고 집필에 즉시 투입 가능한 정량 근거”를 확보하기 위한 Phase-1 파일럿이다.

## 2. 연구 질문 및 가설
### RQ1
T1(Code Review)에서 모델별 strict success rate는 동일한가?

### RQ2
T2(Multi-step Planning)에서 모델별 strict success rate는 동일한가?

### RQ3
관찰된 차이가 Holm 보정 후에도 유의한가?

### 사전 가설(파일럿 수준)
- H1: 모델별 strict success rate 차이가 존재한다.
- H2: 일부 모델 쌍은 보정 전 p<0.05를 보이나, 파일럿 표본에서는 Holm 보정 후 비유의일 가능성이 높다.

## 3. 방법
### 3.1 실험 환경
- 실행 시점(KST): 2026-03-21 새벽 (결과 JSON 생성 시각 UTC 2026-03-20 16:03, 16:12)
- API 경로: OpenRouter (`https://openrouter.ai/api/v1`)
- Harness 설정: `none` (모델 자체 성능 분리 관측 목적)
- 과제 난이도: `MODERATE`

### 3.2 비교 모델
- `nvidia/nemotron-3-super-120b-a12b`
- `openai/gpt-5.4-nano`
- `qwen/qwen3.5-9b`
- `google/gemini-3.1-flash-lite-preview`

참고: `openai/gpt-5.4-pro`는 단일 호출 검증에서는 응답 가능했으나, 런 단위 실행에서 고지연/비용 경로로 반복적으로 time-box를 초과하여 본 파일럿 매트릭스에서는 제외하였다.

### 3.3 태스크 및 반복 수
- T1 (`T1_code_review`): 모델당 2회 반복
- T2 (`T2_multi_step`): 모델당 1회 반복

### 3.4 실행 파라미터
- 파일럿 스크립트: `experiments/run_model_matrix.py`
- T1 파일럿: `--max-steps 4 --token-budget 2000`
- T2 파일럿: `--max-steps 4 --token-budget 2000`
- OpenRouter 호환 보정:
  - `openai/gpt-5.4-*` 계열은 `max_output_tokens` 경로 사용
  - 요청 타임아웃 명시(클라이언트/요청 레벨)

### 3.5 측정 지표
- Strict success rate = successes / n_runs
- Continuous TCR = (successes + 0.5 * partials) / n_runs
- IFR, TCA: 프레임워크 계산값 사용
- 실패 유형: run summary taxonomy 사용

### 3.6 통계 분석
- 모델 쌍별 성공률 비교: two-proportion z-test
- 다중비교 보정: Holm step-down
- 보조 보고: Wilson 95% 신뢰구간(success rate 기준)

## 4. 결과
## 4.1 T1 (Code Review, n=2/model)

| 모델 | Success | Partial | Fail | Success rate | TCR(cont) | IFR | TCA |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| nvidia/nemotron-3-super-120b-a12b | 0 | 2 | 0 | 0.00 | 0.50 | 0.00 | 0.00 |
| openai/gpt-5.4-nano | 2 | 0 | 0 | 1.00 | 1.00 | 0.60 | 0.00 |
| qwen/qwen3.5-9b | 0 | 0 | 2 | 0.00 | 0.00 | 0.00 | 0.00 |
| google/gemini-3.1-flash-lite-preview | 0 | 1 | 1 | 0.00 | 0.25 | 0.20 | 0.00 |

Wilson 95% CI (Success rate):
- nemotron: 0.00 [0.000, 0.658]
- gpt-5.4-nano: 1.00 [0.342, 1.000]
- qwen3.5-9b: 0.00 [0.000, 0.658]
- gemini-3.1-flash-lite-preview: 0.00 [0.000, 0.658]

해석:
- strict success 기준으로 `gpt-5.4-nano`만 2/2 성공.
- nemotron은 전부 partial(실패는 아님), qwen은 전부 failure.
- gemini는 partial/failure 혼합.

## 4.2 T2 (Multi-step Planning, n=1/model)

| 모델 | Success | Partial | Fail | Success rate | TCR(cont) | IFR | TCA |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| nvidia/nemotron-3-super-120b-a12b | 1 | 0 | 0 | 1.00 | 1.00 | 0.00 | 0.00 |
| openai/gpt-5.4-nano | 1 | 0 | 0 | 1.00 | 1.00 | 0.20 | 1.00 |
| qwen/qwen3.5-9b | 0 | 0 | 1 | 0.00 | 0.00 | 0.00 | 0.00 |
| google/gemini-3.1-flash-lite-preview | 1 | 0 | 0 | 1.00 | 1.00 | 0.20 | 1.00 |

Wilson 95% CI (Success rate, n=1):
- 성공 1/1 모델: [0.207, 1.000]
- 실패 0/1 모델: [0.000, 0.793]

해석:
- 표본이 1회이므로 모델 간 비교 결론은 내릴 수 없다.
- 다만 qwen의 실패 패턴이 T1/T2 모두에서 반복 관측되었다는 점은 후속 검증 가치가 있다.

## 4.3 쌍대 비교 검정 결과
T1에서 일부 쌍은 보정 전 p=0.0455를 보였으나, Holm 보정 후 `p_holm=0.273`으로 유의수준 0.05를 충족하지 못했다.

T2는 모든 쌍에서 비유의(Holm 보정 p ≥ 0.9438).

결론:
- **본 파일럿은 “차이의 방향”을 시사하지만, “통계적 확정” 단계는 아니다.**

## 4.4 실패 유형 관찰
- T1:
  - qwen: `silent_logical_drift` 2회
  - gemini: `tool_call_failure` 1회 포함
  - nemotron, nano: `none` 중심(단, nemotron은 partial 다수)
- T2:
  - qwen: `silent_logical_drift` 1회
  - 나머지: `none`

## 5. 논의
### 5.1 실무 의미
- 같은 “agent-targeted” 라벨이라도 strict success 분포가 크게 다를 수 있다.
- 특히 T1에서 partial과 fail의 구분은 운영 정책(재시도/검수 필요도)에 직접 연결된다.
- 따라서 엔지니어링 의사결정에서 “벤더명”보다 **task-specific 성공 분포(success/partial/fail)**를 우선 지표로 삼는 것이 타당하다.

### 5.2 왜 보정 후 비유의인가
- 반복 수가 매우 작아(특히 T2 n=1) 분산이 크다.
- 다중비교(6쌍) 보정으로 임계가 강화되며 파일럿 효과가 쉽게 소거된다.
- 즉, 비유의는 “차이가 없다”가 아니라 “표본이 확정 결론을 지지할 만큼 충분치 않다”로 해석해야 한다.

## 6. 타당도 위협(Threats to Validity)
### 내부 타당도
- Harness=none 설정은 모델 순수 비교에 유리하지만, 실제 운영 시나리오(Harness on)와 분리된다.
- `max_steps=4`, `token_budget=2000`의 타이트한 파일럿 설정이 모델별 잠재 성능을 충분히 발현하지 못할 수 있다.

### 외적 타당도
- T1/T2만으로는 long-horizon(T3) 및 synthesis(T4) 일반화를 주장하기 어렵다.
- OpenRouter provider 라우팅/지연 특성의 영향을 완전히 제거하지 못했다.

### 통계적 결론 타당도
- 작은 n으로 인해 검정력(power)이 부족하다.
- 현재 p-value는 신호 탐지용이며 확정적 우열 판정 근거로 사용하면 과해석 위험이 있다.

## 7. 재현성(Replication Package)
### 산출물
- T1 결과 JSON: `experiments/results/model-matrix/model-matrix-results.json`
- T1 결과 MD: `experiments/results/model-matrix/model-matrix-results.md`
- T2 결과 JSON: `experiments/results/model-matrix-t2/model-matrix-results.json`
- T2 결과 MD: `experiments/results/model-matrix-t2/model-matrix-results.md`
- 실행기: `experiments/run_model_matrix.py`

### 재현 명령
```bash
cd experiments
OPENROUTER_API_KEY="$(cat /root/harness-engineering-book/secret_keys/openrouter_API.txt)" \
python3 run_model_matrix.py \
  --runs 2 \
  --tasks T1_code_review \
  --max-steps 4 \
  --token-budget 2000 \
  --models 'nvidia/nemotron-3-super-120b-a12b,openai/gpt-5.4-nano,qwen/qwen3.5-9b,google/gemini-3.1-flash-lite-preview'
```

```bash
cd experiments
OPENROUTER_API_KEY="$(cat /root/harness-engineering-book/secret_keys/openrouter_API.txt)" \
python3 run_model_matrix.py \
  --runs 1 \
  --tasks T2_multi_step \
  --max-steps 4 \
  --token-budget 2000 \
  --models 'nvidia/nemotron-3-super-120b-a12b,openai/gpt-5.4-nano,qwen/qwen3.5-9b,google/gemini-3.1-flash-lite-preview' \
  --out-dir results/model-matrix-t2
```

## 8. 결론
본 파일럿은 벤더/사이즈 비교 프레임이 실제로 작동하며, 모델별 성능 분포 차이가 관찰된다는 점을 보여준다. 그러나 현재 표본에서는 Holm 보정 후 통계적 유의성을 확보하지 못했다. 다음 단계는 모델당 반복 수를 늘려 검정력을 확보하고(T1/T2 각 n≥6), 동일 프레임으로 T3/T4를 확장해 “agent-targeted 모델의 조건부 우위”를 task별로 확정하는 것이다.

## 9. 후속 실험 권고 (집필 반영용)
1. T1/T2 모두 모델당 `n>=6`으로 확대 (동일 명령, runs만 증가)
2. `openai/gpt-5.4-pro`는 분리 타임박스 트랙으로 별도 수집
3. Harness=full 조건의 E04/E08과 교차 결합해 “모델 우위 vs harness 우위” 분해
4. Ch.2/Ch.5 본문에는 현재 파일럿을 “탐색적(exploratory)”으로 명시하고, 확정 문장은 scale-up 결과 이후에만 채택

