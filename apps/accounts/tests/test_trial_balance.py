import pytest
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

from apps.accounts.models import LedgerEntry
from apps.accounts.services.trial_balance_service import TrialBalanceService


@pytest.mark.django_db
def test_trial_balance_with_date_range(chart_of_accounts):
    ar = chart_of_accounts["AR"]
    now = timezone.now()

    old_entry = LedgerEntry.objects.create(
        account=ar,
        debit=Decimal("100.00"),
        credit=Decimal("0.00"),
        entry_type=LedgerEntry.ENTRY_SALE,
    )
    LedgerEntry.objects.filter(pk=old_entry.pk).update(
        created_at=now - timedelta(days=10)
    )

    recent_entry = LedgerEntry.objects.create(
        account=ar,
        debit=Decimal("50.00"),
        credit=Decimal("0.00"),
        entry_type=LedgerEntry.ENTRY_SALE,
    )
    LedgerEntry.objects.filter(pk=recent_entry.pk).update(
        created_at=now - timedelta(days=1)
    )

    result = TrialBalanceService.generate(
        start_date=now - timedelta(days=5),
        end_date=now,
    )

    rows = result["rows"]

    assert len(rows) == 1
    assert rows[0]["account_code"] == "AR"
    assert rows[0]["debit"] == Decimal("50.00")
    assert rows[0]["credit"] == Decimal("0.00")


@pytest.mark.django_db
def test_trial_balance_start_date_only(chart_of_accounts):
    cash = chart_of_accounts["CASH"]
    now = timezone.now()

    old_entry = LedgerEntry.objects.create(
        account=cash,
        debit=Decimal("0.00"),
        credit=Decimal("100.00"),
        entry_type=LedgerEntry.ENTRY_PAYMENT,
    )
    LedgerEntry.objects.filter(pk=old_entry.pk).update(
        created_at=now - timedelta(days=20)
    )

    recent_entry = LedgerEntry.objects.create(
        account=cash,
        debit=Decimal("0.00"),
        credit=Decimal("200.00"),
        entry_type=LedgerEntry.ENTRY_PAYMENT,
    )
    LedgerEntry.objects.filter(pk=recent_entry.pk).update(
        created_at=now - timedelta(days=2)
    )

    result = TrialBalanceService.generate(
        start_date=now - timedelta(days=7)
    )

    assert result["total_credit"] == Decimal("200.00")

