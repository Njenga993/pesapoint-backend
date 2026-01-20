from decimal import Decimal

from django.db.models import Sum
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import LedgerEntry
from apps.accounts.serializers.reports import ProfitAndLossSerializer
from core.auth.permissions import CanViewFinancialReports


class ReportsViewSet(ViewSet):
    """
    Financial reports (P&L for now).
    """

    permission_classes = [
        IsAuthenticated,
        CanViewFinancialReports,
    ]

    def list(self, request):
        revenue = (
            LedgerEntry.objects
            .filter(account__code__startswith="4")
            .aggregate(total=Sum("credit"))["total"]
            or Decimal("0.00")
        )

        expenses = (
            LedgerEntry.objects
            .filter(account__code__startswith="5")
            .aggregate(total=Sum("debit"))["total"]
            or Decimal("0.00")
        )

        profit = revenue - expenses

        serializer = ProfitAndLossSerializer({
            "revenue": revenue,
            "expenses": expenses,
            "profit": profit,
        })

        return Response(serializer.data, status=status.HTTP_200_OK)
