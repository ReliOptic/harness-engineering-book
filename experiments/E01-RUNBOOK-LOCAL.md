# E01 실험 로컬 실행 가이드 (Runbook)

**생성일**: 2026-04-04
**대상**: 로컬 머신에서 E01 실험 (off-harness baseline) 실행
**소요 시간**: ~2-4시간 (모든 difficulty × 모델 tier 포함)

---

## 1. 사전 준비 (환경 설정)

### 1.1 Python 환경 확인
```bash
python3 --version  # Python 3.10 이상 필수
pip --version
```

### 1.2 의존성 설치
프로젝트 루트 디렉토리에서:
```bash
cd /sessions/peaceful-zen-maxwell/mnt/projects/mine/harness-engineering-book/experiments

# framework 패키지 설치
pip install -r framework/requirements.txt

# 설치된 패키지 확인
pip list | grep -E "openai|numpy|scipy|scikit-learn"
```

**필수 패키지**:
- openai >= 1.50.0 (OpenRouter 통합)
- numpy >= 1.26.0
- scipy >= 1.12.0
- scikit-learn >= 1.4.0

### 1.3 API 키 설정
OpenRouter API를 사용하므로 환경변수 필수:
```bash
# ~/.bashrc 또는 ~/.zshrc에 추가 (또는 터미널에서 export)
export OPENROUTER_API_KEY="sk-or-..."
# https://openrouter.ai/keys에서 발급받기

# 확인
echo $OPENROUTER_API_KEY
```

### 1.4 프로젝트 구조 확인
```bash
ls -la framework/
# 출력:
# - config.py (모델, 설정)
# - tasks.py (T1/T2 fixture)
# - ground_truth.py (L1 검증기)
# - agent.py (LLM 에이전트)
# - arcc.py (모델 능력 지표 메트릭)
# - metrics.py (성능 계산)
# - smoke_test.py (테스트 스위트)
```

---

## 2. 수정 필요 사항

### 2.1 버그 힌트 주석 제거 (중요)

**문제**: tasks.py의 T1 코드 fixture에 버그 위치를 드러내는 인라인 주석이 포함됨.
예: `# Bug 1 (line 15): off-by-one, last order skipped`

이 주석들은 **모델에 전송되기 전에 반드시 제거**해야 합니다.

#### 2.1.1 자동 제거 스크립트 생성
`framework/strip_hints.py` 파일 생성:
```python
#!/usr/bin/env python3
"""
T1 fixture에서 버그 힌트 주석 제거.
(models/agents에 보내기 전 호출)
"""
import re
from framework.tasks import _T1_EASY_CODE, _T1_MODERATE_CODE, _T1_FRONTIER_CODE

def strip_bug_hints(code: str) -> str:
    """주석에서 'Bug N (line X): ...' 패턴 제거"""
    # 패턴: # Bug N (line X): ... 또는 # BUG: ...
    code = re.sub(r'\s*#\s*Bug\s+\d+\s*\(line\s+\d+\)[^"\n]*', '', code)
    code = re.sub(r'\s*#\s*BUG:\s*[^\n]*', '', code)
    return code

if __name__ == "__main__":
    print("=" * 60)
    print("T1 EASY (hint 제거 후)")
    print("=" * 60)
    clean = strip_bug_hints(_T1_EASY_CODE)
    print(clean[:500])  # 첫 500자만 표시

    # 라인 57 확인 (원래 bug hint가 있던 위치)
    lines = clean.split('\n')
    print(f"\nLine 57: {lines[56]}")  # 0-indexed
```

실행:
```bash
python framework/strip_hints.py
```

#### 2.1.2 agent.py에서 자동 strip 적용 (권장)
agent.py의 `call_model()` 함수에서 prompt 전송 전 hint 제거:
```python
# framework/agent.py 내 call_model() 함수 수정
def call_model(prompt: str, model: str, ...) -> str:
    # 버그 힌트 제거 (T1 only)
    import re
    prompt = re.sub(r'\s*#\s*Bug\s+\d+\s*\(line\s+\d+\)[^"\n]*', '', prompt)
    prompt = re.sub(r'\s*#\s*BUG:\s*[^\n]*', '', prompt)

    # 나머지 로직...
```

### 2.2 T3 Fixture 구현 (현재 미완성)

**현재 상태**: `make_t3_task()` 함수만 있고, `make_t3_repo()` 함수가 없음.
**E01 대상**: T1 + T2만 실행하므로 **즉시 필요 없음**, SKIP 가능.

