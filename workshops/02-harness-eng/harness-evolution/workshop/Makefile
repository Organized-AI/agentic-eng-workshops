# Harness Evolution Workshop — uv-native local lab
#
# The loop: `make baseline` → (Claude Code reads trajectories, writes an evolved
# config) → `make eval CONFIG=... TAG=...` → compare. The meta-agent is you.
#
# All targets use `uv run --no-sync` so the tau2 editable install is preserved
# (a bare `uv run` would re-sync from uv.lock and drop it).

# ── Config (override on the CLI: make baseline TASKS=20 DOMAIN=airline) ────────
TAU2_BENCH ?= $(HOME)/tau2-bench
DOMAIN     ?= retail
TASKS      ?= 10
CONC       ?= 1
BASE_CONFIG ?= benchmarks/tau2/harness_config_base.yaml   # vanilla "before"
CONFIG     ?= $(BASE_CONFIG)
TAG        ?= run
RUN = cd .. && uv run --no-sync python -m recipe.tau2_evolver.run

.PHONY: help setup pull baseline eval evolved compare clean-runs
help:
	@echo "make setup            # uv sync + install tau2-bench + pull models"
	@echo "make baseline         # R0 vanilla harness (the 'before')"
	@echo "make eval CONFIG=.. TAG=..   # evaluate an evolved config"
	@echo "make evolved          # eval the repo's hardened config (the 'after')"
	@echo "make compare A=.. B=..       # diff two run tags' rewards"
	@echo "(start inference first: ./serve-local.sh ollama)"

setup:
	cd .. && uv sync
	cd .. && uv pip install -e $(TAU2_BENCH)
	$(MAKE) pull

pull:
	unset LLAMA_API_KEY; ollama pull qwen3:32b; ollama pull qwen3:8b

# R0 baseline — vanilla harness, no evolution. Establishes the number to beat.
baseline:
	$(RUN) --domain $(DOMAIN) --base-config $(BASE_CONFIG) \
	  --num-rounds 1 --max-tasks $(TASKS) --max-concurrency $(CONC) \
	  --run-tag baseline --clean

# Evaluate a specific (evolved) HarnessConfig produced by the meta-agent.
eval:
	$(RUN) --domain $(DOMAIN) --base-config $(CONFIG) \
	  --num-rounds 1 --max-tasks $(TASKS) --max-concurrency $(CONC) \
	  --run-tag $(TAG) --clean

# The repo already ships an evolved "after": StopGuard + tool-correction + hints.
evolved:
	$(RUN) --domain $(DOMAIN) --base-config benchmarks/tau2/harness_config.yaml \
	  --num-rounds 1 --max-tasks $(TASKS) --max-concurrency $(CONC) \
	  --run-tag evolved --clean

compare:
	@python3 -c "import json,sys; \
a=json.load(open('../recipe/tau2_evolver/runs/$(A)/comparison.json')); \
b=json.load(open('../recipe/tau2_evolver/runs/$(B)/comparison.json')); \
print('compare $(A) vs $(B): see comparison.json round_summaries')"
