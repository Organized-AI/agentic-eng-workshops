#!/usr/bin/env python3
"""Reasoning-lever chart: vanilla vs reflect accuracy on CRT + GSM8K.
Frozen qwen3:8B; only the reasoning scaffold changes."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from pathlib import Path

# (label, vanilla, reflect, note)
ROWS = [
    ("GSM8K (40)", 0.650, 0.975, "+0.325 · standard bench · re-derive & self-check"),
    ("CRT traps (15)", 0.533, 0.733, "+0.200 · fixes intuitive traps"),
]
INK="#14181F"; MUTE="#6B7280"; LIFT="#16A34A"; SURF="#FFFFFF"
fig, ax = plt.subplots(figsize=(9.5, 3.0), dpi=200); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
ys = list(range(len(ROWS)))[::-1]
for y,(lbl,v,e,note) in zip(ys,ROWS):
    ax.add_patch(FancyArrowPatch((v,y),(e,y),arrowstyle="-|>",mutation_scale=16,lw=3,color=LIFT,shrinkA=6,shrinkB=6,zorder=2))
    ax.scatter([v],[y],s=150,facecolor=SURF,edgecolor=MUTE,lw=2.2,zorder=3)
    ax.scatter([e],[y],s=170,facecolor=LIFT,edgecolor=SURF,lw=2.2,zorder=4)
    ax.text(v,y+0.24,f"{v:.2f}",ha="center",va="bottom",fontsize=11,color=MUTE)
    ax.text(e,y+0.24,f"{e:.2f}",ha="center",va="bottom",fontsize=11,color=LIFT,fontweight="bold")
    ax.text(-0.03,y,lbl,ha="right",va="center",fontsize=12,color=INK,fontweight="bold",transform=ax.get_yaxis_transform())
    ax.text(1.02,y,note,ha="left",va="center",fontsize=9.5,color=MUTE,transform=ax.get_yaxis_transform())
ax.set_xlim(0.4,1.0); ax.set_ylim(-0.6,len(ROWS)-0.4); ax.set_yticks([])
ax.set_xticks([0.4,0.5,0.6,0.7,0.8,0.9,1.0]); ax.tick_params(length=0,labelsize=9,colors=MUTE)
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color("#E5E7EB")
ax.set_xlabel("accuracy   (○ vanilla harness  →  ● reflect scaffold · same frozen qwen3:8B)",fontsize=10.5,color=INK)
ax.set_title("Reasoning lever: the harness elicits latent reasoning",fontsize=14,color=INK,fontweight="bold",pad=12,loc="left")
plt.subplots_adjust(left=0.22,right=0.72,top=0.80,bottom=0.22)
out=Path(__file__).resolve().parent/"reasoning-chart.png"; plt.savefig(out,facecolor=SURF); print("wrote",out)
