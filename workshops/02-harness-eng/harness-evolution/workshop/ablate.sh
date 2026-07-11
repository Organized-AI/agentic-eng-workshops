#!/usr/bin/env bash
# Multi-trial component ablation — reproducible per-component attribution.
#
# Answers "which harness component makes the biggest difference" by running the
# same tasks under 4 configs (vanilla / control-only / IRMA-only / full), each
# repeated TRIALS times so the per-component signal rises above rollout noise.
#
# Prereqs:
#   - inference servers up:  ./serve-local.sh ...   (or Ollama)
#   - routing set (repo-root .env or exported): TAU2_AGENT_MODEL/_API_BASE,
#     TAU2_USER_MODEL, OPENAI_API_BASE/_API_KEY.  See workshop/.env.example.
#   - run from repo root:  bash workshop/ablate.sh
set -euo pipefail
cd "$(dirname "$0")/.."

DOMAIN="${DOMAIN:-telecom}"
TASKS="${TASKS:-4}"
TRIALS="${TRIALS:-3}"
CONC="${CONC:-2}"

# name -> config path  (kept as parallel arrays for portability)
NAMES=(vanilla control_only irma_only full)
CONFIGS=(
  benchmarks/tau2/harness_config_base.yaml
  benchmarks/tau2/harness_config.yaml
  workshop/evolved/harness_config_policyonly.yaml
  workshop/evolved/harness_config_telecom.yaml
)

for i in "${!NAMES[@]}"; do
  name="${NAMES[$i]}"; cfg="${CONFIGS[$i]}"
  echo "=== ablation: $name  ($cfg)  domain=$DOMAIN tasks=$TASKS trials=$TRIALS ==="
  uv run --no-sync python -m recipe.tau2_evolver.run \
    --domain "$DOMAIN" --base-config "$cfg" \
    --num-rounds 1 --max-tasks "$TASKS" --num-trials "$TRIALS" \
    --max-concurrency "$CONC" --run-tag "ablate_${name}" --clean
done

echo "=== attribution summary ==="
uv run --no-sync python workshop/analyze_ablation.py
