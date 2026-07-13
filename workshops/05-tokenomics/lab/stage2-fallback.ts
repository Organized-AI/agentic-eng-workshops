// Workshop 05 Tokenomics, Stage 2: fallback chains.
//
// Spec source: workshops/05-tokenomics/README.md ("fall back on error or timeout") and
// modules/04-model-routing/README.md ("chained fallbacks, automatically rerouting
// requests to secondary providers when primary options experience failures or
// timeouts").
//
// Checkpoint (this stage): a forced primary-model failure triggers the fallback chain
// and the router still returns a usable result, with the hop recorded.
//
// Standalone per file (this repo's own convention, root CLAUDE.md: "A station must
// work without the others so the room can jump in"), so Stage 1's route() core is
// re-declared here rather than imported.
//
//   npx tsx stage2-fallback.ts

type Quality = "low" | "mid" | "high" | "flagship";
const QUALITY_RANK: Record<Quality, number> = { low: 0, mid: 1, high: 2, flagship: 3 };

interface ModelSpec {
  id: string;
  quality: Quality;
  latencyMs: number;
  priceInPerMtok: number;
  priceOutPerMtok: number;
}

const CATALOG: ModelSpec[] = [
  { id: "haiku-4.5", quality: "low", latencyMs: 400, priceInPerMtok: 1, priceOutPerMtok: 5 },
  { id: "sonnet-5", quality: "mid", latencyMs: 900, priceInPerMtok: 3, priceOutPerMtok: 15 },
  { id: "opus-4.8", quality: "high", latencyMs: 1800, priceInPerMtok: 5, priceOutPerMtok: 25 },
  { id: "fable-5", quality: "flagship", latencyMs: 3000, priceInPerMtok: 10, priceOutPerMtok: 50 },
];

interface Task {
  name: string;
  tokensIn: number;
  tokensOut: number;
}

function costForModel(model: ModelSpec, task: Task): number {
  return (
    (task.tokensIn / 1_000_000) * model.priceInPerMtok +
    (task.tokensOut / 1_000_000) * model.priceOutPerMtok
  );
}

// A fallback chain is an ordered list of model ids to try in sequence.
function buildFallbackChain(preferredQuality: Quality): string[] {
  return CATALOG
    .filter((m) => QUALITY_RANK[m.quality] >= QUALITY_RANK[preferredQuality])
    .sort((a, b) => QUALITY_RANK[a.quality] - QUALITY_RANK[b.quality])
    .map((m) => m.id);
}

interface CallAttempt {
  model: string;
  outcome: "ok" | "error" | "timeout";
  costUsd: number;
  latencyMs: number;
}

interface FallbackReceipt {
  task: string;
  chain: string[];
  attempts: CallAttempt[];
  fallbackTriggered: boolean;
  servedBy: string;
  totalCostUsd: number;
}

// Mock call: deterministic, no network. `forceFail` simulates a primary-model
// error/timeout for the demo, so the fallback path is provable without waiting on a
// real outage.
function mockCallModel(
  modelId: string,
  task: Task,
  opts: { forceFail?: boolean } = {}
): CallAttempt {
  const spec = CATALOG.find((m) => m.id === modelId)!;
  if (opts.forceFail) {
    return { model: modelId, outcome: "timeout", costUsd: 0, latencyMs: spec.latencyMs };
  }
  return {
    model: modelId,
    outcome: "ok",
    costUsd: Number(costForModel(spec, task).toFixed(6)),
    latencyMs: spec.latencyMs,
  };
}

// Tries each model in the chain in order. The first model is called with
// `failPrimary` so the demo can force the exact scenario the checkpoint asks for:
// "primary model failures trigger fallbacks correctly."
function attemptWithFallback(task: Task, chain: string[], failPrimary: boolean): FallbackReceipt {
  const attempts: CallAttempt[] = [];
  let servedBy: string | null = null;

  for (let i = 0; i < chain.length; i++) {
    const modelId = chain[i];
    const isPrimary = i === 0;
    const attempt = mockCallModel(modelId, task, { forceFail: isPrimary && failPrimary });
    attempts.push(attempt);
    if (attempt.outcome === "ok") {
      servedBy = modelId;
      break;
    }
  }

  if (!servedBy) {
    throw new Error(`attemptWithFallback(): every model in the chain failed for "${task.name}"`);
  }

  return {
    task: task.name,
    chain,
    attempts,
    fallbackTriggered: attempts.length > 1,
    servedBy,
    totalCostUsd: attempts.reduce((sum, a) => sum + a.costUsd, 0),
  };
}

function printReceipt(r: FallbackReceipt) {
  console.log(`[receipt] task="${r.task}" chain=[${r.chain.join(" -> ")}]`);
  for (const [i, a] of r.attempts.entries()) {
    const label = i === 0 ? "primary" : `fallback #${i}`;
    console.log(
      `  attempt (${label}): model=${a.model} outcome=${a.outcome} cost=$${a.costUsd.toFixed(
        6
      )} latency=${a.latencyMs}ms`
    );
  }
  console.log(
    `  served by ${r.servedBy}, fallback_triggered=${r.fallbackTriggered}, total_cost=$${r.totalCostUsd.toFixed(
      6
    )}`
  );
}

// --- Demo ---

const task: Task = { name: "generate-release-notes", tokensIn: 600, tokensOut: 250 };
const chain = buildFallbackChain("mid"); // ["sonnet-5", "opus-4.8", "fable-5"]

console.log("Stage 2: fallback chains\n");

console.log("Scenario A: primary succeeds, no fallback expected");
const okReceipt = attemptWithFallback(task, chain, false);
printReceipt(okReceipt);
console.log(`  checkpoint: no fallback when primary is healthy? ${!okReceipt.fallbackTriggered ? "PASS" : "FAIL"}\n`);

console.log("Scenario B: primary forced to fail, fallback must trigger");
const fallbackReceipt = attemptWithFallback(task, chain, true);
printReceipt(fallbackReceipt);
console.log(
  `  checkpoint: forced primary failure triggers fallback and still returns a result? ${
    fallbackReceipt.fallbackTriggered && fallbackReceipt.servedBy !== chain[0] ? "PASS" : "FAIL"
  }`
);

export { attemptWithFallback, buildFallbackChain, mockCallModel, CATALOG, costForModel };
export type { Task, ModelSpec, Quality, CallAttempt, FallbackReceipt };
