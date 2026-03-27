"""
Agent Runner — OpenRouter 기반 실험 실행기

각 실험 trial을 실행하고 RunLog를 생성한다.
Harness를 on/off 조건 모두에서 동일 구조로 실행.

OpenRouter는 OpenAI-compatible API를 제공.
base_url = "https://openrouter.ai/api/v1"
OPENROUTER_API_KEY 환경변수 필요.

tool calling:
  T1 → submit_bug_report(bugs: list)
  T2 → submit_plan(steps: list)
  T4 → submit_answer(answer: str, citations: list)
  T3 → read_file(path), edit_file(path, old, new), run_tests(path)
  TCA (Tool Call Accuracy)는 tool_calls_attempted / tool_calls_valid_output으로 측정.

IFRTracker: 5개 명시 instruction의 준수 여부 자동 판정.
  ARCC 계산 시 compute_ifr(tracker.compliance_log)로 입력.

design-specification.md §1.2 (task 배정), §4 (power analysis에 따른 run 수) 참조.
"""
from __future__ import annotations

import copy
import json
import os
import re
import shlex
import subprocess
import time
from pathlib import Path
from typing import Callable, Optional

from openai import OpenAI, APIError

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

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


# ── Tool Definitions (OpenAI function calling 형식) ────────────────────────────

TOOL_DEFINITIONS: dict[TaskType, list[dict]] = {
    "T1_code_review": [
        {
            "type": "function",
            "function": {
                "name": "submit_bug_report",
                "description": "Submit the complete list of identified bugs.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "bugs": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "line_number": {"type": "integer"},
                                    "bug_type": {"type": "string"},
                                    "severity": {
                                        "type": "string",
                                        "enum": ["low", "medium", "high", "critical"],
                                    },
                                    "fix_suggestion": {"type": "string"},
                                },
                                "required": ["line_number", "bug_type", "severity"],
                            },
                        }
                    },
                    "required": ["bugs"],
                },
            },
        }
    ],
    "T2_multi_step": [
        {
            "type": "function",
            "function": {
                "name": "submit_plan",
                "description": "Submit the complete execution plan.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "steps": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "step":      {"type": "integer"},
                                    "action":    {"type": "string"},
                                    "rationale": {"type": "string"},
                                },
                                "required": ["step", "action"],
                            },
                        }
                    },
                    "required": ["steps"],
                },
            },
        }
    ],
    "T3_long_horizon": [
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read the contents of a file.",
                "parameters": {
                    "type": "object",
                    "properties": {"path": {"type": "string"}},
                    "required": ["path"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "edit_file",
                "description": "Replace old_content with new_content in a file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path":        {"type": "string"},
                        "old_content": {"type": "string"},
                        "new_content": {"type": "string"},
                    },
                    "required": ["path", "old_content", "new_content"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "run_tests",
                "description": "Run the test suite and return pass/fail counts.",
                "parameters": {
                    "type": "object",
                    "properties": {"test_path": {"type": "string"}},
                    "required": ["test_path"],
                },
            },
        },
    ],
    "T4_synthesis": [
        {
            "type": "function",
            "function": {
                "name": "submit_answer",
                "description": "Submit the final synthesized answer with citations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "answer":    {"type": "string"},
                        "citations": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "e.g. ['Doc 1', 'Doc 3']",
                        },
                    },
                    "required": ["answer"],
                },
            },
        }
    ],
}

_IFR_INSTRUCTION_TEXT: dict[TaskType, list[str]] = {
    "T1_code_review": [
        "output JSON",
        "include line_number",
        "include severity",
        "include bug_type",
        "include fix_suggestion",
    ],
    "T2_multi_step": [
        "output JSON",
        "include step number",
        "include action",
        "include rationale",
        "respect constraint order",
    ],
    "T3_long_horizon": [
        "use one tool per step",
        "checkpoint every 10 steps",
        "state current goal",
        "output TASK COMPLETE",
        "stay on task",
    ],
    "T4_synthesis": [
        "use only doc info",
        "cite document number",
        "answer the question",
        "no contradictions",
        "submit answer",
    ],
}


