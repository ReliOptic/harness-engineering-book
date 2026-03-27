"""
실험 설정 dataclass 모음.
HarnessConfig: ablation 제어용 컴포넌트 on/off
ExperimentConfig: 실험 조건 명세
"""
from dataclasses import dataclass, field
from typing import Literal, Optional


# ── Harness Component Configuration (Figure 10 ablation 제어) ──────────────

@dataclass
class HarnessConfig:
    """
    harness의 각 컴포넌트를 독립적으로 on/off.
    Figure 10 Ablation Waterfall을 위해 단일 컴포넌트씩 제거 가능.
    """
    monitoring_hooks: bool = True       # state observation (token, output format, goal)
    recovery_mechanism: bool = True     # retry + rollback
    context_boundary: bool = True       # context isolation
    budget_enforcement: bool = True     # token budget limit
    goal_guardian: bool = True          # goal re-injection on drift
    trust_engine: bool = True           # confidence-based accept/verify/reject

    # 수치 파라미터
    token_budget: int = 100_000         # 전체 budget (tokens)
    budget_alert_threshold: float = 0.80  # 80% 소진 시 경고
    goal_fidelity_reinjection: float = 0.90  # GFS < 0.90이면 goal re-inject
    goal_fidelity_rollback: float = 0.70    # GFS < 0.70이면 rollback
    monitoring_interval_steps: int = 5     # N step마다 state 점검
    max_retries: int = 3                    # failure 시 최대 재시도 횟수

    def enabled_components(self) -> list[str]:
        return [
            name for name, val in {
                "monitoring_hooks": self.monitoring_hooks,
                "recovery_mechanism": self.recovery_mechanism,
                "context_boundary": self.context_boundary,
                "budget_enforcement": self.budget_enforcement,
                "goal_guardian": self.goal_guardian,
                "trust_engine": self.trust_engine,
            }.items() if val
        ]

    @classmethod
    def full(cls) -> "HarnessConfig":
        """모든 컴포넌트 on (Figure 8 Pareto baseline)"""
        return cls()

    @classmethod
    def none(cls) -> "HarnessConfig":
        """모든 컴포넌트 off (harness-off baseline, E04 통제 조건)"""
        return cls(
            monitoring_hooks=False,
            recovery_mechanism=False,
            context_boundary=False,
            budget_enforcement=False,
            goal_guardian=False,
            trust_engine=False,
        )

    @classmethod
    def monitoring_only(cls) -> "HarnessConfig":
        """Figure 9: monitoring hooks만 활성화"""
        return cls(
            monitoring_hooks=True,
            recovery_mechanism=False,
            context_boundary=False,
            budget_enforcement=False,
            goal_guardian=False,
            trust_engine=False,
        )

    @classmethod
    def budget_only(cls) -> "HarnessConfig":
        """Figure 9: budget enforcement만 활성화"""
        return cls(
            monitoring_hooks=False,
            recovery_mechanism=False,
            context_boundary=False,
            budget_enforcement=True,
            goal_guardian=False,
            trust_engine=False,
        )


# ── Task Configuration ──────────────────────────────────────────────────────

TaskType = Literal["T1_code_review", "T2_multi_step", "T3_long_horizon", "T4_synthesis"]
Difficulty = Literal["EASY", "MODERATE", "FRONTIER"]
SurfaceType = Literal["CLI", "REST_API", "SDK_wrapper", "Chat_UI"]
ModelTier = Literal["SOTA", "MID", "SMALL"]


@dataclass
class TaskConfig:
    task_type: TaskType
    difficulty: Difficulty
    max_steps: int          # T3: 40, T1/T2: 20, T4: 10
    token_budget: int       # 이 task에 허용된 총 token
    seed: int = 42          # 재현성


@dataclass
class ExperimentConfig:
    """
    단일 실험 trial의 완전한 명세.
    이 객체 하나 = scenario-master.md의 실험 조건 하나.
    """
    experiment_id: str              # E04, E08 등
    run_id: int                     # 동일 조건 반복 실행 번호 (1~N)
    model: str                      # anthropic model id
    harness: HarnessConfig
    task: TaskConfig
    surface: SurfaceType = "CLI"
    token_budget_ratio: float = 1.0  # E08용: 1.0=100%, 0.75=75%, etc.
    agent_count: int = 1             # E11용: multi-agent 수
    notes: str = ""


# ── Step Log ────────────────────────────────────────────────────────────────

@dataclass
class StepLog:
    """
    agent 실행의 단일 step 기록.
    모든 metric은 이 로그에서 사후 계산된다.
    """
    step_number: int
    timestamp_ms: int
    input_tokens: int
    output_tokens: int
    tool_called: Optional[str]
    tool_success: Optional[bool]
    agent_output: str
    goal_statement: Optional[str]     # checkpoint step에서만 기록
    harness_alert: Optional[str]      # harness가 이 step에서 발생시킨 알림
    harness_action: Optional[str]     # retry / rollback / reinjection / none
    ground_truth_verdict: Optional[Literal["pass", "fail", "uncertain"]] = None


@dataclass
class RunLog:
    """단일 run 전체 기록. 모든 StepLog + 최종 결과."""
    config: ExperimentConfig
    steps: list[StepLog] = field(default_factory=list)
    final_verdict: Optional[Literal["success", "failure", "partial"]] = None
    failure_type: Optional[str] = None
    recovered: bool = False
    total_input_tokens: int = 0
    total_output_tokens: int = 0
