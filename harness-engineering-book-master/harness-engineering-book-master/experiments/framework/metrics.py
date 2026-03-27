"""
핵심 측정 지표 계산기.
모든 Figure의 Y축과 분석 지표를 여기서 계산한다.

지표 목록:
  RSuccR  — Recovery Success Rate          (Figure 2, 8, 10)
  TTFF    — Time to First Failure          (Figure 2)
  HDL     — Harness Detection Latency      (Figure 4)
  SAA     — Self-Assessment Accuracy       (Figure 4, 7)
  GDR     — Goal Drift Rate               (Figure 5)
  CCS     — Context Contamination Score    (Figure 6)
  HOR     — Harness Overhead Ratio         (Figure 8)
  ECE     — Expected Calibration Error     (Figure 7)
"""
from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from typing import Optional, Sequence

import numpy as np

from .config import RunLog, StepLog


# ── 결과 타입 ─────────────────────────────────────────────────────────────────

@dataclass
class MetricResult:
    value: float
    n: int                        # 측정에 사용된 sample 수
    ci_lower: Optional[float] = None
    ci_upper: Optional[float] = None
    notes: str = ""


# ── RSuccR — Recovery Success Rate ───────────────────────────────────────────

def compute_rsucc_r(runs: list[RunLog]) -> MetricResult:
    """
    RSuccR = (recovery_attempted AND succeeded) / recovery_attempted

    recovery_attempted: run 중 harness가 failure를 감지하고 복구를 시도한 경우
    succeeded: final_verdict == "success" OR "partial" 이후 task 완료

    design-specification.md §5.1 참조
    """
    attempted = [r for r in runs if r.recovered or r.final_verdict == "failure"]
    succeeded = [r for r in attempted if r.recovered and r.final_verdict in ("success", "partial")]

    if not attempted:
        return MetricResult(value=float("nan"), n=0, notes="no recovery attempts observed")

    rate = len(succeeded) / len(attempted)
    # Wilson interval (proportion의 95% CI)
    lo, hi = _wilson_ci(len(succeeded), len(attempted))
    return MetricResult(value=rate, n=len(attempted), ci_lower=lo, ci_upper=hi)


# ── TTFF — Time to First Failure ─────────────────────────────────────────────

def compute_ttff(run: RunLog) -> Optional[int]:
    """
    TTFF = step index at which first failure event occurs.
    failure event = harness_alert이 non-None인 첫 번째 step.
    harness가 없는 조건에서는 ground_truth_verdict == "fail"인 첫 step.

    반환값: step number (1-indexed). 실패 없으면 None.
    """
    for step in run.steps:
        if step.harness_alert is not None:
            return step.step_number
        if step.ground_truth_verdict == "fail":
            return step.step_number
    return None


def compute_ttff_distribution(runs: list[RunLog]) -> dict:
    """
    여러 run의 TTFF 분포 통계.
    Figure 2 Panel A (violin plot) 데이터 소스.
    """
    values = [t for r in runs if (t := compute_ttff(r)) is not None]
    if not values:
        return {"mean": float("nan"), "median": float("nan"), "std": float("nan"),
                "n_failure": 0, "n_total": len(runs)}
    arr = np.array(values)
    return {
        "mean": float(np.mean(arr)),
        "median": float(np.median(arr)),
        "std": float(np.std(arr, ddof=1)),
        "q25": float(np.percentile(arr, 25)),
        "q75": float(np.percentile(arr, 75)),
        "min": int(arr.min()),
        "max": int(arr.max()),
        "n_failure": len(values),
        "n_total": len(runs),
        "failure_rate": len(values) / len(runs),
        "raw": values,           # violin plot raw data
    }


# ── HDL — Harness Detection Latency ──────────────────────────────────────────

