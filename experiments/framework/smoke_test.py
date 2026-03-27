"""
Framework smoke test — API call 없이 측정 도구만 검증.
실험 인프라를 실행하기 전 반드시 통과해야 한다.

실행: python3 -m framework.smoke_test  (experiments/ 디렉토리에서)
"""
import sys
import tempfile
from types import SimpleNamespace
import numpy as np

# ── metrics.py ────────────────────────────────────────────────────────────────

def test_metrics():
    from framework.metrics import (
        compute_rsucc_r,
        compute_ttff,
        compute_hdl_lead_time,
        compute_saa,
        compute_goal_fidelity_series,
        detect_drift_regime,
        compute_ccs,
        compute_hor,
        compute_ece,
        compute_roc_data,
    )
    from framework.config import RunLog, StepLog, ExperimentConfig, TaskConfig, HarnessConfig

    dummy_config = ExperimentConfig(
        experiment_id="SMOKE",
        run_id=1,
        model="claude-haiku-4-5-20251001",
        harness=HarnessConfig(),
        task=TaskConfig(
            task_type="T1_code_review",
            difficulty="MODERATE",
            max_steps=10,
            token_budget=10000,
        ),
    )

    # RSuccR
    run_a = RunLog(config=dummy_config, recovered=True, final_verdict="success",
                   total_input_tokens=100, total_output_tokens=50)
    run_b = RunLog(config=dummy_config, recovered=False, final_verdict="failure",
                   total_input_tokens=80, total_output_tokens=30)
    result = compute_rsucc_r([run_a, run_b])
    assert 0.0 <= result.value <= 1.0, f"RSuccR out of range: {result.value}"
    print(f"  RSuccR = {result.value:.3f} (CI {result.ci_lower:.3f}–{result.ci_upper:.3f})")

    # TTFF
    step_with_alert = StepLog(
        step_number=5, timestamp_ms=0, input_tokens=10, output_tokens=5,
        tool_called=None, tool_success=None, agent_output="output",
        goal_statement=None, harness_alert="tool_failure", harness_action="retry",
    )
    run_c = RunLog(config=dummy_config, steps=[step_with_alert])
    ttff = compute_ttff(run_c)
    assert ttff == 5, f"TTFF should be 5, got {ttff}"
    print(f"  TTFF = {ttff}")

    # SAA
    agent_reports = [
        {"step": 1, "agent_verdict": "pass", "confidence": 0.9},
        {"step": 2, "agent_verdict": "fail", "confidence": 0.3},
        {"step": 3, "agent_verdict": "pass", "confidence": 0.7},
    ]
    ground_truth = [
        {"step": 1, "verdict": "pass"},
        {"step": 2, "verdict": "fail"},
        {"step": 3, "verdict": "fail"},  # agent 오판
    ]
    saa = compute_saa(agent_reports, ground_truth)
    assert abs(saa.value - 2/3) < 0.01, f"SAA should be ~0.667, got {saa.value}"
    print(f"  SAA = {saa.value:.3f}")

    # GDR + drift regime
    initial_emb = np.array([1.0, 0.0, 0.0])
    checkpoints = [
        (10, np.array([0.98, 0.20, 0.0])),
        (20, np.array([0.90, 0.44, 0.0])),
        (30, np.array([0.70, 0.71, 0.0])),
        (40, np.array([0.40, 0.92, 0.0])),
    ]
    gfs_series = compute_goal_fidelity_series(initial_emb, checkpoints)
    assert len(gfs_series) == 4
    assert gfs_series[0][1] > gfs_series[-1][1], "GFS should decrease"
    print(f"  GFS series: {[(s, round(g, 3)) for s, g in gfs_series]}")

    drift = detect_drift_regime(gfs_series)
    print(f"  Drift: k_hat={drift['k_hat']}, ΔAIC={drift['delta_aic']:.2f}, {drift['interpretation']}")

    # CCS
    ccs = compute_ccs(
        agent_a_output="project alpha deadline is friday budget approved",
        agent_b_context_terms=["project alpha deadline", "budget approved friday"],
    )
    assert 0.0 <= ccs <= 1.0
    print(f"  CCS = {ccs:.3f}")

    # ECE
    confidences = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]
    correct     = [True, True, True, False, False, False, False]
    ece = compute_ece(confidences, correct)
    assert 0.0 <= ece.value <= 1.0
    print(f"  ECE = {ece.value:.3f}")

    # ROC
    scores = [0.9, 0.8, 0.3, 0.2, 0.7, 0.1, 0.6, 0.4]
    labels = [True, True, False, False, True, False, False, True]
    roc = compute_roc_data(scores, labels)
    assert "auc" in roc
    assert 0.0 <= roc["auc"] <= 1.0
    print(f"  AUC = {roc['auc']:.3f}")

    print("  [PASS] metrics.py")


