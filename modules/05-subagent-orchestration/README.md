# Station 05 — Subagent Orchestration

> Delivers: **"coordinate agent factories."**

## Objective

Build an **orchestrator** that spawns and coordinates a pool of subagents (workers), then
merges their results — the agent factory.

## Concept

- One orchestrator, many workers. The orchestrator plans, dispatches, and reduces.
- Subagents run concurrently; the orchestrator owns ordering and merge.
- This is Station 02's DAG made dynamic: the graph is decided at runtime.

## What you build

- An orchestrator that decomposes a task into subtasks, dispatches to a worker pool, and
  merges typed results into one output — with a combined receipt tree.

## Run

```bash
pnpm --filter 05-subagent-orchestration dev
```

## Checkpoint

A single request fans out to >=3 subagents and returns one merged, schema-valid result with
a nested receipt. `pnpm --filter 05-subagent-orchestration test` is green.
