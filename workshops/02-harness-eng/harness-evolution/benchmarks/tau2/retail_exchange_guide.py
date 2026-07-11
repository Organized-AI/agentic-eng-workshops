"""
RetailExchangeGuide — an IRMA (Intervention via Runtime Message Augmentation)
processor authored by the meta-agent (Claude Code) for the harness-evolution
workshop.

WHY THIS EXISTS (evolve rationale — see workshop/evolved/EVOLVE-JOURNAL.md)
--------------------------------------------------------------------------
R0 baseline (qwen3:32b, vanilla harness) scored 0.00 on retail. The hardened
config's ParseRetryProcessor cleared the first blocker (F1: the qwen3 thinking
model emitting an empty assistant message, aborting the run before any write).
With F1 fixed the trace exposed the NEXT bottleneck (task 0, evolved):

  - executed_actions: [exchange_delivered_order_items]   # it finally wrote
  - tool_error_counts: {exchange_delivered_order_items: 1}  # but with wrong args
  - get_product_details called ONCE (expected TWICE: keyboard AND thermostat)
  - final DB mismatch → reward 0

Diagnosis (lens x lever x intent):
  - Lens:  I/O discipline — the agent skips product-detail gathering and picks
           the wrong/unavailable variant, then calls the write with bad args.
  - Lever: CONTROL (runtime message augmentation), NOT Instruction. tau2 owns
           the system prompt (NullSystemPromptBuilder passes it through), so we
           cannot edit it directly — the framework's own answer to that is IRMA:
           prepend a reminder to event.system_prompt at step_start. We do NOT
           reach for the Action lever (a variant-matcher @tool) because the tools
           to gather the needed data already exist; the gap is the agent's
           DISCIPLINE in using them, which a reminder targets at lower cost/risk.
  - Intent: fix-a-failure (retail exchange/return tasks only).

Mechanism (mirrors benchmarks/tau2/policy_hint.py):
  MultiHookProcessor.on_step_start → prepend the reminder to event.system_prompt
  (prepended, not appended, for stronger attention), gated so it fires ONLY on
  exchange/return tasks and passes through untouched otherwise.
"""

from __future__ import annotations

import dataclasses
import logging
import re
from typing import AsyncIterator

from harnessx.core.events import StepStartEvent
from harnessx.core.processor import MultiHookProcessor

logger = logging.getLogger(__name__)

# Fire only when the conversation is about an exchange / return / replacement.
_EXCHANGE_INTENT = re.compile(
    r"\b(exchange|return|replace|swap)\b", re.IGNORECASE
)

_REMINDER = (
    "[RETAIL EXCHANGE DISCIPLINE — follow before any write]\n"
    "1. Authenticate the user first (find_user_id_by_name_zip or by email) if not done.\n"
    "2. Call get_order_details for the order.\n"
    "3. Call get_product_details for EVERY product you intend to exchange — one call per product "
    "(e.g. keyboard AND thermostat are two separate calls).\n"
    "4. From the returned `variants`, pick the item_id whose `options` match the user's request "
    "AND has `available: true`. If the exact match is unavailable, apply the user's stated fallback "
    "preference; never pick an unavailable variant.\n"
    "5. Then call exchange_delivered_order_items ONCE with order_id, item_ids (current), "
    "new_item_ids (the chosen available variants), and the user's payment_method_id — all items in one call.\n"
    "Execute the tools; do not merely describe the plan in prose."
)


def _has_exchange_intent(messages: tuple) -> bool:
    """True if any user message expresses an exchange/return/replace intent."""
    for msg in messages:
        role = getattr(msg, "role", None) or (msg.get("role") if isinstance(msg, dict) else None)
        if role != "user":
            continue
        content = getattr(msg, "content", None) or (msg.get("content") if isinstance(msg, dict) else None)
        if content and _EXCHANGE_INTENT.search(str(content)):
            return True
    return False


class RetailExchangeGuide(MultiHookProcessor):
    """Prepend a retail-exchange discipline reminder on exchange/return tasks.

    Runs at step_start (order=3), after PolicyHintProcessor(2), before
    TokenBudgetProcessor(10). Passes through unchanged on non-exchange tasks.
    """

    _singleton_group = "retail.exchange_guide"
    _order = 3

    def __init__(self, enabled: bool = True) -> None:
        self.enabled = enabled

    async def on_step_start(self, event: StepStartEvent) -> AsyncIterator[StepStartEvent]:
        if not self.enabled or not event.raw_messages:
            yield event
            return

        if not _has_exchange_intent(event.raw_messages):
            yield event
            return

        # Prepend so the reminder gets strong attention (not buried at the end).
        enhanced = _REMINDER + "\n\n" + event.system_prompt if event.system_prompt else _REMINDER
        logger.info("RetailExchangeGuide: injected exchange-discipline reminder")
        yield dataclasses.replace(event, system_prompt=enhanced)
