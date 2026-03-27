# Phase 1 Execution Plan (Ch.4 → Ch.5 → Ch.2/6/7)

Date: 2026-03-20  
Owner: Codex (execution support)  
Status: Approved-for-run

## Goal

This plan is the execution bridge for the agreed strategy:

1. Complete Ch.4 numeric evidence first (`[X]` removal input)
2. Write Ch.5 as analysis-only from measured outputs
3. Calibrate claim strength in Ch.2/Ch.6/Ch.7 to measured ranges

## Scope (Phase 1)

Run only the minimum experiments that unlock downstream writing:

- `E04` Harness on/off baseline
- `E08` Token-budget pressure sweep
- `E10` Model capability floor (self-reporting reliability)

## Why These Three First

- `E04` provides the baseline contrast (without this, later bottleneck analysis is weak).
- `E08` gives the budget-pressure curve needed for Ch.4 §2 and Ch.5 cost/reliability translation.
- `E10` provides the lower-bound anchor for Agent-2 transition language (Ch.7 claims cannot be fixed without it).

## Execution Protocol

- Runtime: `experiments/framework` (actual agent runner; no mock mode for this phase)
- API backend: OpenRouter (key loaded from local secure file path)
- Logging artifacts:
  - machine-readable: `experiments/results/phase1/phase1-results.json`
  - narrative summary: `experiments/results/phase1/phase1-results.md`
- Reproducibility:
  - deterministic seeds for task fixtures
  - run counts fixed per experiment in this phase

## Experiment Design (Phase 1)

### E04 — Harness Baseline

- Task types: `T1` (code review), `T2` (multi-step planning), both `MODERATE`
- Condition A: harness `full`
- Condition B: harness `none`
- Repeats: 6 runs per condition per task (24 total)
- Primary outputs:
  - TCR
  - RSuccR
  - TTFF distribution
  - TCA / IFR aggregate

### E08 — Token Budget Sweep

- Task type: `T3` (`MODERATE`)
- Harness: `full`
- Budget ratios: `1.00, 0.75, 0.50, 0.25`
- Repeats: 4 runs per ratio (16 total)
- Primary outputs:
  - TCR by budget ratio
  - token usage / step profile
  - IFR / TCA degradation pattern

### E10 — Capability Floor

- Task type: `T1` (`MODERATE`)
- Harness: `none` (pure model self-report behavior)
- Model lineup (user-selected, 2026-03 agent-targeted set):
  - `nvidia/nemotron-3-super-120b-a12b`
  - `openai/gpt-5.4-nano`
  - `qwen/qwen3.5-9b`
  - `openai/gpt-5.4-pro`
  - `google/gemini-3.1-flash-lite-preview`
- Repeats: pilot 2 runs/model, then scale-up to 6+ runs/model
- Primary outputs:
  - TCR by tier
  - Self-reporting accuracy (SAA-style)
  - Calibration error (ECE)
  - Pairwise significance test (two-proportion z + Holm correction)

## Operational Note (OpenRouter)

- `openai/gpt-5.4-*` family is executed with `max_output_tokens` routing compatibility.
- `openai/gpt-5.4-pro` can show high latency/credit pressure in long-run loops, so it is time-boxed as a separate track from the 4-model stable matrix.

## Output-to-Chapter Mapping

- Ch.4 inputs:
  - E04 baseline deltas
  - E08 budget-phase transition indicators
  - E10 floor estimate signals
- Ch.5 inputs:
  - same results translated into reliability/ops language
- Ch.2/6/7 adjustments:
  - claim confidence level reduced/maintained based on measured spread

## Phase Exit Criteria

Phase 1 is complete only if all are satisfied:

- `phase1-results.json` generated
- `phase1-results.md` generated
- each experiment has non-empty metrics table
- explicit caveat section included for unstable or sparse signals
