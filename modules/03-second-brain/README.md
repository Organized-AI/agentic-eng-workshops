# Station 03 — Second Brain

> Delivers: **"second brains"** — memory your agents can query.

## Objective

Give the stack a **knowledge graph + memory** layer: ingest documents, extract entities and
relationships, and retrieve relevant context for a worker.

## Concept

- Memory is a retrieval problem: ingest -> index -> retrieve -> ground.
- A knowledge graph captures entities + relationships, not just embeddings.
- Workers become context-aware by querying the brain before they run.

## What you build

- An ingest worker that writes to a memory store (mem0 / local KG).
- A retrieve step that pulls top-k context and grounds a Station 01 worker.

## Run

```bash
pnpm --filter 03-second-brain dev
```

## Checkpoint

Ingest a small corpus, ask a question, and confirm the answer cites retrieved context.
`pnpm --filter 03-second-brain test` is green.

## Uses

mem0 setup already on the build machine (see `MEM0_SETUP_GUIDE.md`). `MEM0_API_KEY` optional
if running local.
