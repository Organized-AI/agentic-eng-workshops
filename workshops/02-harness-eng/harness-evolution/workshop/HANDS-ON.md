# Hands-On Lab — Feel the Baseline, Then Evolve It Yourself

> This is not a copy-the-answer lab. You run a frozen model on a real benchmark, **watch it fail in the
> trace**, and let **your own Claude Code** evolve the harness using the HarnessX framework. The point is
> the *loop* — diagnose → pick a lever → author a fix → measure — not a specific patch.

You'll reproduce a real result on a laptop: **same frozen model, vanilla harness 0.50 → evolved 0.75**,
by discovering the fix yourself.

---

## 0. Setup (once)

```bash
git clone https://github.com/epuerta9/HarnessX && cd HarnessX
git clone https://github.com/sierra-research/tau2-bench ~/tau2-bench
cd workshop && make setup            # uv sync + install tau2-bench + pull qwen3 models
./serve-local.sh ollama              # local inference (unsets LLAMA_API_KEY; --jinja on)
cp .env.example ../.env              # routing: agent + user-sim → local
```
If you see `Invalid API Key` or 0.00 everywhere, read `README.md` § Troubleshooting (LLAMA_API_KEY / --jinja).

Give your Claude Code the evolver role once:
```bash
cp -r evolver-skill ~/.claude/skills/harness-evolver     # or reference it inline
```

---

## 1. Experience the baseline (feel it fail)

Run the **vanilla** harness on telecom — a real customer-support benchmark:
```bash
make baseline DOMAIN=telecom TASKS=6
```
Watch the tasks run. Some pass, some **fail**. Note the avg reward. **This is the "before" you own.**

---

## 2. Read the trace — where does it hurt?

Open a failing trajectory and read the **frontmatter** (the diagnostic dashboard):
```bash
ls ../recipe/tau2_evolver/runs/baseline/R0/trajectories/
sed -n '1,30p' ../recipe/tau2_evolver/runs/baseline/R0/trajectories/*user_abroad*.md
```
Ask yourself (these are the fields that matter):
- `judge_cause` — *why* did it fail?
- `expected_actions` vs `executed_actions` — did it do the right things?
- `failed_actions` — *which* step is missing?
- `exit_reason` / `tool_error_counts` — how did it end; was it a reliability or strategy failure?

On telecom `user_abroad` tasks you'll typically see the agent never calls `enable_roaming` — a
**harness failure, not a reasoning failure**. Sit with that: the model *could* do it; the scaffold didn't
guide it there.

---

## 3. Evolve it — with YOUR Claude Code

In Claude Code, invoke the evolver skill on your baseline run:

> "Use the **harness-evolver** skill. Read `recipe/tau2_evolver/runs/baseline/R0/trajectories/`,
> diagnose the dominant failure, and author a HarnessConfig (+ any processor) that fixes it. Explain
> which of the 4 levers you chose and why."

Your Claude will (per the skill): sweep the frontmatter → cluster by `judge_cause` → map cause → **lens ×
lever × intent** → author a `config.yaml` (+ a `MultiHookProcessor` if it picks the Control lever) →
self-validate with `canonicalize()`. **You are the meta-agent; the model weights never change.**

The 4 levers it's choosing among:
| Lever | Component | When |
|-------|-----------|------|
| Instruction | prompt / guidance | strong model, subtle rule |
| Action | tools / skills | retrieval / capability gap |
| Control | deterministic processor | weak model, I/O discipline — **usually here** |
| Configuration | memory / compaction / knobs | long-context, retune |

---

## 4. Measure — did it lift?

```bash
make eval DOMAIN=telecom CONFIG=<path-to-your-config.yaml> TAG=myfix TASKS=6
```
Compare `runs/myfix/` vs `runs/baseline/`. Did the avg reward rise? Did the failing task flip? Did
anything **regress**? If it regressed, that's data — read the new trace and pull a different lever.

**Loop steps 2–4 until it improves.** That's harness evolution.

---

## 5. Compare with a reference solution (only after you've tried)

We shipped one worked answer for telecom — the framework's telecom IRMA processor:
`evolved/harness_config_telecom.yaml` (enables `PolicyHintProcessor`, whose `roaming_disabled_abroad`
rule injects a `[POLICY ALERT] → call enable_roaming`).
```bash
make eval DOMAIN=telecom CONFIG=evolved/harness_config_telecom.yaml TAG=telecom_irma TASKS=6
```
Reference result (qwen3:32B, 4 tasks): **0.50 → 0.75 (+50%)**, rescuing the `user_abroad` roaming task,
no regressions. Did your fix find the same lever? A different one? Both are valid if the number moved.

Full worked rationale: `evolved/EVOLVE-JOURNAL.md`. Method + trace-reading: the KB notes 02, 03, 07.

---

## 6. (Advanced) Which component actually made the difference?

Once you have a lift, attribute it. **Don't trust a single run** — rollout noise (±0.25 here) is as big as
the effect. Run the multi-trial ablation:
```bash
DOMAIN=telecom TASKS=4 TRIALS=3 bash workshop/ablate.sh
```
It runs `vanilla / control-only / IRMA-only / full` each `TRIALS` times and prints a per-component
attribution table (avg + marginal Δ vs vanilla). The **larger marginal** is the component doing the work;
components with ~0 marginal are **inert — don't ship them** (leave-one-out). Attribution is statistical:
that's why the paper uses pass^k and 100+ tasks. Reproducible for anyone with the servers up.

## 7. (Capability, not crutch) Give the agent a tool it *needs*

Some failures aren't reasoning or reliability — the model simply **lacks the knowledge**. It cannot know
*your* private data; it's not in the weights. This is where the **Action lever** (a tool/skill) adds
capability the model never had.

Run it on a private company knowledge base (made-up, so the model can't have memorized it):
```bash
python workshop/action_demo/kb_agent.py --config vanilla    # no tool
python workshop/action_demo/kb_agent.py --config action     # + kb_search tool
```
- **vanilla** → ~**0/12**. Watch it *hallucinate* every fact (confident, wrong prices and dates).
- **action** → **12/12**. It calls `kb_search`, retrieves the fact, and answers.

That gap — 0.00 → 1.00 — is **can't → can**: genuine new capability, not plumbing. Now **make it yours**:
1. Add a fact to `action_demo/knowledge_base.json` + a matching question in `questions.json`, re-run.
2. Replace `kb_search` with a **real** tool for *your* vertical — a DB query, an internal API, a document
   retriever. Same pattern (`_KB_TOOL` definition + tool loop in `kb_agent.py`).

**Lesson:** the model's weights are fixed; the tools you give it are the frontier. Proprietary knowledge,
tools, and APIs the base model will never have — *that* is why vertical agents exist. (And note: we tried a
**calculator** tool first — the 8B does 4-digit arithmetic by hand at 100%, so it was redundant. Don't add
a tool the model doesn't need; add the one it *can't* live without.)

## What you should walk away having *felt*
1. A frozen model's realized score is mostly **I/O discipline the scaffold guarantees** — you saw it fail,
   then saw a harness edit (no weight change) fix it.
2. **You** drove the evolve loop with your own Claude — read trace, chose a lever, measured.
3. The lever depends on your **vertical's bottleneck** — which is why one vanilla harness can't serve
   every use case. (Control = crutch that recovers latent ability; Instruction = reshapes reasoning;
   **Action/tools = adds capability the model never had** — the frontier lever.)
4. This is how you **squeeze a cheap/small model** to punch up on *your* problem.
5. **Designing the benchmark is half the work** — it's the reward signal that tells you which lever to
   move. No vertical benchmark → you're guessing.
