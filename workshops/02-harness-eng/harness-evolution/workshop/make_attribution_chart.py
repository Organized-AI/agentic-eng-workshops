#!/usr/bin/env python3
"""Component-attribution chart: marginal Δ reward per component vs vanilla,
from the multi-trial ablation. Reads runs/ablate_<name>/ — reproducible.

Run:  python workshop/make_attribution_chart.py   (after ablate.sh)
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "recipe/tau2_evolver/runs"

def avg(tag):
    rep = RUNS / f"ablate_{tag}" / "R0" / "report.json"
    if not rep.exists():
        return None
    sims = json.loads(rep.read_text()).get("simulations", [])
    # require a reasonably complete run (>= 10 of 12 sims) to trust the average
    if len(sims) < 10:
        return None
    vals = [(s.get("reward_info") or {}).get("reward", 0) or 0 for s in sims]
    return sum(vals) / len(vals)

van = avg("vanilla")
ROWS = [  # label, component group
    ("PolicyHint (IRMA)", "irma_only"),
    ("Control ×5 procs", "control_only"),
    ("Full (control+IRMA)", "full"),
]
data = [(lbl, (avg(tag) - van) if (avg(tag) is not None and van is not None) else None) for lbl, tag in ROWS]
data = [(l, d) for l, d in data if d is not None]

INK="#14181F"; MUTE="#6B7280"; POS="#16A34A"; NEG="#DC2626"; SURF="#FFFFFF"
fig, ax = plt.subplots(figsize=(9.5, max(2.4, 0.9*len(data)+1.4)), dpi=200)
fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)

ys = list(range(len(data)))[::-1]
for y, (lbl, d) in zip(ys, data):
    col = POS if d > 0.001 else (NEG if d < -0.001 else MUTE)
    ax.barh(y, d, height=0.5, color=col, zorder=3)
    ha = "left" if d >= 0 else "right"
    off = 0.008 if d >= 0 else -0.008
    ax.text(d+off, y, f"{d:+.3f}", va="center", ha=ha, fontsize=13, color=col, fontweight="bold")
    # row label parked in the left margin (right-aligned, ends at plot's left edge)
    ax.text(-0.03, y, lbl, va="center", ha="right", fontsize=11.5, color=INK,
            transform=ax.get_yaxis_transform())

ax.axvline(0, color="#9CA3AF", lw=1.2, zorder=2)
lim = max(0.25, max(abs(d) for _, d in data)*1.7)
ax.set_xlim(-lim, lim); ax.set_ylim(-0.6, len(data)-0.4)
ax.set_yticks([])
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color("#E5E7EB"); ax.tick_params(length=0, labelsize=9, colors=MUTE)
ax.set_xlabel("marginal Δ reward vs vanilla  (3 trials × 4 tasks · qwen3:32B telecom)", fontsize=10.5, color=INK)
ax.set_title("Which component makes the difference",
             fontsize=15, color=INK, fontweight="bold", pad=12, loc="left")
plt.subplots_adjust(left=0.30, right=0.94, top=0.80, bottom=0.26)
out = ROOT / "workshop" / "attribution-chart.png"
plt.savefig(out, facecolor=SURF)
print("wrote", out, "| points:", [(l[:20], round(d,3)) for l,d in data])
