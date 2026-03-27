"""
Layer 2 LLM Judge — design-specification.md §3.1 참조.

agent output의 ground truth 검증 (Layer 1 test suite 보완).
Judge 모델: MODEL_JUDGE (gemini-3.1-flash-lite-preview) — 실험 agent와 다른 모델.
Figure 9 ROC curve에서 전체 runs의 ~30%에 적용.
Cohen's κ ≥ 0.70 목표.

사용:
    judge = LLMJudge()
    result = judge.evaluate(task_spec, agent_output, l1_verdict="uncertain", l1_score=0.4)
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Literal, Optional

from openai import OpenAI, APIError

from .config import MODEL_JUDGE

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


# ── 결과 타입 ──────────────────────────────────────────────────────────────────

@dataclass
class JudgeResult:
    verdict: Literal["pass", "fail", "uncertain"]
    confidence: float        # [0, 1]
    rationale: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0


# ── LLM Judge ─────────────────────────────────────────────────────────────────

class LLMJudge:
    """
    Layer 2 LLM Judge.
    실험 agent와 독립적 모델로 agent output을 평가.

    Layer 1 결과가 "uncertain"이거나 harness가 failure로 판정한 step에 적용.
    """

    _JUDGE_PROMPT = (
        "You are an independent evaluator for an AI agent experiment.\n\n"
        "Task specification:\n{task_spec}\n\n"
        "Agent output:\n{agent_output}\n\n"
        "Layer 1 automated test result: {l1_verdict} (score: {l1_score:.2f})\n\n"
        "Evaluate whether the agent output correctly solves the task.\n"
        "Be strict: 'pass' requires genuinely correct output, not just plausible-looking.\n\n"
        "Respond with ONLY a JSON object:\n"
        '{"verdict": "pass"|"fail"|"uncertain", "confidence": 0.0-1.0, '
        '"rationale": "one sentence explaining the decision"}'
    )

    def __init__(
        self,
        model: str = MODEL_JUDGE,
        api_key: Optional[str] = None,
        base_url: str = OPENROUTER_BASE_URL,
    ):
        self.model = model
        self.client = OpenAI(
            api_key=api_key or os.environ.get("OPENROUTER_API_KEY", ""),
            base_url=base_url,
        )

    def evaluate(
        self,
        task_spec: str,
        agent_output: str,
        l1_verdict: str = "uncertain",
        l1_score: float = 0.0,
    ) -> JudgeResult:
        """단일 agent output에 대한 판정."""
        prompt = self._JUDGE_PROMPT.format(
            task_spec=task_spec[:800],           # context 절약
            agent_output=agent_output[:2000],
            l1_verdict=l1_verdict,
            l1_score=l1_score,
        )
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
            )
            content = resp.choices[0].message.content or ""
            parsed = json.loads(_extract_json_str(content))
            return JudgeResult(
                verdict=parsed.get("verdict", "uncertain"),
                confidence=float(parsed.get("confidence", 0.5)),
                rationale=parsed.get("rationale", ""),
                model=self.model,
                input_tokens=resp.usage.prompt_tokens if resp.usage else 0,
                output_tokens=resp.usage.completion_tokens if resp.usage else 0,
            )
        except (APIError, json.JSONDecodeError, Exception) as e:
            return JudgeResult(
                verdict="uncertain",
                confidence=0.0,
                rationale=f"judge error: {e}",
                model=self.model,
            )

    def evaluate_batch(
        self,
        items: list[dict],
        apply_condition: str = "uncertain",
    ) -> list[JudgeResult]:
        """
        items: [{"task_spec": ..., "agent_output": ..., "l1_verdict": ..., "l1_score": ...}]
        apply_condition: "uncertain" → L1이 uncertain인 항목만 평가, "all" → 전체 평가.
        """
        results = []
        for item in items:
            if apply_condition == "uncertain" and item.get("l1_verdict") != "uncertain":
                # L1이 pass/fail로 확정된 항목은 L1 결과를 그대로 사용
                results.append(JudgeResult(
                    verdict=item["l1_verdict"],
                    confidence=1.0,
                    rationale="L1 automated test — no L2 evaluation needed",
                    model="L1_test_suite",
                ))
            else:
                results.append(self.evaluate(
                    task_spec=item.get("task_spec", ""),
                    agent_output=item.get("agent_output", ""),
                    l1_verdict=item.get("l1_verdict", "uncertain"),
                    l1_score=item.get("l1_score", 0.0),
                ))
        return results


# ── Cohen's κ ─────────────────────────────────────────────────────────────────

def compute_cohen_kappa(
    rater_a: list[str],
    rater_b: list[str],
    labels: tuple[str, ...] = ("pass", "fail", "uncertain"),
) -> float:
    """
    Cohen's κ = (p_o - p_e) / (1 - p_e)

    design-specification.md §3.1:
    κ ≥ 0.70 → Layer 2 judge 신뢰 가능
    κ < 0.70 → judge 기준 재조정 필요

    rater_a, rater_b: 동일 케이스에 대한 두 rater의 verdict 목록.
    """
    if len(rater_a) != len(rater_b) or not rater_a:
        return float("nan")

    n = len(rater_a)

    # Observed agreement
    p_o = sum(1 for a, b in zip(rater_a, rater_b) if a == b) / n

    # Expected agreement
    p_e = 0.0
    for label in labels:
        pa = sum(1 for x in rater_a if x == label) / n
        pb = sum(1 for x in rater_b if x == label) / n
        p_e += pa * pb

    if p_e >= 1.0:
        return 1.0
    return (p_o - p_e) / (1.0 - p_e)


def agreement_matrix(
    rater_a: list[str],
    rater_b: list[str],
    labels: tuple[str, ...] = ("pass", "fail", "uncertain"),
) -> dict:
    """
    두 rater 간 agreement 상세 분석.
    κ + confusion matrix.
    """
    kappa = compute_cohen_kappa(rater_a, rater_b, labels)
    matrix: dict[str, dict[str, int]] = {la: {lb: 0 for lb in labels} for la in labels}
    for a, b in zip(rater_a, rater_b):
        if a in matrix and b in matrix[a]:
            matrix[a][b] += 1

    return {
        "kappa": kappa,
        "kappa_interpretation": (
            "reliable (κ≥0.70)"     if kappa >= 0.70 else
            "marginal (0.60≤κ<0.70)" if kappa >= 0.60 else
            "poor (κ<0.60) — recalibrate"
        ),
        "matrix": matrix,
        "n": len(rater_a),
    }


# ── 내부 유틸리티 ──────────────────────────────────────────────────────────────

def _extract_json_str(text: str) -> str:
    match = re.search(r"\{[\s\S]*?\}", text)
    return match.group(0) if match else text
