"""
Task Fixture Generator — T1/T2/T3/T4 실험 task 인스턴스.
design-specification.md §1 (Task Specification) 참조.

각 task는 (prompt, ground_truth) 쌍으로 반환.
ExperimentRunner의 task_prompt_factory로 직접 사용.

T3 (long-horizon): 별도 repo fixture 필요 — make_t3_task() 참조.
"""
from __future__ import annotations

import textwrap
from dataclasses import dataclass, field
from typing import Optional

from .config import Difficulty
from .ground_truth import BugEntry


# ── T1 — Code Review Task ─────────────────────────────────────────────────────

@dataclass
class T1Task:
    code: str
    ground_truth_bugs: list[BugEntry]
    difficulty: Difficulty
    prompt: str = ""

    def __post_init__(self):
        if not self.prompt:
            self.prompt = (
                "Review the following Python code and identify all bugs.\n"
                "Return ONLY a JSON list with this exact schema:\n"
                '[{"line_number": N, "bug_type": "off-by-one|null_check|'
                'type_mismatch|resource_leak|race_condition|state_bug|logic_error", '
                '"severity": "low|medium|high|critical", "fix_suggestion": "..."}]\n\n'
                "Code:\n```python\n" + self.code + "\n```"
            )


# T1 EASY — 50 LOC, 3 single-line bugs
_T1_EASY_CODE = textwrap.dedent("""\
    def process_orders(orders: list, discount_rate: float = 0.0) -> dict:
        \"\"\"
        Process a list of order dicts and return a summary.
        Each order: {"id": str, "items": list, "customer_id": str}
        Each item:  {"name": str, "price": float, "quantity": int}
        \"\"\"
        if not orders:
            return {"total_revenue": 0.0, "order_count": 0,
                    "item_totals": {}, "discounted": False, "errors": []}

        total_revenue = 0.0
        item_totals = {}
        errors = []

        for i in range(len(orders) - 1):        # Bug 1 (line 15): off-by-one, last order skipped
            order = orders[i]
            if not isinstance(order, dict):
                errors.append(f"index {i}: not a dict")
                continue

            cid = order["customer_id"]            # Bug 2 (line 20): KeyError if key absent; use .get()

            for item in order.get("items", []):
                name  = item.get("name", "unknown")
                price = item.get("price", 0.0)
                qty   = item.get("quantity", 1)
                item_totals[name] = item_totals.get(name, 0.0) + price * qty
                total_revenue += price * qty

        if discount_rate > 0:
            total_revenue *= (1 - discount_rate)

        discounted = (discount_rate == "0.0")   # Bug 3 (line 31): type mismatch, should be > 0.0

        return {
            "total_revenue": round(total_revenue, 2),
            "order_count": len(orders),
            "item_totals": item_totals,
            "discounted": discounted,
            "errors": errors,
        }
""")

_T1_EASY_BUGS = [
    BugEntry(line_number=15, bug_type="off-by-one",   severity="high"),
    BugEntry(line_number=20, bug_type="null_check",   severity="high"),
    BugEntry(line_number=31, bug_type="type_mismatch", severity="medium"),
]


