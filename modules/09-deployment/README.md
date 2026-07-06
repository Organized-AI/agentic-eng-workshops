# Station 09 — Deployment

> Delivers: **"deployment."**

## Objective

Ship a typed worker to the **edge** as a Cloudflare Worker, callable over HTTP, receipts
intact.

## Concept

- A worker built locally should deploy without rewrites — same contract, new runtime.
- Cloudflare Workers + Worker Assets (KV / D1 / DO / Queue / R2) are the target.
- Wrangler is the deploy path; secrets go in `.dev.vars` / Wrangler secrets, not code.

## What you build

- A `wrangler.toml` and a fetch handler wrapping a Station 01 worker.
- A deployed endpoint that runs the worker and returns output + receipt.

## Run

```bash
pnpm --filter 09-deployment dev      # local via wrangler dev
# then: wrangler deploy
```

## Checkpoint

`wrangler dev` serves the worker locally and a POST returns schema-valid output + a receipt.
Deploy is one command away. `pnpm --filter 09-deployment test` is green.

## Uses

Existing `.wrangler/` config + Cloudflare MCP on the build machine.
