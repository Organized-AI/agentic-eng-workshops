# Workshop 05 Lab: route(), fallback, budget + receipts

> Three standalone TypeScript stages that build this station's `route()` primitive, from the live Tokenomics session (July 11, 2026).

## Objective

Build a router that picks the cheapest model clearing a policy, falls back on failure, enforces a per-session budget, and prints a receipt for every decision.

## Concept

- A route is a **policy** (cost-sensitive or quality-first), not a hardcoded model name.
- Fallback chains hop down an ordered list on error or timeout, and the receipt records the hop.
- A budget ceiling can force a below-policy model; the receipt **discloses** the tradeoff instead of hiding it.
- Pricing anchors are real published list prices (July 2026), so the cost model teaches real numbers.

## What you build

| File | Stage | Adds |
|---|---|---|
| `stage1-route.ts` | 1: policy routing | `route(task, policy)`: cheapest model that clears a cost/latency/quality policy |
| `stage2-fallback.ts` | 2: fallback chain | Ordered model chain, forced-failure demo, hop recorded in the receipt |
| `stage3-budget-receipts.ts` | 3: budget + receipts | Per-session budget ceiling, full receipts ledger, disclosure when budget forces a tradeoff |

Each file is standalone (no imports between them). Stage 3 is cumulative: running it once exercises all three checkpoint criteria.

## Run

No install, no API keys. Mock mode (simulated cost, latency, and failure) is the only mode. Requires Node 20+.

```bash
npx tsx stage1-route.ts
npx tsx stage2-fallback.ts
npx tsx stage3-budget-receipts.ts
```

## Checkpoint

A cheap task routes to the cheap model; a forced primary failure falls back; the receipt records the decision and the cost. All three print as PASS lines at the end of stage 3.

## Uses

The station spec in `../README.md` and `modules/04-model-routing`. More session materials are linked from the station README.
