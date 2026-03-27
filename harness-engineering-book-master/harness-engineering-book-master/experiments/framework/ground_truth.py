"""
Ground Truth Infrastructure — Layer 1 (Test Suite)

design-specification.md §3 참조.
T1~T4 task에 대한 자동 검증기.

Layer 2 (LLM Judge)와 Layer 3 (Human)은 별도 파이프라인.
이 모듈은 Layer 1만 담당.
"""
from __future__ import annotations

import ast
import json
import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class ValidationResult:
    verdict: str          # "pass" | "fail" | "partial" | "uncertain"
    score: float          # [0, 1] — TCR 연속 변수 버전
    details: dict
    layer: str = "L1_test_suite"


# ── T1 — Code Review Validator ────────────────────────────────────────────────

@dataclass
class BugEntry:
    line_number: int
    bug_type: str
    severity: str  # "low" | "medium" | "high" | "critical"


def validate_t1(
    agent_output: str,
    ground_truth_bugs: list[BugEntry],
    f1_threshold: float = 0.70,
    line_tolerance: int = 2,
) -> ValidationResult:
    """
    T1 Code Review: F1 score vs ground truth bug list.

    agent_output: agent가 JSON으로 반환한 버그 목록
    ground_truth_bugs: seeded bug의 정답 목록
    line_tolerance: 줄 번호 ±tolerance 이내면 같은 버그로 인정
    """
    try:
        raw = _extract_json(agent_output)
        reported = raw if isinstance(raw, list) else raw.get("bugs", raw.get("results", []))
    except (json.JSONDecodeError, AttributeError, ValueError):
        return ValidationResult(
            verdict="fail",
            score=0.0,
            details={"error": "agent output is not valid JSON"},
        )

    tp = 0
    matched_gt = set()
    for rep in reported:
        rep_line = rep.get("line_number", rep.get("line", -1))
        rep_type = rep.get("bug_type", rep.get("type", ""))
        for i, gt in enumerate(ground_truth_bugs):
            if i in matched_gt:
                continue
            if abs(rep_line - gt.line_number) <= line_tolerance:
                tp += 1
                matched_gt.add(i)
                break

    precision = tp / len(reported) if reported else 0.0
    recall = tp / len(ground_truth_bugs) if ground_truth_bugs else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    verdict = "pass" if f1 >= f1_threshold else "partial" if f1 > 0 else "fail"
    return ValidationResult(
        verdict=verdict,
        score=f1,
        details={
            "f1": f1,
            "precision": precision,
            "recall": recall,
            "tp": tp,
            "fp": len(reported) - tp,
            "fn": len(ground_truth_bugs) - tp,
            "n_reported": len(reported),
            "n_ground_truth": len(ground_truth_bugs),
        },
    )


# ── T2 — Multi-Step Reasoning Validator ──────────────────────────────────────

def validate_t2(
    agent_plan: str,
    constraints: list[dict],
    resources: Optional[dict] = None,
) -> ValidationResult:
    """
    T2 Constraint Checker: agent의 계획이 모든 constraint를 만족하는가.

    agent_plan: JSON list [{"step": N, "action": "...", "rationale": "..."}]
    constraints: [{"type": "dependency", "before": "A", "after": "B"},
                  {"type": "resource", "item": "GPU", "limit": 2}, ...]
    """
    try:
        raw = _extract_json(agent_plan)
        plan = raw if isinstance(raw, list) else raw.get("plan", raw.get("steps", []))
    except (json.JSONDecodeError, AttributeError, ValueError):
        return ValidationResult(
            verdict="fail",
            score=0.0,
            details={"error": "plan is not valid JSON"},
        )

    violations = []
    valid_steps = 0
    action_order = [step.get("action", "") for step in plan]

    for c in constraints:
        if c["type"] == "dependency":
            before, after = c["before"], c["after"]
            if before in action_order and after in action_order:
                if action_order.index(before) > action_order.index(after):
                    violations.append(f"dependency violated: {before} must precede {after}")
                else:
                    valid_steps += 1
        elif c["type"] == "resource":
            # 동시 실행 resource 사용량 체크 (단순화: sequential 가정)
            item, limit = c["item"], c["limit"]
            if resources and resources.get(item, 0) <= limit:
                valid_steps += 1
            elif not resources:
                valid_steps += 1  # resource info 없으면 pass

    if not constraints:
        score = 1.0 if plan else 0.0
    else:
        score = valid_steps / len(constraints) if constraints else 0.0

    verdict = "pass" if not violations and score >= 1.0 else \
              "partial" if score > 0 else "fail"

    return ValidationResult(
        verdict=verdict,
        score=score,
        details={
            "violations": violations,
            "valid_constraints": valid_steps,
            "total_constraints": len(constraints),
            "plan_steps": len(plan),
        },
    )


# ── T3 — Long-Horizon Execution Validator ────────────────────────────────────

