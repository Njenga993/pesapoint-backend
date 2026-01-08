import pytest
from decimal import Decimal
from apps.accounts.models import LedgerEntry
from apps.accounts.services.cash_flow import CashFlowService


@pytest.mark.django_db
def test_cash_flow_in_and_out(chart_of_accounts):
    cash = chart_of_accounts["CASH"]

    LedgerEntry.objects.create(
        account=cash,
        debit=Decimal("300.00"),
        credit=Decimal("0.00"),
        entry_type=LedgerEntry.ENTRY_PAYMENT,
    )

    LedgerEntry.objects.create(
        account=cash,
        debit=Decimal("0.00"),
        credit=Decimal("120.00"),
        entry_type=LedgerEntry.ENTRY_REFUND,
    )

    result = CashFlowService.generate()

    assert result["cash_in"] == Decimal("300.00")
    assert result["cash_out"] == Decimal("120.00")
    assert result["net_cash"] == Decimal("180.00")
