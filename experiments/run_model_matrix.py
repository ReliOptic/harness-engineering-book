#!/usr/bin/env python3
"""
Model matrix experiment runner (OpenRouter).

Purpose:
- Compare agent-targeted models across vendors/tiers with the same task set.
- Produce engineer-facing evidence: TCR/TCA/IFR + pairwise significance test.

Outputs:
- experiments/results/model-matrix/model-matrix-results.json
- experiments/results/model-matrix/model-matrix-results.md
"""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from framework.agent import ExperimentRunner
from framework.arcc import compute_ifr, compute_tca
from framework.config import ExperimentConfig, HarnessConfig, TaskConfig
from framework.ground_truth import validate_t1, validate_t2
from framework.harness import Harness
from framework.tasks import make_t1_task, make_t2_task


MODEL_LINEUP = [
    "nvidia/nemotron-3-super-120b-a12b",
    "openai/gpt-5.4-nano",
    "qwen/qwen3.5-9b",
    "openai/gpt-5.4-pro",
    "google/gemini-3.1-flash-lite-preview",
]


def _t1_bundle() -> tuple[str, str, dict, Callable]:
    task = make_t1_task("MODERATE")
    prompt = task.prompt
    ground_truth = task.ground_truth_bugs

    def _validator(output: str, gt):
        return validate_t1(output, gt)

    return "T1_code_review", prompt, {"ground_truth": ground_truth}, _validator


def _t2_bundle() -> tuple[str, str, dict, Callable]:
    task = make_t2_task("MODERATE")
    prompt = task.prompt
    ground_truth = {
        "constraints": task.constraints,
        "required_actions": task.required_actions,
        "optional_actions": task.optional_actions,
    }

    def _validator(output: str, gt):
        return validate_t2(output, gt)

    return "T2_multi_step", prompt, {"ground_truth": ground_truth}, _validator


TASK_BUNDLES = {
    "T1_code_review": _t1_bundle,
    "T2_multi_step": _t2_bundle,
}


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _two_prop_z_test(x1: int, n1: int, x2: int, n2: int) -> dict:
    if n1 <= 0 or n2 <= 0:
        return {"z": float("nan"), "p_value": 1.0}
    p1 = x1 / n1
    p2 = x2 / n2
    p_pool = (x1 + x2) / (n1 + n2)
    se = math.sqrt(max(p_pool * (1.0 - p_pool) * (1.0 / n1 + 1.0 / n2), 0.0))
    if se == 0:
        return {"z": 0.0, "p_value": 1.0}
    z = (p1 - p2) / se
    p = 2.0 * (1.0 - _norm_cdf(abs(z)))
    return {"z": z, "p_value": p}


def _holm_adjust(rows: list[dict], p_key: str = "p_value") -> list[dict]:
    indexed = list(enumerate(rows))
    indexed.sort(key=lambda pair: pair[1][p_key])
    m = len(rows)
    adjusted = [0.0] * m
    running_max = 0.0
    for rank, (orig_idx, row) in enumerate(indexed, start=1):
        raw = row[p_key]
        adj = min(1.0, raw * (m - rank + 1))
        running_max = max(running_max, adj)
        adjusted[orig_idx] = running_max
    out = []
    for i, row in enumerate(rows):
        row2 = dict(row)
        row2["p_holm"] = adjusted[i]
        row2["significant_0_05"] = adjusted[i] < 0.05
        out.append(row2)
    return out


