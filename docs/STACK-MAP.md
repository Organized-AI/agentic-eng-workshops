# Stack Map

The big picture: a factory of agents builds 10 stations that compose into one visible,
receipt-emitting system, fronted by a tracked registration funnel.

```
                         +---------------------------------------------+
                         |      AGENTIC ENGINEERING STACK (Vol 2)       |
                         +---------------------------------------------+
                                          |
        +---------------------------------+---------------------------------+
        |                                 |                                 |
   +----v-----+                     +-----v------+                    +------v------+
   |  FACTORY |                     |   SHARED   |                    |   SKILLS    |
   | agents/  |                     | primitives |                    | portable    |
   | -------- |                     | ---------- |                    | procedures  |
   | orchestr.|                     | worker.ts  |                    | verify      |
   | builder  |                     | schema.ts  |                    | receipts    |
   | qa-tester|                     | router.ts  |                    | ship-edge   |
   | docs     |                     | telemetry  |                    +-------------+
   +----+-----+                     +-----+------+
        |                                 |
        +---------------+-----------------+
                        |  builds + powers
                        v
   +---------------------------------------------------------------------------+
   |                            10 BUILD STATIONS                               |
   |                                                                           |
   |  01 Agents --> 02 Workflows --> 03 Second Brain --> 04 Model Routing       |
   |   (typed        (DAG +           (KG + memory)        (cost/latency/       |
   |    workers)      retries)                              quality route)      |
   |      |                                                      |             |
   |      +---------------------> 05 Subagent Orchestration <-----+             |
   |                                (agent factory)                            |
   |                                     |                                     |
   |          +--------------------------+--------------------------+          |
   |          v                          v                          v          |
   |    06 Browser QA            07 Telemetry            08 Self-Improvement    |
   |    (verify outputs)         (token receipts)        (eval->critique->patch)|
   |          |                          |                          |          |
   |          +--------------+-----------+--------------+-----------+           |
   |                         v                          v                      |
   |                  09 Deployment              10 Visual System Design        |
   |                  (edge / Workers)           (live receipts dashboard)       |
   +---------------------------------------------------------------------------+
                        |
                        v
   +---------------------------------------------------------------------------+
   |  LANDING + CONVERSION FUNNEL                                               |
   |  page view -> "Request to Join" -> registered -> attended -> repo cloned   |
   |         [ GTM container -> Meta Pixel + TikTok Pixel + GA4 ]               |
   +---------------------------------------------------------------------------+
```