T3가 필요하면 나중에:
```python
# framework/tasks.py에 추가 (약 50줄)
def make_t3_repo(difficulty: Difficulty, temp_dir: str = None) -> tuple[str, list[str]]:
    """
    T3용 fixture repo를 임시 디렉토리에 생성.
    반환: (repo_path, created_files)
    """
    import tempfile
    import os

    if temp_dir is None:
        temp_dir = tempfile.mkdtemp(prefix=f"t3_repo_{difficulty}_")

    os.makedirs(temp_dir, exist_ok=True)
    files = []

    # difficulty별로 file_count & magic_number_count 결정
    config = {
        "EASY": {"files": 10, "magic_nums": 20, "lines_per_file": 50},
        "MODERATE": {"files": 25, "magic_nums": 50, "lines_per_file": 100},
        "FRONTIER": {"files": 50, "magic_nums": 100, "lines_per_file": 150},
    }
    cfg = config[difficulty]

    # 각 파일에 magic numbers 분산 배치
    magic_per_file = cfg["magic_nums"] // cfg["files"]
    remainder = cfg["magic_nums"] % cfg["files"]

    for f_idx in range(cfg["files"]):
        filename = f"module_{f_idx:03d}.py"
        filepath = os.path.join(temp_dir, filename)

        # magic numbers 개수 (균형)
        magic_count = magic_per_file + (1 if f_idx < remainder else 0)

        # 간단한 Python 코드 생성 (magic numbers 포함)
        code_lines = [f"# File: {filename}\n"]
        for i in range(cfg["lines_per_file"]):
            if i < magic_count:
                code_lines.append(f"value_{i} = {100 + i * 10}  # magic number\n")
            else:
                code_lines.append(f"# placeholder line {i}\n")

        with open(filepath, 'w') as f:
            f.writelines(code_lines)
        files.append(filepath)

    return temp_dir, files
```

---

## 3. 실행 순서

### 3.1 E01 실험 요약
- **변수**: 모델 tier (SOTA vs SMALL)
- **Task**: T1 (Code Review) + T2 (Multi-Step Reasoning)
- **Difficulty**: EASY → MODERATE → FRONTIER
- **Harness**: OFF (baseline)
- **토큰 예산**: T1: 32K, T2: 64K
- **모델 선택**:
  - SOTA: `google/gemini-3.1-flash-lite-preview`
  - SMALL: `google/gemini-2.5-flash-lite`

### 3.2 실행 명령어

#### 3.2.1 사전 검사
```bash
python framework/smoke_test.py
# 출력 예상:
# [T1] EASY fixture validation: PASS
# [T2] EASY fixture validation: PASS
# [Ground Truth] BugEntry structure: PASS
# [모델 능력 지표] Metrics calculation: PASS
```

#### 3.2.2 T1 EASY (대약 5-10분)
```bash
# SOTA 모델
python -m experiments.run_e01 \
  --task T1 \
  --difficulty EASY \
  --model google/gemini-3.1-flash-lite-preview \
  --harness off \
  --output results/e01_t1_easy_sota.json

# SMALL 모델
python -m experiments.run_e01 \
  --task T1 \
  --difficulty EASY \
  --model google/gemini-2.5-flash-lite \
  --harness off \
  --output results/e01_t1_easy_small.json
```

#### 3.2.3 T1 MODERATE (대약 10-15분)
```bash
python -m experiments.run_e01 \
  --task T1 \
  --difficulty MODERATE \
  --model google/gemini-3.1-flash-lite-preview \
  --harness off \
  --output results/e01_t1_moderate_sota.json

python -m experiments.run_e01 \
  --task T1 \
  --difficulty MODERATE \
  --model google/gemini-2.5-flash-lite \
  --harness off \
  --output results/e01_t1_moderate_small.json
```

#### 3.2.4 T1 FRONTIER (대약 15-20분)
```bash
python -m experiments.run_e01 \
  --task T1 \
  --difficulty FRONTIER \
  --model google/gemini-3.1-flash-lite-preview \
  --harness off \
  --output results/e01_t1_frontier_sota.json

python -m experiments.run_e01 \
  --task T1 \
  --difficulty FRONTIER \
  --model google/gemini-2.5-flash-lite \
  --harness off \
  --output results/e01_t1_frontier_small.json
```

#### 3.2.5 T2 EASY (대약 5-10분)
```bash
python -m experiments.run_e01 \
  --task T2 \
  --difficulty EASY \
  --model google/gemini-3.1-flash-lite-preview \
  --harness off \
  --output results/e01_t2_easy_sota.json

python -m experiments.run_e01 \
  --task T2 \
  --difficulty EASY \
  --model google/gemini-2.5-flash-lite \
  --harness off \
  --output results/e01_t2_easy_small.json
```

