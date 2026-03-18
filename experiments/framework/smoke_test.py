"""
Framework smoke test — API call 없이 측정 도구만 검증.
실험 인프라를 실행하기 전 반드시 통과해야 한다.

실행: python3 -m framework.smoke_test  (experiments/ 디렉토리에서)
"""
import sys
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

    # T2
    plan = '[{"step": 1, "action": "install_A"}, {"step": 2, "action": "install_B"}]'
    constraints = [{"type": "dependency", "before": "install_A", "after": "install_B"}]
    result = validate_t2(plan, constraints)
    assert result.verdict == "pass"
    print(f"  T2 verdict = {result.verdict} (score={result.score:.3f})")

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


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("Harness Engineering Framework — Smoke Test")
    print("=" * 50)

    tests = [
        ("metrics.py",      test_metrics),
        ("arcc.py",         test_arcc),
        ("ground_truth.py", test_ground_truth),
        ("harness.py",      test_harness),
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
