# Stack Map

Seven workshops assemble one visible, receipt-emitting stack, fronted by a tracked
registration funnel. Each workshop draws on granular build stations in `../modules/`.

```
                    +-------------------------------------------------+
                    |        AGENTIC ENGINEERING STACK (Vol 2)        |
                    |        7 Workshops - Antler VC, Austin          |
                    +-------------------------------------------------+
                                         |
   +-----------+-----------+-----------+-----------+-----------+-----------+-----------+
   |           |           |           |           |           |           |           |
 +-v-------+ +-v-------+ +-v-------+ +-v-------+ +-v-------+ +-v-------+ +-v---------+
 | 01 PLAN | | 02 DATA | | 03 LOOP | | 04 HARN.| |05 TOKEN-| | 06 2ND  | | 07 OBSERV |
 | ------- | | ------- | | ------- | | ------- | |  NOMICS | |  BRAIN  | | -ABILITY  |
 | typed   | | tools/  | | RSI     | | factory/| |cost/lat/| | KG +    | | receipts  |
 | workers | | MCP/    | | eval->  | | orchestr| |quality  | | memory  | | + browser |
 | + DAGs  | | APIs +  | | critique| | subagent| |routing  | | retrieval| | QA +     |
 |         | | retriev.| | -> patch| | pool    | |+ budgets| |         | | dashboard |
 +----+----+ +----+----+ +----+----+ +----+----+ +----+----+ +----+----+ +-----+-----+
      |           |           |           |           |           |            |
      +-----------+-----------+-----+-----+-----------+-----------+------------+
                                    |  compose into
                                    v
                    +-------------------------------------------------+
                    |   ONE VISIBLE STACK  (receipts on every run)    |
                    +-------------------------------------------------+
                                         |
                                         v
   +-------------------------------------------------------------------------------+
   |  LANDING + CONVERSION FUNNEL                                                   |
   |  page view -> "Request to Join" -> registered -> attended -> repo cloned       |
   |         [ GTM container -> Meta Pixel + TikTok Pixel + GA4 ]                   |
   +-------------------------------------------------------------------------------+
```

## Workshop -> module mapping

```
01 Planning            -> modules/01-agents, 02-workflows
02 Giving Agents Data  -> modules/03-second-brain (retrieval), tool/MCP patterns
03 Agent Loops / RSI   -> modules/08-recursive-self-improvement
04 Harness Eng         -> modules/05-subagent-orchestration, shared/
05 Tokenomics          -> modules/04-model-routing
06 2nd Brain           -> modules/03-second-brain (memory/KG)
07 Observability       -> modules/06-browser-qa, 07-telemetry, 10-visual-system-design

Cross-cutting: modules/09-deployment (edge/local) used by Harness Eng + Observability
```
