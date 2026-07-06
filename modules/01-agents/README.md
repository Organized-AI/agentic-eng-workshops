# Station 01 — Agents

> Delivers: **"turn prompts into typed workers."**

## Objective

Take a plain prompt and wrap it into a **typed worker**: defined input schema, defined
output schema, validated at the boundary, retryable, and receipt-emitting.

## Concept

- A prompt is a string; a worker is a **contract**. Contracts compose; strings don't.
- Input and output are validated with zod. Bad output fails loud, not silently.
- `defineWorker({ input, output, run })` is the primitive every later station builds on.

## What you build

- A `summarize` worker: `{ text }` in, `{ summary, bullets }` out.
- Schema validation on both sides; a retry on invalid output.
- A telemetry receipt (tokens + latency) emitted per run.

## Run

```bash
pnpm --filter 01-agents dev
```

## Checkpoint

You pass when: valid input produces schema-valid output, malformed model output triggers a
retry, and a receipt is printed. `pnpm --filter 01-agents test` is green.

## Uses

`shared/src/worker.ts`, `shared/src/schema.ts`, `shared/src/telemetry.ts`.
