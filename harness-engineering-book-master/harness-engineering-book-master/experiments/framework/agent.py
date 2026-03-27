"""
Agent Runner — Claude API 기반 실험 실행기

각 실험 trial을 실행하고 RunLog를 생성한다.
Harness를 on/off 조건 모두에서 동일 구조로 실행.

design-specification.md §1.2 (task 배정), §4 (power analysis에 따른 run 수) 참조.
"""
from __future__ import annotations

import json
import os
import time
from typing import Callable, Optional

import anthropic

from .config import ExperimentConfig, RunLog, StepLog, TaskType
from .ground_truth import (
    ValidationResult,
    validate_t1,
    validate_t2,
    validate_t3_goal_fidelity,
    validate_t4,
)
from .harness import Harness
from .metrics import classify_failure, compute_hor


# ── System Prompts ─────────────────────────────────────────────────────────────

SYSTEM_PROMPTS: dict[TaskType, str] = {
    "T1_code_review": (
        "You are a senior software engineer performing a code review. "
        "Identify all bugs in the provided code. "
        "Return your findings as a JSON list: "
        '[{"line_number": N, "bug_type": "...", "severity": "low|medium|high|critical", '
        '"fix_suggestion": "..."}]. '
        "Be precise about line numbers."
    ),
    "T2_multi_step": (
        "You are a planning agent. Given a set of tasks with dependencies and constraints, "
        "produce a valid execution plan. "
        "Return as JSON: "
        '[{"step": N, "action": "...", "rationale": "..."}]. '
        "Ensure all dependency constraints are satisfied."
    ),
    "T3_long_horizon": (
        "You are an autonomous coding agent. Execute the given task step by step. "
        "Each step should use exactly one tool. "
        "At every 10th step, include your current goal statement in your response "
        'with the prefix "CURRENT GOAL: ". '
        "Continue until the task is complete or you reach the step budget."
    ),
    "T4_synthesis": (
        "You are a research synthesis agent. Read the provided documents carefully. "
        "Answer the question using only information from the documents. "
        "Cite the document number for each key fact you use. "
        "Do not include information that contradicts the majority of sources."
    ),
}


# ── Agent Runner ───────────────────────────────────────────────────────────────

