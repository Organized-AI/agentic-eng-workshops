#!/usr/bin/env python3
"""Evolve the harness on REASONING tasks.

A minimal harness whose "config" is a reasoning scaffold (the Instruction/Control
lever) wrapped around a FROZEN model. Shows genuine realized-reasoning gains, not
I/O plumbing:

  vanilla          — one fast pass, answer only            (baseline)
  reflect          — solve, then re-derive & self-correct  (reflection lever)
  self_consistency — sample N, majority-vote the answer    (sampling lever)

Same frozen model throughout; only the scaffold changes.

Run (servers up, see workshop/serve-local.sh):
  python workshop/reasoning/reasoning_harness.py --config vanilla
  python workshop/reasoning/reasoning_harness.py --config reflect
  python workshop/reasoning/reasoning_harness.py --config self_consistency --n 5
"""
from __future__ import annotations
import argparse
import concurrent.futures as cf
import json
import re
import urllib.request
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _post(api_base, model, messages, temperature=0.0, max_tokens=1200, tools=None):
    payload = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
    if tools:
        payload["tools"] = tools
    req = urllib.request.Request(api_base.rstrip("/") + "/chat/completions",
                                 data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json", "Authorization": "Bearer sk-local"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())["choices"][0]["message"]


def call(api_base, model, messages, temperature=0.0, max_tokens=1200):
    return _post(api_base, model, messages, temperature, max_tokens).get("content") or ""


import ast, operator as _op
_OPS = {ast.Add: _op.add, ast.Sub: _op.sub, ast.Mult: _op.mul, ast.Div: _op.truediv,
        ast.Pow: _op.pow, ast.USub: _op.neg, ast.Mod: _op.mod, ast.FloorDiv: _op.floordiv}

def safe_calc(expr):
    """Evaluate an arithmetic expression exactly and safely (no eval of names/calls)."""
    expr = str(expr).replace(",", "").replace("$", "").replace("%", "/100").strip()
    def ev(n):
        if isinstance(n, ast.Constant):
            return n.value
        if isinstance(n, ast.BinOp):
            return _OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp):
            return _OPS[type(n.op)](ev(n.operand))
        raise ValueError("unsupported")
    try:
        return ev(ast.parse(expr, mode="eval").body)
    except Exception as e:
        return f"error: {e}"


_CALC_TOOL = [{"type": "function", "function": {
    "name": "calculator", "description": "Evaluate an arithmetic expression exactly. Use for ALL arithmetic.",
    "parameters": {"type": "object", "properties": {
        "expression": {"type": "string", "description": "e.g. '4736 * 8291' or '10000 * 1.05**3'"}},
        "required": ["expression"]}}}]


_NUM = re.compile(r"-?\$?\d[\d,]*\.?\d*")

def _to_float(cand):
    try:
        return float(cand.replace("$", "").replace(",", "").rstrip("."))
    except (ValueError, AttributeError):
        return None

def extract(text):
    """Pull the final numeric answer. Prefer an explicit 'Answer:'/boxed value;
    ignore the model's <think> scratchpad; fall back to the last number in the
    post-thinking text."""
    # drop the thinking scratchpad content (its numbers are not the answer)
    answer_part = re.split(r"</think>", text)[-1] if "</think>" in text else text
    for pat in (r"answer\s*[:=]?\s*\**\s*\$?(-?\d[\d,]*\.?\d*)",
                r"\\boxed\{\$?(-?\d[\d,]*\.?\d*)\}",
                r"final answer\s*(?:is)?\s*[:=]?\s*\$?(-?\d[\d,]*\.?\d*)",
                r"=\s*\$?(-?\d[\d,]*\.?\d*)\s*$"):
        m = re.search(pat, answer_part, re.IGNORECASE | re.MULTILINE)
        if m:
            return _to_float(m.group(1))
    nums = _NUM.findall(answer_part) or _NUM.findall(text)
    return _to_float(nums[-1]) if nums else None


def correct(pred, ans):
    if pred is None:
        return False
    tol = max(0.01, abs(ans) * 0.001)
    return abs(pred - ans) <= tol


# ── the three reasoning-harness configs ───────────────────────────────────────
def run_vanilla(p, api_base, model):
    msgs = [{"role": "user", "content":
             "/no_think\nSolve this problem. Reply with ONLY the final number, nothing else.\n\n" + p["q"]}]
    return extract(call(api_base, model, msgs, max_tokens=200))


