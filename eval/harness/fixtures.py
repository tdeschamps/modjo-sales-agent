"""FIXTURE predicate validation. Predicates re-assert a live deal still matches the
scenario's shape before a run, so data drift becomes FIXTURE_STALE, not a fake pass/fail.

Deal data is fetched by the orchestrator (run.py) and passed in here as a dict; this
module is pure so it is unit-testable without network."""
from __future__ import annotations


class PredicateError(Exception):
    pass


def _contact_roles(deal: dict) -> list[str]:
    return [(c.get("role") or "") for c in deal.get("contacts", [])]


def check_predicates(predicates: list[dict], deal: dict) -> tuple[bool, str]:
    """Return (all_hold, reason_if_failed)."""
    for pred in predicates:
        (kind, value), = pred.items()
        if kind == "deal_status":
            if deal.get("status") not in value:
                return False, f"deal status {deal.get('status')!r} not in {value}"
        elif kind == "no_contact_role":
            if any(r.lower() == value.lower() for r in _contact_roles(deal)):
                return False, f"contact with role {value!r} now present"
        elif kind == "min_calls":
            if (deal.get("call_count") or 0) < value:
                return False, f"call_count {deal.get('call_count')} < {value}"
        elif kind == "amount_lt":
            if (deal.get("amount") or 0) >= value:
                return False, f"amount {deal.get('amount')} not < {value}"
        else:
            raise PredicateError(f"unknown predicate kind: {kind!r}")
    return True, ""