# ── arcc.py ───────────────────────────────────────────────────────────────────

def test_arcc():
    from framework.arcc import (
        compute_tca, compute_ifr, compute_msrd, compute_cue,
        compute_arcc, detect_capability_cliff,
    )

    tca = compute_tca([
        {"called": True, "success": True},
        {"called": True, "success": False},
        {"called": True, "success": True},
    ])
    assert abs(tca.value - 2/3) < 0.01
    print(f"  TCA = {tca.value:.3f}")

    ifr = compute_ifr([
        {"instruction": "use JSON", "complied": True},
        {"instruction": "max 3 lines", "complied": False},
        {"instruction": "English only", "complied": True},
    ])
    assert abs(ifr.value - 2/3) < 0.01
    print(f"  IFR = {ifr.value:.3f}")

    msrd = compute_msrd([True, True, True, False, True], task_max_steps=10)
    assert abs(msrd.value - 0.4) < 0.01  # error at step 4 → 4/10
    print(f"  MSRD = {msrd.value:.3f}")

    cue = compute_cue(
        relevant_passages=["the model failed because of memory pressure"],
        agent_output="According to doc 1, the model failed because of memory pressure during execution",
    )
    assert cue.value > 0.0
    print(f"  CUE = {cue.value:.3f}")

    arcc = compute_arcc(tca, ifr, msrd, cue)
    assert 0.0 <= arcc.arcc <= 1.0
    print(f"  ARCC = {arcc.arcc:.3f} (weights={[round(w,2) for w in arcc.weights]})")

    # Capability cliff
    arcc_scores = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    tcr_values  = [0.1, 0.15, 0.2, 0.45, 0.75, 0.88, 0.93, 0.95]
    cliff = detect_capability_cliff(arcc_scores, tcr_values)
    assert "cliff_arcc" in cliff
    print(f"  Capability cliff: ARCC={cliff['cliff_arcc']:.3f} (R²={cliff.get('r2', 'N/A')})")

    print("  [PASS] arcc.py")


# ── ground_truth.py ───────────────────────────────────────────────────────────

def test_ground_truth():
    from framework.ground_truth import validate_t1, validate_t2, validate_t4, BugEntry

    # T1
    agent_output = '[{"line_number": 10, "bug_type": "null_check", "severity": "high"}]'
    bugs = [BugEntry(line_number=10, bug_type="null_check", severity="high")]
    result = validate_t1(agent_output, bugs)
    assert result.score > 0.9, f"T1 score should be high: {result.score}"
    print(f"  T1 F1 = {result.score:.3f} ({result.verdict})")

    wrong_type = '[{"line_number": 10, "bug_type": "totally_wrong", "severity": "low"}]'
    wrong_result = validate_t1(wrong_type, bugs)
    assert wrong_result.verdict == "fail", "wrong bug type/severity must not pass"
    print(f"  T1 wrong-classification verdict = {wrong_result.verdict}")

    # T2
    plan = '[{"step": 1, "action": "install_A"}, {"step": 2, "action": "install_B"}]'
    constraints = {
        "constraints": [{"type": "dependency", "before": "install_A", "after": "install_B"}],
        "required_actions": ["install_A", "install_B"],
    }
    result = validate_t2(plan, constraints)
    assert result.verdict == "pass"
    print(f"  T2 verdict = {result.verdict} (score={result.score:.3f})")

    partial_plan = '[{"step": 1, "action": "install_A"}]'
    partial_result = validate_t2(partial_plan, constraints)
    assert partial_result.verdict != "pass", "missing required action must not pass"
    print(f"  T2 partial-plan verdict = {partial_result.verdict} (score={partial_result.score:.3f})")

    # T4
    result = validate_t4(
        agent_output="The experiment showed 42% improvement in accuracy according to document 3.",
        key_facts=["42% improvement in accuracy"],
        misleading_claims=["experiment was a failure"],
    )
    assert result.score > 0.5
    print(f"  T4 score = {result.score:.3f} ({result.verdict})")

    print("  [PASS] ground_truth.py")


# ── harness.py ────────────────────────────────────────────────────────────────