def compute_hdl(run: RunLog) -> Optional[int]:
    """
    HDL = step index of first harness_alert − step index of actual failure onset.

    actual failure onset: ground_truth_verdict == "fail"인 첫 step
    harness alert: harness_alert != None인 첫 step

    HDL < 0 → harness가 agent 자신보다 먼저 감지 (sentinel 역할)
    HDL = 0 → 동시 감지
    HDL > 0 → harness가 늦게 감지
    HDL = None → harness가 실패 자체를 감지하지 못함 (false negative)
    """
    gt_fail_step = None
    harness_detect_step = None

    for step in run.steps:
        if gt_fail_step is None and step.ground_truth_verdict == "fail":
            gt_fail_step = step.step_number
        if harness_detect_step is None and step.harness_alert is not None:
            harness_detect_step = step.step_number

    if gt_fail_step is None:
        return None  # 실제 failure 없음
    if harness_detect_step is None:
        return None  # False negative: harness가 놓침

    return harness_detect_step - gt_fail_step


def compute_hdl_lead_time(runs: list[RunLog]) -> MetricResult:
    """
    Figure 4 Panel B: mean HDL lead time.
    음수이면 harness가 평균적으로 먼저 감지 (좋은 신호).
    """
    values = [h for r in runs if (h := compute_hdl(r)) is not None]
    if not values:
        return MetricResult(value=float("nan"), n=0, notes="no detectable failures")

    arr = np.array(values)
    mean_val = float(np.mean(arr))
    se = float(np.std(arr, ddof=1) / math.sqrt(len(arr)))
    return MetricResult(
        value=mean_val,
        n=len(values),
        ci_lower=mean_val - 1.96 * se,
        ci_upper=mean_val + 1.96 * se,
        notes="negative = harness detects before agent self-reports",
    )


# ── SAA — Self-Assessment Accuracy ───────────────────────────────────────────

def compute_saa(
    agent_reports: list[dict],
    ground_truth: list[dict],
) -> MetricResult:
    """
    SAA = P(agent_judgment == ground_truth_verdict)

    agent_reports: [{"step": N, "agent_verdict": "pass"|"fail", "confidence": 0-1}]
    ground_truth:  [{"step": N, "verdict": "pass"|"fail"}]

    design-specification.md §5.2 참조
    """
    gt_map = {g["step"]: g["verdict"] for g in ground_truth}
    matched = [
        r for r in agent_reports
        if r["step"] in gt_map and r["agent_verdict"] in ("pass", "fail")
    ]
    if not matched:
        return MetricResult(value=float("nan"), n=0)

    correct = sum(1 for r in matched if r["agent_verdict"] == gt_map[r["step"]])
    rate = correct / len(matched)
    lo, hi = _wilson_ci(correct, len(matched))
    return MetricResult(value=rate, n=len(matched), ci_lower=lo, ci_upper=hi)


# ── GDR — Goal Drift Rate ─────────────────────────────────────────────────────

def compute_goal_fidelity_series(
    initial_goal_embedding: np.ndarray,
    checkpoint_embeddings: list[tuple[int, np.ndarray]],
) -> list[tuple[int, float]]:
    """
    각 checkpoint에서 Goal Fidelity Score (GFS) 계산.
    GFS = cosine_similarity(initial_goal_embedding, checkpoint_embedding)

    반환: [(step, gfs), ...]
    Figure 5 Panel A의 Y축 데이터.
    """
    return [
        (step, float(_cosine_similarity(initial_goal_embedding, emb)))
        for step, emb in checkpoint_embeddings
    ]


def compute_gdr(gfs_series: list[tuple[int, float]]) -> float:
    """
    GDR = mean rate of GFS decline per step.
    전체 시계열의 선형 기울기 (negative = drift).

    piecewise regression은 별도 함수 (detect_drift_regime).
    """
    if len(gfs_series) < 2:
        return 0.0
    steps = np.array([s for s, _ in gfs_series], dtype=float)
    scores = np.array([g for _, g in gfs_series])
    # 단순 선형 회귀 기울기
    slope = float(np.polyfit(steps, scores, 1)[0])
    return slope  # 음수이면 drift


