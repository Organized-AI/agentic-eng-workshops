#!/usr/bin/env python3
"""The spectrum of harness value — three levers, three value types, real numbers.
Frozen model throughout; only the harness changes."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from pathlib import Path

# label, vanilla, evolved, value-type
ROWS = [
    ("Action · private KB\n(tool: kb_search)", 0.00, 1.00, "ADDS capability — can't → can"),
    ("Instruction · GSM8K\n(reflect scaffold)", 0.65, 0.975, "reshapes realized reasoning"),
    ("Control · telecom\n(IRMA policy alert)", 0.50, 0.75, "recovers latent capability (crutch)"),
]
INK="#14181F"; MUTE="#6B7280"; LIFT="#16A34A"; SURF="#FFFFFF"
fig, ax = plt.subplots(figsize=(10.5, 3.7), dpi=200); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
ys = list(range(len(ROWS)))[::-1]
for y,(lbl,v,e,note) in zip(ys,ROWS):
    ax.add_patch(FancyArrowPatch((v,y),(e,y),arrowstyle="-|>",mutation_scale=17,lw=3.2,color=LIFT,shrinkA=6,shrinkB=6,zorder=2))
    ax.scatter([v],[y],s=160,facecolor=SURF,edgecolor=MUTE,lw=2.2,zorder=3)
    ax.scatter([e],[y],s=180,facecolor=LIFT,edgecolor=SURF,lw=2.2,zorder=4)
    ax.text(v,y+0.26,f"{v:.2f}",ha="center",va="bottom",fontsize=11,color=MUTE)
    ax.text(e,y+0.26,f"{e:.2f}",ha="center",va="bottom",fontsize=11.5,color=LIFT,fontweight="bold")
    ax.text(-0.035,y,lbl,ha="right",va="center",fontsize=11,color=INK,fontweight="bold",transform=ax.get_yaxis_transform())
    ax.text(1.02,y,note,ha="left",va="center",fontsize=10,color=MUTE,transform=ax.get_yaxis_transform())
ax.set_xlim(-0.02,1.02); ax.set_ylim(-0.6,len(ROWS)-0.4); ax.set_yticks([])
ax.set_xticks([0,0.25,0.5,0.75,1.0]); ax.tick_params(length=0,labelsize=9,colors=MUTE)
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color("#E5E7EB")
ax.set_xlabel("benchmark score   (○ vanilla harness → ● evolved · SAME frozen qwen3 throughout)",fontsize=10.5,color=INK)
ax.set_title("The spectrum of harness value — crutch → reshape → add",fontsize=15,color=INK,fontweight="bold",pad=12,loc="left")
plt.subplots_adjust(left=0.27,right=0.70,top=0.82,bottom=0.20)
out=Path(__file__).resolve().parent/"levers-spectrum-chart.png"; plt.savefig(out,facecolor=SURF); print("wrote",out)
