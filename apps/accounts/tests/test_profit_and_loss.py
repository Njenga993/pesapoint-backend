import pytest
from decimal import Decimal
from django.utils import timezone
from apps.accounts.models import LedgerEntry
from apps.accounts.services.profit_and_loss import ProfitAndLossService


@pytest.mark.django_db
def test_profit_and_loss_basic_revenue(chart_of_accounts):
    rev = chart_of_accounts["REV"]

    LedgerEntry.objects.create(
        account=rev,
        debit=Decimal("0.00"),
        credit=Decimal("500.00"),
        entry_type=LedgerEntry.ENTRY_SALE,
    )

    result = ProfitAndLossService.generate()

    assert result["revenue"] == Decimal("500.00")
    assert result["expenses"] == Decimal("0.00")
    assert result["net_profit"] == Decimal("500.00")
