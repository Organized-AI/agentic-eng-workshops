# Attendee Setup — get to green in 5 minutes

Do this before the first station.

## 1. Tools

- **Node 20+** and **pnpm 9+** (`corepack enable` then `corepack prepare pnpm@9 --activate`)
- **git**
- A terminal + your editor of choice
- (Optional, for on-the-go) Claude Code Web

## 2. Clone + install

```bash
git clone https://github.com/Organized-AI/agentic-eng-workshops.git
cd agentic-eng-workshops
pnpm install
```

## 3. Keys

```bash
cp .env.example .env
```

At minimum set `ANTHROPIC_API_KEY`. Everything else is per-station and optional — each
station README tells you which keys it needs.

## 4. Green check

You're ready when `pnpm install` completes cleanly and `node -v` prints 20 or higher.

## Working the stations

Each station lives in `modules/NN-name/`. Start in its `starter/`, follow the README lab
guide, and stop at the **Checkpoint** to confirm you're green before moving on.

> On the go? The same steps work in Claude Code Web — see the env var block in the repo
> and paste your keys into the Claude Code Web environment.
