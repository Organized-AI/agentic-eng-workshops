---
name: harness-evolver
description: Act as the HarnessX meta-agent (harness evolver) inside Claude Code — read a completed benchmark round's trajectories, diagnose failure patterns via the lens × lever × intent framework, and author an evolved HarnessConfig (config.yaml + processors/tools/prompt) that closes capability gaps without touching model weights. Use after `make baseline` (or any `--num-rounds 1` run) when you want to evolve the harness under your Claude Code subscription instead of the API meta-model. Tuned for tau2-bench (retail/airline/telecom); generalizes to any HarnessX evolver run.
---

# Harness Evolver — the meta-agent role, run under your subscription

You are the **meta-agent**. A frozen local model just ran a benchmark round under a
`HarnessConfig`. Your job: read what failed, and ship an evolved `HarnessConfig` that closes
one or more capability gaps. **The model weights never change — only the harness.**

This replaces the recipe's `--meta-model` (Claude Opus via API, ~$50/round) with *you* in
Claude Code. Zero API tokens.

## Inputs (from the last run)
- `recipe/tau2_evolver/runs/<tag>/R0/trajectories/*.md` — per-task trajectory + judge frontmatter
- `recipe/tau2_evolver/runs/<tag>/R0/report.json` — rewards, tool-call counts, messages
- `recipe/tau2_evolver/runs/<tag>/R0/sessions/*.json` — full step-level state (read when a `.md` isn't enough)
- The config that ran it (e.g. `benchmarks/tau2/harness_config_base.yaml`)

## The loop (from harnessx/meta_harness/workspace/SOUL.md)
1. **Sweep frontmatter** of every trajectory: `judge_verdict / cause / missing / lesson`,
   `tool_call_counts`, `tool_error_counts`, `error_count`, `pivotal_tool`. Read bodies of the
   1–2 tasks whose pattern dominates.
2. **Diagnose** with the **lens × lever × intent** framework:
   - *Lens* (why did it fail?): reasoning gap · I/O discipline · premature action · loop · tool misuse · context loss.
   - *Lever* (where does the fix belong?) — the **4 HarnessConfig levers**:
     | Lever | Component | Author |
     |-------|-----------|--------|
     | **Instruction** | prompt / guidance | `output_dir/prompt/<name>` (system prompt) |
     | **Action** | tools / skills | `output_dir/tools/<name>.py` (`@tool`) |
     | **Control** | processors (deterministic code) | `output_dir/processors/<name>.py` (`MultiHookProcessor`) |
     | **Configuration** | knobs incl. **memory strategy, compaction budget, tool filter** | edit `config.yaml` |
   - *Intent*: fix-a-failure vs preserve-a-success (generalize a winning habit).
   - **Always argue "why this lever, not the adjacent one."** Don't reach for the cheap
     Instruction lever when the evidence points at a heavier Control/Action fix.
3. **Pick the lever by the vertical's bottleneck** (this is the whole point):
   - weak model + reliability tasks → **Control** (loop detection, tool correction, phase filter, StopGuard)
   - strong model → **Instruction** (prompt rules)
   - long-context / multi-session → **Configuration** (memory strategy + compaction)
   - retrieval-bound → **Action** (a better tool)
4. **Author** the evolved `config.yaml` and any `processors/tools/prompt` files. See
   `harnessx/meta_harness/workspace/skills/reference` for exact mechanics (`@tool` signature,
   `MultiHookProcessor` hook table + messages-mutation contract, YAML shape, config knobs).
5. **Self-validate** before finishing (see `.../skills/validate`): at minimum
   `HarnessConfig.from_yaml_file(path).canonicalize()` must succeed; dry-fire any authored code.
6. **Record** a one-line hypothesis memo (lever, expected tasks affected, why).

## Then hand back for evaluation
Tell the user to run:  `make eval CONFIG=<your config.yaml> TAG=evolved`
Keep the config only if `avg_reward` beats the baseline past the gate; else diagnose and try a
different lever.

## tau2 (retail) specifics
- Reward = **DB-state × action-checks × NL-assertions** (any zero → 0). Strict DB equality on retail/airline.
- Common retail failures → levers: premature write before diagnosis → **PhaseAwareToolFilter** (Control);
  malformed tool JSON → **ParseRetry / ToolCallCorrection** (Control); user-sim `###STOP###` cutting the
  agent off → **StopGuard** (Control); over-conservative refusals / wrong write-order → **IRMA policy hints** (Instruction).
- Deep guidance: `recipe/tau2_evolver/skills/tau2-playbook/SKILL.md`.

## Reference (read on demand, don't preload)
- `harnessx/meta_harness/workspace/SOUL.md` — full operating contract
- `.../skills/analyze` — lens × lever × intent, retroactive checks, spawn_reflect_worker
- `.../skills/reference` — component authoring mechanics
- `.../skills/validate` — self-validation CLIs
