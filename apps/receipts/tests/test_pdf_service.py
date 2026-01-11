import pytest

from apps.receipts.services.pdf_service import ReceiptPDFService


@pytest.mark.django_db
def test_generate_pdf_success(completed_payment_with_receipt):
    receipt = completed_payment_with_receipt.receipt

    pdf = ReceiptPDFService.generate(receipt)

    assert pdf.name.endswith(".pdf")
    assert pdf.size > 0


@pytest.mark.django_db
def test_generate_pdf_fails_if_already_generated(completed_payment_with_receipt):
    receipt = completed_payment_with_receipt.receipt

    ReceiptPDFService.generate(receipt)

    with pytest.raises(ValueError):
        ReceiptPDFService.generate(receipt)
