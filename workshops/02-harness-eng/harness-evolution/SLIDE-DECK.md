---
tags:
  - type/deck
  - repo/harnessx
  - domain/agent-harness
  - domain/llm
  - project/harness-rd
  - workshop
aliases:
  - Harness Evolution Slide Deck
  - Gamma Deck Source
created: 2026-07-08
---

# Harness Evolution — Slide Deck (Gamma / Claude-Design source)

> **How to use:** each `---`-delimited section is one slide. Paste this whole file into Gamma
> ("Import → Paste text") or Claude Design to generate the PowerPoint. Charts are the `.png`
> files in this folder — keep them alongside this file when exporting. Speaker notes are in
> `> blockquotes`. The **LAB** and **RESULTS** slides are for attendees to fill in during the workshop.

---

## Evolve the Harness, Not (Just) the Model

**Reinforcement learning on agent harnesses — reproduced locally on a frozen model.**

Same weights, a better wrapper. Double-digit gains on real benchmarks — and a loop you drive yourself.

> Opening line: "A frozen model that solves 0% of a task end-to-end is not as weak as that score looks."

---

## Prerequisites — to reproduce the lab

**Hardware:** any Mac/Linux with ~16 GB free RAM (Apple M-series or a GPU helps). We used an M5 Pro / 48 GB.