#### 3.2.6 T2 MODERATE (대약 15-20분)
```bash
python -m experiments.run_e01 \
  --task T2 \
  --difficulty MODERATE \
  --model google/gemini-3.1-flash-lite-preview \
  --harness off \
  --output results/e01_t2_moderate_sota.json

python -m experiments.run_e01 \
  --task T2 \
  --difficulty MODERATE \
  --model google/gemini-2.5-flash-lite \
  --harness off \
  --output results/e01_t2_moderate_small.json
```

#### 3.2.7 T2 FRONTIER (대약 20-30분)
```bash
python -m experiments.run_e01 \
  --task T2 \
  --difficulty FRONTIER \
  --model google/gemini-3.1-flash-lite-preview \
  --harness off \
  --output results/e01_t2_frontier_sota.json

python -m experiments.run_e01 \
  --task T2 \
  --difficulty FRONTIER \
  --model google/gemini-2.5-flash-lite \
  --harness off \
  --output results/e01_t2_frontier_small.json
```

### 3.3 배치 실행 (권장)
모든 조합을 자동으로 실행하는 스크립트:

`run_e01_batch.py` 생성:
```python
#!/usr/bin/env python3
import subprocess
import json
from pathlib import Path

TASKS = ["T1", "T2"]
DIFFICULTIES = ["EASY", "MODERATE", "FRONTIER"]
MODELS = {
    "SOTA": "google/gemini-3.1-flash-lite-preview",
    "SMALL": "google/gemini-2.5-flash-lite",
}

def run_experiment(task, difficulty, model_name, model_id):
    """한 번의 실험 실행"""
    output_file = f"results/e01_{task.lower()}_{difficulty.lower()}_{model_name.lower()}.json"

    cmd = [
        "python", "-m", "experiments.run_e01",
        "--task", task,
        "--difficulty", difficulty,
        "--model", model_id,
        "--harness", "off",
        "--output", output_file,
    ]

    print(f"[{task} {difficulty:8} {model_name:5}] 실행 중...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✓ {output_file} 저장됨")
        return True
    else:
        print(f"✗ 실패: {result.stderr}")
        return False

if __name__ == "__main__":
    Path("results").mkdir(exist_ok=True)

    total = 0
    passed = 0

    for task in TASKS:
        for difficulty in DIFFICULTIES:
            for model_name, model_id in MODELS.items():
                total += 1
                if run_experiment(task, difficulty, model_name, model_id):
                    passed += 1
                print()

    print(f"\n결과: {passed}/{total} 성공")
```

실행:
```bash
python run_e01_batch.py
```

---

## 4. 검증 방법

### 4.1 Ground Truth 비교 (T1 Code Review)

T1 EASY의 3개 버그가 올바르게 감지되는지 확인:

```bash
python -c "
from framework.ground_truth import validate_t1
from framework.tasks import make_t1_task
import json

# 실험 결과 로드
with open('results/e01_t1_easy_sota.json') as f:
    result = json.load(f)

agent_output = result['model_response']  # JSON 응답
task = make_t1_task('EASY')
ground_truth = task.ground_truth_bugs

# 검증 실행
validation = validate_t1(agent_output, ground_truth)
print(f'Verdict: {validation.verdict}')
print(f'Score (F1): {validation.score:.3f}')
print(f'Details: {validation.details}')
"
```

**예상 결과**:
- Verdict: "pass" (모든 3개 버그 감지) 또는 "partial" (2/3 감지)
- Score: 0.70 이상 (F1 threshold)

### 4.2 T2 Constraints 검증

T2 fixture의 constraint graph 검증:
```bash
python -c "
from framework.tasks import make_t2_task
from framework.ground_truth import validate_t2

task = make_t2_task('MODERATE')
print(f'Constraints: {len(task.constraints)}')
print(f'Expected valid orderings: {task.expected_valid_orderings}')

# 모델 응답 로드 및 검증
import json
with open('results/e01_t2_moderate_sota.json') as f:
    result = json.load(f)

validation = validate_t2(result['model_response'], task.constraints)
print(f'Validation: {validation.verdict} ({validation.score:.3f})')
"
```

### 4.3 모델 능력 지표 메트릭 계산

