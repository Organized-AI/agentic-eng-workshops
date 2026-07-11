---
name: penumbra-second-brain-workshop
description: Guide a user through the Organized AI Penumbra workshop, from source-grounded market research to a separate evidence-grounded sensemaking layer. Use when the user asks to run Workshop 06, build the Penumbra second brain, or continue to Phase 2.
---

# Penumbra Second-Brain Workshop

Guide the user through two visibly separate phases. Use the main Penumbra
Runtime MCP. Explain outcomes in plain language; do not narrate every tool call.

## Ground rules

- Confirm the active Penumbra project before writing.
- Add the exact public Shape for each phase and introspect it before capture.
- Follow the returned type, property, and relationship grammar. Do not invent
  fields or relationships.
- Search the brain before creating something that may already exist.
- Stage related writes in a workspace, validate, submit, and read committed
  entities back before claiming success.
- Never start Phase 2 in the same turn as Phase 1. Pause for the user to inspect
  Context and wait for explicit permission to continue.

## Phase 1 — Market Research

1. Confirm Runtime MCP access and the active project. If authentication is
   missing, help the user reconnect and stop.
2. Add and introspect **Market Research** using public Shape ID
   `725fce02-b026-4d2f-b904-f2c13ffbc9f3`.
3. Ask:
   - What product, idea, or market are we researching?
   - What decision should the research inform?
4. Research current sources with the host's web or browser tools. Prefer
   first-party sources and credible corroboration. If no research tool exists,
   ask the user for URLs rather than relying on model memory.
5. Capture source-grounded findings, subjects, contradictions, and open
   questions using the Shape's introspected grammar. Preserve source and subject
   relationships.
6. Read the staged workspace, repair duplicates or unsupported claims,
   validate, and submit it.
7. Read back the committed knowledge and summarize what was added with its
   sources.
8. Stop and invite the user to inspect **Context**. Continue only when the user
   explicitly asks for Phase 2.

## Phase 2 — Market Sensemaking

1. Confirm the same project and recover the committed Phase 1 research from the
   current conversation.
2. Add and introspect **Market Sensemaking** using public Shape ID
   `98f003ca-23c7-470c-9252-b933e723f4cf`.
3. Do not acquire new web evidence. Reason only from the committed Phase 1
   knowledge.
4. Capture only interpretations supported by that evidence: patterns, tensions,
   unmet needs, opportunities, implications, or risks. Preserve the evidence
   lineage and any meaningful challenges using the Shape's actual grammar.
5. Read, validate, and submit the Phase 2 workspace. Read the committed
   interpretations back.
6. Report each interpretation with the evidence that supports or challenges it,
   then point the user back to **Context** to inspect the two layers.

## Safe stops

Stop rather than improvise when:

- the exact Shape is unavailable;
- the workspace cannot validate;
- Phase 1 has not committed;
- a Phase 2 interpretation cannot be traced to committed research; or
- the active project changes between phases.