**Software:**
- [`uv`](https://docs.astral.sh/uv/) (Python env), Python 3.12
- A local OpenAI-compatible inference server: **Ollama** *or* **llama.cpp** (`llama-server`)
- `git`, and one Claude Code session (you are the meta-agent)

**Models (pulled once):** `qwen3:8b` (fast), `qwen3:32b` (stronger). ~5 GB / ~20 GB.

**Repos:**
```bash
git clone <this workshop repo>            # the lab
git clone https://github.com/sierra-research/tau2-bench ~/tau2-bench   # τ² benchmark
cd workshop && make setup                 # uv sync + install + pull models
```

> ⚠️ **Two gotchas we hit (documented in workshop/README):** (1) if `LLAMA_API_KEY` is set in your shell,
> llama.cpp 401s every local call — `unset` it. (2) Start `llama-server` with `--jinja` or tool-calling
> silently breaks and rewards go to 0.

---

## The thesis

**Vanilla, off-the-shelf harnesses are fine at baseline. The more vertical-specific your use case,
the more the harness must evolve with it — or you design your own.**

A frozen model has a fixed reasoning ceiling but a *hugely variable realized score*. The harness
determines how much of the ceiling you actually reach. That gap is where the value is — and it's
**vertical-specific**, because every domain fails differently.

> "The harness — not just the model — determines agent performance." — HarnessX README

---

## What is a vertical agent?

An agent specialized to **one domain's tasks, data, tools, and rules** — customer support for *your*
telecom product, a paralegal for *your* firm, an ops agent over *your* systems.

- The base model is **general**; your vertical is **specific**.
- Off-the-shelf model + off-the-shelf harness → **plateaus**: it doesn't know your data, your policies,
  or your failure modes.
- A vertical agent needs a harness **tuned to its bottleneck** — and a **benchmark that represents its
  real tasks** to tune against.

---

## Why off-the-shelf plateaus (and what fixes it)

The default harness leaves performance on the table because:
- it can't apply **domain I/O discipline** the model doesn't volunteer,
- it lacks **tools/knowledge** specific to your vertical,
- it doesn't **elicit** the reasoning the model is capable of.

Fix: **evolve the harness against a vertical benchmark.** Not by guessing — by reading traces.

---

## The point: close the loop, evolve from traces

> **The techniques are basic. The closed LOOP is the point.**

```
      ┌───────────────────────────────────────────────┐
      ▼                                               │
   run tasks ─▶ TRACES ─▶ read the trace (Claude) ─▶ diagnose failure
   under config   (.md)     judge_cause, expected vs      │
                            executed_actions, errors      ▼
   keep if reward↑ ◀─ REWARD ◀─ re-run ◀─ evolve harness (pick the matching lever)
   (gate) else revert                        + validate
```

Every lever we pulled was chosen **from a trace**, not from a menu. That is the transferable skill —
not "reflect exists," but *read the trace → know which lever → close the loop → re-measure.*

---

## Harness evolution IS reinforcement learning (the "operational mirror")

With the model **frozen**, the harness is the policy being optimized:

| RL concept | In harness evolution |
|-----------|----------------------|
| **State** | the current `HarnessConfig` |
| **Action** | one harness edit = pull a lever |
| **Policy** | a stronger model reading the traces (Claude Code) |
| **Reward** | the benchmark score from the verifier |
| **Rollout / update** | re-run the task set; keep the edit iff reward improves |

> "AEGIS maps harness configs → RL states, edits → actions, traces+verifier → reward." — HarnessX paper

---

## The 4 levers you can tweak

| Lever | Component | Author it as | Wins when… |
|-------|-----------|--------------|-----------|
| **Instruction** | prompts / guidance | system-prompt / reminder | model is strong; reasoning-bound |
| **Action** | tools / skills | a new `@tool` | knowledge/capability-bound |
| **Control** | deterministic processors | `MultiHookProcessor` | model weak/frozen; I/O-discipline-bound |
| **Configuration** | memory, compaction, knobs | edit `config.yaml` | long-context / retune |

**Which lever wins depends on the vertical's bottleneck.** That is *why* one vanilla harness can't serve
every vertical.

---

## The spectrum of harness value — crutch → reshape → add

![The spectrum of harness value](levers-spectrum-chart.png)

- **Control** recovers *latent* capability (a crutch — capped at the model's ceiling).
- **Instruction** reshapes *realized* reasoning.
- **Action** *adds* capability the model never had.

> Same frozen qwen3 throughout. Only the harness changes.

---

## Result 1 — Control lever (τ² telecom, tool-use)

![Which lever moved the number](lever-result-chart.png)

Frozen **qwen3:32B**, same 4 `mobile_data_issue` tasks:
**vanilla 0.50 → IRMA policy-hint 0.75 (+50%)**, zero weight changes, no regressions.

The trace said *"agent never called `enable_roaming`"* → we injected a `[POLICY ALERT]` (Control lever) →
it rescued the roaming task 0.0 → 1.0.

---

## Result 2 — Instruction lever (GSM8K, reasoning)

![Reasoning lever: the harness elicits latent reasoning](reasoning-chart.png)

Frozen **qwen3:8B** on the **GSM8K** standard benchmark:
**vanilla 0.65 → reflect scaffold 0.975 (+0.325)**.

The trace said *"fast intuition, wrong"* → a *re-derive & self-check* scaffold (Instruction lever) →
the model reasons carefully and catches its own errors. Realized reasoning, not plumbing.

---

## Result 3 — Action lever (private knowledge, can't → can)

Frozen **qwen3:8B** on a **private company KB** (made-up, so it can't be memorized):

- **vanilla: 0/12** — every fact hallucinated (Sentinel Arm → $12,500, not $8,450; founded 1998, not 2019).
- **+ `kb_search` tool: 12/12** — it retrieves the fact and answers, including a retrieval+arithmetic question.

**0.00 → 1.00 = genuine new capability.** This is the whole reason vertical agents exist: proprietary
knowledge, tools, and APIs the base model will *never* have in its weights.

---

## Which component makes the biggest difference?

![Which component makes the difference — marginal contribution](attribution-chart.png)

Multi-trial ablation (3 trials) on telecom:
- **PolicyHint (IRMA): +0.167** — carries the entire lift.
- **Control ×5 processors: −0.083** — inert on this vertical.

**Attribution is statistical, not anecdotal.** Single runs mislead (variance ±0.25 ≈ the effect); you need
trials + leave-one-out to know which lever earns its place. *Don't ship inert processors.*

---

## Designing the vertical benchmark is HALF the work

The benchmark **is the reward function** for the loop. No signal → no evolution.

A benchmark you can evolve against needs:
- a **non-zero baseline** (model not floored) · **room** (not at ceiling)
- a **failure mode that matches a lever** · **grading that gives a gradient** (partial credit / enough tasks)

**Evidence:** τ² *retail* (strict DB-equality grading) → 0.00, dead end. τ² *telecom* (lenient
outcome-state) → moves. GSM8K → a clean gradient. **Co-design the harness AND the benchmark.**

---

## What we discovered (the honest findings)

- **Grading choice decides everything** — strict all-or-nothing grading floors a local model; pick a
  benchmark whose grading gives a gradient.
- **The infra layer is silent and decisive** — a `LLAMA_API_KEY` collision and a missing `--jinja` flag
  each sent every reward to 0. *None were framework bugs; all were the runtime harness around it.*
- **Even a reasoning lever depends on plumbing** — our reflect scaffold first scored 0.45 due to a
  token-truncation bug; fixing the I/O took it to 0.975.
- **Don't add a tool the model doesn't need** — a calculator was redundant (the 8B does 4-digit
  arithmetic by hand at 100%). *Knowledge*, not arithmetic, was the real "can't."

---

## How to read a trace (the loop's decision step)

The framework writes `runs/<tag>/R0/trajectories/<task>.md`. The **frontmatter is the dashboard**:

```yaml
exit_reason: "user_stop"          # how it ended
judge_cause: "db_mismatch"         # WHY it failed (the headline)
expected_actions: [find_user, get_order, get_product, get_product, exchange_items]
executed_actions: []               # did it do the right things? (here: none)
failed_actions:  [get_product, exchange_items]   # which step is missing
tool_error_counts: {}              # reliability vs strategy failure
```

Read: `judge_cause` (why) → `expected vs executed` (what) → `failed_actions` (which) →
map cause → lens → **lever**. Full method: KB note 07.

---

## Code — author a Control lever (IRMA reminder)

```python
class RetailExchangeGuide(MultiHookProcessor):
    _order = 3
    async def on_step_start(self, event: StepStartEvent):
        if not _has_exchange_intent(event.raw_messages):
            yield event; return
        # prepend a domain reminder to the system prompt (IRMA)
        yield dataclasses.replace(event,
            system_prompt=_REMINDER + "\n\n" + event.system_prompt)
```

## Code — add an Action lever (a tool)

```python
_KB_TOOL = [{"type": "function", "function": {
    "name": "kb_search", "description": "Search the internal knowledge base.",
    "parameters": {"type": "object",
        "properties": {"query": {"type": "string"}}, "required": ["query"]}}}]
# loop: model → if tool_call: run kb_search(query) → feed result back → repeat → final answer
```

---

## Two value props (don't conflate them)

1. **Harness evolution (frozen model)** — recover latent capability, reshape reasoning, add tools/memory.
   Ceiling = the model's latent ability. **Value = deployment**: make a cheap/frozen model production-grade
   on *your* vertical. *(This whole workshop.)*
2. **Model evolution (RL on the weights / co-evolution)** — actually **raises the ceiling**. HarnessX's
   cross-harness GRPO does this (+4.7% over harness-only). **Needs GPUs; not run here.**

If your gut says "make the model *better*, not patched around" → that's loop 2. Both are real; different games.

---

## Quotes — HarnessX paper, repo & the "Evolve the Harness" blog

> "The harness — not just the model — determines agent performance." — HarnessX README

> "Five of the top six harnesses are deterministic code, not prompt edits." — *Don't Train the Model, Evolve the Harness* (Niklaus)

> "For a weak agent, a lot of 'capability' is I/O discipline the scaffold can guarantee." — blog

> "The weakest task agent consistently gains most… gain magnitude tracks (inverse) baseline performance." — HarnessX paper (inverse scaling)

> "With a capable meta-agent, the accuracy gains derive primarily from HarnessX's **infrastructure** — not the evolver's architecture." — HarnessX paper

> Headline numbers: **+14.5% avg, up to +44%** (ALFWorld Qwen3.5-9B 53→97); blog legal **63.4 → 80.1%**.

---

## References

- **HarnessX** — arXiv:2606.14249 · repo `github.com/Darwin-Agent/HarnessX`
- **"Don't Train the Model, Evolve the Harness"** — huggingface.co/spaces/joelniklaus/harness-optimization · repo `github.com/JoelNiklaus/harness-optimization`
- **τ²-Bench** — `github.com/sierra-research/tau2-bench` (arXiv:2506.07982)
- **GSM8K** — `github.com/openai/grade-school-math`
- **VERL** (model co-evolution) — `github.com/volcengine/verl`
- This lab: the workshop repo · KB study: `repo-studies/go-harness/harnessx/`

---

## 🧪 LAB — now you drive the loop

Follow `workshop/HANDS-ON.md`:
1. `make baseline DOMAIN=telecom` — run the vanilla harness; **watch it fail**.
2. Open a failing `trajectories/*.md` — read the frontmatter; **name the failure**.
3. In Claude Code: *"Use the `harness-evolver` skill on `runs/baseline/R0/trajectories/` — diagnose,
   pick a lever, author a config."* — **your** Claude is the meta-agent.
4. `make eval CONFIG=<your config> TAG=myfix` — **did the number move?**
5. Loop until it lifts. Then try the reasoning (`reasoning/`) and tool (`action_demo/`) demos.

> Time-box: 30–40 min. Pair up. Share what lever you pulled and why.

---

## 📊 RESULTS — record yours

| Vertical / benchmark | Lever pulled | Vanilla | Evolved | Δ | Why this lever (from the trace) |
|----------------------|--------------|---------|---------|---|-------------------------------|
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

**Reference results to beat / compare:** telecom Control 0.50→0.75 · GSM8K Instruction 0.65→0.97 ·
private-KB Action 0.00→1.00.

---

## Takeaways

1. **The deliverable is the LOOP** — run → read traces → pick the lever → evolve → re-run. Not the technique.
2. **Every lever is chosen FROM a trace** — the trace names the failure; you match a lever to it.
3. **The harness, not the weights, sets realized performance** — proven across 3 levers, frozen model.
4. **Vertical agents need a strong benchmark** — it's the reward signal; no benchmark → you're guessing.
5. **Designing the benchmark is half the work; owning testable harness components is the other half.**
6. **This is how you squeeze a cheap, frozen model to punch up on YOUR vertical.**
