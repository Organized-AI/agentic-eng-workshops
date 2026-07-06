# Workshop 02 — Harness Eng

> Engineer the **harness**: the factory that spawns, coordinates, and merges a pool of agents.

## What this covers

- The harness vs. the model: the scaffolding is where reliability lives.
- An **orchestrator** that decomposes a task, dispatches to a worker pool, and reduces.
- Concurrency, ordering, and merge — the DAG made dynamic at runtime.
- Shared typed primitives every agent in the factory reuses.

## You leave with

- An orchestrator running >=3 subagents concurrently and merging one typed result.
- A nested receipt tree showing what each subagent did.

## Draws on

`modules/05-subagent-orchestration`, `shared/`, and the agent templates in `agents/`.

## Checkpoint

A single request fans out to a worker pool and returns one merged, schema-valid result with
a nested receipt.
