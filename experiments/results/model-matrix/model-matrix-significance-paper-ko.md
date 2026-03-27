# 파일럿 실험의 통계적 유의성 판정 보고서 (논문형)

## 제목
**Agent-Targeted 모델 비교 파일럿(T1/T2)에서 통계적으로 유의한 결과가 도출되었는가?**

## 초록
본 보고서는 OpenRouter 기반 모델 매트릭스 파일럿 결과(T1: 모델당 n=2, T2: 모델당 n=1)를 사용해, 관찰된 성능 차이가 통계적으로 유의한지 평가한다. 1차 판정은 기존 산출물의 two-proportion z-test와 Holm 보정 결과를 사용했고, 2차 점검으로 소표본 타당성을 위해 Fisher exact 해석을 병기했다. 결과적으로 T1에서 일부 쌍은 보정 전 p=0.0455를 보였으나, Holm 보정 후 p=0.273으로 유의수준 0.05를 충족하지 못했다. T2는 전 비교에서 비유의였다. 따라서 현재 데이터는 **확증적(confirmatory) 유의성은 확보하지 못했으며**, 다만 모델별 실패 패턴 분화는 **탐색적(exploratory) 신호**로 해석할 수 있다.

## 1. 데이터셋과 분석 범위
### 1.1 데이터 출처
- T1 결과: `experiments/results/model-matrix/model-matrix-results.json`
- T2 결과: `experiments/results/model-matrix-t2/model-matrix-results.json`

### 1.2 비교 모델
- `nvidia/nemotron-3-super-120b-a12b`
- `openai/gpt-5.4-nano`
- `qwen/qwen3.5-9b`
- `google/gemini-3.1-flash-lite-preview`

### 1.3 표본 크기
- T1: 각 모델 2회
- T2: 각 모델 1회

## 2. 분석 방법
1. 쌍대 성공률 차이에 대해 two-proportion z-test 실시
2. 다중비교(모델 4개 → 6쌍)에 Holm 보정 적용
3. 소표본 왜곡 점검을 위해 Fisher exact(two-sided) 해석 병기
4. 보조지표: success rate Wilson 95% CI

## 3. 결과
## 3.1 T1 (Code Review, n=2/model)

strict success rate:
- nemotron: 0/2 (0.00)
- gpt-5.4-nano: 2/2 (1.00)
- qwen3.5-9b: 0/2 (0.00)
- gemini-3.1-flash-lite-preview: 0/2 (0.00)

핵심 쌍대 비교:
- `gpt-5.4-nano` vs `qwen3.5-9b`: z-test p=0.0455 (보정 전)
- `gpt-5.4-nano` vs `nemotron`: z-test p=0.0455 (보정 전)
- `gpt-5.4-nano` vs `gemini-3.1-flash-lite-preview`: z-test p=0.0455 (보정 전)

다중비교 보정(Holm):
- 위 3개 비교 모두 p_holm=0.2730 → **비유의**

소표본 exact 점검:
- 2/2 vs 0/2의 Fisher exact(two-sided) p=0.3333 → **비유의**

해석:
- 방향성 신호(한 모델만 2/2 success)는 존재하나, 소표본 exact 기준에서도 유의성 확보 실패.

## 3.2 T2 (Multi-step Planning, n=1/model)

strict success rate:
- nemotron: 1/1
- gpt-5.4-nano: 1/1
- qwen3.5-9b: 0/1
- gemini-3.1-flash-lite-preview: 1/1

검정 결과:
- z-test 기준도 전 비교 비유의(예: 1/1 vs 0/1은 p=0.1573)
- Holm 보정 후 모두 p_holm=0.9438 이상
- Fisher exact(two-sided) 1/1 vs 0/1은 p=1.0

해석:
- T2는 파일럿 단계에서 통계적 결론을 내릴 근거가 부족하다.

## 4. 유의미성 판정
## 4.1 통계적 유의미성(Confirmatory)
판정: **아니오**  
근거: 모든 핵심 비교가 Holm 보정 후 유의수준 0.05 미달.

## 4.2 실험적/실무적 유의미성(Exploratory)
판정: **예, 제한적으로 존재**  
근거:
- 모델별 성공/partial/failure 분포가 구분되는 방향성 신호 관찰
- qwen에서 T1/T2 모두 failure가 관찰되어 실패 양상 추적 가치가 높음
- gpt-5.4-nano는 파일럿 조건에서 반복 성공 신호를 보임

단, 이는 확증적 우열 결론이 아니라 **후속 검증 우선순위 설정 근거**다.

## 5. 결론
현재 파일럿 데이터만으로는 “통계적으로 유의한 성능 우열”을 주장할 수 없다. 다만 모델별 분화 신호는 존재하며, 이는 실험 설계 확장(n 증가, 과제 축 확장, 시간/비용 제약 분리)으로 검증할 가치가 충분하다. 따라서 본 데이터의 올바른 위치는 **확정 결론이 아닌 탐색적 근거**다.

## 6. 후속 설계 권고
1. T1/T2 모두 모델당 최소 n>=6으로 확대
2. 동일 조건에서 T3/T4 추가로 과제 일반화 점검
3. `gpt-5.4-pro`는 분리 타임박스 트랙으로 수집하여 본 매트릭스와 병렬 비교
4. 본문 서술 규칙: 파일럿 결과는 exploratory로 명시, confirmatory 문장은 scale-up 이후에만 채택