# T1 MODERATE — 100 LOC, 3 single-line + 1 multi-line logic bug
_T1_MODERATE_CODE = textwrap.dedent("""\
    import time

    class TTLCache:
        \"\"\"In-memory cache with time-to-live expiration.\"\"\"

        def __init__(self, max_size: int = 128, ttl: int = 60):
            self._store: dict = {}
            self._max_size = max_size
            self._ttl = ttl

        def get(self, key: str):
            \"\"\"Return cached value or None if missing/expired.\"\"\"
            if key not in self._store:
                return None
            value, expiry = self._store[key]
            if time.time() > expiry:
                del self._store[key]
                return None
            return value

        def set(self, key: str, value) -> None:
            \"\"\"Insert or update a cache entry.\"\"\"
            if len(self._store) >= self._max_size:
                self._evict_lru()
            expiry = time.time() + self._ttl
            self._store[key] = (value, expiry)

        def _evict_lru(self) -> None:
            \"\"\"Remove the entry with the earliest expiry (approximate LRU).\"\"\"
            if not self._store:
                return
            oldest = min(self._store, key=lambda k: self._store[k][1])
            del self._store[oldest]

        def invalidate(self, prefix: str = "") -> int:
            \"\"\"Invalidate all keys matching prefix. Returns count removed.\"\"\"
            if not prefix:
                count = len(self._store)
                self._store.clear()
                return count
            to_delete = [k for k in self._store if k.startswith(prefix)]
            for k in to_delete:
                del self._store[k]
            return len(to_delete)

        def stats(self) -> dict:
            \"\"\"Return cache statistics.\"\"\"
            now = time.time()
            active = sum(1 for _, (_, exp) in self._store.items() if exp > now)
            return {
                "total_entries": len(self._store),
                "active_entries": active,
                "expired_entries": len(self._store) - active,
                "utilization": len(self._store) / self._max_size,
            }

        def get_or_set(self, key: str, factory, ttl_override: int = None):
            \"\"\"Return cached value; if absent, compute via factory() and cache it.\"\"\"
            cached = self.get(key)
            if cached is not None:
                return cached
            value = factory()               # Bug 1 (line 59): factory may be None — no null check
            if ttl_override is not None:
                old_ttl = self._ttl
                self._ttl = ttl_override
            self.set(key, value)
            if ttl_override is not None:    # Bug 2 (line 64): missing else branch
                self._ttl = old_ttl         # old_ttl potentially unbound if first branch not taken
            return value

        def bulk_get(self, keys: list) -> dict:
            \"\"\"Return dict of {key: value} for all requested keys (None if missing).\"\"\"
            result = {}
            for key in keys:
                result[key] = self.get(key)
            return result

        def extend_ttl(self, key: str, extra_seconds: int) -> bool:
            \"\"\"Extend the TTL of an existing cache entry. Returns True if extended.\"\"\"
            if key not in self._store:
                return False
            value, expiry = self._store[key]
            # Bug 3 (line 80): multi-line logic error — adds extra_seconds to expiry
            # but expiry is already an absolute timestamp; should be:
            #   new_expiry = max(expiry, time.time()) + extra_seconds
            new_expiry = expiry + extra_seconds + self._ttl   # BUG: double-adds _ttl
            self._store[key] = (value, new_expiry)
            return True

        def touch(self, key: str) -> bool:
            \"\"\"Reset TTL for an existing entry. Returns True if key existed.\"\"\"
            if key not in self._store:
                return False
            value, _ = self._store[key]
            self.set(key, value)
            return True

        def __len__(self) -> int:
            return len(self._store)

        def __contains__(self, key: str) -> bool:
            return self.get(key) is not None

        def batch_set(self, items: dict, ttl_override: int = None) -> None:
            \"\"\"Insert multiple key-value pairs.\"\"\"
            # Bug 4 (line 102-103): type check compares len to string literal
            if len(items) == "0":           # BUG: should be len(items) == 0 or not items
                return
            for key, value in items.items():
                if ttl_override:
                    old = self._ttl
                    self._ttl = ttl_override
                    self.set(key, value)
                    self._ttl = old
                else:
                    self.set(key, value)
""")

_T1_MODERATE_BUGS = [
    BugEntry(line_number=59,  bug_type="null_check",   severity="high"),
    BugEntry(line_number=64,  bug_type="logic_error",  severity="medium"),
    BugEntry(line_number=80,  bug_type="logic_error",  severity="medium"),
    BugEntry(line_number=102, bug_type="type_mismatch", severity="low"),
]