def test_harness():
    from framework.harness import Harness
    from framework.config import HarnessConfig

    config = HarnessConfig.full()
    h = Harness(config, initial_goal="refactor all magic numbers to named constants")

    # Normal step — no alert expected
    log = h.observe(
        step_number=1,
        agent_output='{"bugs": []}',
        input_tokens=100,
        output_tokens=50,
    )
    assert log.harness_alert is None, f"unexpected alert: {log.harness_alert}"
    print(f"  Step 1: alert={log.harness_alert}, action={log.harness_action}")

    # Budget critical step
    h.state.total_input_tokens = 98_000
    log = h.observe(
        step_number=2,
        agent_output="continuing...",
        input_tokens=1_500,
        output_tokens=500,
    )
    assert log.harness_alert is not None
    print(f"  Step 2 (budget critical): alert={log.harness_alert}")

    # Failure probability
    h2 = Harness(HarnessConfig.full())
    prob = h2.compute_failure_probability(
        agent_output="",        # empty output → format error signal
        input_tokens=100,
        output_tokens=0,
        agent_confidence=0.2,   # low confidence
    )
    assert 0.0 <= prob <= 1.0
    print(f"  Failure probability (empty+low_conf) = {prob:.3f}")

    # Ablation: none config
    h_none = Harness(HarnessConfig.none())
    log_none = h_none.observe(
        step_number=1, agent_output="", input_tokens=100, output_tokens=0
    )
    assert log_none.harness_alert is None, "harness-off should not generate alerts"
    print(f"  HarnessConfig.none(): alert={log_none.harness_alert} (expected None)")

    summary = h.summary()
    assert "enabled_components" in summary
    print(f"  Summary: {summary['enabled_components']}")

    print("  [PASS] harness.py")


# ── embedding.py ──────────────────────────────────────────────────────────────

def test_embedding():
    from framework.embedding import make_offline_embedding_fn, _hash_embed
    import numpy as np

    embed = make_offline_embedding_fn()

    v1 = embed("refactor all magic numbers to named constants")
    v2 = embed("refactor all magic numbers to named constants")
    v3 = embed("the weather today is sunny and warm")

    assert v1.shape == v2.shape, "embeddings must have same shape"
    sim_same = float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    sim_diff = float(np.dot(v1, v3) / (np.linalg.norm(v1) * np.linalg.norm(v3)))
    assert sim_same > sim_diff, f"identical text should have higher similarity: {sim_same:.3f} vs {sim_diff:.3f}"
    print(f"  sim(same)={sim_same:.3f}, sim(diff)={sim_diff:.3f}")
    print("  [PASS] embedding.py")


# ── tasks.py ──────────────────────────────────────────────────────────────────

def test_tasks():
    from framework.tasks import make_t1_task, make_t2_task, make_t4_task
    from framework.ground_truth import validate_t1, validate_t2, validate_t4

    for diff in ("EASY", "MODERATE", "FRONTIER"):
        t1 = make_t1_task(diff)
        assert t1.code, f"T1 {diff}: no code"
        assert len(t1.ground_truth_bugs) >= 3, f"T1 {diff}: fewer than 3 bugs defined"
        assert t1.prompt, f"T1 {diff}: no prompt"
        print(f"  T1 {diff}: {len(t1.code.splitlines())} LOC, {len(t1.ground_truth_bugs)} bugs")

    for diff in ("EASY", "MODERATE", "FRONTIER"):
        t2 = make_t2_task(diff)
        assert t2.constraints, f"T2 {diff}: no constraints"
        print(f"  T2 {diff}: {len(t2.constraints)} constraints")

    for diff in ("EASY", "MODERATE", "FRONTIER"):
        t4 = make_t4_task(diff)
        assert len(t4.documents) == 10, f"T4 {diff}: expected 10 docs"
        assert t4.key_facts, f"T4 {diff}: no key facts"
        print(f"  T4 {diff}: {len(t4.key_facts)} key facts, {len(t4.misleading_claims)} misleading")

    # T1 ground truth round-trip (EASY: perfect answer should pass)
    t1_easy = make_t1_task("EASY")
    perfect_answer = "[" + ", ".join(
        f'{{"line_number": {b.line_number}, "bug_type": "{b.bug_type}", '
        f'"severity": "{b.severity}", "fix_suggestion": "fix it"}}'
        for b in t1_easy.ground_truth_bugs
    ) + "]"
    result = validate_t1(perfect_answer, t1_easy.ground_truth_bugs)
    assert result.score > 0.8, f"T1 perfect answer should score >0.8: {result.score}"
    print(f"  T1 EASY perfect-answer F1 = {result.score:.3f} ({result.verdict})")

    print("  [PASS] tasks.py")


# ── judge.py ──────────────────────────────────────────────────────────────────

