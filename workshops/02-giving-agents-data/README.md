# Workshop 02 — Giving Agents Data

> Agents are only as good as what they can see. This track is the **data plane**: getting
> real tools, connectors, APIs, and retrieved context to a typed worker at runtime.

## What this covers

- **Tools & MCP** — give a worker callable tools and connect it to MCP servers so it can
  reach live systems instead of guessing.
- **APIs & structured inputs** — feed typed, validated data into a worker's context.
- **Retrieval at runtime** — assemble top-k context on demand and ground the worker in it.
- **The line vs. 2nd Brain** — this is the *inputs* plane (data to the agent now);
  Workshop 06 is the *memory* plane (what the agent remembers over time).

## You leave with

- A typed worker wired to at least one tool / MCP connector and one live data source.
- A retrieval step that assembles context and grounds the worker, with the data it used
  recorded in the receipt.

## Draws on

`modules/03-second-brain` (retrieval side), tool/MCP patterns, `shared/src/worker.ts`.
MCP connectors already on the build machine are fair game as data sources.

## Checkpoint

A worker answers using data it fetched through a tool/connector (not just the prompt), and
the receipt shows which sources it pulled from.
