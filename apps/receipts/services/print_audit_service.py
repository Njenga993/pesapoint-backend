from typing import Optional

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.receipts.models import Receipt, ReceiptPrintLog
from apps.accounts.models import User


class ReceiptPrintAuditService:
    """
    Centralized audit logging for all receipt print actions.
    Append-only, immutable, compliance-safe.
    """

    @staticmethod
    @transaction.atomic
    def log_print(
        *,
        receipt: Receipt,
        method: str,
        printed_by: Optional[User] = None,
        printer_name: str = "",
    ) -> ReceiptPrintLog:
        """
        Record a receipt print event.

        Args:
            receipt: Receipt being printed
            method: 'pdf' or 'thermal'
            printed_by: Optional user who initiated the print
            printer_name: Optional printer identifier

        Raises:
            ValidationError: if receipt is invalid or method unsupported
        """

        if receipt is None:
            raise ValidationError("Receipt is required")

        if receipt.pk is None:
            raise ValidationError("Receipt must be persisted before printing")

        if method not in {
            ReceiptPrintLog.METHOD_PDF,
            ReceiptPrintLog.METHOD_THERMAL,
        }:
            raise ValidationError("Unsupported print method")

        return ReceiptPrintLog.objects.create(
            receipt=receipt,
            method=method,
            printed_by=printed_by,
            printer_name=printer_name or "",
        )
