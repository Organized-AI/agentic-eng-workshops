# Station 08 — Recursive Self-Improvement

> Delivers: **"recursive self-improvement."**

## Objective

Build an **eval -> critique -> patch -> re-eval** loop so a worker improves its own output
until it passes.

## Concept

- Generate, then judge. A critic scores output against a rubric.
- If it fails, patch the prompt/args and try again — bounded by a max iteration count.
- Station 06's verifier and Station 07's receipts feed the eval signal.

## What you build

- An eval harness with a rubric, a critique step, and a patch step in a bounded loop.
- A receipt showing the score trajectory across iterations.

## Run

```bash
pnpm --filter 08-recursive-self-improvement dev
```

## Checkpoint

A worker that fails the rubric on pass 1 improves to passing within the iteration budget, and
the receipt shows the climb. `pnpm --filter 08-recursive-self-improvement test` is green.
