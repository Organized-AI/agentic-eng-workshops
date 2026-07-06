# Workshop 03 — Agent Loops / RSI

> Close the loop: **eval → critique → patch → re-eval** so a worker improves its own output.

## What this covers

- Generate, then judge: a critic scores output against a rubric.
- Bounded self-improvement — patch the prompt/args and retry within an iteration budget.
- Wiring the eval signal from verification (Observability) back into the loop.
- Where recursion helps and where it just burns tokens.

## You leave with

- An eval harness with a rubric, a critique step, and a patch step in a bounded loop.
- A receipt showing the score trajectory across iterations.

## Draws on

`modules/08-recursive-self-improvement`, plus signals from `modules/06-browser-qa`.

## Checkpoint

A worker that fails the rubric on pass 1 improves to passing within the budget, and the
receipt shows the climb.
