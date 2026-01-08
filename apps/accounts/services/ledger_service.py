from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError

from apps.accounts.models import LedgerEntry, Account


class LedgerService:
    """
    Append-only accounting ledger.
    Records accounting facts only.
    """

    # -------------------------
    # Helpers
    # -------------------------
    @staticmethod
    def _validate_amount(amount: Decimal) -> None:
        if amount <= 0:
            raise ValidationError("Ledger amount must be positive")

    @staticmethod
    def _account(code: str) -> Account:
        return Account.objects.get(code=code)

    # -------------------------
    # Sales
    # -------------------------
    @staticmethod
    @transaction.atomic
    def record_sale(*, order, amount: Decimal) -> None:
        """
        DR Accounts Receivable
        CR Revenue
        """
        LedgerService._validate_amount(amount)

        LedgerEntry.objects.create(
            order=order,
            entry_type=LedgerEntry.ENTRY_SALE,
            account=LedgerService._account("AR"),
            debit=amount,
            reference=f"Sale Order #{order.id}",
        )

        LedgerEntry.objects.create(
            order=order,
            entry_type=LedgerEntry.ENTRY_SALE,
            account=LedgerService._account("REV"),
            credit=amount,
            reference=f"Sale Order #{order.id}",
        )

    # -------------------------
    # Payments
    # -------------------------
    @staticmethod
    @transaction.atomic
    def record_payment(*, order, payment, amount: Decimal) -> None:
        """
        DR Cash
        CR Accounts Receivable
        """
        LedgerService._validate_amount(amount)

        LedgerEntry.objects.create(
            order=order,
            payment=payment,
            entry_type=LedgerEntry.ENTRY_PAYMENT,
            account=LedgerService._account("CASH"),
            debit=amount,
            reference=f"Payment #{payment.id} for Order #{order.id}",
        )

        LedgerEntry.objects.create(
            order=order,
            payment=payment,
            entry_type=LedgerEntry.ENTRY_PAYMENT,
            account=LedgerService._account("AR"),
            credit=amount,
            reference=f"Payment #{payment.id} for Order #{order.id}",
        )

    # -------------------------
    # Refunds
    # -------------------------
    @staticmethod
    @transaction.atomic
    def record_refund(*, order, payment, amount: Decimal) -> None:
        """
        DR Refunds
        CR Cash
        """
        LedgerService._validate_amount(amount)

        LedgerEntry.objects.create(
            order=order,
            payment=payment,
            entry_type=LedgerEntry.ENTRY_REFUND,
            account=LedgerService._account("REFUND"),
            debit=amount,
            reference=f"Refund #{payment.id} for Order #{order.id}",
        )

        LedgerEntry.objects.create(
            order=order,
            payment=payment,
            entry_type=LedgerEntry.ENTRY_REFUND,
            account=LedgerService._account("CASH"),
            credit=amount,
            reference=f"Refund #{payment.id} for Order #{order.id}",
        )