# T1 FRONTIER — 150 LOC, 5 bugs (race condition + state bug)
_T1_FRONTIER_CODE = textwrap.dedent("""\
    import threading
    import time
    from collections import deque
    from typing import Callable, Optional

    class RateLimiter:
        \"\"\"
        Token-bucket rate limiter with per-client tracking.
        Thread-safe: multiple threads may call acquire() concurrently.
        \"\"\"

        def __init__(
            self,
            max_requests: int,
            window_seconds: float,
            clients: dict = {},             # Bug 1 (line 14): mutable default arg — shared across instances
        ):
            self._max_requests = max_requests
            self._window = window_seconds
            self._clients = clients
            self._lock = threading.Lock()
            self._global_requests: deque = deque()

        def _cleanup_expired(self, now: float) -> None:
            \"\"\"Remove requests older than the window.\"\"\"
            cutoff = now - self._window
            while self._global_requests and self._global_requests[0] <= cutoff:
                self._global_requests.popleft()

        def is_allowed(self, client_id: Optional[str] = None) -> bool:
            \"\"\"
            Check if a request is currently allowed.
            Does NOT consume a token — call acquire() to consume.
            \"\"\"
            now = time.time()
            # Bug 2 (line 33): read without lock — race condition (check without acquire)
            self._cleanup_expired(now)
            if len(self._global_requests) >= self._max_requests:
                return False
            if client_id is not None:
                client_q = self._clients[client_id]     # Bug 3 (line 37): KeyError if new client; use .get()
                client_cutoff = now - self._window
                client_active = sum(1 for t in client_q if t > client_cutoff)
                if client_active >= self._max_requests:
                    return False
            return True

        def acquire(self, client_id: Optional[str] = None, timeout: float = 0.0) -> bool:
            \"\"\"
            Consume one token. Blocks up to `timeout` seconds if limit reached.
            Returns True if token acquired, False if timeout expired.
            \"\"\"
            deadline = time.time() + timeout
            while True:
                with self._lock:
                    now = time.time()
                    self._cleanup_expired(now)
                    if len(self._global_requests) < self._max_requests:
                        self._global_requests.append(now)
                        if client_id is not None:
                            if client_id not in self._clients:
                                self._clients[client_id] = deque()
                            self._clients[client_id].append(now)
                        return True
                if time.time() >= deadline:
                    return False
                time.sleep(0.01)

        def get_stats(self) -> dict:
            \"\"\"Current rate limiter statistics.\"\"\"
            with self._lock:
                now = time.time()
                self._cleanup_expired(now)
                return {
                    "active_global": len(self._global_requests),
                    "max_requests": self._max_requests,
                    "window_seconds": self._window,
                    "utilization": len(self._global_requests) / self._max_requests,
                    "client_count": len(self._clients),
                }

        def reset(self, client_id: Optional[str] = None) -> None:
            \"\"\"Clear rate limit counters. If client_id given, reset only that client.\"\"\"
            with self._lock:
                if client_id is not None:
                    if client_id in self._clients:
                        self._clients[client_id].clear()
                else:
                    self._global_requests.clear()
                    self._clients.clear()

        def wait_until_allowed(self, client_id: Optional[str] = None) -> float:
            \"\"\"Block until a token is available. Returns wait time in seconds.\"\"\"
            start = time.time()
            while not self.acquire(client_id, timeout=0):
                with self._lock:
                    now = time.time()
                    self._cleanup_expired(now)
                    if self._global_requests:
                        oldest = self._global_requests[0]
                        wait = (oldest + self._window) - now
                    else:
                        wait = 0.0
                if wait > 0:
                    time.sleep(min(wait, 0.1))
            return time.time() - start

        def batch_acquire(self, count: int, client_id: Optional[str] = None) -> int:
            \"\"\"
            Acquire up to `count` tokens. Returns number actually acquired.
            Bug 4 (line 120): off-by-one — acquires one fewer token than requested.
            \"\"\"
            acquired = 0
            for _ in range(count - 1):      # BUG: should be range(count)
                if self.acquire(client_id, timeout=0):
                    acquired += 1
                else:
                    break
            return acquired

        def __enter__(self):
            self.acquire(timeout=float("inf"))
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            # Bug 5 (line 133): resource leak — lock not released on exception path
            # acquire() is non-blocking here (token already consumed in __enter__)
            # but _lock may still be held if acquire() internal state is mid-update
            pass    # intentionally incomplete cleanup

        def __repr__(self) -> str:
            stats = self.get_stats()
            return (
                f"RateLimiter(max={self._max_requests}, window={self._window}s, "
                f"active={stats['active_global']})"
            )
""")

_T1_FRONTIER_BUGS = [
    BugEntry(line_number=14,  bug_type="state_bug",       severity="high"),
    BugEntry(line_number=33,  bug_type="race_condition",  severity="critical"),
    BugEntry(line_number=37,  bug_type="null_check",      severity="high"),
    BugEntry(line_number=120, bug_type="off-by-one",      severity="medium"),
    BugEntry(line_number=133, bug_type="resource_leak",   severity="medium"),
]


