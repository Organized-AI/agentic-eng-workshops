# Workshop 06 — A Structured Second Brain with Penumbra

> Research the world, keep what you learn as structured knowledge, then use a
> second cognitive lens to turn those facts into evidence-grounded insight.

This is a live, agent-guided exercise. You do not need to write API code or run
a local service.

## What you will do

1. Connect your agent to one MCP.
2. Give the agent a **Market Research** Shape for organizing sourced facts.
3. Inspect the resulting entities and relationships in your Penumbra brain.
4. Add a **Market Sensemaking** Shape and derive interpretations from the facts
   already in the brain.

The point is not merely to save a conversation. It is to keep evidence and
interpretation as distinct, reusable layers.

## 1. Create your workshop brain

Sign up here:

**[Open the Developer Free workshop signup](https://app.getpenumbra.ai/sign-up?ref=DEV-FREE)**

Penumbra will provision a Developer Free workspace, brain, and 50 credits. No
payment method is required.

## 2. Connect the Runtime MCP

Runtime MCP URL:

```text
https://mcp.getpenumbra.ai/sse
```

For Codex:

```bash
codex mcp add penumbra --url https://mcp.getpenumbra.ai/sse
codex mcp login penumbra
```

For another MCP-capable agent, add the URL as a remote MCP server and complete
the Penumbra OAuth flow. The Penumbra Quick Start page includes client-specific
connection instructions.

## 3. Let your agent guide the exercise

Tell your agent:

```text
Read workshops/06-second-brain/penumbra/SKILL.md and guide me through the
Penumbra second-brain workshop. Start with Phase 1 and pause before Phase 2.
```

If your agent cannot read this repository, paste the Phase 1 prompt below.

### Phase 1 — build the evidence layer

```text
Use the Penumbra Runtime MCP to build a market-research layer in my brain. Add
and introspect the public Market Research Shape
(725fce02-b026-4d2f-b904-f2c13ffbc9f3). Ask what I am building and what decision
the research should inform. Research current sources, then capture
source-grounded findings, contradictions, and open questions using the Shape's
exact grammar. Validate and submit the workspace, show me what was committed,
then pause so I can inspect Context before we interpret anything.
```

Open **Context** in Penumbra when the agent pauses. Inspect the research before
continuing: Can you see the subjects, findings, sources, contradictions, and
relationships? Edit anything that needs correction.

### Phase 2 — think with the brain

When you are ready, tell the same agent:

```text
Start Phase 2. Add and introspect the public Market Sensemaking Shape
(98f003ca-23c7-470c-9252-b933e723f4cf). Use only the Phase 1 knowledge already
committed to this brain—do not research the web again. Capture supported
patterns, tensions, unmet needs, opportunities, implications, and risks using
the Shape's exact grammar and preserve their evidence lineage. Validate and
submit the workspace, then show me each interpretation and the evidence that
supports or challenges it.
```

Return to **Context** and compare the factual layer with the interpretive layer.

## Checkpoint

You are done when:

- the Runtime MCP is connected;
- Market Research facts and sources are committed and visible in Context;
- the agent paused before interpretation;
- Market Sensemaking interpretations were derived from committed evidence; and
- the agent can explain what evidence supports or challenges each conclusion.

## If you get stuck

- **MCP is unauthenticated:** rerun your client's MCP login flow.
- **A Shape is not found:** use the exact public UUID shown above.
- **No web/search tool is available:** give the agent a few source URLs; do not
  ask it to invent research from memory.
- **A workspace is pending review:** finish or approve Phase 1 before starting
  Phase 2.
- **Time is short:** finish Phase 1 and inspect Context. That is already a
  complete demonstration of structured capture.

## After the workshop

Explore **Shapes** in Penumbra to inspect these cognitive frames or use your
Developer Free credits to design one for your own domain.
