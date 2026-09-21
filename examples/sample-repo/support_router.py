"""Toy support-ticket router — the kind of code find-jevable-code is meant to audit.

Nothing here calls a model. Meaning is approximated with keyword lists and a
hand-tuned score. This file is a fixture: a compact, realistic decision surface,
not production code.
"""

from dataclasses import dataclass

QUEUES = ("billing", "technical", "general")

_BILLING = ("invoice", "refund", "charge", "payment", "billed", "subscription")
_TECH = ("error", "crash", "bug", "broken", "not working", "500", "timeout")


@dataclass
class Ticket:
    subject: str
    body: str
    minutes_waiting: int


def route(ticket: Ticket) -> str:
    """Pick a queue by counting keyword hits. Ties fall through to 'general'."""
    text = f"{ticket.subject} {ticket.body}".lower()
    billing = sum(text.count(w) for w in _BILLING)
    tech = sum(text.count(w) for w in _TECH)
    if billing == 0 and tech == 0:
        return "general"
    return "billing" if billing >= tech else "technical"


def needs_human(ticket: Ticket) -> bool:
    """Escalate when the customer 'seems' to ask for a person, or has waited long."""
    text = ticket.body.lower()
    asked = any(p in text for p in ("speak to", "real person", "agent", "human"))
    return asked or ticket.minutes_waiting > 30


def urgency_weight(ticket: Ticket) -> float:
    """Subjective 0..1 severity, hand-weighted. Feeds an in-code priority sort."""
    text = ticket.body.lower()
    w = 0.2
    if any(k in text for k in ("urgent", "asap", "immediately")):
        w += 0.4
    if any(k in text for k in ("down", "outage", "cannot", "can't")):
        w += 0.3
    return min(w, 1.0)


def handle(ticket: Ticket) -> dict:
    return {
        "queue": route(ticket),
        "escalate": needs_human(ticket),
        "priority": urgency_weight(ticket),
    }
