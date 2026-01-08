from decimal import Decimal
from django.db.models import Sum
from apps.accounts.models import LedgerEntry, Account


class ProfitAndLossService:
    @staticmethod
    def generate(start_date=None, end_date=None):
        qs = LedgerEntry.objects.all()

        if start_date:
            qs = qs.filter(created_at__gte=start_date)
        if end_date:
            qs = qs.filter(created_at__lte=end_date)

        revenue_account = Account.objects.get(code="REV")

        revenue = qs.filter(account=revenue_account).aggregate(
            total=Sum("credit") - Sum("debit")
        )["total"] or Decimal("0.00")

        return {
            "revenue": revenue,
            "expenses": Decimal("0.00"),  # future
            "net_profit": revenue,
        }