### 4.3.1 개별 실험의 모델 능력 지표 점수
```bash
python -c "
from framework.arcc import compute_arcc_score
import json

# 모든 T1 결과 로드
results = {}
for difficulty in ['EASY', 'MODERATE', 'FRONTIER']:
    with open(f'results/e01_t1_{difficulty.lower()}_sota.json') as f:
        results[difficulty] = json.load(f)

# 모델 능력 지표 계산 (4개 메트릭: TCA, IFR, MSRD, CUE)
for diff, result in results.items():
    arcc = compute_arcc_score(
        task_complexity_alignment=result.get('tca', 0.5),
        inference_followability_rate=result.get('ifr', 0.5),
        mean_step_reasoning_depth=result.get('msrd', 0.5),
        coherence_utility_engagement=result.get('cue', 0.5),
    )
    print(f'{diff}: 모델 능력 지표={arcc:.3f}')
"
```

### 4.3.2 모델 간 비교 (SOTA vs SMALL)
```bash
python framework/arcc.py \
  --sota_results results/e01_t1_easy_sota.json \
  --small_results results/e01_t1_easy_small.json \
  --output arcc_comparison.json
```

**출력 형식**:
```json
{
  "sota_arcc": 0.75,
  "small_arcc": 0.62,
  "arcc_gap": 0.13,
  "r_squared": 0.68,
  "metric_breakdown": {
    "tca": {"sota": 0.80, "small": 0.65},
    "ifr": {"sota": 0.78, "small": 0.60},
    "msrd": {"sota": 0.72, "small": 0.58},
    "cue": {"sota": 0.70, "small": 0.63}
  }
}
```

**검증**:
- R² >= 0.65 이어야 모델 능력 지표 유효
- SOTA vs SMALL gap >= 0.10 권장 (capability cliff 증명)

---

## 5. 결과 기록 형식

### 5.1 표준 결과 JSON 형식
각 실험별 결과 파일 구조:

```json
{
  "metadata": {
    "timestamp": "2026-04-04T14:30:00Z",
    "experiment_id": "E01_T1_EASY_SOTA",
    "task": "T1",
    "difficulty": "EASY",
    "model": "google/gemini-3.1-flash-lite-preview",
    "harness_enabled": false,
    "token_budget": 32000
  },
  "task_spec": {
    "code": "def process_orders(...)",
    "ground_truth_bugs": [
      {
        "line_number": 15,
        "bug_type": "off-by-one",
        "severity": "high"
      },
      {
        "line_number": 20,
        "bug_type": "null_check",
        "severity": "high"
      },
      {
        "line_number": 31,
        "bug_type": "type_mismatch",
        "severity": "medium"
      }
    ]
  },
  "execution": {
    "start_time": "2026-04-04T14:30:00Z",
    "end_time": "2026-04-04T14:30:45Z",
    "duration_seconds": 45,
    "input_tokens": 2150,
    "output_tokens": 420,
    "total_tokens": 2570,
    "cost_usd": 0.001
  },
  "model_response": "[{\"line_number\": 15, \"bug_type\": \"off-by-one\", \"severity\": \"high\", \"fix_suggestion\": \"Change range(len(orders)-1) to range(len(orders))\"}]",
  "validation": {
    "layer": "L1_test_suite",
    "verdict": "pass",
    "score": 0.78,
    "details": {
      "true_positives": 3,
      "false_positives": 0,
      "false_negatives": 0,
      "precision": 1.0,
      "recall": 1.0,
      "f1_score": 1.0
    }
  },
  "arcc_metrics": {
    "task_complexity_alignment": 0.85,
    "inference_followability_rate": 0.82,
    "mean_step_reasoning_depth": 0.78,
    "coherence_utility_engagement": 0.75,
    "composite_arcc_score": 0.80,
    "r_squared_validation": 0.72
  },
  "errors": null
}
```

### 5.2 수집 체크리스트

각 실험 실행 후 확인:
- [ ] 결과 JSON 파일 생성됨
- [ ] `validation.verdict` == "pass" 또는 "partial"
- [ ] `execution.total_tokens` <= token_budget
- [ ] `arcc_metrics.composite_arcc_score` >= 0.50
- [ ] 모델이 정상 응답 (syntax error 없음)

### 5.3 통합 분석 (모든 실험 완료 후)

