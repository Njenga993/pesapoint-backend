from decimal import Decimal
from django.db.models import Sum
from apps.accounts.models import LedgerEntry


class TrialBalanceService:
    @staticmethod
    def generate(start_date=None, end_date=None):
        qs = LedgerEntry.objects.all()

        if start_date:
            qs = qs.filter(created_at__gte=start_date)
        if end_date:
            qs = qs.filter(created_at__lte=end_date)

        totals = qs.values(
            "account__code",
            "account__name",
        ).annotate(
            total_debit=Sum("debit"),
            total_credit=Sum("credit"),
        )

        rows = []
        total_debit = Decimal("0.00")
        total_credit = Decimal("0.00")

        for t in totals:
            debit = t["total_debit"] or Decimal("0.00")
            credit = t["total_credit"] or Decimal("0.00")

            total_debit += debit
            total_credit += credit

            rows.append({
                "account_code": t["account__code"],
                "account_name": t["account__name"],
                "debit": debit,
                "credit": credit,
            })

        return {
            "rows": rows,
            "total_debit": total_debit,
            "total_credit": total_credit,
            "balanced": total_debit == total_credit,
        }