# ── IFR Tracker ────────────────────────────────────────────────────────────────

class IFRTracker:
    """
    5개 명시 instruction에 대한 준수 여부를 자동 판정.
    ARCC §2.1 IFR 계산을 위한 데이터 수집기.

    사용:
        tracker = IFRTracker(task_type)
        tracker.check(agent_output)          # 매 step에서 호출
        ifr = compute_ifr(tracker.compliance_log)
    """

    def __init__(self, task_type: TaskType):
        self.task_type = task_type
        self._instructions = _IFR_INSTRUCTION_TEXT.get(task_type, [])
        self.compliance_log: list[dict] = []

    def check(
        self,
        agent_output: str,
        *,
        step_number: Optional[int] = None,
        tool_calls: Optional[list[str]] = None,
        task_complete: bool = False,
        ground_truth: Optional[dict] = None,
    ) -> None:
        """agent_output과 step metadata에 대해 instruction 준수 여부를 판정하고 기록."""
        tool_calls = tool_calls or []
        parsed = _try_extract_json(agent_output)

        if self.task_type == "T1_code_review":
            results = self._check_t1(parsed, tool_calls)
        elif self.task_type == "T2_multi_step":
            results = self._check_t2(parsed, tool_calls, ground_truth)
        elif self.task_type == "T3_long_horizon":
            results = self._check_t3(agent_output, step_number, tool_calls, task_complete)
        elif self.task_type == "T4_synthesis":
            results = self._check_t4(agent_output, parsed, tool_calls, ground_truth)
        else:
            results = []

        self.compliance_log.extend(results)

    def latest_compliance(self) -> list[dict]:
        """마지막 check() 호출의 결과만 반환 (step별 최신 상태)."""
        n = len(self._instructions)
        return self.compliance_log[-n:] if len(self.compliance_log) >= n else self.compliance_log

    def _check_t1(self, parsed: object, tool_calls: list[str]) -> list[dict]:
        report = _extract_report_items(parsed, "bugs")
        return [
            _ifr_entry("output JSON", parsed is not None or "submit_bug_report" in tool_calls),
            _ifr_entry("include line_number", bool(report) and all(isinstance(b.get("line_number"), int) for b in report)),
            _ifr_entry(
                "include severity",
                bool(report) and all(b.get("severity") in {"low", "medium", "high", "critical"} for b in report),
            ),
            _ifr_entry("include bug_type", bool(report) and all(bool(b.get("bug_type")) for b in report)),
            _ifr_entry("include fix_suggestion", bool(report) and all(bool(b.get("fix_suggestion")) for b in report)),
        ]

    def _check_t2(
        self,
        parsed: object,
        tool_calls: list[str],
        ground_truth: Optional[dict],
    ) -> list[dict]:
        steps = _extract_report_items(parsed, "steps")
        valid_plan = bool(steps) and all(
            isinstance(item.get("step"), int) and bool(item.get("action"))
            for item in steps
        )
        order_ok = False
        if valid_plan and ground_truth:
            constraints = _ground_truth_field(ground_truth, "constraints", ground_truth)
            required_actions = _ground_truth_field(ground_truth, "required_actions", [])
            optional_actions = _ground_truth_field(ground_truth, "optional_actions", [])
            if isinstance(constraints, list):
                constraints = {
                    "constraints": constraints,
                    "required_actions": required_actions,
                    "optional_actions": optional_actions,
                }
            verdict = validate_t2(json.dumps({"steps": steps}), constraints)
            order_ok = verdict.verdict == "pass"
        return [
            _ifr_entry("output JSON", parsed is not None or "submit_plan" in tool_calls),
            _ifr_entry("include step number", bool(steps) and all(isinstance(item.get("step"), int) for item in steps)),
            _ifr_entry("include action", bool(steps) and all(bool(item.get("action")) for item in steps)),
            _ifr_entry("include rationale", bool(steps) and all(bool(item.get("rationale")) for item in steps)),
            _ifr_entry("respect constraint order", order_ok, applicable=ground_truth is not None),
        ]

    def _check_t3(
        self,
        agent_output: str,
        step_number: Optional[int],
        tool_calls: list[str],
        task_complete: bool,
    ) -> list[dict]:
        checkpoint_step = step_number is not None and step_number % 10 == 0
        has_goal = "CURRENT GOAL:" in agent_output
        has_completion = "TASK COMPLETE" in agent_output
        active_step = not task_complete
        return [
            _ifr_entry(
                "use one tool per step",
                len(tool_calls) == 1 if active_step else (len(tool_calls) == 0 and has_completion),
            ),
            _ifr_entry("checkpoint every 10 steps", has_goal, applicable=checkpoint_step),
            _ifr_entry("state current goal", has_goal, applicable=checkpoint_step),
            _ifr_entry("output TASK COMPLETE", has_completion, applicable=task_complete),
            _ifr_entry("stay on task", bool(tool_calls) or has_goal or has_completion),
        ]

    def _check_t4(
        self,
        agent_output: str,
        parsed: object,
        tool_calls: list[str],
        ground_truth: Optional[dict],
    ) -> list[dict]:
        answer = _extract_answer_text(parsed, agent_output)
        citations = _extract_citations(parsed, answer)
        misleading_claims = _ground_truth_field(ground_truth, "misleading_claims", []) if ground_truth else []
        has_misleading = any(claim.lower() in answer.lower() for claim in misleading_claims)
        return [
            _ifr_entry("use only doc info", bool(answer.strip()) and not has_misleading, applicable=ground_truth is not None),
            _ifr_entry("cite document number", bool(citations)),
            _ifr_entry("answer the question", len(answer.strip()) >= 80),
            _ifr_entry("no contradictions", not has_misleading, applicable=ground_truth is not None),
            _ifr_entry("submit answer", "submit_answer" in tool_calls or bool(answer.strip())),
        ]


