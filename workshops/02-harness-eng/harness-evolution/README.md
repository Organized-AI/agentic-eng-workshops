# Harness Evolution — Workshop & Lab

> **Evolve the harness, not (just) the model.** A hands-on lab: run a frozen local model on real
> benchmarks, read the traces, and evolve the harness — closing the loop the way agentic RL does.

This is a **stripped-down** fork of [HarnessX](https://github.com/Darwin-Agent/HarnessX) containing only
what the workshop needs: the core framework (`harnessx/`), the τ²-bench adapter (`benchmarks/tau2/`), the
evolution recipe (`recipe/tau2_evolver/`), and the workshop itself (`workshop/`). The rest of the HarnessX
framework (UI, gateway, other benchmarks/recipes) has been removed for clarity.

## Start here → [`workshop/HANDS-ON.md`](workshop/HANDS-ON.md)

The experiential lab: you run the baseline, feel it fail in the trace, and let your own Claude Code evolve
the harness. Reference material and the deck live alongside it.

## What's inside `workshop/`

| Path | What |
|------|------|
| `HANDS-ON.md` | the guided lab (run → read trace → evolve → measure) |
| `Makefile`, `serve-local.sh`, `.env.example` | uv-native local runner + keyless llama.cpp / Ollama |
| `reasoning/` | reasoning-lever demo: GSM8K + CRT (`reasoning_harness.py`) |
| `action_demo/` | Action-lever demo: private-KB retrieval tool (`kb_agent.py`) |
| `evolved/` | authored components + configs + `EVOLVE-JOURNAL.md` (one full loop, documented) |
| `evolver-skill/` | the `harness-evolver` Claude Code skill (run the meta-agent role) |
| `ablate.sh`, `analyze_ablation.py` | multi-trial component attribution |
| `*.png`, `make_*_chart.py`, `build_deck.py` | charts + the slide deck |

## Results reproduced here (frozen model, harness-only)

| Lever | Benchmark | Vanilla → Evolved |
|-------|-----------|-------------------|
| Action (kb_search tool) | private company KB | **0.00 → 1.00** (can't → can) |
| Instruction (reflect scaffold) | GSM8K | 0.65 → 0.975 |
| Control (IRMA policy alert) | τ² telecom | 0.50 → 0.75 |

## Setup

```bash
git clone https://github.com/sierra-research/tau2-bench ~/tau2-bench   # for the τ² lab only
cd workshop && make setup        # uv sync + install harnessx + tau2-bench + pull qwen3 models
./serve-local.sh ollama          # local inference
```
The `reasoning/` and `action_demo/` demos are self-contained (just a local OpenAI-compatible endpoint).

---
Built on [HarnessX](https://github.com/Darwin-Agent/HarnessX) (arXiv:2606.14249), MIT.