def make_t1_task(difficulty: Difficulty, seed: int = 42) -> T1Task:
    if difficulty == "EASY":
        return T1Task(_T1_EASY_CODE, _T1_EASY_BUGS, difficulty)
    if difficulty == "MODERATE":
        return T1Task(_T1_MODERATE_CODE, _T1_MODERATE_BUGS, difficulty)
    return T1Task(_T1_FRONTIER_CODE, _T1_FRONTIER_BUGS, difficulty)


# ── T2 — Multi-Step Reasoning Task ───────────────────────────────────────────

@dataclass
class T2Task:
    problem_description: str
    constraints: list[dict]
    difficulty: Difficulty
    expected_valid_orderings: int = 1    # 유효한 순서의 수 (검증용)
    required_actions: list[str] = field(default_factory=list)
    optional_actions: list[str] = field(default_factory=list)
    prompt: str = ""

    def __post_init__(self):
        if not self.prompt:
            self.prompt = (
                "Given the following software dependency resolution problem, "
                "produce a valid installation order.\n\n"
                + self.problem_description
                + "\n\nReturn ONLY a JSON list:\n"
                '[{"step": N, "action": "install_<package>", "rationale": "..."}]\n'
                "Ensure all dependency constraints are satisfied."
            )


_T2_EASY_DESC = textwrap.dedent("""\
    You need to install 5 packages: A, B, C, D, E.
    Dependencies (must install X before Y):
      - B must be installed before A
      - C must be installed before B
      - C must be installed before D
      - D must be installed before E
    There are no version conflicts.
    Find a valid installation order.
""")

_T2_EASY_CONSTRAINTS = [
    {"type": "dependency", "before": "install_C", "after": "install_B"},
    {"type": "dependency", "before": "install_B", "after": "install_A"},
    {"type": "dependency", "before": "install_C", "after": "install_D"},
    {"type": "dependency", "before": "install_D", "after": "install_E"},
]

_T2_MODERATE_DESC = textwrap.dedent("""\
    You need to install 10 packages for a data science environment.
    Packages: core, numpy, scipy, pandas, matplotlib, seaborn, sklearn, torch, tqdm, requests

    Dependencies:
      - core must be installed first (no dependencies)
      - numpy requires core
      - scipy requires numpy
      - pandas requires numpy
      - matplotlib requires numpy
      - seaborn requires matplotlib AND pandas
      - sklearn requires scipy AND numpy
      - torch requires numpy
      - tqdm requires core
      - requests requires core

    Conflicts:
      - CONFLICT: seaborn must be installed AFTER sklearn (seaborn has sklearn integration test)
      - CONFLICT: torch must be installed BEFORE sklearn (torch provides BLAS optimizations sklearn uses)

    Optional:
      - tqdm is optional and can be installed at any point after core.

    Find a valid installation order satisfying all constraints.
""")

_T2_MODERATE_CONSTRAINTS = [
    {"type": "dependency", "before": "install_core",        "after": "install_numpy"},
    {"type": "dependency", "before": "install_numpy",       "after": "install_scipy"},
    {"type": "dependency", "before": "install_numpy",       "after": "install_pandas"},
    {"type": "dependency", "before": "install_numpy",       "after": "install_matplotlib"},
    {"type": "dependency", "before": "install_matplotlib",  "after": "install_seaborn"},
    {"type": "dependency", "before": "install_pandas",      "after": "install_seaborn"},
    {"type": "dependency", "before": "install_scipy",       "after": "install_sklearn"},
    {"type": "dependency", "before": "install_numpy",       "after": "install_sklearn"},
    {"type": "dependency", "before": "install_numpy",       "after": "install_torch"},
    {"type": "dependency", "before": "install_sklearn",     "after": "install_seaborn"},  # conflict 1
    {"type": "dependency", "before": "install_torch",       "after": "install_sklearn"},  # conflict 2
]

