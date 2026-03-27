"""
Harness — Agent Operational Envelope

design-specification.md §1, figure_expansion.md Figure 2, 8, 10 참조.

6개 컴포넌트 (HarnessConfig로 ablation 제어):
  1. monitoring_hooks       — step마다 state 관찰
  2. recovery_mechanism     — retry + rollback
  3. context_boundary       — context isolation
  4. budget_enforcement     — token budget 추적
  5. goal_guardian          — goal drift 감지 + re-injection
  6. trust_engine           — confidence 기반 accept/verify/reject

Figure 10 Ablation: 각 컴포넌트를 독립적으로 제거하여 RSuccR 기여도 측정.
Figure 9 ROC:  harness_score (failure probability)를 각 step에서 계산.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable, Optional

import numpy as np

from .config import HarnessConfig, StepLog


# ── Harness 상태 ───────────────────────────────────────────────────────────────

@dataclass
class HarnessState:
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    step_count: int = 0
    failure_count: int = 0
    retry_count: int = 0
    last_goal_injection_step: int = 0
    goal_fidelity_history: list[tuple[int, float]] = field(default_factory=list)
    checkpoints: list[dict] = field(default_factory=list)   # rollback용
    alert_log: list[dict] = field(default_factory=list)

    @property
    def token_budget_used(self) -> int:
        return self.total_input_tokens + self.total_output_tokens

    def record_checkpoint(self, step: int, context_snapshot: dict) -> None:
        self.checkpoints.append({"step": step, "context": context_snapshot})

    def get_last_stable_checkpoint(self) -> Optional[dict]:
        return self.checkpoints[-1] if self.checkpoints else None


# ── Harness 경보 타입 ──────────────────────────────────────────────────────────

class AlertType:
    BUDGET_WARNING    = "budget_warning"      # 80% 소진
    BUDGET_CRITICAL   = "budget_critical"     # 95% 소진
    GOAL_DRIFT        = "goal_drift"          # GFS < 0.90
    GOAL_DIVERGE      = "goal_divergence"     # GFS < 0.70 → rollback
    FORMAT_ERROR      = "format_error"        # 출력 형식 불일치
    TOOL_FAILURE      = "tool_failure"        # tool call 실패
    CONTEXT_OVERFLOW  = "context_overflow"    # context window 한계 접근
    CONFIDENCE_LOW    = "confidence_low"      # trust engine: 신뢰도 부족


# ── Harness ───────────────────────────────────────────────────────────────────

class Harness:
    """
    Agent의 operational envelope.

    사용법:
        harness = Harness(config, initial_goal, embedding_fn)
        for step_output in agent.run():
            action = harness.observe(step_output)
            if action == "rollback":
                agent.rollback(harness.state.get_last_stable_checkpoint())
            elif action == "reinjection":
                agent.inject_goal(initial_goal)
    """

    def __init__(
        self,
        config: HarnessConfig,
        initial_goal: str = "",
        embedding_fn: Optional[Callable[[str], np.ndarray]] = None,
        token_budget: Optional[int] = None,
    ):
        self.config = config
        self.initial_goal = initial_goal
        self.embedding_fn = embedding_fn
        self.token_budget = token_budget or config.token_budget
        self.state = HarnessState()

        self._initial_goal_embedding: Optional[np.ndarray] = None
        if embedding_fn and initial_goal and config.goal_guardian:
            self._initial_goal_embedding = embedding_fn(initial_goal)

    # ── 메인 observe 메서드 ────────────────────────────────────────────────────

    def observe(
        self,
        step_number: int,
        agent_output: str,
        input_tokens: int,
        output_tokens: int,
        tool_called: Optional[str] = None,
        tool_success: Optional[bool] = None,
        agent_confidence: Optional[float] = None,
        goal_statement: Optional[str] = None,
        context_snapshot: Optional[dict] = None,
    ) -> StepLog:
        """
        step 하나를 관찰하고 harness action을 결정한다.
        모든 컴포넌트가 이 메서드에서 순서대로 실행된다.

        반환: StepLog (harness_alert, harness_action 포함)
        """
        self.state.step_count += 1
        alert: Optional[str] = None
        action: Optional[str] = None

        # 1. Token budget enforcement
        if self.config.budget_enforcement:
            alert, action = self._check_budget(
                input_tokens, output_tokens, alert, action
            )

        # 2. Monitoring hooks — tool failure, format error
        if self.config.monitoring_hooks:
            alert, action = self._check_output_quality(
                agent_output, tool_called, tool_success, alert, action
            )

        # 3. Goal guardian — drift detection
        if self.config.goal_guardian and goal_statement:
            gfs = self._compute_goal_fidelity(step_number, goal_statement)
            if gfs is not None:
                self.state.goal_fidelity_history.append((step_number, gfs))
                alert, action = self._check_goal_drift(step_number, gfs, alert, action)

        # 4. Trust engine — confidence-based decision
        if self.config.trust_engine and agent_confidence is not None:
            alert, action = self._check_trust(agent_confidence, alert, action)

        # 5. Context boundary — checkpoint at stable steps
        if self.config.context_boundary and alert is None and context_snapshot:
            if step_number % self.config.monitoring_interval_steps == 0:
                self.state.record_checkpoint(step_number, context_snapshot)

        # 6. Recovery — retry/rollback 결정
        if self.config.recovery_mechanism and action is None and alert is not None:
            action = self._decide_recovery(alert)

        # 상태 업데이트
        self.state.total_input_tokens += input_tokens
        self.state.total_output_tokens += output_tokens
        if alert:
            self.state.alert_log.append({
                "step": step_number,
                "alert": alert,
                "action": action,
            })
            if action in ("retry", "rollback"):
                self.state.failure_count += 1

        return StepLog(
            step_number=step_number,
            timestamp_ms=int(time.time() * 1000),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            tool_called=tool_called,
            tool_success=tool_success,
            agent_output=agent_output,
            goal_statement=goal_statement,
            harness_alert=alert,
            harness_action=action,
        )

    # ── harness_score (Figure 9 ROC용) ────────────────────────────────────────

    def compute_failure_probability(
        self,
        agent_output: str,
        input_tokens: int,
        output_tokens: int,
        agent_confidence: Optional[float] = None,
        goal_statement: Optional[str] = None,
    ) -> float:
        """
        이 step이 failure일 확률 [0, 1].
        Figure 9 ROC curve의 score 입력.

        개별 신호들을 logistic combination으로 합산.
        """
        signals: list[float] = []

        if self.config.budget_enforcement:
            used = self.state.token_budget_used + input_tokens + output_tokens
            budget_ratio = used / self.token_budget
            signals.append(_sigmoid(budget_ratio - 0.85, k=20))  # 85% 이상이면 위험

        if self.config.monitoring_hooks:
            format_ok = len(agent_output.strip()) > 10
            signals.append(0.0 if format_ok else 0.8)

        if self.config.goal_guardian and goal_statement and self._initial_goal_embedding is not None:
            gfs = self._compute_goal_fidelity(self.state.step_count, goal_statement)
            if gfs is not None:
                signals.append(_sigmoid(0.85 - gfs, k=15))  # GFS < 0.85이면 위험

        if self.config.trust_engine and agent_confidence is not None:
            signals.append(_sigmoid(0.50 - agent_confidence, k=10))  # confidence < 0.5이면 위험

        return float(np.mean(signals)) if signals else 0.0

    # ── 컴포넌트별 내부 메서드 ─────────────────────────────────────────────────

    def _check_budget(
        self, input_tokens: int, output_tokens: int,
        alert: Optional[str], action: Optional[str]
    ) -> tuple[Optional[str], Optional[str]]:
        used = self.state.token_budget_used + input_tokens + output_tokens
        ratio = used / self.token_budget
        if ratio >= 0.95:
            return AlertType.BUDGET_CRITICAL, "graceful_stop"
        if ratio >= self.config.budget_alert_threshold:
            return AlertType.BUDGET_WARNING, action  # 경고만, action은 유지
        return alert, action

    def _check_output_quality(
        self, output: str, tool: Optional[str], tool_ok: Optional[bool],
        alert: Optional[str], action: Optional[str]
    ) -> tuple[Optional[str], Optional[str]]:
        if tool is not None and tool_ok is False:
            return AlertType.TOOL_FAILURE, action
        if not output or len(output.strip()) < 5:
            return AlertType.FORMAT_ERROR, action
        return alert, action

    def _check_goal_drift(
        self, step: int, gfs: float,
        alert: Optional[str], action: Optional[str]
    ) -> tuple[Optional[str], Optional[str]]:
        if gfs < self.config.goal_fidelity_rollback:
            return AlertType.GOAL_DIVERGE, "rollback"
        if gfs < self.config.goal_fidelity_reinjection:
            if step - self.state.last_goal_injection_step > 5:
                self.state.last_goal_injection_step = step
                return AlertType.GOAL_DRIFT, "goal_reinjection"
        return alert, action

    def _check_trust(
        self, confidence: float,
        alert: Optional[str], action: Optional[str]
    ) -> tuple[Optional[str], Optional[str]]:
        if confidence < 0.40:
            return AlertType.CONFIDENCE_LOW, "escalate_verification"
        return alert, action

    def _decide_recovery(self, alert: str) -> str:
        if alert in (AlertType.TOOL_FAILURE, AlertType.FORMAT_ERROR):
            if self.state.retry_count < self.config.max_retries:
                self.state.retry_count += 1
                return "retry"
            return "rollback"
        if alert == AlertType.GOAL_DIVERGE:
            return "rollback"
        return "none"

    def _compute_goal_fidelity(
        self, step: int, goal_statement: str
    ) -> Optional[float]:
        if self._initial_goal_embedding is None or self.embedding_fn is None:
            return None
        current_emb = self.embedding_fn(goal_statement)
        norm_i = np.linalg.norm(self._initial_goal_embedding)
        norm_c = np.linalg.norm(current_emb)
        if norm_i == 0 or norm_c == 0:
            return None
        return float(
            np.dot(self._initial_goal_embedding, current_emb) / (norm_i * norm_c)
        )

    # ── Summary (실험 로그 생성용) ─────────────────────────────────────────────

    def summary(self) -> dict:
        return {
            "enabled_components": self.config.enabled_components(),
            "total_steps": self.state.step_count,
            "total_tokens": self.state.token_budget_used,
            "token_budget": self.token_budget,
            "budget_utilization": self.state.token_budget_used / self.token_budget,
            "failure_count": self.state.failure_count,
            "retry_count": self.state.retry_count,
            "alerts": len(self.state.alert_log),
            "alert_breakdown": _count_alerts(self.state.alert_log),
            "goal_fidelity_final": (
                self.state.goal_fidelity_history[-1][1]
                if self.state.goal_fidelity_history else None
            ),
        }


# ── 유틸리티 ──────────────────────────────────────────────────────────────────

def _sigmoid(x: float, k: float = 10.0) -> float:
    return 1.0 / (1.0 + np.exp(-k * x))


def _count_alerts(alert_log: list[dict]) -> dict:
    counts: dict[str, int] = {}
    for entry in alert_log:
        alert = entry.get("alert", "unknown")
        counts[alert] = counts.get(alert, 0) + 1
    return counts
