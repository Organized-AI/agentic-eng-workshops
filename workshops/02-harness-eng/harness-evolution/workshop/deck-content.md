# Deck source — Evolve the Harness, Not the Model
(placeholders: {{BASELINE}}, {{EVOLVED}}, {{DELTA}} filled from local run)

## Slide 1 — Title
**Evolve the Harness, Not (Just) the Model**
Reinforcement learning on agent harnesses — reproduced locally on a frozen model
Workshop · HarnessX + "Don't Train the Model, Evolve the Harness"

## Slide 2 — The hook
> "A frozen open model that solves **0% of Harvey's Legal Agent Benchmark end to end**
> is not as weak as that score looks. Zero model weights changed."
- Same model. Change the *wrapper*. Double-digit accuracy gains.
- The question isn't "which model" — it's "which harness."

## Slide 3 — What is a "harness"?
The runtime wrapper around the model: context assembly · tools · memory · control flow ·
error recovery · evaluation. `agent = model.agentic(harness)`.
- Model = fixed reasoning ceiling.
- Harness = how much of that ceiling you actually realize.

## Slide 4 — Thesis
**Vanilla off-the-shelf harnesses are fine at baseline. Vertical-specific use cases need the
harness to evolve with them — or you design your own.**
Because each domain *fails differently*, one harness can't serve every vertical.

## Slide 5 — Two papers, one idea
| | HarnessX (arXiv:2606.14249) | "Evolve the Harness" (Niklaus) |
|--|--|--|
| Method | MetaAgent.evolve() over trajectories | Meta-Harness proposer + gate |
| Model | frozen Qwen3.5-9B / GPT-5 | frozen DeepSeek-V4-Pro |
| Result | +14.5% avg, up to +44% | 63.4% → 80.1% (+16.7pp) |
Both: **zero weight changes.**

## Slide 6 — How harness evolution works (the loop)
R0 run tasks → judge trajectories → meta-agent reads failures → writes new config.yaml →
gate (keep if reward↑ past tolerance, else revert) → R1 … 
It's harness-edit-as-MDP: state=config+traces, action=one edit, reward=gated pass delta.

## Slide 7 — Why it works (the core teaching)
Most failures are **not reasoning failures — they're harness failures**:
wrong file path · chunked-write corruption · malformed tool JSON · context overflow ·
loop-without-progress · premature/wrong-context action.
> "For a weak agent, a lot of 'capability' is I/O discipline the scaffold can guarantee."

## Slide 8 — The punchline: code beats prompts
> "**Five of the top six harnesses are deterministic code, not prompt edits.**"
Prompt edits are local + brittle + don't transfer across models. Code fixes are structural + portable.

## Slide 9 — Inverse scaling
The **weakest** model gains the most. ALFWorld Qwen3.5-9B: **53 → 97 (+44)** vs Sonnet 83→95 (+11).
Harness evolution makes small/cheap models punch up. (Caveat: a capability floor exists.)

## Slide 10 — Vertical-specific harnesses
τ²-Bench = real business verticals: **retail · airline · telecom**. Evolve each independently.
Reference (retail, Qwen3.5-27B agent): 0.807 → **0.965**, 18/22 badcases fixed.
Database domain elsewhere: 0% → 53.8%. Each vertical needs different processors.

## Slide 11 — Our reproduction: the "before"
Vanilla harness (`harness_config_base.yaml`): system prompt + token budget. That's it.
No loop detection. No parse retry. No tool correction. No tool filtering.
Frozen local model (qwen3, via Ollama/llama.cpp). Local baseline: **{{BASELINE}}**

## Slide 12 — The "after" — what the meta-agent added
6 deterministic processors, 0 prompt edits:
- LoopDetection · ParseRetry · **ToolCallCorrection** · ToolFailureGuard
- **PhaseAwareToolFilter** (read-only until step 2 — no premature writes)
- StopGuard (+8pp on retail alone) · IRMA policy hints
Local evolved: **{{EVOLVED}}**  (Δ {{DELTA}}), same frozen model.

## Slide 13 — The meta-agent is *you* (Claude Code)
The evolve() step = an agent that reads traces + writes config. We used Claude Code directly:
read failure trajectories → diagnose pattern → author processor → re-eval → keep if it gates.
No RL training, no GPU. The loop runs on a laptop.

## Slide 14 — Reproduce it
`uv` + Ollama + one fork. `make baseline` → (Claude Code evolves) → `make eval`.
Gotcha we hit: `LLAMA_API_KEY` in your shell 401s all local inference — `unset` it.
Fork: github.com/epuerta9/HarnessX (branch workshop/harness-evolution)

## Slide 15 — Takeaways
1. The harness, not just the model, determines agent performance.
2. Vertical-specific → evolve (or design) a vertical-specific harness.
3. The wins are mostly deterministic code — testable, portable, versionable.
4. Own your harness components: optimization tracks business-need drift.
5. Weakest models gain most — harness evolution is how small models punch up.
