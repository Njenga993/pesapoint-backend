from decimal import Decimal
from django.db.models import Sum
from apps.accounts.models import LedgerEntry, Account


class CashFlowService:
    @staticmethod
    def generate(start_date=None, end_date=None):
        qs = LedgerEntry.objects.all()

        if start_date:
            qs = qs.filter(created_at__gte=start_date)
        if end_date:
            qs = qs.filter(created_at__lte=end_date)

        cash_account = Account.objects.get(code="CASH")

        totals = qs.filter(account=cash_account).aggregate(
            total_debit=Sum("debit"),
            total_credit=Sum("credit"),
        )

        inflow = totals["total_debit"] or Decimal("0.00")
        outflow = totals["total_credit"] or Decimal("0.00")

        return {
            "cash_in": inflow,
            "cash_out": outflow,
            "net_cash": inflow - outflow,
        }
