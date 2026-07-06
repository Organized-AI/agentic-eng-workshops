# Workshop 01 — Planning

> Turn prompts into a plan the machine can execute: **typed workers + workflow DAGs.**

## What this covers

- Why a prompt is a string but a worker is a **contract** — and why contracts compose.
- Defining input/output schemas (zod) so bad output fails loud, not silent.
- Composing typed workers into a **workflow DAG**: ordering, retries, fan-out/fan-in.
- Planning agentic work up front instead of chatting your way into it.

## You leave with

- A `defineWorker()` contract and one real typed worker.
- A small DAG that runs those workers with retries and a merged result.

## Draws on

`modules/01-agents`, `modules/02-workflows`, `shared/src/worker.ts`, `shared/src/schema.ts`.

## Checkpoint

Valid input → schema-valid output; a forced node failure retries then recovers; the run
emits one combined receipt.
