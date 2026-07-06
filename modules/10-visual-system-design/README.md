# Station 10 — Visual System Design

> Delivers: **"ship visible systems with receipts."** The payoff screen.

## Objective

Build a **live dashboard** that renders the whole stack: workers, routes, orchestration
tree, verification verdicts, and receipts — the system made visible.

## Concept

- A system you can't see is a system you can't trust. Make it visible.
- The dashboard reads the receipts from Station 07 and renders them live.
- This is what's on screen at the close: the stack, working, with proof.

## What you build

- A dashboard (`dashboard/`) that streams receipts and shows: active workers, routing
  decisions, orchestration tree, QA pass/fail, token + cost totals.
- Deployed as Cloudflare Worker Assets alongside Station 09.

## Run

```bash
pnpm --filter dashboard dev
```

## Checkpoint

Trigger a Station 05 orchestration and watch the dashboard render the full receipt tree live.
The stack is visible, end to end.

## Note

When deploying the HTML, use GSAP for transitions/interactivity per the house UI/UX standard.
