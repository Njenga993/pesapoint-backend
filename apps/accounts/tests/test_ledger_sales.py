import pytest
from decimal import Decimal

from apps.accounts.models import LedgerEntry, Account
from apps.accounts.services.ledger_service import LedgerService
from apps.sales.models import Payment


@pytest.mark.django_db
@pytest.mark.django_db
def test_record_sale_creates_double_entry(order_with_items, chart_of_accounts):
    LedgerService.record_sale(order=order_with_items, amount=Decimal("150.00"))

    entries = LedgerEntry.objects.filter(entry_type=LedgerEntry.ENTRY_SALE)
    assert entries.count() == 2

    ar = entries.get(account__code="AR")
    rev = entries.get(account__code="REV")

    assert ar.debit == Decimal("150.00")
    assert rev.credit == Decimal("150.00")


@pytest.mark.django_db
def test_record_payment_creates_double_entry(order_with_items, chart_of_accounts):
    payment = Payment.objects.create(
        order=order_with_items,
        amount=Decimal("50.00"),
        method="cash",
    )

    LedgerService.record_payment(
        order=order_with_items,
        payment=payment,
        amount=Decimal("50.00"),
    )

    entries = LedgerEntry.objects.filter(entry_type=LedgerEntry.ENTRY_PAYMENT)
    assert entries.count() == 2

    cash = entries.get(account__code="CASH")
    ar = entries.get(account__code="AR")

    assert cash.debit == Decimal("50.00")
    assert ar.credit == Decimal("50.00")


@pytest.mark.django_db
def test_record_refund_creates_double_entry(order_with_items, chart_of_accounts):
    payment = Payment.objects.create(
        order=order_with_items,
        amount=Decimal("25.00"),
        method="cash",
    )

    LedgerService.record_refund(
        order=order_with_items,
        payment=payment,
        amount=Decimal("25.00"),
    )

    entries = LedgerEntry.objects.filter(entry_type=LedgerEntry.ENTRY_REFUND)
    assert entries.count() == 2

    refund = entries.get(account__code="REFUND")
    cash = entries.get(account__code="CASH")

    assert refund.debit == Decimal("25.00")
    assert cash.credit == Decimal("25.00")