def run_matrix(
    models: list[str],
    runs_per_model: int,
    task_ids: list[str],
    max_steps: int,
    token_budget: int,
) -> dict:
    bundles = [TASK_BUNDLES[task_id]() for task_id in task_ids]
    all_rows: list[dict] = []

    for task_type, prompt, gt_wrap, validator_fn in bundles:
        for model in models:
            config_template = ExperimentConfig(
                experiment_id=f"MATRIX_{task_type}",
                run_id=1,
                model=model,
                harness=HarnessConfig.none(),
                task=TaskConfig(
                    task_type=task_type,  # type: ignore[arg-type]
                    difficulty="MODERATE",
                    max_steps=max_steps,
                    token_budget=token_budget,
                ),
                token_budget_ratio=1.0,
            )
            runner = ExperimentRunner(
                n_runs=runs_per_model,
                config_template=config_template,
                harness_factory=lambda: Harness(HarnessConfig.none()),
                task_prompt_factory=lambda _run_id, p=prompt: p,
                ground_truth=gt_wrap["ground_truth"],
                validator_fn=validator_fn,
            )
            runs = runner.run_all()
            summary = runner.summary(runs)

            strict_success = sum(1 for r in runs if r.final_verdict == "success")
            partial = sum(1 for r in runs if r.final_verdict == "partial")
            tcr_cont = (strict_success + 0.5 * partial) / len(runs) if runs else 0.0

            tool_call_log = [e for r in runs for e in r.tool_call_log]
            instruction_log = [e for r in runs for e in r.instruction_compliance]
            tca = compute_tca(tool_call_log).value
            ifr = compute_ifr(instruction_log).value

            all_rows.append(
                {
                    "task_type": task_type,
                    "model": model,
                    "n_runs": len(runs),
                    "successes": strict_success,
                    "partials": partial,
                    "failures": sum(1 for r in runs if r.final_verdict == "failure"),
                    "tcr_continuous": tcr_cont,
                    "tca": tca,
                    "ifr": ifr,
                    "rsucc_r": summary["rsucc_r"]["value"],
                    "ttff_mean": summary["ttff"].get("mean"),
                    "hor_mean": summary.get("hor_mean"),
                    "failure_types": summary.get("failure_types", {}),
                }
            )

    pairwise: list[dict] = []
    for task in sorted({r["task_type"] for r in all_rows}):
        rows = [r for r in all_rows if r["task_type"] == task]
        for i in range(len(rows)):
            for j in range(i + 1, len(rows)):
                a, b = rows[i], rows[j]
                test = _two_prop_z_test(a["successes"], a["n_runs"], b["successes"], b["n_runs"])
                pairwise.append(
                    {
                        "task_type": task,
                        "model_a": a["model"],
                        "model_b": b["model"],
                        "success_rate_a": a["successes"] / a["n_runs"] if a["n_runs"] else 0.0,
                        "success_rate_b": b["successes"] / b["n_runs"] if b["n_runs"] else 0.0,
                        "delta_success_rate": (
                            (a["successes"] / a["n_runs"]) - (b["successes"] / b["n_runs"])
                            if a["n_runs"] and b["n_runs"]
                            else 0.0
                        ),
                        "z": test["z"],
                        "p_value": test["p_value"],
                    }
                )

    adjusted = []
    for task in sorted({r["task_type"] for r in pairwise}):
        task_rows = [r for r in pairwise if r["task_type"] == task]
        adjusted.extend(_holm_adjust(task_rows))

    return {
        "meta": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "runs_per_model": runs_per_model,
            "models": models,
            "tasks": task_ids,
            "harness": "none",
            "difficulty": "MODERATE",
            "note": "Pilot matrix for model-size/vendor differentiation (agent-oriented tasks).",
        },
        "results": all_rows,
        "pairwise_tests": adjusted,
    }


def _write_markdown(path: Path, payload: dict) -> None:
    rows = payload["results"]
    tests = payload["pairwise_tests"]
    lines: list[str] = []
    lines.append("# Model Matrix Results (Pilot)")
    lines.append("")
    lines.append(f"- Generated: {payload['meta']['generated_at_utc']}")
    lines.append(f"- Runs/model: {payload['meta']['runs_per_model']}")
    lines.append(f"- Harness: {payload['meta']['harness']}")
    lines.append("")
    for task in sorted({r["task_type"] for r in rows}):
        lines.append(f"## {task}")
        lines.append("")
        lines.append("| model | n | success | partial | fail | TCR(cont) | TCA | IFR |")
        lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
        for r in [x for x in rows if x["task_type"] == task]:
            lines.append(
                f"| {r['model']} | {r['n_runs']} | {r['successes']} | {r['partials']} | {r['failures']} | "
                f"{r['tcr_continuous']:.3f} | {r['tca']:.3f} | {r['ifr']:.3f} |"
            )
        lines.append("")
        lines.append("### Pairwise Significance (success rate)")
        lines.append("")
        lines.append("| model_a | model_b | delta | p | p_holm | sig<0.05 |")
        lines.append("| --- | --- | ---: | ---: | ---: | --- |")
        for t in [x for x in tests if x["task_type"] == task]:
            lines.append(
                f"| {t['model_a']} | {t['model_b']} | {t['delta_success_rate']:.3f} | "
                f"{t['p_value']:.4f} | {t['p_holm']:.4f} | {t['significant_0_05']} |"
            )
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def _json_safe(value):
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return value
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Run model matrix pilot experiments.")
    parser.add_argument("--runs", type=int, default=3, help="runs per model per task")
    parser.add_argument(
        "--tasks",
        type=str,
        default="T1_code_review",
        help="comma-separated task IDs: T1_code_review,T2_multi_step",
    )
    parser.add_argument("--max-steps", type=int, default=4, help="max steps per run")
    parser.add_argument("--token-budget", type=int, default=2000, help="token budget per run")
    parser.add_argument(
        "--models",
        type=str,
        default=",".join(MODEL_LINEUP),
        help="comma-separated OpenRouter model IDs",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("results/model-matrix"),
        help="output directory under experiments/",
    )
    args = parser.parse_args()
    task_ids = [t.strip() for t in args.tasks.split(",") if t.strip()]
    model_ids = [m.strip() for m in args.models.split(",") if m.strip()]
    unknown = [t for t in task_ids if t not in TASK_BUNDLES]
    if unknown:
        raise SystemExit(f"Unknown task IDs: {', '.join(unknown)}")
    if not model_ids:
        raise SystemExit("No models specified.")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    payload = run_matrix(
        model_ids,
        args.runs,
        task_ids=task_ids,
        max_steps=args.max_steps,
        token_budget=args.token_budget,
    )

    json_path = args.out_dir / "model-matrix-results.json"
    md_path = args.out_dir / "model-matrix-results.md"
    json_path.write_text(
        json.dumps(_json_safe(payload), ensure_ascii=False, indent=2, allow_nan=False),
        encoding="utf-8",
    )
    _write_markdown(md_path, payload)

    print(f"Wrote: {json_path}")
    print(f"Wrote: {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
