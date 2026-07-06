# Build Plan

**Repo:** `github.com/Organized-AI/agentic-eng-workshops` (private)
**Event:** Vol 2 · The Agentic Engineering Stack Workshops — Antler VC, Austin TX (in-person + livestream)
**Local path:** `/Users/supabowl/agentic-eng-workshops`
**Promise:** "Bring your laptop. Leave with a stack."

> Phases are **dependency-ordered, not time-boxed.** Each phase is one Claude Code session.
> Stop after each phase and summarize before continuing.

## Phase 0 — Foundation & Factory
- Drop in Organized Codebase **agent templates** (`agents/`) as the build crew.
- pnpm workspace, `tsconfig.base.json`, root `CLAUDE.md`, `.env.example`, `.gitignore`.
- `shared/` typed primitives: `defineWorker()`, zod schemas, telemetry stub, router stub.
- `docs/ATTENDEE-SETUP.md` so the room gets to green fast.

## Phase 1 — Agents & Workflows (Stations 01–02)
- 01: prompt → **typed worker** (input/output zod schemas, validated, retryable).
- 02: compose workers into a **workflow DAG** with retries + fan-out.
- Each station ships `starter/`, `solution/`, README lab guide, checkpoint test.

## Phase 2 — Memory & Routing (Stations 03–04)
- 03: **Second brain** — knowledge graph ingest + retrieval (mem0 / local KG).
- 04: **Model routing** — route by cost/latency/quality with fallback chains.

## Phase 3 — Orchestration (Station 05)
- 05: **Agent factory** — orchestrator spawns + coordinates a worker pool, merges results.

## Phase 4 — Verify & Receipts (Stations 06–07)
- 06: **Browser QA** — headless verification of agent outputs (Playwright loop).
- 07: **Telemetry** — token + span receipts from every worker (the "receipts").

## Phase 5 — Self-Improvement & Deployment (Stations 08–09)
- 08: **Recursive self-improvement** — eval → critique → patch → re-eval loop.
- 09: **Deployment** — ship a worker to the edge (Cloudflare Workers / Wrangler).

## Phase 6 — Visible System (Station 10)
- 10: **Dashboard** rendering the live stack: workers, routes, receipts, evals.
- The "ship visible systems with receipts" payoff screen. GSAP for interactivity.

## Phase 7 — Landing + Conversion Tracking
- `landing/` page mirroring the Luma event, CTA → registration.
- Tracking layer: GTM container → Meta Pixel + TikTok Pixel + GA4.
- `docs/FACILITATOR.md` run-of-show; final README polish.

## Reused assets on the build machine (supabowl — MacBook M1 Pro)
- **Agent templates:** `/Users/supabowl/.claude/agents/` + `/Users/supabowl/sub-agent-framework/agents/templates/`
- **Memory/KG (03):** mem0 env (`MEM0_SETUP_GUIDE.md`)
- **Telemetry (07):** `Organized-AI/openclaw-workshop-infra` (token observability)
- **Edge deploy (09):** existing `.wrangler/` + Cloudflare MCP
- **Tracking:** `google-tag-manager-mcp-server` MCP connected

See `STACK-MAP.md` for the ASCII feature map.
