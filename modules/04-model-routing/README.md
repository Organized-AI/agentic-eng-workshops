# Station 04 — Model Routing

> Delivers: **"model routing."**

## Objective

Route each call to the right model by **cost, latency, and quality**, with fallback chains
when a provider fails.

## Concept

- Not every task needs the biggest model. Route cheap tasks cheap.
- A route is a policy: pick by constraint, fall back on error or timeout.
- The router is a worker too — typed in, typed out, receipt on the way out.

## What you build

- A `route()` primitive: policy in, chosen model + call out.
- A fallback chain (primary -> secondary) with a receipt noting which model served.

## Run

```bash
pnpm --filter 04-model-routing dev
```

## Checkpoint

A cheap task routes to the cheap model, a forced primary failure falls back, and the receipt
records the decision. `pnpm --filter 04-model-routing test` is green.

## Uses

`shared/src/router.ts`. Optional `OPENAI_API_KEY` / `OPENROUTER_API_KEY` for real fallback.
