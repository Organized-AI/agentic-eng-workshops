# Moved

**Harness Eng is now Workshop 04** → see [`../04-harness-eng/`](../04-harness-eng/).

This folder is a leftover from a renumbering and can be safely deleted:

- The harness vs. the model: the scaffolding is where reliability lives.
- An **orchestrator** that decomposes a task, dispatches to a worker pool, and reduces.
- Concurrency, ordering, and merge — the DAG made dynamic at runtime.
- Shared typed primitives every agent in the factory reuses.

## You leave with

- An orchestrator running >=3 subagents concurrently and merging one typed result.
- A nested receipt tree showing what each subagent did.

## Draws on

`modules/05-subagent-orchestration`, `shared/`, and the agent templates in `agents/`.

## Checkpoint

A single request fans out to a worker pool and returns one merged, schema-valid result with
a nested receipt.

---

## Companion lab — Evolve the Harness → [`harness-evolution/`](harness-evolution/)

A second angle on harness engineering: don't just *build* the harness — **evolve** it against a
vertical benchmark. A hands-on Python lab where you run a **frozen** local model, read the traces, and
pull the right lever (prompt / tool / processor / config) to lift the score — the closed loop of agentic RL.

- **Start:** [`harness-evolution/workshop/HANDS-ON.md`](harness-evolution/workshop/HANDS-ON.md)
- **Deck (Gamma-ready):** [`harness-evolution/SLIDE-DECK.md`](harness-evolution/SLIDE-DECK.md)
- **Results (frozen model, harness-only):** Control τ²-telecom 0.50→0.75 · Instruction GSM8K 0.65→0.97 ·
  Action private-KB 0.00→1.00.

> Note: this sub-lab is **Python** (built on HarnessX + τ²-bench), self-contained under `harness-evolution/`
> — it runs independently of the repo's TypeScript stations.
```bash
git rm -r workshops/02-harness-eng && git commit -m "Remove stale 02-harness-eng" && git push
```
