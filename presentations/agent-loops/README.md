# Stop Prompting Agents, Start Designing Loops

Speaker deck by **Henry Fuentes** (Founder & Fractional CTO, [Scaled By Design](https://scaledbydesign.com)).

A practical walkthrough of agent loops: what a loop actually is (trigger → action → stop
condition), the five loop patterns, when a loop is worth building vs. overkill, how to
prompt one, and three real end-to-end runs — plus a cheat sheet for keeping loops lean
on tokens, memory, and agent handoff.

## Open the deck

| Format | File |
|--------|------|
| PowerPoint | [`agent-loops.pptx`](./agent-loops.pptx) |

## Where this fits the workshops

This deck is companion material for **[Workshop 03 — Agent Loops / RSI](../../workshops/03-agent-loops-rsi/README.md)**:
eval → critique → patch, bounded self-improvement, and where recursion helps vs. burns
tokens. Use it as the framing talk before the room builds the eval harness in
`modules/08-recursive-self-improvement`.

## Arc (high level)

1. The core claim — a loop is three things: trigger, action, stop condition
2. Anatomy of a loop — reason, act, observe, until actually done
3. Why loops beat one-shot prompting
4. Where loops actually fit — and where they're overkill
5. Three ways to build a loop (solo, maker → checker, manager + helpers)
6. Five loop patterns, from stateless to workflow-improving
7. Three real runs: a stateless loop, a Three.js build loop, an Abbey Road recreation loop
8. Nesting loops — the Super Loop pattern (manager loop spawning worker loops)
9. Cheat sheet — token usage, memory, and agent handoff tips
10. The takeaway — adopt loops selectively, matched to the task

## Source

Built by [Scaled By Design](https://scaledbydesign.com).
