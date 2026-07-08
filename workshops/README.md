# workshops/ — The 7 Tracks

The event runs as seven hands-on workshops. Each is self-contained (start anywhere) but
ordered so the stack builds on itself. Each track maps to granular build stations in
[`../modules/`](../modules/).

| # | Workshop | Delivers | Draws on (modules) |
|---|----------|----------|--------------------|
| 01 | [Planning](01-planning/) | Typed workers + workflow DAGs | 01-agents, 02-workflows |
| 02 | [Giving Agents Data](02-giving-agents-data/) | Tools, MCP, APIs + retrieval at runtime | 03-second-brain (retrieval), tool/MCP |
| 03 | [Agent Loops / RSI](03-agent-loops-rsi/) | Eval → critique → patch loop | 08-recursive-self-improvement |
| 04 | [Harness Eng](04-harness-eng/) | Orchestrator + worker pool (the factory) | 05-subagent-orchestration, shared/ |
| 05 | [Tokenomics](05-tokenomics/) | Cost-aware routing + budgets | 04-model-routing |
| 06 | [2nd Brain](06-second-brain/) | Knowledge graph + memory | 03-second-brain (memory/KG) |
| 07 | [Observability](07-observability/) | Receipts, verification, dashboard | 06-browser-qa, 07-telemetry, 10-visual-system-design |

> Deployment (`modules/09-deployment`) is cross-cutting infra used by Harness Eng and
> Observability rather than a standalone track.

## The arc

```
Plan it -> Feed it -> Loop it -> Harness it -> Price it -> Remember it -> See it
  01         02         03          04           05           06            07
```

Every track ends at a **checkpoint** so the room stays synced.