def _ifr_entry(instruction: str, complied: bool, *, applicable: bool = True) -> dict:
    return {
        "instruction": instruction,
        "complied": bool(complied),
        "applicable": applicable,
    }


def _try_extract_json(text: str) -> object | None:
    for pattern in (r"```(?:json)?\s*([\s\S]+?)```", r"(\[[\s\S]+\])", r"(\{[\s\S]+\})"):
        match = re.search(pattern, text)
        if not match:
            continue
        block = match.group(1).strip() if match.lastindex else match.group(0).strip()
        try:
            return json.loads(block)
        except json.JSONDecodeError:
            continue
    return None


def _extract_report_items(parsed: object, key: str) -> list[dict]:
    if isinstance(parsed, list):
        return [item for item in parsed if isinstance(item, dict)]
    if isinstance(parsed, dict):
        value = parsed.get(key, parsed.get("results", []))
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def _extract_answer_text(parsed: object, fallback: str) -> str:
    if isinstance(parsed, dict) and isinstance(parsed.get("answer"), str):
        return parsed["answer"]
    return fallback


def _extract_citations(parsed: object, answer: str) -> list[str]:
    if isinstance(parsed, dict) and isinstance(parsed.get("citations"), list):
        return [str(item) for item in parsed["citations"] if str(item).strip()]
    return re.findall(r"\[Doc(?:ument)?\s+\d+\]", answer, flags=re.IGNORECASE)