`analyze_e01_results.py` 생성:
```python
#!/usr/bin/env python3
import json
import glob
from pathlib import Path
import statistics

def analyze_all_results():
    """E01 모든 결과 종합 분석"""

    results_by_tier = {"SOTA": {}, "SMALL": {}}

    # 모든 결과 파일 수집
    for json_file in glob.glob("results/e01_*.json"):
        with open(json_file) as f:
            result = json.load(f)

        tier = "SOTA" if "sota" in json_file else "SMALL"
        task = result["metadata"]["task"]
        diff = result["metadata"]["difficulty"]

        key = f"{task}_{diff}"
        if key not in results_by_tier[tier]:
            results_by_tier[tier][key] = []
        results_by_tier[tier][key].append(result)

    # 각 difficulty 별 성능 비교
    print("=" * 70)
    print("E01 최종 결과: SOTA vs SMALL")
    print("=" * 70)

    for tier in ["SOTA", "SMALL"]:
        print(f"\n{tier} 모델:")
        for key in sorted(results_by_tier[tier].keys()):
            arcc_scores = [
                r["arcc_metrics"]["composite_arcc_score"]
                for r in results_by_tier[tier][key]
            ]
            mean_arcc = statistics.mean(arcc_scores)
            print(f"  {key:20} 모델 능력 지표={mean_arcc:.3f}")

    # Capability gap 계산
    print("\nCapability Gap (SOTA - SMALL):")
    for key in results_by_tier["SOTA"].keys():
        sota_arcc = statistics.mean([
            r["arcc_metrics"]["composite_arcc_score"]
            for r in results_by_tier["SOTA"][key]
        ])
        small_arcc = statistics.mean([
            r["arcc_metrics"]["composite_arcc_score"]
            for r in results_by_tier["SMALL"].get(key, [])
        ]) if key in results_by_tier["SMALL"] else 0

        gap = sota_arcc - small_arcc
        print(f"  {key:20} gap={gap:+.3f}")

if __name__ == "__main__":
    analyze_all_results()
```

실행:
```bash
python analyze_e01_results.py
```

---

## 6. 자주 발생하는 문제 및 해결책

### 문제 1: "OPENROUTER_API_KEY not found"
**해결책**:
```bash
export OPENROUTER_API_KEY="sk-or-..."
# 그리고 다시 실행
```

### 문제 2: "JSON decode error" (모델 응답 파싱 실패)
**원인**: 모델이 pure JSON이 아닌 markdown 형식 반환
**해결책**: agent.py에 JSON 추출 로직 추가
```python
def extract_json(response: str) -> str:
    import json, re
    # ```json ... ``` 블록 추출
    match = re.search(r'```(?:json)?\s*(.*?)\s*```', response, re.DOTALL)
    if match:
        return match.group(1)
    # 일반 JSON 추출
    try:
        json.loads(response)
        return response
    except:
        raise ValueError(f"Cannot extract JSON from: {response[:100]}")
```

### 문제 3: "Token budget exceeded" (T2 FRONTIER)
**해결책**:
- 실제 모델은 1M context를 가지므로 budget 초과는 무시 가능
- 또는 `--token_budget 128000` 옵션으로 증액

### 문제 4: 버그 힌트가 여전히 모델에 전송됨
**확인**:
```bash
# agent.py 호출 로그 검사
grep -n "# Bug\|# BUG:" results/*.json
```
**해결책**: Section 2.1의 strip 로직 재확인

---

## 7. 타이밍 및 비용 예상

### 실행 시간
- T1 EASY (2 models) → 10-20분
- T1 MODERATE (2 models) → 20-30분
- T1 FRONTIER (2 models) → 30-40분
- T2 EASY (2 models) → 10-20분
- T2 MODERATE (2 models) → 20-40분
- T2 FRONTIER (2 models) → 40-60분

**총 소요 시간**: ~2.5-4시간

### API 비용 (OpenRouter)
Gemini 3.1 Flash Lite Preview:
- 입력: $0.25/M, 출력: $1.50/M

예상:
- T1 EASY (SOTA): ~$0.005
- T1 FRONTIER (SOTA): ~$0.015
- T2 MODERATE (SOTA): ~$0.010
- **전체 12개 실험 예상**: ~$0.12-0.20

---

## 8. 체크리스트: 최종 검증

실험 완료 후:
- [ ] 12개 결과 파일 생성됨 (T1×3diff×2models + T2×3diff×2models)
- [ ] 모든 파일에 `validation.verdict` 존재
- [ ] 모든 파일에 `arcc_metrics` 존재
- [ ] SOTA 모델의 모델 능력 지표 >= 0.60 평균
- [ ] SMALL 모델의 모델 능력 지표 >= 0.45 평균
- [ ] R² >= 0.65 (모델 능력 지표 메트릭 유효성)
- [ ] Capability gap >= 0.05 (의미 있는 차이)

---

## 9. 참고 자료

- **설계 문서**: `../design-specification.md` (§1 Task Spec, §3 Ground Truth)
- **프레임워크**: `framework/config.py` (모델 설정)
- **실행기**: `run_e01_batch.py` (배치 실행)
- **OpenRouter 문서**: https://openrouter.ai/docs
