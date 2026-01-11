from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.receipts.models import Receipt
from apps.sales.models import Payment
from apps.receipts.services.pdf_service import ReceiptPDFService


class ReceiptService:
    """
    Responsible for receipt creation, numbering,
    and orchestration of receipt artifacts (PDF).
    """

    # =====================================================
    # Receipt creation
    # =====================================================
    @staticmethod
    @transaction.atomic
    def generate_receipt(payment: Payment) -> Receipt:
        """
        Generate an immutable receipt for a finalized payment.
        """

        if payment.status != Payment.STATUS_COMPLETED:
            raise ValidationError("Cannot generate receipt for non-finalized payment")

        if hasattr(payment, "receipt"):
            raise ValidationError("Receipt already exists for this payment")

        receipt_number = ReceiptService._generate_receipt_number()

        receipt = Receipt.objects.create(
            payment=payment,
            receipt_number=receipt_number,
        )

        return receipt

    @staticmethod
    def _generate_receipt_number() -> str:
        """
        Deterministic, sortable receipt number.

        Format:
            RCT-YYYYMMDD-000001
        """

        today = timezone.now().date()
        prefix = today.strftime("RCT-%Y%m%d")

        last_receipt = (
            Receipt.objects
            .filter(receipt_number__startswith=prefix)
            .order_by("-receipt_number")
            .first()
        )

        next_seq = (
            int(last_receipt.receipt_number.split("-")[-1]) + 1
            if last_receipt
            else 1
        )

        return f"{prefix}-{next_seq:06d}"

    # =====================================================
    # Receipt + PDF orchestration
    # =====================================================
    @staticmethod
    @transaction.atomic
    def generate_receipt_with_pdf(payment: Payment) -> Receipt:
        """
        High-level operation:
        - create receipt
        - generate and attach PDF
        """

        receipt = ReceiptService.generate_receipt(payment)

        pdf_file = ReceiptPDFService.generate(receipt)
        receipt.pdf.save(pdf_file.name, pdf_file)

        return receipt