def test_judge():
    from framework.judge import compute_cohen_kappa, agreement_matrix

    # κ = 1.0 when both raters agree perfectly
    a = ["pass", "fail", "pass", "uncertain", "fail"]
    b = ["pass", "fail", "pass", "uncertain", "fail"]
    kappa = compute_cohen_kappa(a, b)
    assert abs(kappa - 1.0) < 0.01, f"perfect agreement should give κ=1.0: {kappa}"
    print(f"  κ(perfect)={kappa:.3f}")

    # κ = 0 when raters agree only by chance
    a2 = ["pass", "pass", "fail", "fail"]
    b2 = ["fail", "fail", "pass", "pass"]
    kappa2 = compute_cohen_kappa(a2, b2)
    assert kappa2 <= 0.0, f"complete disagreement should give κ≤0: {kappa2}"
    print(f"  κ(disagree)={kappa2:.3f}")

    report = agreement_matrix(a, b)
    assert "kappa" in report and "matrix" in report
    print(f"  agreement_matrix: κ={report['kappa']:.3f}, {report['kappa_interpretation']}")

    print("  [PASS] judge.py")


# ── agent.py IFRTracker ────────────────────────────────────────────────────────

def test_ifr_tracker():
    from framework.agent import IFRTracker

    tracker = IFRTracker("T1_code_review")
    output = '[{"line_number": 10, "bug_type": "null_check", "severity": "high", "fix_suggestion": "use .get()"}]'
    tracker.check(output, tool_calls=[])
    log = tracker.compliance_log
    assert len(log) == 5, f"T1 should have 5 instructions, got {len(log)}"
    # JSON output + line_number + severity 준수 확인
    json_inst = next(e for e in log if e["instruction"] == "output JSON")
    assert json_inst["complied"], "T1 JSON output instruction should be complied"
    print(f"  IFRTracker T1: {sum(e['complied'] for e in log)}/5 instructions complied")

    tracker_t3 = IFRTracker("T3_long_horizon")
    tracker_t3.check("nonsense", step_number=10, tool_calls=[], task_complete=False)
    applicable = [e for e in tracker_t3.compliance_log if e.get("applicable", True)]
    assert sum(e["complied"] for e in applicable) == 0, "nonsense output must not satisfy T3 IFR"
    print(f"  IFRTracker T3 nonsense: {sum(e['complied'] for e in applicable)}/{len(applicable)} applicable instructions complied")

    print("  [PASS] agent.py IFRTracker")


def test_agent_local_tools():
    from framework.agent import AgentRunner
    from framework.config import ExperimentConfig, TaskConfig, HarnessConfig
    from framework.harness import Harness

    config = ExperimentConfig(
        experiment_id="SMOKE_T3",
        run_id=1,
        model="openai/gpt-5-mini",
        harness=HarnessConfig.none(),
        task=TaskConfig(
            task_type="T3_long_horizon",
            difficulty="EASY",
            max_steps=5,
            token_budget=1000,
        ),
    )
    runner = AgentRunner(config=config, harness=Harness(HarnessConfig.none()))

    with tempfile.TemporaryDirectory() as tmpdir:
        repo = f"{tmpdir}/repo"
        import os
        os.makedirs(repo, exist_ok=True)
        sample = f"{repo}/sample.py"
        with open(sample, "w", encoding="utf-8") as f:
            f.write("VALUE = 1\n")

        ok_read, read_text = runner._execute_local_tool(
            "read_file",
            {"path": "sample.py"},
            runner._resolve_repo_root({"repo_path": repo}),
            {"repo_path": repo},
        )
        assert ok_read and "VALUE = 1" in read_text

        ok_edit, _ = runner._execute_local_tool(
            "edit_file",
            {"path": "sample.py", "old_content": "VALUE = 1", "new_content": "VALUE = 2"},
            runner._resolve_repo_root({"repo_path": repo}),
            {"repo_path": repo},
        )
        assert ok_edit
        with open(sample, "r", encoding="utf-8") as f:
            assert "VALUE = 2" in f.read()

        ok_tests, tests_text = runner._execute_local_tool(
            "run_tests",
            {"test_path": "."},
            runner._resolve_repo_root({"repo_path": repo}),
            {"repo_path": repo, "test_command": "python3 -c \"print('ok')\""},
        )
        assert ok_tests and "\"returncode\": 0" in tests_text

    print("  [PASS] agent.py local tools")