class AgentRunner:
    """
    단일 실험 trial 실행.
    harness.observe()를 매 step에서 호출하여 RunLog를 생성.
    """

    def __init__(
        self,
        config: ExperimentConfig,
        harness: Harness,
        embedding_fn: Optional[Callable[[str], object]] = None,
        validator_fn: Optional[Callable] = None,
        api_key: Optional[str] = None,
    ):
        self.config = config
        self.harness = harness
        self.embedding_fn = embedding_fn
        self.validator_fn = validator_fn
        self.client = anthropic.Anthropic(
            api_key=api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        )
        self.run_log = RunLog(config=config)

    def run(
        self,
        task_prompt: str,
        ground_truth: Optional[dict] = None,
        initial_goal: str = "",
    ) -> RunLog:
        """
        task_prompt를 agent에게 주고 실험을 실행한다.
        harness가 on이면 매 step에서 observe().
        """
        messages: list[dict] = [{"role": "user", "content": task_prompt}]
        system = SYSTEM_PROMPTS.get(self.config.task.task_type, "You are a helpful assistant.")

        # token budget을 config.token_budget_ratio로 조정 (E08용)
        effective_budget = int(
            self.config.task.token_budget * self.config.token_budget_ratio
        )
        self.harness.token_budget = effective_budget

        max_tokens_per_step = min(2048, effective_budget // 5)
        step = 0
        recovered = False

        while step < self.config.task.max_steps:
            step += 1

            # ── API call ──────────────────────────────────────────────────────
            try:
                response = self.client.messages.create(
                    model=self.config.model,
                    max_tokens=max_tokens_per_step,
                    system=system,
                    messages=messages,
                )
            except anthropic.APIError as e:
                step_log = StepLog(
                    step_number=step,
                    timestamp_ms=int(time.time() * 1000),
                    input_tokens=0,
                    output_tokens=0,
                    tool_called=None,
                    tool_success=None,
                    agent_output="",
                    goal_statement=None,
                    harness_alert="api_error",
                    harness_action="abort",
                )
                self.run_log.steps.append(step_log)
                self.run_log.final_verdict = "failure"
                self.run_log.failure_type = "api_error"
                break

            content = response.content[0].text if response.content else ""
            input_tok = response.usage.input_tokens
            output_tok = response.usage.output_tokens
            self.run_log.total_input_tokens += input_tok
            self.run_log.total_output_tokens += output_tok

            # ── Goal statement 추출 (T3 checkpoint) ──────────────────────────
            goal_stmt = None
            if "CURRENT GOAL:" in content:
                for line in content.splitlines():
                    if line.startswith("CURRENT GOAL:"):
                        goal_stmt = line.replace("CURRENT GOAL:", "").strip()
                        break

            # ── Harness observe ───────────────────────────────────────────────
            step_log = self.harness.observe(
                step_number=step,
                agent_output=content,
                input_tokens=input_tok,
                output_tokens=output_tok,
                goal_statement=goal_stmt,
            )

            # ── Ground truth Layer 1 판정 (있을 경우) ─────────────────────────
            if ground_truth and self.validator_fn:
                verdict = self.validator_fn(content, ground_truth)
                step_log.ground_truth_verdict = verdict.verdict

            self.run_log.steps.append(step_log)

            # ── Harness action 처리 ───────────────────────────────────────────
            action = step_log.harness_action
            if action == "abort" or action == "graceful_stop":
                self.run_log.final_verdict = "failure"
                self.run_log.failure_type = step_log.harness_alert
                break

            if action == "rollback":
                checkpoint = self.harness.state.get_last_stable_checkpoint()
                if checkpoint:
                    # 마지막 stable context로 복귀
                    messages = checkpoint["context"].get("messages", messages[:2])
                    recovered = True
                else:
                    self.run_log.final_verdict = "failure"
                    self.run_log.failure_type = "no_checkpoint_for_rollback"
                    break
                continue

            if action == "retry":
                # 동일 메시지로 재시도 (messages 유지)
                step -= 1  # step count 보정
                continue

            if action == "goal_reinjection":
                # system prompt에 goal 재삽입
                messages.append({
                    "role": "user",
                    "content": f"[HARNESS] Reminder — your original goal: {initial_goal}",
                })

            # ── 정상 진행: 다음 step ──────────────────────────────────────────
            messages.append({"role": "assistant", "content": content})
            messages.append({"role": "user", "content": "[Continue]"})

            # ── Task 완료 감지 ─────────────────────────────────────────────────
            if _is_task_complete(content, self.config.task.task_type):
                self.run_log.final_verdict = "success"
                break

        # ── Run 마무리 ────────────────────────────────────────────────────────
        if self.run_log.final_verdict is None:
            # max_steps 도달 → 결과로 판정
            last_output = self.run_log.steps[-1].agent_output if self.run_log.steps else ""
            self.run_log.final_verdict = "partial" if len(last_output) > 50 else "failure"

        self.run_log.recovered = recovered
        if self.run_log.final_verdict == "failure":
            self.run_log.failure_type = (
                self.run_log.failure_type or
                classify_failure(self.run_log)
            )

        return self.run_log


# ── Experiment Runner (다중 run 오케스트레이터) ─────────────────────────────────

class ExperimentRunner:
    """
    동일 조건에서 N회 반복 실행하여 통계 기반 결과를 생성.
    design-specification.md §4 (power analysis)에서 결정된 n을 사용.
    """

    def __init__(
        self,
        n_runs: int,
        config_template: ExperimentConfig,
        harness_factory: Callable[[], Harness],
        task_prompt_factory: Callable[[int], str],  # run_id → prompt
        ground_truth: Optional[dict] = None,
        validator_fn: Optional[Callable] = None,
        embedding_fn: Optional[Callable] = None,
        api_key: Optional[str] = None,
    ):
        self.n_runs = n_runs
        self.config_template = config_template
        self.harness_factory = harness_factory
        self.task_prompt_factory = task_prompt_factory
        self.ground_truth = ground_truth
        self.validator_fn = validator_fn
        self.embedding_fn = embedding_fn
        self.api_key = api_key

    def run_all(self, initial_goal: str = "") -> list[RunLog]:
        """
        n_runs회 반복 실행. 각 run은 독립 HarnessState로 시작.
        진행 상황을 stdout에 출력 (실험 중 모니터링).
        """
        results = []
        for i in range(self.n_runs):
            config = ExperimentConfig(
                experiment_id=self.config_template.experiment_id,
                run_id=i + 1,
                model=self.config_template.model,
                harness=self.config_template.harness,
                task=self.config_template.task,
                surface=self.config_template.surface,
                token_budget_ratio=self.config_template.token_budget_ratio,
                agent_count=self.config_template.agent_count,
            )

            harness = self.harness_factory()
            runner = AgentRunner(
                config=config,
                harness=harness,
                embedding_fn=self.embedding_fn,
                validator_fn=self.validator_fn,
                api_key=self.api_key,
            )

            prompt = self.task_prompt_factory(i + 1)
            print(
                f"[{config.experiment_id}] run {i+1}/{self.n_runs} | "
                f"model={config.model} | harness={config.harness.enabled_components()}"
            )

            run_log = runner.run(prompt, self.ground_truth, initial_goal)
            results.append(run_log)

            print(
                f"  → verdict={run_log.final_verdict} | "
                f"recovered={run_log.recovered} | "
                f"steps={len(run_log.steps)} | "
                f"tokens={run_log.total_input_tokens + run_log.total_output_tokens}"
            )

        return results

    def summary(self, results: list[RunLog]) -> dict:
        """
        실험 결과 요약 통계.
        figure_expansion.md의 각 figure에 직접 입력 가능한 형태.
        """
        from .metrics import (
            compute_rsucc_r,
            compute_hor,
            compute_ttff_distribution,
        )

        rsucc = compute_rsucc_r(results)
        ttff_dist = compute_ttff_distribution(results)
        hor_values = [compute_hor(r).value for r in results]
        hor_values = [v for v in hor_values if not (v != v)]  # NaN 제거

        return {
            "experiment_id": self.config_template.experiment_id,
            "n_runs": len(results),
            "model": self.config_template.model,
            "harness_components": self.config_template.harness.enabled_components(),
            "rsucc_r": {
                "value": rsucc.value,
                "ci_lower": rsucc.ci_lower,
                "ci_upper": rsucc.ci_upper,
                "n": rsucc.n,
            },
            "ttff": ttff_dist,
            "hor_mean": float(sum(hor_values) / len(hor_values)) if hor_values else None,
            "verdicts": {
                "success": sum(1 for r in results if r.final_verdict == "success"),
                "partial": sum(1 for r in results if r.final_verdict == "partial"),
                "failure": sum(1 for r in results if r.final_verdict == "failure"),
            },
            "failure_types": _count_failure_types(results),
        }


# ── 유틸리티 ──────────────────────────────────────────────────────────────────

def _is_task_complete(output: str, task_type: TaskType) -> bool:
    """agent 출력에서 task 완료 신호 감지."""
    completion_signals = {
        "T1_code_review": lambda o: ("```json" in o or "[{" in o or "[]" in o),
        "T2_multi_step":  lambda o: ("step" in o.lower() and "[" in o),
        "T3_long_horizon": lambda o: ("TASK COMPLETE" in o or "all changes applied" in o.lower()),
        "T4_synthesis":   lambda o: len(o.strip()) > 100,
    }
    fn = completion_signals.get(task_type)
    return fn(output) if fn else len(output) > 50


def _count_failure_types(results: list[RunLog]) -> dict:
    counts: dict[str, int] = {}
    for r in results:
        ft = r.failure_type or "none"
        counts[ft] = counts.get(ft, 0) + 1
    return counts
