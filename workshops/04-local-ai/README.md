# Workshop 04 — Local AI

> Run AI where you control it: **local models + edge deployment.**

## What this covers

- Running models locally (Ollama / LM Studio) and calling them behind the same worker contract.
- When local wins: privacy, cost, latency, offline, no rate limits.
- Shipping a typed worker to the **edge** as a Cloudflare Worker — same contract, new runtime.
- Local ↔ edge ↔ hosted as interchangeable backends behind one interface.

## You leave with

- A worker that can target a local model or an edge deployment without a rewrite.
- A `wrangler`-served endpoint returning output + receipt.

## Draws on

`modules/09-deployment`, local runtimes on the machine, existing `.wrangler/` + Cloudflare MCP.

## Checkpoint

The same worker runs against a local model and against `wrangler dev`, returning schema-valid
output + a receipt from both.
