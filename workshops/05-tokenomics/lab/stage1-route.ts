// Workshop 05 Tokenomics, Stage 1: the route() primitive.
//
// Spec source: workshops/05-tokenomics/README.md ("A route() primitive: policy in,
// chosen model + call out") and modules/04-model-routing/README.md ("accepts a policy
// definition and returns both the selected model identifier and the execution result,
// along with metadata documenting the routing decision").
//
// Checkpoint (this stage): a low-cost task routes to the cheap model.
//
// Runnable standalone, no dependencies beyond Node built-ins, no API keys required.
//   npx tsx stage1-route.ts

type Quality = "low" | "mid" | "high" | "flagship";

const QUALITY_RANK: Record<Quality, number> = {
  low: 0,
  mid: 1,
  high: 2,
  flagship: 3,
};

interface ModelSpec {
  id: string;
  quality: Quality;
  latencyMs: number;
  // Per-Mtok pricing, USD. Real published list prices (verified July 2026),
  // used so the cost model teaches real numbers, not invented ones.
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

interface Policy {
  name: string;
  maxCostUsd?: number;
  maxLatencyMs?: number;
  minQuality?: Quality;
}

function costForModel(model: ModelSpec, task: Task): number {
  return (
    (task.tokensIn / 1_000_000) * model.priceInPerMtok +
    (task.tokensOut / 1_000_000) * model.priceOutPerMtok
  );
}

interface RouteDecision {
  task: string;
  policy: string;
  chosenModel: string;
  estCostUsd: number;
  estLatencyMs: number;
  reason: string;
}

// The primitive: policy in, chosen model + cost/latency estimate out, with the
// reasoning recorded for the receipt.
function route(task: Task, policy: Policy): RouteDecision {
  const candidates = CATALOG
    .filter((m) => (policy.minQuality ? QUALITY_RANK[m.quality] >= QUALITY_RANK[policy.minQuality] : true))
    .filter((m) => (policy.maxLatencyMs ? m.latencyMs <= policy.maxLatencyMs : true))
    .filter((m) => (policy.maxCostUsd ? costForModel(m, task) <= policy.maxCostUsd : true))
    .sort((a, b) => costForModel(a, task) - costForModel(b, task));

  if (candidates.length === 0) {
    throw new Error(
      `route(): no model in the catalog satisfies policy "${policy.name}" for task "${task.name}"`
    );
  }

  const chosen = candidates[0];
  return {
    task: task.name,
    policy: policy.name,
    chosenModel: chosen.id,
    estCostUsd: Number(costForModel(chosen, task).toFixed(6)),
    estLatencyMs: chosen.latencyMs,
    reason: `cheapest model clearing policy "${policy.name}" (${candidates.length} candidate(s) qualified)`,
  };
}

function printReceipt(d: RouteDecision) {
  console.log(
    `[receipt] task="${d.task}" policy="${d.policy}" -> model=${d.chosenModel} ` +
      `cost=$${d.estCostUsd.toFixed(6)} latency=${d.estLatencyMs}ms reason="${d.reason}"`
  );
}

// --- Demo ---

const cheapTask: Task = { name: "summarize-changelog-line", tokensIn: 300, tokensOut: 100 };
const cheapPolicy: Policy = { name: "cost-sensitive", maxCostUsd: 0.005 };

const hardTask: Task = { name: "design-db-migration-plan", tokensIn: 2000, tokensOut: 800 };
const hardPolicy: Policy = { name: "quality-first", minQuality: "high" };

console.log("Stage 1: route() by policy\n");

const cheapDecision = route(cheapTask, cheapPolicy);
printReceipt(cheapDecision);
console.log(
  `  checkpoint: low-cost task routed to a cheap model? ${
    cheapDecision.chosenModel === "haiku-4.5" ? "PASS" : "FAIL"
  }`
);

const hardDecision = route(hardTask, hardPolicy);
printReceipt(hardDecision);
console.log(
  `  checkpoint: quality-first task routed to a high-or-better model? ${
    QUALITY_RANK[CATALOG.find((m) => m.id === hardDecision.chosenModel)!.quality] >=
    QUALITY_RANK.high
      ? "PASS"
      : "FAIL"
  }`
);

export { route, CATALOG, costForModel };
export type { Task, Policy, RouteDecision, ModelSpec, Quality };
