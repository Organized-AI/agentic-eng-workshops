#!/usr/bin/env python3
"""Summarize the multi-trial component ablation into a per-component attribution
table + a bar chart of marginal contribution. Reads runs/ablate_<name>/.

Run:  python workshop/analyze_ablation.py   (from repo root, after ablate.sh)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "recipe/tau2_evolver/runs"
ORDER = [("vanilla", "—"), ("control_only", "ParseRetry+LoopDet+ToolCorr+PhaseFilter"),
         ("irma_only", "PolicyHint (IRMA)"), ("full", "all")]


def run_avg(tag):
    """Average reward across all trials×tasks for a run tag; None-safe."""
    rep = RUNS / f"ablate_{tag}" / "R0" / "report.json"
    if not rep.exists():
        return None, []
    sims = json.loads(rep.read_text()).get("simulations", [])
    rows = [((s.get("reward_info") or {}).get("reward"), s.get("task_id")) for s in sims]
    vals = [r or 0.0 for r, _ in rows]
    return (sum(vals) / len(vals) if vals else None), rows


def main():
    print(f"{'config':14} {'components':46} {'avg':>6}  {'Δ vs vanilla':>12}")
    print("-" * 84)
    base = None
    results = {}
    for tag, comps in ORDER:
        avg, rows = run_avg(tag)
        results[tag] = avg
        if tag == "vanilla":
            base = avg
        d = "" if (avg is None or base is None) else f"{avg - base:+.3f}"
        print(f"{tag:14} {comps[:46]:46} {('n/a' if avg is None else f'{avg:.3f}'):>6}  {d:>12}")
    print()
    # marginal attribution: IRMA-only Δ vs control-only Δ tells which lever carries the lift
    if all(results.get(k) is not None for k in ("vanilla", "irma_only", "control_only")):
        print(f"IRMA marginal (irma_only - vanilla):    {results['irma_only'] - results['vanilla']:+.3f}")
        print(f"Control marginal (control_only - vanilla): {results['control_only'] - results['vanilla']:+.3f}")
        print("→ the larger marginal is the component that makes the biggest difference on this vertical.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
