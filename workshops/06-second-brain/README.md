# Workshop 06 — 2nd Brain

> Give the stack memory: a **knowledge graph + retrieval** your agents can query.

## What this covers

- Memory as a retrieval problem: ingest → index → retrieve → ground.
- A knowledge graph that captures entities + relationships, not just embeddings.
- Grounding a worker: query the brain before the worker runs.
- Keeping memory fresh and scoped so retrieval stays relevant.

## You leave with

- An ingest worker writing to a memory store (mem0 / local KG).
- A retrieve step that grounds a typed worker in top-k context.

## Draws on

`modules/03-second-brain`, the mem0 setup on the machine (`MEM0_SETUP_GUIDE.md`).

## Checkpoint

Ingest a small corpus, ask a question, and confirm the answer cites retrieved context.