def test_agent_runner_integration():
    from framework.agent import AgentRunner
    from framework.config import ExperimentConfig, TaskConfig, HarnessConfig
    from framework.ground_truth import BugEntry, validate_t1
    from framework.harness import Harness
    import json
    import os

    def fake_response(content, tool_calls=None, prompt_tokens=10, completion_tokens=5):
        message = SimpleNamespace(content=content, tool_calls=tool_calls or [])
        choice = SimpleNamespace(message=message)
        usage = SimpleNamespace(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens)
        return SimpleNamespace(choices=[choice], usage=usage)

    class FakeCompletions:
        def __init__(self, responses):
            self.responses = list(responses)
            self.calls = []

        def create(self, **kwargs):
            self.calls.append(kwargs["messages"])
            return self.responses.pop(0)

    class FakeClient:
        def __init__(self, responses):
            self.chat = SimpleNamespace(completions=FakeCompletions(responses))

    # Trust-engine action should inject a verification turn.
    trust_config = ExperimentConfig(
        experiment_id="SMOKE_VERIFY",
        run_id=1,
        model="openai/gpt-5-mini",
        harness=HarnessConfig.full(),
        task=TaskConfig(task_type="T1_code_review", difficulty="EASY", max_steps=3, token_budget=2000),
    )
    trust_runner = AgentRunner(
        config=trust_config,
        harness=Harness(HarnessConfig.full()),
        validator_fn=validate_t1,
    )
    trust_runner.client = FakeClient([
        fake_response("CONFIDENCE: 0.2\nNeed to double-check."),
        fake_response(
            'CONFIDENCE: 0.9\n[{"line_number": 1, "bug_type": "null_check", "severity": "high", "fix_suggestion": "guard it"}]'
        ),
    ])
    trust_log = trust_runner.run(
        "Review this code.",
        ground_truth=[BugEntry(line_number=1, bug_type="null_check", severity="high")],
    )
    second_call_messages = trust_runner.client.chat.completions.calls[1]
    assert any(
        "[HARNESS] Low confidence detected." in (m.get("content", "") or "")
        for m in second_call_messages if isinstance(m, dict)
    ), "verification prompt must be injected after low confidence"
    assert trust_log.final_verdict == "success"
    print("  trust-engine verification turn injected")

    # T3 tool loop should carry tool state into the next model call.
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = f"{tmpdir}/repo"
        os.makedirs(repo, exist_ok=True)
        with open(f"{repo}/sample.py", "w", encoding="utf-8") as f:
            f.write("VALUE = 1\n")

        tool_call = SimpleNamespace(
            id="tc1",
            function=SimpleNamespace(name="read_file", arguments=json.dumps({"path": "sample.py"})),
        )
        tool_config = ExperimentConfig(
            experiment_id="SMOKE_TOOL_LOOP",
            run_id=1,
            model="openai/gpt-5-mini",
            harness=HarnessConfig.none(),
            task=TaskConfig(task_type="T3_long_horizon", difficulty="EASY", max_steps=3, token_budget=2000),
        )
        tool_runner = AgentRunner(config=tool_config, harness=Harness(HarnessConfig.none()))
        tool_runner.client = FakeClient([
            fake_response("", tool_calls=[tool_call]),
            fake_response("TASK COMPLETE"),
        ])
        tool_log = tool_runner.run(
            "Refactor the repo.",
            ground_truth={"repo_path": repo, "test_command": "python3 -c \"print('ok')\""},
        )
        second_tool_call_messages = tool_runner.client.chat.completions.calls[1]
        assert any(m.get("role") == "tool" for m in second_tool_call_messages if isinstance(m, dict))
        assert any("VALUE = 1" in (m.get("content", "") or "") for m in second_tool_call_messages if isinstance(m, dict))
        assert tool_log.final_verdict == "success"
        print("  T3 tool state carried across turns")

    print("  [PASS] agent.py integration")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("Harness Engineering Framework — Smoke Test")
    print("=" * 50)

    tests = [
        ("metrics.py",           test_metrics),
        ("arcc.py",              test_arcc),
        ("ground_truth.py",      test_ground_truth),
        ("harness.py",           test_harness),
        ("embedding.py",         test_embedding),
        ("tasks.py",             test_tasks),
        ("judge.py",             test_judge),
        ("agent IFRTracker",     test_ifr_tracker),
        ("agent local tools",    test_agent_local_tools),
        ("agent integration",    test_agent_runner_integration),
    ]

    passed, failed = 0, 0
    for name, fn in tests:
        print(f"\n[{name}]")
        try:
            fn()
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {e}")
            import traceback; traceback.print_exc()
            failed += 1

    print(f"\n{'='*50}")
    print(f"Result: {passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
