import unittest
from datetime import date
from decimal import Decimal

from ap_aging.aging import aging_buckets, bucket_for, days_past_due

AS_OF = date(2026, 10, 25)


class AgingTest(unittest.TestCase):
    def test_days_past_due(self):
        self.assertEqual(days_past_due(date(2026, 10, 20), AS_OF), 5)
        self.assertEqual(days_past_due(date(2026, 11, 1), AS_OF), 0)

    def test_bucket_edges(self):
        self.assertEqual(bucket_for(0), "current")
        self.assertEqual(bucket_for(31), "31-60")
        self.assertEqual(bucket_for(90), "61-90")
        self.assertEqual(bucket_for(91), "90+")

    def test_aging_buckets_skips_paid(self):
        invoices = [{"id": "A", "due_date": date(2026, 9, 1), "amount": Decimal("100.00"), "paid": False},
                    {"id": "B", "due_date": date(2026, 9, 1), "amount": Decimal("50.00"), "paid": True},
                    {"id": "C", "due_date": date(2026, 11, 30), "amount": Decimal("10.00"), "paid": False}]
        totals = aging_buckets(invoices, AS_OF)
        self.assertEqual(totals["31-60"], Decimal("100.00"))
        self.assertEqual(totals["current"], Decimal("10.00"))


if __name__ == "__main__":
    unittest.main()
