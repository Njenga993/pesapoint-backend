import pytest
from django.core.exceptions import ValidationError

from apps.receipts.services.thermal_service import (
    ThermalReceiptService,
    ThermalPrintPayload,
)
from apps.receipts.models import Receipt


@pytest.mark.django_db
def test_generate_thermal_payload_success(completed_payment_with_receipt):
    """
    Thermal payload is generated correctly for a valid receipt.
    """
    receipt = completed_payment_with_receipt.receipt

    payload = ThermalReceiptService.generate_payload(receipt)

    assert isinstance(payload, ThermalPrintPayload)
    assert payload.paper_width == 80

    # ESC/POS bytes must exist
    assert isinstance(payload.escpos, bytes)
    assert len(payload.escpos) > 0

    # Text fallback must exist
    assert isinstance(payload.text, str)
    assert receipt.receipt_number in payload.text
    assert "Amount Paid" in payload.text


@pytest.mark.django_db
def test_thermal_payload_does_not_modify_receipt(completed_payment_with_receipt):
    receipt = completed_payment_with_receipt.receipt
    original_pdf_name = receipt.pdf.name

    ThermalReceiptService.generate_payload(receipt)

    receipt.refresh_from_db()

    assert (receipt.pdf.name or None) == (original_pdf_name or None)



@pytest.mark.django_db
def test_thermal_payload_contains_core_fields(completed_payment_with_receipt):
    """
    Core business fields must appear in output.
    """
    receipt = completed_payment_with_receipt.receipt
    payment = receipt.payment

    payload = ThermalReceiptService.generate_payload(receipt)

    assert receipt.receipt_number in payload.text
    assert payment.method in payload.text
    assert str(payment.amount) in payload.text


@pytest.mark.django_db
def test_generate_thermal_payload_fails_without_receipt():
    """
    Receipt is mandatory.
    """
    with pytest.raises(ValidationError):
        ThermalReceiptService.generate_payload(None)


@pytest.mark.django_db
def test_generate_thermal_payload_fails_if_receipt_has_no_payment(db):
    """
    Defensive check: receipt must have payment.
    """
    receipt = Receipt(
        receipt_number="RCT-TEST-0001",
        payment=None,
    )

    with pytest.raises(ValidationError):
        ThermalReceiptService.generate_payload(receipt)
