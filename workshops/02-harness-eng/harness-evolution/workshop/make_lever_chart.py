#!/usr/bin/env python3
"""Lever → result dumbbell chart for the workshop.

Shows, per experiment: vanilla harness reward → evolved harness reward, which
lever was pulled, and whether it lifted. The visual form of the "operational
mirror" (config=state, edit=action, benchmark=reward).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# ── data (edit here; add rows as experiments complete) ────────────────────────
EXPERIMENTS = [
    # label, vanilla, evolved, lever, note
    ("Retail · 32B", 0.00, 0.00, "Control", "grading mismatch (strict DB) → no room"),
    ("Telecom · 32B", 0.50, 0.75, "Control / IRMA", "PolicyHint rescues roaming task"),
    # ("Telecom · 8B", None, None, "Control / IRMA", ""),  # fill when done
]

INK = "#14181F"; MUTE = "#6B7280"; LIFT = "#16A34A"; FLAT = "#9CA3AF"; SURF = "#FFFFFF"

fig, ax = plt.subplots(figsize=(9.5, 3.6), dpi=200)
fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)

ys = list(range(len(EXPERIMENTS)))[::-1]
for y, (label, v, e, lever, note) in zip(ys, EXPERIMENTS):
    lifted = e > v
    col = LIFT if lifted else FLAT
    # connector
    if e != v:
        ax.add_patch(FancyArrowPatch((v, y), (e, y), arrowstyle="-|>", mutation_scale=16,
                     lw=3, color=col, shrinkA=6, shrinkB=6, zorder=2))
    else:
        ax.plot([v-0.008, v+0.008], [y, y], color=col, lw=3, zorder=2)
    # vanilla (hollow) + evolved (solid)
    ax.scatter([v], [y], s=150, facecolor=SURF, edgecolor=MUTE, lw=2.2, zorder=3)
    ax.scatter([e], [y], s=170, facecolor=col, edgecolor=SURF, lw=2.2, zorder=4)
    # value labels
    ax.text(v, y+0.22, f"{v:.2f}", ha="center", va="bottom", fontsize=11, color=MUTE)
    ax.text(e, y+0.22, f"{e:.2f}", ha="center", va="bottom", fontsize=11, color=col, fontweight="bold")
    # row label + lever
    ax.text(-0.03, y, label, ha="right", va="center", fontsize=12.5, color=INK, fontweight="bold")
    delta = f"+{e-v:.2f}" if lifted else "±0.00"
    tag = f"{lever}   {delta}"
    ax.text(1.02, y, tag, ha="left", va="center", fontsize=11,
            color=(LIFT if lifted else MUTE), fontweight="bold")
    ax.text(1.02, y-0.28, note, ha="left", va="center", fontsize=8.5, color=MUTE)

ax.set_xlim(-0.02, 1.0); ax.set_ylim(-0.7, len(EXPERIMENTS)-0.3)
ax.set_yticks([])
ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_xticklabels(["0", ".25", ".50", ".75", "1.0"], fontsize=10, color=MUTE)
for sp in ["top", "right", "left"]:
    ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color("#E5E7EB")
ax.tick_params(length=0)
ax.set_xlabel("avg benchmark reward   (○ vanilla harness  →  ● evolved harness · same frozen model)",
              fontsize=10.5, color=INK)
ax.set_title("Which lever moved the number — harness evolution, weights frozen",
             fontsize=14, color=INK, fontweight="bold", pad=14, loc="left")
plt.subplots_adjust(left=0.16, right=0.72, top=0.82, bottom=0.20)
plt.savefig("workshop/lever-result-chart.png", facecolor=SURF)
print("wrote workshop/lever-result-chart.png")
