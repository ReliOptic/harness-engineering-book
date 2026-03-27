"""
ARCC — Agent-Relevant Capability Composite

Figure 1의 X축. Vendor tier 대신 연속 capability spectrum.
4개 하위 지표 → weighted composite → capability cliff 탐지.

design-specification.md §2 참조.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Optional

import numpy as np


# ── 하위 지표 결과 타입 ─────────────────────────────────────────────────────────

@dataclass
class SubMetricResult:
    value: float      # [0, 1]
    n: int            # 측정 횟수
    notes: str = ""


@dataclass
class ARCCResult:
    arcc: float                     # [0, 1] composite score
    tca: SubMetricResult
    ifr: SubMetricResult
    msrd: SubMetricResult
    cue: SubMetricResult
    weights: tuple[float, float, float, float]
    model_id: str
    task_type: str


# ── TCA — Tool Call Accuracy ──────────────────────────────────────────────────

def compute_tca(tool_call_log: list[dict]) -> SubMetricResult:
    """
    TCA = valid_tool_calls / attempted_tool_calls

    valid: JSON schema 통과 + 내용이 task context에 관련됨
    tool_call_log: [{"called": bool, "success": bool, "tool": str}]
    """
    attempted = [e for e in tool_call_log if e.get("called", False)]
    if not attempted:
        return SubMetricResult(value=0.0, n=0, notes="no tool calls attempted")

    valid = [e for e in attempted if e.get("success", False)]
    rate = len(valid) / len(attempted)
    return SubMetricResult(value=rate, n=len(attempted))


# ── IFR — Instruction Following Rate ─────────────────────────────────────────

def compute_ifr(instruction_compliance: list[dict]) -> SubMetricResult:
    """
    IFR = mean(binary_compliance_scores)

    instruction_compliance: [{"instruction": str, "complied": bool}]
    5개 명시적 instruction에 대한 이진 준수 여부.
    자동 판정: JSON 형식 → 파싱 성공 여부, 길이 제한 → len 체크 등.
    """
    applicable = [e for e in instruction_compliance if e.get("applicable", True)]
    if not applicable:
        return SubMetricResult(value=0.0, n=0, notes="no instructions recorded")

    scores = [1.0 if e.get("complied", False) else 0.0 for e in applicable]
    rate = sum(scores) / len(scores)
    return SubMetricResult(value=rate, n=len(scores))


# ── MSRD — Multi-Step Reasoning Depth (정규화) ────────────────────────────────

def compute_msrd(
    step_validity: list[bool],
    task_max_steps: int,
) -> SubMetricResult:
    """
    MSRD_normalized = (첫 번째 오류 발생 step index) / task_max_steps

    step_validity: [True, True, False, ...] — 각 step의 validity
    error-free 완주 → MSRD = 1.0
    첫 step 오류 → MSRD = 1 / task_max_steps (최솟값)
    """
    if not step_validity:
        return SubMetricResult(value=0.0, n=0, notes="no steps recorded")

    for i, valid in enumerate(step_validity):
        if not valid:
            return SubMetricResult(
                value=(i + 1) / task_max_steps,
                n=len(step_validity),
                notes=f"first error at step {i+1}",
            )

    return SubMetricResult(
        value=min(1.0, len(step_validity) / task_max_steps),
        n=len(step_validity),
        notes="error-free completion",
    )


# ── CUE — Context Utilization Efficiency ─────────────────────────────────────

def compute_cue(
    relevant_passages: list[str],
    agent_output: str,
) -> SubMetricResult:
    """
    CUE = cited_relevant_passages / total_relevant_passages

    relevant_passages: ground truth에서 미리 표시된 핵심 passage 목록
    agent_output: agent의 최종 출력 (T4 task)

    passage 포함 여부: 핵심 구문(≥4 words)이 output에 존재하면 cited.
    """
    if not relevant_passages:
        return SubMetricResult(value=0.0, n=0, notes="no relevant passages defined")

    cited = 0
    output_lower = agent_output.lower()
    for passage in relevant_passages:
        # 4-gram 이상의 핵심 구문이 output에 있으면 cited
        key_phrases = _extract_key_phrases(passage, min_words=4)
        if any(phrase in output_lower for phrase in key_phrases):
            cited += 1

    rate = cited / len(relevant_passages)
    return SubMetricResult(value=rate, n=len(relevant_passages))


# ── ARCC Composite ────────────────────────────────────────────────────────────

DEFAULT_WEIGHTS = (0.25, 0.25, 0.25, 0.25)  # equal weighting


def compute_arcc(
    tca: SubMetricResult,
    ifr: SubMetricResult,
    msrd: SubMetricResult,
    cue: SubMetricResult,
    weights: tuple[float, float, float, float] = DEFAULT_WEIGHTS,
    model_id: str = "",
    task_type: str = "",
) -> ARCCResult:
    """
    ARCC = w1·TCA + w2·IFR + w3·MSRD_n + w4·CUE

    가중치 합 = 1.0 강제.
    """
    w = np.array(weights)
    if abs(w.sum() - 1.0) > 1e-6:
        w = w / w.sum()

    values = np.array([tca.value, ifr.value, msrd.value, cue.value])
    arcc = float(np.dot(w, values))

    return ARCCResult(
        arcc=arcc,
        tca=tca,
        ifr=ifr,
        msrd=msrd,
        cue=cue,
        weights=tuple(w),
        model_id=model_id,
        task_type=task_type,
    )


# ── ARCC Construct Validation ──────────────────────────────────────────────────

def validate_arcc(
    arcc_scores: list[float],
    tcr_observed: list[float],
    test_size: float = 0.20,
    seed: int = 42,
) -> dict:
    """
    design-specification.md §2.3:
    ARCC → TCR 예측력을 holdout R²로 검증.

    arcc_scores: 각 (model, task) 조합의 ARCC
    tcr_observed: 동일 조합의 실측 TCR

    반환: {r2_train, r2_holdout, verdict, slope, intercept}
    """
    from sklearn.linear_model import LinearRegression  # type: ignore
    from sklearn.model_selection import train_test_split  # type: ignore

    X = np.array(arcc_scores).reshape(-1, 1)
    y = np.array(tcr_observed)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=seed
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    r2_train = float(model.score(X_train, y_train))
    r2_test = float(model.score(X_test, y_test))

    verdict = (
        "valid (R²≥0.65)"         if r2_test >= 0.65 else
        "marginal (0.50≤R²<0.65)" if r2_test >= 0.50 else
        "invalid — redesign needed"
    )

    return {
        "r2_train": r2_train,
        "r2_holdout": r2_test,
        "slope": float(model.coef_[0]),
        "intercept": float(model.intercept_),
        "verdict": verdict,
        "n_total": len(arcc_scores),
        "n_train": len(X_train),
        "n_test": len(X_test),
    }


def sensitivity_analysis(
    arcc_results: list[ARCCResult],
    tcr_observed: list[float],
    delta: float = 0.15,
    n_samples: int = 500,
    seed: int = 42,
) -> dict:
    """
    가중치 ±0.15 범위의 grid search → TCR 예측의 R² 분산.
    결과가 robust하면 equal weighting 유지.
    """
    rng = np.random.default_rng(seed)
    r2_samples = []

    for _ in range(n_samples):
        # w ∈ [0.25-delta, 0.25+delta]^4, normalized
        w = rng.uniform(max(0, 0.25 - delta), 0.25 + delta, 4)
        w = w / w.sum()

        arcc_recomputed = []
        for r in arcc_results:
            vals = np.array([r.tca.value, r.ifr.value, r.msrd.value, r.cue.value])
            arcc_recomputed.append(float(np.dot(w, vals)))

        result = validate_arcc(arcc_recomputed, tcr_observed)
        r2_samples.append(result["r2_holdout"])

    arr = np.array(r2_samples)
    return {
        "r2_mean": float(np.mean(arr)),
        "r2_std": float(np.std(arr)),
        "r2_min": float(np.min(arr)),
        "r2_max": float(np.max(arr)),
        "robust": float(np.std(arr)) < 0.05,  # std < 0.05이면 robust
        "interpretation": (
            "weight choice does not significantly affect predictive validity — equal weighting justified"
            if float(np.std(arr)) < 0.05
            else "prediction is sensitive to weight choice — data-driven weighting recommended"
        ),
    }


# ── Capability Cliff Detection ────────────────────────────────────────────────

def detect_capability_cliff(
    arcc_scores: list[float],
    tcr_values: list[float],
    tcr_threshold: float = 0.50,
) -> dict:
    """
    Figure 1: Capability Cliff 위치 추정.

    TCR = 50%인 ARCC 값 (logistic regression으로 추정).
    task type별로 별도 호출.

    반환: {cliff_arcc, ci_lower, ci_upper, model_type, fit_quality}
    """
    from scipy.optimize import curve_fit  # type: ignore
    from scipy.stats import norm  # type: ignore

    x = np.array(arcc_scores)
    y = np.array(tcr_values)

    # Sigmoid fit: TCR = 1 / (1 + exp(-k*(x - x0)))
    def sigmoid(x, k, x0):
        return 1.0 / (1.0 + np.exp(-k * (x - x0)))

    try:
        popt, pcov = curve_fit(sigmoid, x, y, p0=[10, 0.5], maxfev=5000)
        k_hat, x0_hat = popt
        perr = np.sqrt(np.diag(pcov))

        # x0 (cliff position) 95% CI
        cliff_ci_lower = x0_hat - 1.96 * perr[1]
        cliff_ci_upper = x0_hat + 1.96 * perr[1]

        # Residuals for fit quality
        y_pred = sigmoid(x, *popt)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")

        return {
            "cliff_arcc": float(x0_hat),
            "ci_lower": float(cliff_ci_lower),
            "ci_upper": float(cliff_ci_upper),
            "slope_k": float(k_hat),
            "model_type": "sigmoid",
            "r2": float(r2),
            "fit_quality": "good" if r2 > 0.70 else "marginal" if r2 > 0.50 else "poor",
        }

    except (RuntimeError, ValueError):
        # sigmoid fit 실패 → linear 근사
        coeffs = np.polyfit(x, y, 1)
        cliff_x = (tcr_threshold - coeffs[1]) / coeffs[0] if coeffs[0] != 0 else float("nan")
        return {
            "cliff_arcc": float(cliff_x),
            "ci_lower": None,
            "ci_upper": None,
            "slope_k": None,
            "model_type": "linear_fallback",
            "r2": None,
            "fit_quality": "fallback",
        }


# ── 내부 유틸리티 ──────────────────────────────────────────────────────────────

def _extract_key_phrases(text: str, min_words: int = 4) -> list[str]:
    """텍스트에서 min_words 이상의 연속 구문 추출 (CUE용)."""
    words = text.lower().split()
    phrases = []
    for size in range(min_words, min(len(words) + 1, min_words + 4)):
        for i in range(len(words) - size + 1):
            phrases.append(" ".join(words[i : i + size]))
    return phrases