def run_reflect(p, api_base, model):
    first = call(api_base, model, [{"role": "user", "content":
             "/no_think\nSolve this problem. Reply with ONLY the final number.\n\n" + p["q"]}], max_tokens=200)
    # revise pass: /no_think keeps the reasoning VISIBLE (not in a hidden <think>
    # block that would eat the token budget) so the re-derivation is parseable.
    rev = call(api_base, model, [{"role": "user", "content":
             ("/no_think\n"
              "A student was asked this problem and gave the answer below. Re-derive the solution "
              "carefully, showing your work step by step. Check the student's answer for mistakes "
              "(watch for intuitive traps and arithmetic slips). Then give the corrected final answer.\n\n"
              f"PROBLEM: {p['q']}\n\nSTUDENT ANSWER: {first.strip()}\n\n"
              "End with exactly one line: 'Answer: <number>'.")}], max_tokens=900)
    return extract(rev)


def run_cot(p, api_base, model):
    """Reasoning, NO tool — isolates the Action lever (arithmetic done by hand fails).
    /no_think keeps the work VISIBLE (not truncated in a hidden <think> block)."""
    return extract(call(api_base, model, [{"role": "user", "content":
             "/no_think\nSolve this problem step by step, showing all your arithmetic work by hand. "
             "End with exactly one line: 'Answer: <number>'.\n\n" + p["q"]}], max_tokens=1200))


def run_action(p, api_base, model):
    """Reasoning + a calculator tool (the Action lever): can't-arithmetic -> can."""
    msgs = [{"role": "user", "content":
             "Solve this problem. Use the calculator tool for ALL arithmetic — never compute by hand. "
             "After the final calculation, end with exactly one line: 'Answer: <number>'.\n\n" + p["q"]}]
    for _ in range(8):
        m = _post(api_base, model, msgs, tools=_CALC_TOOL, max_tokens=1500)
        msgs.append({"role": "assistant", "content": m.get("content") or "",
                     "tool_calls": m.get("tool_calls")})
        tcs = m.get("tool_calls") or []
        if not tcs:
            return extract(m.get("content") or "")
        for tc in tcs:
            try:
                expr = json.loads(tc["function"]["arguments"]).get("expression", "")
            except Exception:
                expr = ""
            msgs.append({"role": "tool", "tool_call_id": tc.get("id", ""),
                         "content": str(safe_calc(expr))})
    return extract(msgs[-1].get("content") or "")


def run_self_consistency(p, api_base, model, n=5):
    preds = []
    for i in range(n):
        out = call(api_base, model, [{"role": "user", "content":
                   "Solve step by step, then end with 'Answer: <number>'.\n\n" + p["q"]}],
                   temperature=0.8, max_tokens=1200)
        e = extract(out)
        if e is not None:
            preds.append(round(e, 4))
    if not preds:
        return None
    return Counter(preds).most_common(1)[0][0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", choices=["vanilla", "cot", "reflect", "action", "self_consistency"], default="vanilla")
    ap.add_argument("--model", default="qwen3:8b")
    ap.add_argument("--api-base", default="http://127.0.0.1:8088/v1")
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--dataset", default="problems.json",
                    help="'problems.json' (CRT set) or a GSM8K-format .jsonl (question + '#### answer')")
    ap.add_argument("--limit", type=int, default=0, help="cap number of problems (0 = all)")
    args = ap.parse_args()

    dpath = HERE / args.dataset if not Path(args.dataset).is_absolute() else Path(args.dataset)
    if dpath.suffix == ".jsonl":  # GSM8K format
        problems = []
        for line in dpath.read_text().splitlines():
            if not line.strip():
                continue
            d = json.loads(line)
            ans = d["answer"].split("####")[-1].strip().replace(",", "")
            problems.append({"q": d["question"], "a": float(ans)})
    else:
        problems = json.loads(dpath.read_text())
    if args.limit:
        problems = problems[:args.limit]
    fn = {"vanilla": run_vanilla, "cot": run_cot, "reflect": run_reflect, "action": run_action,
          "self_consistency": lambda p, a, m: run_self_consistency(p, a, m, args.n)}[args.config]

    def solve(p):
        try:
            pred = fn(p, args.api_base, args.model)
        except Exception as e:
            pred = None
        ok = correct(pred, p["a"])
        return p, pred, ok

    results = []
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for r in ex.map(solve, problems):
            results.append(r)
            p, pred, ok = r
            print(f"  [{'✓' if ok else '✗'}] ans={p['a']:<8} pred={pred}  {p['q'][:52]}")
    acc = sum(1 for _, _, ok in results if ok) / len(results)
    print(f"\n{args.config}: accuracy = {acc:.3f}  ({sum(ok for _,_,ok in results)}/{len(results)})  model={args.model}")
    (HERE / f"result_{args.config}.json").write_text(json.dumps(
        {"config": args.config, "model": args.model, "accuracy": acc,
         "results": [{"q": p["q"], "a": p["a"], "pred": pred, "ok": ok} for p, pred, ok in results]}, indent=1))


if __name__ == "__main__":
    main()