def detect_drift_regime(
    gfs_series: list[tuple[int, float]],
    k_candidates: Optional[list[int]] = None,
) -> dict:
    """
    Piecewise linear regression으로 K-step (drift inflection) 추정.
    Figure 5 Panel A: Regime classification.

    design-specification.md §5.3 참조.
    반환: {k_hat, slope_before, slope_after, aic_piecewise, aic_linear, delta_aic}
    """
    steps = np.array([s for s, _ in gfs_series], dtype=float)
    scores = np.array([g for _, g in gfs_series])
    n = len(steps)

    # Linear fit AIC
    aic_linear = _aic_linear(steps, scores)

    if k_candidates is None:
        # step 범위의 20%~80%에서 탐색
        lo = int(steps.min() + 0.2 * (steps.max() - steps.min()))
        hi = int(steps.min() + 0.8 * (steps.max() - steps.min()))
        k_candidates = list(range(lo, hi + 1))

    best = {"k_hat": None, "aic_piecewise": float("inf")}
    for k in k_candidates:
        mask = steps <= k
        if mask.sum() < 2 or (~mask).sum() < 2:
            continue
        aic = _aic_piecewise(steps, scores, k)
        if aic < best["aic_piecewise"]:
            best = {"k_hat": k, "aic_piecewise": aic}

    delta_aic = aic_linear - best["aic_piecewise"]

    # 최적 K에서 각 regime 기울기
    slope_before, slope_after = float("nan"), float("nan")
    if best["k_hat"] is not None:
        k = best["k_hat"]
        mask = steps <= k
        if mask.sum() >= 2:
            slope_before = float(np.polyfit(steps[mask], scores[mask], 1)[0])
        if (~mask).sum() >= 2:
            slope_after = float(np.polyfit(steps[~mask], scores[~mask], 1)[0])

    return {
        "k_hat": best["k_hat"],
        "slope_before": slope_before,
        "slope_after": slope_after,
        "aic_piecewise": best["aic_piecewise"],
        "aic_linear": aic_linear,
        "delta_aic": delta_aic,
        "interpretation": (
            "phase transition detected (strong)"   if delta_aic > 10 else
            "phase transition detected (moderate)" if delta_aic > 4  else
            "no clear phase transition"
        ),
    }


# ── CCS — Context Contamination Score ────────────────────────────────────────

def compute_ccs(
    agent_a_output: str,
    agent_b_context_terms: list[str],
    n: int = 3,
) -> float:
    """
    CCS = (agent_a_output의 n-gram 중 agent_b_context_terms에서 온 것의 비율)

    agent_a_output: agent A의 출력 텍스트
    agent_b_context_terms: agent B의 고유 context에서 추출한 n-gram 목록
    n: n-gram size (default 3)

    Figure 6: Multi-Agent Contention Cascade의 Y2축.
    design-specification.md §5.4 참조.
    """
    a_ngrams = set(_extract_ngrams(agent_a_output, n))
    b_terms = set(agent_b_context_terms)
    if not a_ngrams:
        return 0.0
    overlap = a_ngrams & b_terms
    return len(overlap) / len(a_ngrams)


# ── HOR — Harness Overhead Ratio ─────────────────────────────────────────────

def compute_hor(run: RunLog) -> MetricResult:
    """
    HOR = harness_tokens / task_tokens

    harness_tokens: harness monitoring, goal re-injection, trust engine 등에
                    소비된 tokens (harness_alert이 발생한 step의 추가 tokens)
    task_tokens:    task 수행에 직접 사용된 tokens

    design-specification.md §6.1 참조.
    환경 독립적: 상대 비율이므로 절대값 불필요.
    """
    harness_tokens = sum(
        s.input_tokens + s.output_tokens
        for s in run.steps
        if s.harness_action is not None
    )
    task_tokens = run.total_input_tokens + run.total_output_tokens - harness_tokens

    if task_tokens <= 0:
        return MetricResult(value=float("nan"), n=1, notes="no task tokens recorded")

    hor = harness_tokens / task_tokens
    return MetricResult(value=hor, n=1)