def validate_t3(
    repo_path: str,
    test_command: str = "pytest",
    baseline_pass_rate: float = 1.0,
    pass_rate_threshold: float = 0.95,
) -> ValidationResult:
    """
    T3: test suite 실행 후 pass rate 측정.

    repo_path: agent가 수정한 코드가 있는 경로
    test_command: pytest 또는 유사 커맨드
    baseline_pass_rate: 수정 전 pass rate (regression 감지용)
    """
    try:
        result = subprocess.run(
            test_command.split(),
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=120,
        )
        output = result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return ValidationResult(
            verdict="fail",
            score=0.0,
            details={"error": "test timeout (120s)"},
        )
    except FileNotFoundError:
        return ValidationResult(
            verdict="uncertain",
            score=0.0,
            details={"error": f"test command not found: {test_command}"},
        )

    # pytest 출력 파싱
    passed, failed, total = _parse_pytest_output(output)
    pass_rate = passed / total if total > 0 else 0.0

    regression = pass_rate < baseline_pass_rate - 0.05
    verdict = (
        "pass"    if pass_rate >= pass_rate_threshold and not regression else
        "partial" if pass_rate >= 0.70 else
        "fail"
    )

    return ValidationResult(
        verdict=verdict,
        score=pass_rate,
        details={
            "passed": passed,
            "failed": failed,
            "total": total,
            "pass_rate": pass_rate,
            "baseline_pass_rate": baseline_pass_rate,
            "regression_detected": regression,
            "raw_output_tail": output[-500:],
        },
    )


def validate_t3_goal_fidelity(
    initial_goal: str,
    checkpoint_responses: list[tuple[int, str]],
    embedding_fn,
) -> list[tuple[int, float]]:
    """
    T3 checkpoint에서의 Goal Fidelity Score.
    embedding_fn: (text: str) -> np.ndarray

    반환: [(step, gfs), ...] — metrics.py의 compute_goal_fidelity_series와 연동.
    """
    import numpy as np

    initial_emb = embedding_fn(initial_goal)
    result = []
    for step, response in checkpoint_responses:
        emb = embedding_fn(response)
        norm_i = np.linalg.norm(initial_emb)
        norm_r = np.linalg.norm(emb)
        if norm_i > 0 and norm_r > 0:
            gfs = float(np.dot(initial_emb, emb) / (norm_i * norm_r))
        else:
            gfs = 0.0
        result.append((step, gfs))
    return result


# ── T4 — Context-Sensitive Synthesis Validator ───────────────────────────────

def validate_t4(
    agent_output: str,
    key_facts: list[str],
    misleading_claims: list[str],
    recall_threshold: float = 0.80,
    precision_threshold: float = 0.90,
) -> ValidationResult:
    """
    T4: recall (핵심 사실 포함률) + precision (오답 유도 내용 회피율).

    key_facts: 정답 내 반드시 포함되어야 할 핵심 사실 목록
    misleading_claims: 출력에 포함되면 안 되는 오답 유도 내용
    """
    output_lower = agent_output.lower()

    # Recall
    found_facts = []
    for fact in key_facts:
        key_words = [w for w in fact.lower().split() if len(w) > 3]
        if key_words and sum(1 for w in key_words if w in output_lower) / len(key_words) >= 0.75:
            found_facts.append(fact)

    recall = len(found_facts) / len(key_facts) if key_facts else 1.0

    # Precision (misleading content 회피)
    found_misleading = [c for c in misleading_claims if c.lower()[:30] in output_lower]
    precision = 1.0 - (len(found_misleading) / len(misleading_claims)) if misleading_claims else 1.0

    score = (recall + precision) / 2
    verdict = (
        "pass"    if recall >= recall_threshold and precision >= precision_threshold else
        "partial" if score >= 0.60 else
        "fail"
    )

    return ValidationResult(
        verdict=verdict,
        score=score,
        details={
            "recall": recall,
            "precision": precision,
            "found_facts": len(found_facts),
            "total_facts": len(key_facts),
            "misleading_included": len(found_misleading),
            "misleading_items": found_misleading,
        },
    )


# ── Harness Detection Ground Truth (Figure 9 ROC용) ──────────────────────────

def build_detection_ground_truth(
    run_steps: list[dict],
    validator_fn,
    delayed_evaluation: bool = False,
) -> list[dict]:
    """
    각 step에 대한 ground truth failure/non-failure 레이블 생성.
    Figure 9 ROC 계산의 입력.

    run_steps: [{"step": N, "output": str, "context": dict}]
    validator_fn: (output, context) -> ValidationResult
    delayed_evaluation: True이면 task 완료 후 재평가 (silent failure 포착)

    반환: [{"step": N, "is_failure": bool, "method": "L1"}]
    """
    labels = []
    for step_data in run_steps:
        result = validator_fn(step_data["output"], step_data.get("context", {}))
        is_failure = result.verdict in ("fail", "partial")
        labels.append({
            "step": step_data["step"],
            "is_failure": is_failure,
            "verdict": result.verdict,
            "score": result.score,
            "method": "L1_delayed" if delayed_evaluation else "L1",
        })
    return labels


# ── 내부 유틸리티 ──────────────────────────────────────────────────────────────

def _extract_json(text: str) -> dict | list:
    """agent output에서 JSON 블록 추출."""
    # 코드 블록 우선
    match = re.search(r"```(?:json)?\s*([\s\S]+?)```", text)
    if match:
        return json.loads(match.group(1).strip())
    # 중괄호/대괄호 직접 탐색
    for pattern in [r"(\[[\s\S]+\])", r"(\{[\s\S]+\})"]:
        match = re.search(pattern, text)
        if match:
            return json.loads(match.group(1))
    raise ValueError("no JSON found in output")


def _parse_pytest_output(output: str) -> tuple[int, int, int]:
    """pytest 출력에서 passed/failed/total 추출."""
    # 예: "5 passed, 2 failed in 1.23s"
    match = re.search(r"(\d+) passed", output)
    passed = int(match.group(1)) if match else 0

    match = re.search(r"(\d+) failed", output)
    failed = int(match.group(1)) if match else 0

    match = re.search(r"(\d+) error", output)
    errors = int(match.group(1)) if match else 0

    total = passed + failed + errors
    return passed, failed + errors, total