def _ground_truth_field(ground_truth: object, name: str, default=None):
    if isinstance(ground_truth, dict):
        return ground_truth.get(name, default)
    return getattr(ground_truth, name, default)


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
        self.client = OpenAI(
            api_key=api_key or os.environ.get("OPENROUTER_API_KEY", ""),
            base_url=OPENROUTER_BASE_URL,
            timeout=120.0,
        )
        self.run_log = RunLog(config=config)
        self.ifr_tracker = IFRTracker(config.task.task_type)
        self._tool_call_log: list[dict] = []   # TCA 계산용

    def _resolve_repo_root(self, ground_truth: Optional[dict]) -> Path:
        repo_path = _ground_truth_field(ground_truth, "repo_path")
        if repo_path:
            return Path(str(repo_path)).resolve()
        return Path.cwd().resolve()

    def _resolve_safe_path(self, repo_root: Path, requested_path: str) -> Path:
        candidate = Path(requested_path)
        path = candidate.resolve() if candidate.is_absolute() else (repo_root / candidate).resolve()
        if path != repo_root and repo_root not in path.parents:
            raise ValueError(f"path escapes repo root: {requested_path}")
        return path

    def _tool_call_to_message(self, tool_call) -> dict:
        return {
            "id": tool_call.id,
            "type": "function",
            "function": {
                "name": tool_call.function.name,
                "arguments": tool_call.function.arguments,
            },
        }

    def _validate_submission_tool(
        self,
        tool_name: str,
        args: dict,
        ground_truth: Optional[dict],
    ) -> tuple[bool, str]:
        if tool_name == "submit_bug_report":
            bugs = args.get("bugs")
            schema_ok = (
                isinstance(bugs, list) and bugs and all(
                    isinstance(item, dict)
                    and isinstance(item.get("line_number"), int)
                    and item.get("severity") in {"low", "medium", "high", "critical"}
                    and bool(item.get("bug_type"))
                    and bool(item.get("fix_suggestion"))
                    for item in bugs
                )
            )
            if not schema_ok:
                return False, "invalid bug report schema"
            if ground_truth:
                result = validate_t1(json.dumps({"bugs": bugs}), ground_truth)
                return result.verdict == "pass", f"T1 validation={result.verdict} score={result.score:.3f}"
            return True, "bug report schema valid"

        if tool_name == "submit_plan":
            steps = args.get("steps")
            schema_ok = (
                isinstance(steps, list) and steps and all(
                    isinstance(item, dict)
                    and isinstance(item.get("step"), int)
                    and bool(item.get("action"))
                    and bool(item.get("rationale"))
                    for item in steps
                )
            )
            if not schema_ok:
                return False, "invalid plan schema"
            if ground_truth:
                constraints = _ground_truth_field(ground_truth, "constraints", ground_truth)
                required_actions = _ground_truth_field(ground_truth, "required_actions", [])
                optional_actions = _ground_truth_field(ground_truth, "optional_actions", [])
                if isinstance(constraints, list):
                    constraints = {
                        "constraints": constraints,
                        "required_actions": required_actions,
                        "optional_actions": optional_actions,
                    }
                result = validate_t2(json.dumps({"steps": steps}), constraints)
                return result.verdict == "pass", f"T2 validation={result.verdict} score={result.score:.3f}"
            return True, "plan schema valid"

        if tool_name == "submit_answer":
            answer = args.get("answer", "")
            citations = args.get("citations", [])
            schema_ok = isinstance(answer, str) and bool(answer.strip()) and isinstance(citations, list)
            if not schema_ok:
                return False, "invalid synthesis schema"
            has_doc_citations = bool(citations) or bool(re.findall(r"\[Doc(?:ument)?\s+\d+\]", answer, flags=re.IGNORECASE))
            if not has_doc_citations:
                return False, "missing document citations"
            if ground_truth:
                result = validate_t4(
                    answer,
                    _ground_truth_field(ground_truth, "key_facts", []),
                    _ground_truth_field(ground_truth, "misleading_claims", []),
                )
                return result.verdict == "pass", f"T4 validation={result.verdict} score={result.score:.3f}"
            return True, "answer schema valid"

        return False, f"unknown submission tool: {tool_name}"

    def _execute_local_tool(
        self,
        tool_name: str,
        args: dict,
        repo_root: Path,
        ground_truth: Optional[dict],
    ) -> tuple[bool, str]:
        if tool_name == "read_file":
            path = self._resolve_safe_path(repo_root, str(args["path"]))
            if not path.is_file():
                raise FileNotFoundError(f"not a file: {path}")
            content = path.read_text(encoding="utf-8")
            return True, json.dumps(
                {"ok": True, "path": str(path), "content": content},
                ensure_ascii=False,
            )

        if tool_name == "edit_file":
            path = self._resolve_safe_path(repo_root, str(args["path"]))
            if not path.is_file():
                raise FileNotFoundError(f"not a file: {path}")
            old_content = str(args["old_content"])
            new_content = str(args["new_content"])
            original = path.read_text(encoding="utf-8")
            occurrences = original.count(old_content)
            if occurrences != 1:
                raise ValueError(f"expected exactly one match for edit, found {occurrences}")
            updated = original.replace(old_content, new_content, 1)
            path.write_text(updated, encoding="utf-8")
            return True, json.dumps(
                {"ok": True, "path": str(path), "replacements": 1},
                ensure_ascii=False,
            )

        if tool_name == "run_tests":
            test_path = self._resolve_safe_path(repo_root, str(args["test_path"]))
            test_command = str(_ground_truth_field(ground_truth, "test_command", "pytest"))
            cwd = test_path if test_path.is_dir() else test_path.parent
            result = subprocess.run(
                shlex.split(test_command),
                cwd=str(cwd),
                capture_output=True,
                text=True,
                timeout=120,
            )
            output = (result.stdout + result.stderr)[-2000:]
            return result.returncode == 0, json.dumps(
                {
                    "ok": result.returncode == 0,
                    "cwd": str(cwd),
                    "returncode": result.returncode,
                    "output_tail": output,
                },
                ensure_ascii=False,
            )

        raise ValueError(f"unknown local tool: {tool_name}")

    def _handle_tool_call(
        self,
        tool_call,
        repo_root: Path,
        ground_truth: Optional[dict],
    ) -> tuple[bool, str, dict]:
        args = json.loads(tool_call.function.arguments)
        tool_name = tool_call.function.name
        if self.config.task.task_type == "T3_long_horizon":
            success, result_text = self._execute_local_tool(tool_name, args, repo_root, ground_truth)
        else:
            success, result_text = self._validate_submission_tool(tool_name, args, ground_truth)
        tool_message = {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result_text,
        }
        return success, result_text, tool_message

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
        repo_root = self._resolve_repo_root(ground_truth)

        while step < self.config.task.max_steps:
            step += 1

            # ── API call (tool calling 포함) ──────────────────────────────────
            tools = TOOL_DEFINITIONS.get(self.config.task.task_type, [])
            try:
                openai_messages = [{"role": "system", "content": system}] + messages
                call_kwargs: dict = dict(
                    model=self.config.model,
                    messages=openai_messages,
                )
                # OpenRouter routing for certain OpenAI-family models expects
                # max_output_tokens instead of max_tokens.
                if self.config.model.startswith("openai/gpt-5.4"):
                    call_kwargs["extra_body"] = {"max_output_tokens": max_tokens_per_step}
                else:
                    call_kwargs["max_tokens"] = max_tokens_per_step
                if tools:
                    call_kwargs["tools"] = tools
                    call_kwargs["tool_choice"] = "auto"
                response = self.client.chat.completions.create(timeout=60.0, **call_kwargs)
            except APIError as e:
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

            msg = response.choices[0].message
            content = msg.content or ""
            input_tok = response.usage.prompt_tokens
            output_tok = response.usage.completion_tokens
            self.run_log.total_input_tokens += input_tok
            self.run_log.total_output_tokens += output_tok

            # ── Tool call 처리 (실행 + TCA 기록 + tool state 반영) ─────────────
            tool_called_name: Optional[str] = None
            tool_success: Optional[bool] = None
            candidate_messages: list[dict]
            tool_names: list[str] = []
            tool_feedback: list[str] = []
            assistant_message: dict = {"role": "assistant", "content": content}

            if msg.tool_calls:
                assistant_message = {
                    "role": "assistant",
                    "content": content or "",
                    "tool_calls": [self._tool_call_to_message(tc) for tc in msg.tool_calls],
                }
                tool_messages: list[dict] = []
                tool_successes: list[bool] = []
                for tc in msg.tool_calls:
                    try:
                        success, result_text, tool_message = self._handle_tool_call(tc, repo_root, ground_truth)
                    except Exception as exc:
                        success = False
                        result_text = json.dumps(
                            {
                                "ok": False,
                                "tool": tc.function.name,
                                "error": str(exc),
                            },
                            ensure_ascii=False,
                        )
                        tool_message = {
                            "role": "tool",
                            "tool_call_id": tc.id,
                            "content": result_text,
                        }
                    tool_names.append(tc.function.name)
                    tool_successes.append(success)
                    tool_messages.append(tool_message)
                    tool_feedback.append(f"{tc.function.name}: {result_text}")
                    self._tool_call_log.append(
                        {"called": True, "success": success, "tool": tc.function.name}
                    )

                tool_called_name = ",".join(tool_names)
                tool_success = all(tool_successes)
                content = "\n".join(([content] if content else []) + tool_feedback)
                candidate_messages = messages + [assistant_message] + tool_messages
            else:
                candidate_messages = messages + [{"role": "assistant", "content": content}, {"role": "user", "content": "[Continue]"}]

            # ── Agent confidence 추출 (trust engine 입력) ─────────────────────
            agent_confidence: Optional[float] = None
            for line in content.splitlines():
                if line.upper().startswith("CONFIDENCE:"):
                    try:
                        agent_confidence = float(line.split(":", 1)[1].strip())
                    except ValueError:
                        pass

            task_complete = _is_task_complete(content, self.config.task.task_type)

            # ── IFR 판정 ──────────────────────────────────────────────────────
            self.ifr_tracker.check(
                content,
                step_number=step,
                tool_calls=tool_names,
                task_complete=task_complete,
                ground_truth=ground_truth,
            )

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
                tool_called=tool_called_name,
                tool_success=tool_success,
                agent_confidence=agent_confidence,
                goal_statement=goal_stmt,
                context_snapshot={"messages": copy.deepcopy(candidate_messages)},
            )

            # ── Ground truth Layer 1 판정 (있을 경우) ─────────────────────────
            if ground_truth and self.validator_fn and not msg.tool_calls:
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

            if action == "escalate_verification":
                messages = candidate_messages + [{
                    "role": "user",
                    "content": (
                        "[HARNESS] Low confidence detected. Verify the previous step against "
                        "the task constraints, correct any mistakes, and restate your answer "
                        "with an explicit CONFIDENCE: <0.0-1.0> line."
                    ),
                }]
                continue

            if action == "goal_reinjection":
                candidate_messages = candidate_messages + [{
                    "role": "user",
                    "content": f"[HARNESS] Reminder — your original goal: {initial_goal}",
                }]

            # ── 정상 진행: 다음 step ──────────────────────────────────────────
            messages = candidate_messages

            # submit_* tool call은 성공적으로 검증되면 task 완료로 본다.
            if msg.tool_calls and tool_success and self.config.task.task_type in (
                "T1_code_review",
                "T2_multi_step",
                "T4_synthesis",
            ):
                self.run_log.final_verdict = "success"
                break

            # T3 tool step은 tool state를 반영한 뒤 다음 턴으로 바로 진행한다.
            if msg.tool_calls:
                continue

            # ── Task 완료 감지 ─────────────────────────────────────────────────
            if task_complete:
                self.run_log.final_verdict = "success"
                break

        # ── Run 마무리 ────────────────────────────────────────────────────────
        self.run_log.tool_call_log = list(self._tool_call_log)
        self.run_log.instruction_compliance = list(self.ifr_tracker.compliance_log)
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
        from .arcc import compute_tca, compute_ifr

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
