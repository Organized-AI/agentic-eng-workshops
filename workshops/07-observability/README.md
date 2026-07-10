# Workshop 07 — Observability

> Make the system visible: **receipts, verification, and a live dashboard.**

## What this covers

- A **receipt** = what ran, how long, how many tokens, what it cost, pass/fail.
- Nested spans: a workflow's receipt contains its workers' receipts.
- **Browser QA** — verify outputs actually do what they claim (headless loop).
- A dashboard that renders the whole stack live: workers, routes, QA, cost totals.
- "Ship visible systems with receipts" — the proof the system did the work.

## You leave with

- A telemetry layer wrapping every worker so runs auto-emit spans + token counts.
- A verifier that pass/fails generated output, attached to the run.
- A live dashboard reading those receipts.

## Draws on

`modules/06-browser-qa`, `modules/07-telemetry`, `modules/10-visual-system-design`,
`shared/src/telemetry.ts`. Pattern reference: `Organized-AI/openclaw-workshop-infra`.
Deploy the dashboard HTML as Cloudflare Worker Assets with GSAP for interactivity.

## Presentation

The **Observe · Trace · Rank** lightning talk — a live, deployed instance of
exactly this workshop's promise: agent events → CF Queue → D1 (truth) → KV (hot)
→ a live leaderboard, with the board ranking the account's own real deployed
Workers.

- **Live:** <https://talk.organizedai.vip/Observability-Talk/>
- **Local:** [`presentation/index.html`](presentation/index.html) — a self-contained
  21-slide GSAP/Three.js deck (Cloudflare Worker Assets). Open it directly or serve
  the folder statically.

Interactive diagrams embedded in the deck (each a standalone page):

| File | Diagram |
|------|---------|
| [`presentation/district.html`](presentation/district.html) | Observability District — the loop as a walkable 3D city |
| [`presentation/agentic-fit.html`](presentation/agentic-fit.html) | Agentic Loop Factory |
| [`presentation/zine-build-factory.html`](presentation/zine-build-factory.html) | Vertical Zine Exploded Factory |
| [`presentation/jockey/index.html?view=catalogue`](presentation/jockey/) | Jockey Ad Forge — Catalogue Building cutaway |

> The deck reads its leaderboard from `/api/leaderboard` (KV → D1 → demo) and
> degrades to a baked real-Worker snapshot when served statically, so it renders
> anywhere without the backend.

## Checkpoint

Trigger a Harness Eng orchestration and watch the dashboard render the full receipt tree
live — good output verifies pass, broken output verifies fail.
