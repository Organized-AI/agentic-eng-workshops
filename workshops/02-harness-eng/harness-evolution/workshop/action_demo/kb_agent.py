#!/usr/bin/env python3
"""Action-lever demo: private, vertical-specific knowledge the model CANNOT have
in its weights. Without a retrieval tool the frozen model hallucinates; with a
`kb_search` tool it retrieves the fact and answers. Genuine can't -> can.

  vanilla — answer from the model's weights (no tool)
  action  — same model + a kb_search tool over a private knowledge base

Run (server up):
  python workshop/action_demo/kb_agent.py --config vanilla
  python workshop/action_demo/kb_agent.py --config action
"""
from __future__ import annotations
import argparse, json, re, urllib.request
import concurrent.futures as cf
from pathlib import Path

HERE = Path(__file__).resolve().parent
KB = json.loads((HERE / "knowledge_base.json").read_text())


def _post(api_base, model, messages, tools=None, max_tokens=800):
    payload = {"model": model, "messages": messages, "temperature": 0.0, "max_tokens": max_tokens}
    if tools:
        payload["tools"] = tools
    req = urllib.request.Request(api_base.rstrip("/") + "/chat/completions",
                                 data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json", "Authorization": "Bearer sk-local"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())["choices"][0]["message"]


_NUM = re.compile(r"-?\$?\d[\d,]*\.?\d*")
def extract(text):
    part = re.split(r"</think>", text or "")[-1]
    m = re.search(r"answer\s*[:=]?\s*\**\s*\$?(-?\d[\d,]*\.?\d*)", part, re.IGNORECASE)
    cand = m.group(1) if m else (_NUM.findall(part)[-1] if _NUM.findall(part) else None)
    if cand is None:
        return None
    try:
        return float(cand.replace("$", "").replace(",", "").rstrip("."))
    except ValueError:
        return None


def kb_search(query):
    """Keyword-overlap search over the private KB; returns the best-matching facts."""
    qs = set(re.findall(r"[a-z0-9]+", query.lower()))
    scored = sorted(KB, key=lambda f: len(qs & set(re.findall(r"[a-z0-9]+", f.lower()))), reverse=True)
    top = [f for f in scored if qs & set(re.findall(r"[a-z0-9]+", f.lower()))][:3]
    return "\n".join(top) if top else "No matching records found."


_KB_TOOL = [{"type": "function", "function": {
    "name": "kb_search", "description": "Search the Acme Robotics internal knowledge base for facts "
    "(product prices, SKUs, policies, contacts). Use it for ANY company-specific fact.",
    "parameters": {"type": "object", "properties": {
        "query": {"type": "string", "description": "keywords, e.g. 'Sentinel Arm price'"}}, "required": ["query"]}}}]


def run_vanilla(p, api_base, model):
    return extract(_post(api_base, model, [{"role": "user", "content":
        "/no_think\nAnswer the question about Acme Robotics. End with 'Answer: <number>'.\n\n" + p["q"]}]).get("content") or "")


def run_action(p, api_base, model):
    msgs = [{"role": "user", "content":
             "Answer the question about Acme Robotics. You do NOT know its private data — you MUST use "
             "the kb_search tool to look up any company fact. End with 'Answer: <number>'.\n\n" + p["q"]}]
    for _ in range(6):
        m = _post(api_base, model, msgs, tools=_KB_TOOL, max_tokens=800)
        msgs.append({"role": "assistant", "content": m.get("content") or "", "tool_calls": m.get("tool_calls")})
        tcs = m.get("tool_calls") or []
        if not tcs:
            return extract(m.get("content") or "")
        for tc in tcs:
            try:
                q = json.loads(tc["function"]["arguments"]).get("query", "")
            except Exception:
                q = ""
            msgs.append({"role": "tool", "tool_call_id": tc.get("id", ""), "content": kb_search(q)})
    return extract(msgs[-1].get("content") or "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", choices=["vanilla", "action"], default="vanilla")
    ap.add_argument("--model", default="qwen3:8b")
    ap.add_argument("--api-base", default="http://127.0.0.1:8088/v1")
    ap.add_argument("--workers", type=int, default=3)
    args = ap.parse_args()
    problems = json.loads((HERE / "questions.json").read_text())
    fn = {"vanilla": run_vanilla, "action": run_action}[args.config]

    def solve(p):
        try:
            pred = fn(p, args.api_base, args.model)
        except Exception:
            pred = None
        ok = pred is not None and abs(pred - p["a"]) <= max(0.01, abs(p["a"]) * 0.001)
        return p, pred, ok

    res = []
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for p, pred, ok in ex.map(solve, problems):
            res.append(ok)
            print(f"  [{'✓' if ok else '✗'}] a={p['a']:<9} pred={pred}  {p['q'][:50]}")
    print(f"\n{args.config}: accuracy = {sum(res)/len(res):.3f}  ({sum(res)}/{len(res)})  model={args.model}")


if __name__ == "__main__":
    main()
