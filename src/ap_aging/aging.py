"""Accounts-payable aging: group open invoices into days-past-due buckets."""
from datetime import date
from decimal import Decimal
from typing import Dict, Iterable

BUCKETS = ("current", "1-30", "31-60", "61-90", "90+")


def days_past_due(due_date: date, as_of: date) -> int:
    """Calendar days after the due date (0 when not yet due)."""
    return max((as_of - due_date).days, 0)


def bucket_for(days: int) -> str:
    if days == 0:
        return "current"
    if days < 30:
        return "1-30"
    if days <= 60:
        return "31-60"
    if days <= 90:
        return "61-90"
    return "90+"


def aging_buckets(invoices: Iterable[Dict], as_of: date) -> Dict[str, Decimal]:
    """Total open amount per bucket. Each invoice: {'id', 'due_date': date, 'amount': Decimal, 'paid': bool}."""
    totals = {b: Decimal("0") for b in BUCKETS}
    for inv in invoices:
        if inv.get("paid"):
            continue
        totals[bucket_for(days_past_due(inv["due_date"], as_of))] += Decimal(inv["amount"])
    return totals