_T2_FRONTIER_DESC = textwrap.dedent("""\
    You need to build and deploy 20 microservices in a distributed system.
    Services: gateway, auth, user, session, profile, feed, post, comment, like,
              media, search, notification, email, sms, analytics, billing, cache,
              queue, storage, config

    Dependencies (service X must start before service Y):
      config    → cache, queue, storage
      storage   → media, profile
      cache     → session, feed, search
      queue     → notification, email, sms, analytics
      auth      → session, user
      user      → profile, billing
      session   → feed, post
      post      → comment, like, media
      feed      → search
      gateway   → auth, feed, search, notification

    Resource constraints (max 3 services starting simultaneously):
      {"type": "resource", "item": "deploy_slots", "limit": 3}

    Cyclic dependency to resolve:
      billing requires analytics for fraud detection,
      analytics requires billing for revenue data.
      Resolution: start billing in "read-only" mode first, then analytics,
                  then upgrade billing to "full" mode.

    Find a valid startup order. For the billing/analytics cycle,
    use actions "start_billing_readonly", "start_analytics", "upgrade_billing".
""")

_T2_FRONTIER_CONSTRAINTS = [
    {"type": "dependency", "before": "install_config",   "after": "install_cache"},
    {"type": "dependency", "before": "install_config",   "after": "install_queue"},
    {"type": "dependency", "before": "install_config",   "after": "install_storage"},
    {"type": "dependency", "before": "install_storage",  "after": "install_media"},
    {"type": "dependency", "before": "install_storage",  "after": "install_profile"},
    {"type": "dependency", "before": "install_cache",    "after": "install_session"},
    {"type": "dependency", "before": "install_cache",    "after": "install_feed"},
    {"type": "dependency", "before": "install_cache",    "after": "install_search"},
    {"type": "dependency", "before": "install_auth",     "after": "install_session"},
    {"type": "dependency", "before": "install_session",  "after": "install_feed"},
    {"type": "dependency", "before": "install_session",  "after": "install_post"},
    {"type": "dependency", "before": "install_post",     "after": "install_comment"},
    {"type": "dependency", "before": "install_post",     "after": "install_like"},
    {"type": "resource",   "item": "deploy_slots",       "limit": 3},
]


def make_t2_task(difficulty: Difficulty, seed: int = 42) -> T2Task:
    if difficulty == "EASY":
        return T2Task(
            _T2_EASY_DESC,
            _T2_EASY_CONSTRAINTS,
            difficulty,
            expected_valid_orderings=3,
            required_actions=["install_A", "install_B", "install_C", "install_D", "install_E"],
        )
    if difficulty == "MODERATE":
        return T2Task(
            _T2_MODERATE_DESC,
            _T2_MODERATE_CONSTRAINTS,
            difficulty,
            expected_valid_orderings=2,
            required_actions=[
                "install_core",
                "install_numpy",
                "install_scipy",
                "install_pandas",
                "install_matplotlib",
                "install_seaborn",
                "install_sklearn",
                "install_torch",
            ],
            optional_actions=["install_tqdm", "install_requests"],
        )
    return T2Task(
        _T2_FRONTIER_DESC,
        _T2_FRONTIER_CONSTRAINTS,
        difficulty,
        expected_valid_orderings=1,
        required_actions=[
            "install_gateway",
            "install_auth",
            "install_user",
            "install_session",
            "install_profile",
            "install_feed",
            "install_post",
            "install_comment",
            "install_like",
            "install_media",
            "install_search",
            "install_notification",
            "install_email",
            "install_sms",
            "install_cache",
            "install_queue",
            "install_storage",
            "install_config",
            "start_billing_readonly",
            "start_analytics",
            "upgrade_billing",
        ],
    )


# ── T3 — Long-Horizon Execution Task ──────────────────────────────────────────

@dataclass
class T3Task:
    """
    T3는 실제 파일 시스템 repo가 필요.
    make_t3_repo()로 임시 디렉토리에 fixture repo를 생성하고
    해당 경로를 AgentRunner에 전달.
    """
    repo_description: str
    initial_goal: str
    difficulty: Difficulty
    magic_number_count: int     # EASY=20, MODERATE=50, FRONTIER=100
    file_count: int             # EASY=10, MODERATE=25, FRONTIER=50
    prompt: str = ""

    def __post_init__(self):
        if not self.prompt:
            self.prompt = (
                f"Task: {self.initial_goal}\n\n"
                f"The codebase has {self.file_count} Python files "
                f"with approximately {self.magic_number_count} magic numbers to replace.\n\n"
                "Work through the codebase systematically. "
                "At every 10th step, output 'CURRENT GOAL: <one sentence>'.\n"
                "When done, output 'TASK COMPLETE'."
            )


