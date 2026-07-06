# Station 02 — Workflows

> Delivers: chained agentic steps that don't fall over.

## Objective

Compose typed workers from Station 01 into a **workflow DAG** with ordering, retries, and
fan-out/fan-in.

## Concept

- A workflow is a directed graph of workers; edges pass typed values.
- Retries and backoff live at the edge, not inside the worker.
- Fan-out then fan-in: run N workers in parallel, merge their typed results.

## What you build

- A 3-node workflow: fetch -> (summarize x N in parallel) -> merge.
- Per-node retry policy and a merged receipt for the whole run.

## Run

```bash
pnpm --filter 02-workflows dev
```

## Checkpoint

The DAG runs end to end, a forced node failure retries then recovers, and the run emits one
combined receipt. `pnpm --filter 02-workflows test` is green.
