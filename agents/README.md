# agents/ — The Factory

These are the build crew that scaffold and maintain the stations. They mirror the
Organized Codebase agent templates. Point Claude Code at these before writing feature code.

| Agent | Role |
|-------|------|
| `master-orchestrator` | Coordinates the phased build; delegates to the others. |
| `module-builder` | Scaffolds a station: `starter/`, `solution/`, README, CLAUDE.md. |
| `qa-tester` | Writes the checkpoint test that gates each station as "done". |
| `docs-writer` | Keeps every station README in the standard lab-guide shape. |

## Source templates on the build machine

- `/Users/supabowl/.claude/agents/` (master-orchestrator, qa-tester, mcp-builder, ...)
- `/Users/supabowl/sub-agent-framework/agents/templates/`

Copy + tune these into this folder as the first step of the build (see `docs/BUILD-PLAN.md`,
Phase 0).
