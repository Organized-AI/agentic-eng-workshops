# Workshop 05 — Tokenomics

> The economics of tokens: **route by cost, latency, and quality** with budgets and fallback.

## What this covers

- Not every task needs the biggest model — route cheap tasks cheap.
- A route as a **policy**: pick by constraint, fall back on error or timeout.
- Budgets and cost ceilings enforced per run, surfaced in the receipt.
- Reading token receipts to find where the money actually goes.

## You leave with

- A `route()` primitive: policy in, chosen model + call out, with a fallback chain.
- Receipts that record which model served and what it cost.

## Draws on

`modules/04-model-routing`, `shared/src/router.ts`, and Observability's receipts.

## Checkpoint

A cheap task routes to the cheap model; a forced primary failure falls back; the receipt
records the decision and the cost.
