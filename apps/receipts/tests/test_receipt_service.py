import pytest
from django.core.exceptions import ValidationError

from apps.receipts.services.receipt_service import ReceiptService


@pytest.mark.django_db
def test_generate_receipt_success(completed_payment_without_receipt):
    receipt = ReceiptService.generate_receipt(completed_payment_without_receipt)

    assert receipt.payment == completed_payment_without_receipt


@pytest.mark.django_db
def test_generate_receipt_fails_if_payment_not_completed(pending_payment):
    with pytest.raises(ValidationError):
        ReceiptService.generate_receipt(pending_payment)


@pytest.mark.django_db
def test_generate_receipt_fails_if_duplicate(completed_payment_without_receipt):
    ReceiptService.generate_receipt(completed_payment_without_receipt)

    with pytest.raises(ValidationError):
        ReceiptService.generate_receipt(completed_payment_without_receipt)