def make_t3_task(difficulty: Difficulty) -> T3Task:
    goals = {
        "EASY": "Replace all magic numbers with named constants in this codebase.",
        "MODERATE": "Replace all magic numbers with named constants and add module-level __all__ exports.",
        "FRONTIER": "Replace all magic numbers with named constants, preserving runtime-computed values as properties.",
    }
    counts = {"EASY": (20, 10), "MODERATE": (50, 25), "FRONTIER": (100, 50)}
    mc, fc = counts[difficulty]
    return T3Task(
        repo_description=f"{difficulty} codebase with {mc} magic numbers across {fc} files",
        initial_goal=goals[difficulty],
        difficulty=difficulty,
        magic_number_count=mc,
        file_count=fc,
    )


# ── T4 — Context-Sensitive Synthesis Task ────────────────────────────────────

@dataclass
class T4Task:
    documents: list[str]        # 10개 문서 텍스트
    question: str
    key_facts: list[str]        # 정답에 반드시 포함되어야 할 핵심 사실
    misleading_claims: list[str]  # 포함되면 안 되는 오답 유도 내용
    difficulty: Difficulty
    prompt: str = ""

    def __post_init__(self):
        if not self.prompt:
            docs_text = "\n\n".join(
                f"[Document {i+1}]\n{doc}" for i, doc in enumerate(self.documents)
            )
            self.prompt = (
                f"Read the following {len(self.documents)} documents carefully.\n\n"
                + docs_text
                + f"\n\nQuestion: {self.question}\n\n"
                "Answer using ONLY information from the documents above. "
                "Cite the document number for each key fact (e.g., '[Doc 3]'). "
                "Do not include information that contradicts the majority of sources."
            )


_T4_DOCS_EASY = [
    # Doc 1 — contains the answer
    "The Prometheus incident occurred on March 14, 2026. "
    "Root cause: the context window of the primary agent exceeded 800K tokens, "
    "causing silent output degradation. The agent continued to respond but "
    "with progressively lower coherence scores. Recovery time was 47 minutes.",

    # Doc 2 — partially related
    "Agent memory management requires careful monitoring of token accumulation. "
    "Standard practice is to reset context at 70% utilization to prevent degradation.",

    # Doc 3 — unrelated (distractor)
    "The GPU cluster upgrade was completed on March 10, 2026. "
    "New A100 nodes increased throughput by 340% for batch inference workloads.",

    # Doc 4 — unrelated
    "The quarterly budget review identified compute costs as the primary driver "
    "of infrastructure spend, accounting for 67% of total AI operations budget.",

    # Docs 5-10 — padding
    "Monitoring dashboards were updated to include real-time token utilization metrics.",
    "The on-call rotation was revised to include an AI systems specialist.",
    "Load balancing improvements reduced P99 latency by 18ms.",
    "Documentation for the harness API was updated with new examples.",
    "The staging environment was upgraded to mirror production configuration.",
    "Weekly sync meetings were moved from Thursday to Tuesday.",
]

_T4_DOCS_MODERATE = [
    # Answer is distributed across docs 1, 3, 6
    "On March 14, 2026 at 14:32 UTC, the Prometheus agent cluster experienced "
    "a cascading failure. The incident was first detected by automated monitoring "
    "when response quality scores dropped below 0.72.",

    "The engineering team had deployed a new harness version (v2.3.1) at 14:15 UTC, "
    "seventeen minutes before the incident began. The deployment included changes "
    "to context boundary enforcement logic.",

    "Investigation revealed that the context window exceeded 800K tokens in 4 of 6 "
    "agent instances. The root cause was traced to a missing context reset trigger "
    "in the new harness version when processing long multi-turn conversations.",

    "The fallback mechanism was triggered at 14:45 UTC, routing traffic to backup "
    "agents with the previous harness version (v2.2.9). This was the point of "
    "service restoration.",

    # Misleading doc
    "A similar incident in December 2025 was caused by a GPU memory leak, "
    "not a context window issue. Recovery required full cluster restart, taking 3 hours.",

    # Contains partial answer
    "Full recovery was confirmed at 15:19 UTC. Total incident duration: 47 minutes. "
    "The fix involved rolling back to v2.2.9 and adding a context window size check "
    "to the deployment validation pipeline.",

    # Distractors
    "The post-incident review recommended adding automated rollback triggers.",
    "Token budget monitoring was identified as a key gap in the observability stack.",
    "The incident affected 12% of production traffic during the peak window.",
    "SLA breach threshold was not crossed; the incident was classified as P2.",
]

