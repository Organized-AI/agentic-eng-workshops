# Station 06 — Browser QA

> Delivers: **"verify outputs."**

## Objective

Close the loop: use a **headless browser** to verify an agent's output actually does what it
claims (renders, links work, values match).

## Concept

- Trust, but verify. An agent claiming success isn't proof of success.
- A verification loop turns "looks done" into "checked done."
- Failures feed back — a hook into Station 08's self-improvement loop.

## What you build

- A Playwright-based verifier that loads generated output and asserts on it.
- A pass/fail verdict emitted as a receipt attached to the original worker run.

## Run

```bash
pnpm --filter 06-browser-qa dev
```

## Checkpoint

Good output verifies pass, deliberately broken output verifies fail, and both produce a
receipt. `pnpm --filter 06-browser-qa test` is green.
