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

## Checkpoint

Trigger a Harness Eng orchestration and watch the dashboard render the full receipt tree
live — good output verifies pass, broken output verifies fail.
