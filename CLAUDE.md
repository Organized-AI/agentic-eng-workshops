# CLAUDE.md — Root Context

Project context for Claude Code working in this repo.

## What we're building

A workshop repo of 10 self-contained build **stations** that together form the agentic
engineering stack. Attendees start from `starter/` scaffolds and build to `solution/`.

## Conventions

- **TypeScript everywhere.** The through-line of the whole event is "turn prompts into
  typed workers" — every unit of work is a typed, schema-validated worker.
- **pnpm workspace.** Each module is a package, runnable standalone via `pnpm --filter`.
- **Every worker emits a receipt.** Token + span telemetry is not optional; it's the
  "ship visible systems with receipts" promise.
- **Cloudflare-first deploy.** Ship workers + HTML as Cloudflare Workers / Worker Assets
  (KV, D1, DO, Queue, R2). Wrangler is the deploy path.
- **Runnable standalone.** A station must work without the others so the room can jump in.

## The factory (agents/)

Use the agent templates in `agents/` as the build crew:
- `master-orchestrator` coordinates phases.
- `module-builder` scaffolds a station (starter + solution + checkpoint).
- `qa-tester` adds the checkpoint test before a station is considered done.
- `docs-writer` keeps each station README in the standard lab-guide shape.

## Standard station shape

```
modules/NN-name/
├── README.md      # lab guide: objective → concept → build → checkpoint
├── CLAUDE.md      # module-specific context
├── starter/       # what the attendee starts from
└── solution/      # reference implementation (gated)
```

## Build order

See `docs/BUILD-PLAN.md`. Phases are dependency-ordered, not time-boxed. Stop after each
phase and summarize before continuing.
