# Station 07 — Telemetry

> Delivers: **"ship systems with receipts."**

## Objective

Make every worker emit **token + span receipts** so the whole system is observable — the
"receipts" that make it visible.

## Concept

- A receipt = what ran, how long, how many tokens, what it cost, pass/fail.
- Spans nest: a workflow's receipt contains its workers' receipts.
- Observability isn't an add-on; it's the proof the system did the work.

## What you build

- A telemetry layer that wraps `defineWorker` so every run auto-emits a span + token count.
- A receipt aggregator that rolls nested runs into one tree (console or OTEL exporter).

## Run

```bash
pnpm --filter 07-telemetry dev
```

## Checkpoint

Run a Station 02 workflow and get one nested receipt tree with token + latency per node.
`pnpm --filter 07-telemetry test` is green.

## Uses

`shared/src/telemetry.ts`. Optional `OTEL_EXPORTER_OTLP_ENDPOINT`. Pattern reference:
`Organized-AI/openclaw-workshop-infra` (token observability).
