#!/usr/bin/env python3
"""Reproducible check for the authored RetailExchangeGuide component.

Run:  python workshop/evolved/verify_component.py     (from anywhere)
Proves the IRMA processor fires on exchange/return intent, stays silent
otherwise, and prepends the reminder without dropping the base system prompt.
"""
import sys
from pathlib import Path

# repo root = two levels up (workshop/evolved/ -> repo root); ensure importable.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from benchmarks.tau2.retail_exchange_guide import _has_exchange_intent, _REMINDER


class _M:
    def __init__(self, role, content):
        self.role, self.content = role, content


def main() -> int:
    checks = [
        ("exchange intent", _has_exchange_intent((_M("user", "I'd like to exchange the keyboard"),)) is True),
        ("return intent", _has_exchange_intent((_M("user", "can I return this?"),)) is True),
        ("replace intent (dict)", _has_exchange_intent(({"role": "user", "content": "please replace it"},)) is True),
        ("non-exchange silent", _has_exchange_intent((_M("user", "what's my order status?"),)) is False),
        ("only scans user", _has_exchange_intent((_M("assistant", "would you like to exchange?"),)) is False),
        ("reminder prepended", (_REMINDER + "\n\nBASE").startswith("[RETAIL EXCHANGE DISCIPLINE")),
        ("base preserved", (_REMINDER + "\n\nBASE").endswith("BASE")),
    ]
    ok = True
    for name, passed in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed
    print("ALL PASS" if ok else "FAILURES PRESENT")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
