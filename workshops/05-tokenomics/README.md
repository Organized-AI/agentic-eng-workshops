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

## Materials from the live session (July 11, 2026: Christopher, Ovae)

- **Presentation:** [ovae.ai/workshop](https://ovae.ai/workshop)
- **Your own token receipt** (runs locally, nothing leaves your machine):
  `curl -sL ovae.ai/workshop/receipt.py | python3`, or start at [ovae.ai/workshop/start](https://ovae.ai/workshop/start)
- **Deep audit prompt** (Claude Code in the terminal, not the chat app): [ovae.ai/workshop/audit.md](https://ovae.ai/workshop/audit.md)
- **Conductor:** the routing layer from the talk, one-command install and uninstall: [conductorskill.com](https://conductorskill.com)
- **EBI:** the improvement-loop skill: [ebiskill.com](https://ebiskill.com)
- **Build-along lab for this station:** [./lab](./lab) (three standalone stages, mock mode, no API keys needed)
