# Harness Evolution Workshop — Local Lab

**Evolve the harness, not (just) the model.** Reproduce HarnessX harness evolution on a
**frozen local model**, on the τ²-Bench **retail** vertical, with **Claude Code as the meta-agent**.

> The harness — not just the model — determines agent performance. Vanilla harnesses are fine at
> baseline; vertical-specific use cases need the harness to evolve with them. This lab makes that
> visible: same frozen model, vanilla vs. evolved harness, measured on a real business vertical.

Everything runs locally via **`uv`** + a local OpenAI-compatible inference server. No GPU cluster,
no model training — the model weights never change; only the `HarnessConfig` evolves.

> **👉 Doing the workshop? Start with [`HANDS-ON.md`](HANDS-ON.md)** — the experiential lab where *you*
> run the baseline, feel it fail in the trace, and let *your own* Claude Code evolve the harness. This
> README is the reference; HANDS-ON is the journey.

---

## What you'll see

| | Harness | Frozen model | Retail reward |
|---|---|---|---|
| **Before** | `harness_config_base.yaml` — system prompt + token budget only. *No* loop detection, parse retry, tool correction, or tool filtering. | qwen3 (local) | _baseline_ |
| **After** | evolved config — StopGuard + tool correction + IRMA policy hints | *same* model | _higher_ |

The "after" fixes are mostly **deterministic code** (processors), not prompt edits — the core finding
of both HarnessX and the "Don't Train the Model, Evolve the Harness" paper.

---

## Prerequisites

- [`uv`](https://docs.astral.sh/uv/), a local inference server (Ollama **or** llama.cpp), ~6 GB (8B) / ~20 GB (32B) disk.
- This repo (a fork of HarnessX) + [`tau2-bench`](https://github.com/sierra-research/tau2-bench) cloned next to it.

```bash
git clone https://github.com/sierra-research/tau2-bench ~/tau2-bench
cd workshop
make setup            # uv sync + install tau2-bench + pull qwen3 models
```

## Run the lab

```bash
# 1. Start local inference (unsets LLAMA_API_KEY — see Troubleshooting)
./serve-local.sh ollama

# 2. Copy routing config
cp .env.example ../.env     # edit models/ports if needed

# 3. Baseline — the vanilla harness (the "before")
make baseline TASKS=10

# 4. Evolve — Claude Code reads runs/baseline/R0/trajectories/*.md,
#    diagnoses failures, writes an evolved config.yaml (+ processors).
#    Then evaluate it:
make eval CONFIG=path/to/evolved/config.yaml TAG=evolved TASKS=10

# 5. Or just eval the repo's pre-evolved "after" config:
make evolved TASKS=10
```

Compare `runs/baseline/` vs `runs/evolved/` — `comparison.json` (rewards), the config diff (what
changed), and the trajectory `.md` files (why).

---

## The meta-agent is you (Claude Code)

The evolve step is deliberately **manual/driven**: after `make baseline`, open the trajectories and
have Claude Code (a) grep the failure patterns in the judge frontmatter, (b) author a new
`config.yaml` + any `processors/*.py`, (c) `make eval` it, (d) keep it only if reward improves past the
gate. That's the `evolve()` MDP done in the open — the workshop's whole point.

To use the built-in automated `MetaAgent` instead, set `TAU2_META_MODEL` + `ANTHROPIC_API_KEY` and use
`--num-rounds 3` (see `recipe/tau2_evolver/README.md`).

---

## Troubleshooting

**Every local call 401s with `Invalid API Key` / `tokenize error`.**
llama.cpp's server (used by *both* Ollama and standalone `llama-server`) treats the **`LLAMA_API_KEY`**
env var as a required server key. If your shell exports it, all local inference 401s — even
long-installed models. Fix:
```bash
unset LLAMA_API_KEY          # then restart the server
# For the Ollama GUI app: killall Ollama; launchctl unsetenv LLAMA_API_KEY; open -a Ollama
```

**Reward is 0.00 on every task and the agent "talks" instead of acting.**
Tool-calling isn't wired. With standalone `llama-server` you MUST pass **`--jinja`** (use the model's
embedded chat template) — otherwise qwen3 emits tool calls as JSON prose in the message content,
tau2 never executes them, and the (weak) user-simulator hallucinates the results. Symptom in a
trajectory: assistant messages like `{ "action": "tool_call", "tool": "..." }` as text, followed by
a user turn that invents the tool's output. `serve-local.sh` sets `--jinja` for you.

**`request exceeds available context size`.** Per-slot context is too small for τ²'s large system
prompts. Size `-c` so each of `-np N` slots gets ≥ ~12k tokens (e.g. `-c 28672 -np 2`).

**Ollama unavailable / broken.** Use the standalone fallback on the model blobs:
```bash
./serve-local.sh llama ~/.ollama/models/blobs/sha256-<qwen3-8b-blob> 8088
# then point TAU2_AGENT_API_BASE / OPENAI_API_BASE at http://127.0.0.1:8088/v1
```

**Weak model, near-zero baseline.** Retail needs a ~27B-class agent for a strong baseline
(the paper used Qwen3.5-27B → 0.807). qwen3:8b is faster and shows bigger *relative* lift but may sit
near the capability floor. Switch the agent to `qwen3:32b` for paper-faithful numbers.

---

See the full study + workshop notes in the knowledge base:
`Engineering Lab/harness-evolution-workshop/` and `exploration/repo-studies/go-harness/harnessx/`.
