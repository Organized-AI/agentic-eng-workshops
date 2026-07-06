# workshops/ — The 7 Tracks

The event runs as seven hands-on workshops. Each is self-contained (start anywhere) but
ordered so the stack builds on itself. Each track maps to granular build stations in
[`../modules/`](../modules/).

| # | Workshop | Delivers | Draws on (modules) |
|---|----------|----------|--------------------|
| 01 | [Planning](01-planning/) | Typed workers + workflow DAGs | 01-agents, 02-workflows |
| 02 | [Harness Eng](02-harness-eng/) | Orchestrator + worker pool (the factory) | 05-subagent-orchestration, shared/ |
| 03 | [Agent Loops / RSI](03-agent-loops-rsi/) | Eval → critique → patch loop | 08-recursive-self-improvement |
| 04 | [Local AI](04-local-ai/) | Local models + edge deploy | 09-deployment, local runtimes |
| 05 | [Tokenomics](05-tokenomics/) | Cost-aware routing + budgets | 04-model-routing |
| 06 | [2nd Brain](06-second-brain/) | Knowledge graph + memory | 03-second-brain |
| 07 | [Observability](07-observability/) | Receipts, verification, dashboard | 06-browser-qa, 07-telemetry, 10-visual-system-design |

## The arc

```
Plan it  →  Harness it  →  Loop it  →  Run it local  →  Price it  →  Give it memory  →  See it
  01           02            03           04              05             06                07
```

Every track ends at a **checkpoint** so the room stays synced.