# ── ECE — Expected Calibration Error ─────────────────────────────────────────

def compute_ece(
    confidences: list[float],
    correct: list[bool],
    n_bins: int = 10,
) -> MetricResult:
    """
    ECE = Σ (|B_m| / n) × |acc(B_m) − conf(B_m)|

    Figure 7 Panel A의 calibration curve 기반 요약 통계.
    B_m: m번째 confidence bin
    acc: bin 내 실제 정확도, conf: bin 내 평균 confidence

    adaptive binning 사용 (equal-mass bins).
    """
    if len(confidences) != len(correct) or not confidences:
        return MetricResult(value=float("nan"), n=0)

    n = len(confidences)
    sorted_pairs = sorted(zip(confidences, correct))
    bin_size = max(1, n // n_bins)

    ece = 0.0
    bins_used = 0
    for i in range(0, n, bin_size):
        chunk = sorted_pairs[i : i + bin_size]
        if not chunk:
            continue
        avg_conf = sum(c for c, _ in chunk) / len(chunk)
        avg_acc = sum(1 for _, ok in chunk if ok) / len(chunk)
        ece += (len(chunk) / n) * abs(avg_acc - avg_conf)
        bins_used += 1

    # Bootstrap 95% CI for ECE (재귀 없이 직접 계산)
    ece_bootstrap = []
    rng = np.random.default_rng(42)
    for _ in range(1000):
        idx = rng.integers(0, n, n)
        b_confs = [confidences[i] for i in idx]
        b_correct = [correct[i] for i in idx]
        # inline ECE 계산 (재귀 방지)
        b_n = len(b_confs)
        b_pairs = sorted(zip(b_confs, b_correct))
        b_bin_size = max(1, b_n // n_bins)
        b_ece = 0.0
        for j in range(0, b_n, b_bin_size):
            chunk = b_pairs[j : j + b_bin_size]
            if not chunk:
                continue
            avg_c = sum(c for c, _ in chunk) / len(chunk)
            avg_a = sum(1 for _, ok in chunk if ok) / len(chunk)
            b_ece += (len(chunk) / b_n) * abs(avg_a - avg_c)
        ece_bootstrap.append(b_ece)
    ci_lo = float(np.percentile(ece_bootstrap, 2.5))
    ci_hi = float(np.percentile(ece_bootstrap, 97.5))

    return MetricResult(
        value=ece,
        n=n,
        ci_lower=ci_lo,
        ci_upper=ci_hi,
        notes=f"adaptive bins used: {bins_used}",
    )


# ── Harness ROC 데이터 ────────────────────────────────────────────────────────

def compute_roc_data(
    harness_scores: list[float],
    ground_truth_labels: list[bool],
) -> dict:
    """
    Figure 9: Harness Detection ROC curve 데이터.

    harness_scores: 각 step에 대한 harness의 failure probability (0~1)
    ground_truth_labels: 실제 failure 여부 (True = failure)

    반환: {thresholds, tpr, fpr, auc, auc_ci}
    """
    if len(harness_scores) != len(ground_truth_labels):
        raise ValueError("scores and labels must be same length")

    thresholds = sorted(set(harness_scores), reverse=True)
    tpr_list, fpr_list = [], []
    pos = sum(ground_truth_labels)
    neg = len(ground_truth_labels) - pos

    if pos == 0 or neg == 0:
        return {"error": "no positive or negative samples"}

    for t in thresholds:
        tp = sum(1 for s, l in zip(harness_scores, ground_truth_labels) if s >= t and l)
        fp = sum(1 for s, l in zip(harness_scores, ground_truth_labels) if s >= t and not l)
        tpr_list.append(tp / pos)
        fpr_list.append(fp / neg)

    # fpr_list는 이미 증가 순서 → [::-1] 불필요
    auc = float(np.trapz(tpr_list, fpr_list))

    # DeLong-style bootstrap CI
    auc_samples = []
    pairs = list(zip(harness_scores, ground_truth_labels))
    rng = np.random.default_rng(42)
    for _ in range(2000):
        idx = rng.integers(0, len(pairs), len(pairs))
        b_scores = [pairs[i][0] for i in idx]
        b_labels = [pairs[i][1] for i in idx]
        if not any(b_labels) or all(b_labels):
            continue
        b_pos = sum(b_labels)
        b_neg = len(b_labels) - b_pos
        b_thresholds = sorted(set(b_scores), reverse=True)
        b_tpr, b_fpr = [], []
        for t in b_thresholds:
            tp = sum(1 for s, l in zip(b_scores, b_labels) if s >= t and l)
            fp = sum(1 for s, l in zip(b_scores, b_labels) if s >= t and not l)
            b_tpr.append(tp / b_pos)
            b_fpr.append(fp / b_neg)
        auc_samples.append(float(np.trapz(b_tpr, b_fpr)))

    return {
        "thresholds": thresholds,
        "tpr": tpr_list,
        "fpr": fpr_list,
        "auc": auc,
        "auc_ci_lower": float(np.percentile(auc_samples, 2.5)) if auc_samples else None,
        "auc_ci_upper": float(np.percentile(auc_samples, 97.5)) if auc_samples else None,
        "n_positive": pos,
        "n_negative": neg,
    }


# ── Failure Taxonomy Classification ──────────────────────────────────────────

FAILURE_TYPES = [
    "tool_call_failure",
    "context_window_overflow",
    "output_format_error",
    "silent_logical_drift",
    "recovery_succeeded",
    "recovery_failed",
]


def classify_failure(run: RunLog) -> Optional[str]:
    """
    Figure 2 Panel B (Radar chart) 및 Figure 3 (Surface heatmap)을 위한
    failure type 분류.

    현재 rule-based. Phase 0 taxonomy codebook 완성 후 LLM-based로 교체 예정.
    """
    if run.failure_type:
        return run.failure_type

    for step in run.steps:
        if step.tool_called and step.tool_success is False:
            return "tool_call_failure"
        if step.harness_alert and "context_overflow" in (step.harness_alert or ""):
            return "context_window_overflow"
        if step.harness_alert and "format_error" in (step.harness_alert or ""):
            return "output_format_error"

    if run.final_verdict == "failure":
        return "silent_logical_drift"

    return None


# ── 내부 유틸리티 ──────────────────────────────────────────────────────────────

def _wilson_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for proportion k/n."""
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    norm_a, norm_b = np.linalg.norm(a), np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def _extract_ngrams(text: str, n: int) -> list[str]:
    tokens = text.lower().split()
    return [" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def _aic_linear(x: np.ndarray, y: np.ndarray) -> float:
    """Linear fit AIC: k=2 parameters (slope, intercept)."""
    coeffs = np.polyfit(x, y, 1)
    residuals = y - np.polyval(coeffs, x)
    sse = float(np.sum(residuals**2))
    n = len(x)
    if sse <= 0:
        return float("-inf")
    return n * math.log(sse / n) + 2 * 2


def _aic_piecewise(x: np.ndarray, y: np.ndarray, k: float) -> float:
    """Piecewise linear fit AIC at breakpoint k: k=4 parameters."""
    mask = x <= k
    if mask.sum() < 2 or (~mask).sum() < 2:
        return float("inf")
    sse = 0.0
    for segment_x, segment_y in [(x[mask], y[mask]), (x[~mask], y[~mask])]:
        coeffs = np.polyfit(segment_x, segment_y, 1)
        residuals = segment_y - np.polyval(coeffs, segment_x)
        sse += float(np.sum(residuals**2))
    n = len(x)
    if sse <= 0:
        return float("-inf")
    return n * math.log(sse / n) + 2 * 4