_T4_DOCS_FRONTIER = [
    # Answer fragments distributed across 5 docs, some contradictions
    "The Prometheus incident root cause was context window overflow (>800K tokens). "
    "Three separate failure modes were observed simultaneously.",

    # Contradicts doc 1 partially
    "Initial reports suggested a GPU memory leak caused the Prometheus incident. "
    "This theory was later disproven when heap dumps showed normal GPU utilization.",

    "The harness v2.3.1 deployment at 14:15 UTC introduced a regression in the "
    "context boundary enforcement. Specifically, the _reset_threshold parameter "
    "was inadvertently set to float('inf') in the configuration serializer.",

    "Agent self-assessment accuracy dropped from 0.91 to 0.34 during the incident, "
    "indicating the agents were unaware of their own degradation — a pattern "
    "consistent with context saturation rather than hardware failure.",

    "Recovery was achieved through three sequential interventions: "
    "(1) traffic rerouting to backup cluster at T+13min, "
    "(2) harness rollback at T+34min, "
    "(3) context flush on primary cluster at T+47min.",

    # Misleading
    "The December 2025 incident had identical symptoms and was caused by a network "
    "partition, not a software bug. The same recovery procedure was applied.",

    # Partial — corroborates doc 3
    "Code review of v2.3.1 identified the serializer bug on line 847 of "
    "context_manager.py. The fix was a one-line change: replacing float('inf') "
    "with the intended value of 0.80.",

    # Distractors
    "Post-incident, 23 additional test cases were added to the harness test suite.",
    "The incident was the first P1 event in 94 days of production operation.",
    "Four engineers were involved in the incident response.",
]


def make_t4_task(difficulty: Difficulty, seed: int = 42) -> T4Task:
    if difficulty == "EASY":
        return T4Task(
            documents=_T4_DOCS_EASY,
            question="What was the root cause of the Prometheus incident, "
                     "and how long did it take to recover?",
            key_facts=[
                "context window exceeded 800K tokens",
                "recovery time was 47 minutes",
                "March 14 2026",
            ],
            misleading_claims=[
                "GPU memory leak",
                "network partition",
                "3 hours",
            ],
            difficulty=difficulty,
        )

    if difficulty == "MODERATE":
        return T4Task(
            documents=_T4_DOCS_MODERATE,
            question="Describe the timeline and root cause of the Prometheus incident "
                     "on March 14, 2026, including what triggered recovery.",
            key_facts=[
                "14:32 UTC incident start",
                "harness version v2.3.1",
                "context boundary enforcement",
                "800K tokens",
                "47 minutes total duration",
                "rollback to v2.2.9",
            ],
            misleading_claims=[
                "GPU memory leak",
                "3 hours recovery",
                "December 2025 incident same cause",
            ],
            difficulty=difficulty,
        )

    # FRONTIER
    return T4Task(
        documents=_T4_DOCS_FRONTIER,
        question="Synthesize the complete account of the Prometheus incident: "
                 "root cause, failure mechanism, timeline of interventions, and fix.",
        key_facts=[
            "context window overflow 800K tokens",
            "_reset_threshold set to float inf",
            "serializer bug line 847",
            "agent self-assessment accuracy dropped to 0.34",
            "three sequential interventions",
            "traffic rerouting T+13min",
            "harness rollback T+34min",
        ],
        misleading_claims=[
            "GPU memory leak caused the incident",
            "network partition",
            "identical to December 2025",
        ],
        difficulty=difficulty,
    )
