from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class User(AbstractUser):
    """
    Core user model for PesaPoint.
    RBAC is handled via Django Groups & Permissions.
    """
    pass


class Account(models.Model):
    """
    Chart of Accounts.
    """

    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class LedgerEntry(models.Model):
    """
    Immutable accounting ledger.
    Append-only. Source of truth for audits.
    """

    # -------------------------
    # Entry types
    # -------------------------
    ENTRY_SALE = "sale"
    ENTRY_PAYMENT = "payment"
    ENTRY_REFUND = "refund"
    ENTRY_ADJUSTMENT = "adjustment"

    ENTRY_TYPES = [
        (ENTRY_SALE, "Sale"),
        (ENTRY_PAYMENT, "Payment"),
        (ENTRY_REFUND, "Refund"),
        (ENTRY_ADJUSTMENT, "Adjustment"),
    ]

    # -------------------------
    # Relations
    # -------------------------
    order = models.ForeignKey(
        "sales.Order",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ledger_entries",
    )

    payment = models.ForeignKey(
        "sales.Payment",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ledger_entries",
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="ledger_entries",
    )

    # -------------------------
    # Ledger fields
    # -------------------------
    entry_type = models.CharField(max_length=20, choices=ENTRY_TYPES)

    debit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    credit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    reference = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    # -------------------------
    # Meta & Constraints
    # -------------------------
    class Meta:
        ordering = ["created_at"]
        permissions = [
            ("view_financial_reports", "Can view financial reports"),
            ("print_financial_reports", "Can print financial reports"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(debit__gt=0, credit=0)
                    | Q(credit__gt=0, debit=0)
                ),
                name="ledger_exactly_one_side_positive",
            ),
            models.CheckConstraint(
                condition=Q(debit__gte=0, credit__gte=0),
                name="ledger_non_negative_amounts",
            ),
        ]

    # -------------------------
    # Validation
    # -------------------------
    def clean(self):
        if self.debit > 0 and self.credit > 0:
            raise ValidationError("Ledger entry cannot have both debit and credit.")
        if self.debit == 0 and self.credit == 0:
            raise ValidationError("Ledger entry must have a debit or credit.")

    # -------------------------
    # Immutability guarantees
    # -------------------------
    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError("Ledger entries are immutable and cannot be modified.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Ledger entries are immutable and cannot be deleted.")

    def __str__(self):
        side = "D" if self.debit > 0 else "C"
        amount = self.debit if self.debit > 0 else self.credit
        return (
            f"{self.entry_type.upper()} | "
            f"{self.account.code} | "
            f"{side}:{amount}"
        )
