import pytest
from django.core.exceptions import ValidationError

from apps.receipts.models import ReceiptPrintLog
from apps.receipts.services.print_audit_service import (
    ReceiptPrintAuditService,
)


@pytest.mark.django_db
def test_log_pdf_print_success(completed_payment_with_receipt, user):
    receipt = completed_payment_with_receipt.receipt

    log = ReceiptPrintAuditService.log_print(
        receipt=receipt,
        method=ReceiptPrintLog.METHOD_PDF,
        printed_by=user,
        printer_name="Office Printer",
    )

    assert isinstance(log, ReceiptPrintLog)
    assert log.receipt == receipt
    assert log.method == ReceiptPrintLog.METHOD_PDF
    assert log.printed_by == user
    assert log.printer_name == "Office Printer"


@pytest.mark.django_db
def test_log_thermal_print_success(completed_payment_with_receipt):
    receipt = completed_payment_with_receipt.receipt

    log = ReceiptPrintAuditService.log_print(
        receipt=receipt,
        method=ReceiptPrintLog.METHOD_THERMAL,
    )

    assert log.method == ReceiptPrintLog.METHOD_THERMAL
    assert log.printed_by is None


@pytest.mark.django_db
def test_print_log_is_immutable(completed_payment_with_receipt):
    receipt = completed_payment_with_receipt.receipt

    log = ReceiptPrintAuditService.log_print(
        receipt=receipt,
        method=ReceiptPrintLog.METHOD_PDF,
    )

    with pytest.raises(ValidationError):
        log.printer_name = "Changed Printer"
        log.save()


@pytest.mark.django_db
def test_log_print_fails_without_receipt():
    with pytest.raises(ValidationError):
        ReceiptPrintAuditService.log_print(
            receipt=None,
            method=ReceiptPrintLog.METHOD_PDF,
        )


@pytest.mark.django_db
def test_log_print_fails_for_unsaved_receipt():
    from apps.receipts.models import Receipt

    receipt = Receipt(receipt_number="RCT-TMP-001")

    with pytest.raises(ValidationError):
        ReceiptPrintAuditService.log_print(
            receipt=receipt,
            method=ReceiptPrintLog.METHOD_PDF,
        )


@pytest.mark.django_db
def test_log_print_fails_for_invalid_method(completed_payment_with_receipt):
    receipt = completed_payment_with_receipt.receipt

    with pytest.raises(ValidationError):
        ReceiptPrintAuditService.log_print(
            receipt=receipt,
            method="email",
        )
