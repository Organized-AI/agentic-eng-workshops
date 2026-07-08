# Evolve Journal — retail, Round 1 (meta-agent = Claude Code)

A reproducible record of one evolution step: what the traces showed, why each
decision was made, what was authored, and how to reproduce it. This is the
"why we did what we did" for the workshop.

## Inputs
- Baseline run: `runs/r0_baseline_32b_jinja/` (qwen3:32b, vanilla `harness_config_base.yaml`)
- Agent: frozen qwen3:32b (local, llama.cpp `--jinja`). User-sim: qwen3:8b. Meta-agent: Claude Code (this).
- 3 retail tasks, `--num-rounds 1`.

## Step 1 — read the traces (frontmatter sweep)
All 3 tasks reward 0.00. Dominant `judge_cause`: `db_mismatch`. Key fields on task 0:
```
executed_actions: []           # none of the 5 expected actions counted
exit_reason: user_stop
error_count: 0
```
Body read (Execution Steps): steps 3–6 correct (auth, order, keyboard variants), then
**Step 7 = empty assistant message** → `Assistant message must contain 'content' or 'tool_calls'`.
qwen3 is a thinking model; it emitted `<think>` only. Hard abort before any write.

## Step 2 — first lever (already available): ParseRetry
Ran the shipped hardened config (`harness_config.yaml`). Result on task 0:
```
executed_actions: [exchange_delivered_order_items]   # F1 CLEARED — it reached the write
error_count: 2                                       # ParseRetry retried through the empty msgs
```
**F1 fixed.** The agent now survives the thinking-abort and executes the exchange. But reward
still 0.00, and the trace exposed the NEXT bottleneck.

## Step 3 — diagnose the new bottleneck (lens × lever × intent)
Task 0 (evolved) frontmatter:
```
tool_error_counts: {exchange_delivered_order_items: 1}   # write called with WRONG args
get_product_details called 1×  (expected 2×: keyboard AND thermostat)
failed_actions: [find_user_id_by_name_zip, get_product_details, exchange_delivered_order_items]
```
- **Lens**: I/O discipline — skips product-detail gathering, picks an unavailable/wrong variant,
  then calls the write with bad args.
- **Lever**: **Control (IRMA)**. *Why not Instruction?* tau2 owns the system prompt
  (`NullSystemPromptBuilder` passes it through) — we can't edit it; the framework's answer is IRMA
  (prepend a reminder to `event.system_prompt` at `on_step_start`). *Why not Action (a variant-matcher
  @tool)?* the data-gathering tools already exist; the gap is DISCIPLINE using them, which a reminder
  fixes at lower cost/risk than authoring + wiring a new tool into tau2's env.
- **Intent**: fix-a-failure, scoped to exchange/return tasks (gated, so non-exchange tasks are untouched).

## Step 4 — author the component
`benchmarks/tau2/retail_exchange_guide.py` → `RetailExchangeGuide(MultiHookProcessor)`:
- `on_step_start` gated on an exchange/return intent regex over user messages.
- Prepends a 5-point exchange-discipline reminder to `event.system_prompt` (auth → order →
  get_product_details for EVERY item → match available variant / apply fallback → single correct
  exchange call; execute don't describe).
- Mirrors `benchmarks/tau2/policy_hint.py` (the framework's IRMA reference). Order 3.

Config: `workshop/evolved/harness_config_evolved.yaml` = hardened config + this processor.

## Step 5 — self-validate
`HarnessConfig.from_yaml_file(...).canonicalize()` must succeed (see run log below).

## Step 6 — evaluate + gate
`cd workshop && make eval CONFIG=evolved/harness_config_evolved.yaml TAG=evolved2`
Compare `runs/evolved2/` reward + traces vs `runs/r1_evolved_32b_jinja/`. Keep only if it improves
or the trace shows the target failures (incomplete gathering, wrong variant) resolved.

## Result (3-way, qwen3:32b, same 3 retail tasks)

| Config | avg_reward | trace signal |
|--------|------------|--------------|
| vanilla (2 procs) | 0.000 | F1: empty-msg abort, never writes |
| hardened (7 procs) | 0.000 | F1 cleared — reaches + executes the write |
| **+ RetailExchangeGuide** | **0.000** | processor **fired** (reminder present in session JSONL); pushed behavior further |

**No reward lift, but the lever worked as designed.** Confirmed firing: `RETAIL EXCHANGE DISCIPLINE`
found in `runs/r2_evolved2_32b/R0/sessions/.../*.jsonl`. Behavioral change vs hardened:
- **task 1**: hardened `executed_actions: []` → +guide gathers (`get_product_details`, `get_order_details`)
  and executes `exchange_delivered_order_items`. The reminder pushed gather+write as intended.
- **task 0**: hit `infrastructure_error` this run (server timeout) → did nothing = **noise**, not comparable.
- **task 2**: 11-action multi-item *return*; agent floundered → `transfer_to_human_agents` = **capability** gap.

**Why the metric didn't move (the lesson):** binary reward on **3 tasks × 1 trial** is too noisy/coarse;
confounds = weak **8B user-simulator** (paper used GPT-4.1/GPT-5) + **Q4-quantized** 32B. This is exactly
why the paper uses 100+ tasks, pass@k, multiple trials, and a strong user-sim. The **method** reproduces
(diagnose→lever→author→validate→measure); the **headline number** does not, on a laptop, at this scale.

**Next to get a number**: scale to ~15–20 tasks × ≥2 trials and/or a 32B user-sim; expect the trace-level
gains (survive-abort, gather+write) to surface as a small but real % over vanilla.

## Reproduce
1. Servers: `./serve-local.sh llama <qwen3-32b-blob> 8090 2` and `... <qwen3-8b-blob> 8088 3` (both `--jinja`).
2. `.env` routes agent→:8090, user-sim→:8088.
3. `make baseline` (vanilla) · `make eval CONFIG=../benchmarks/tau2/harness_config.yaml TAG=hardened` (F1 fix)
   · `make eval CONFIG=evolved/harness_config_evolved.yaml TAG=evolved2` (this step).
