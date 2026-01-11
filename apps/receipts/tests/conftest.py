import pytest
from decimal import Decimal

from apps.products.models import Inventory
from apps.sales.models import Payment
from apps.sales.services.sales_service import SalesService
from apps.sales.services.payment_service import PaymentService


@pytest.fixture
def pending_payment(
    business,
    product,
    order_with_items,
    chart_of_accounts,
):
    """
    Payment recorded but NOT finalized.
    """

    Inventory.objects.create(
        business=business,
        product=product,
        quantity=20,
    )

    SalesService.finalize_order(order_with_items)

    payment = PaymentService.record_payment(
        order=order_with_items,
        amount=Decimal("100.00"),
        method="cash",
    )

    # status is PENDING by default
    return payment


@pytest.fixture
def completed_payment_without_receipt(pending_payment):
    """
    Payment completed manually WITHOUT receipt.
    """

    pending_payment.status = Payment.STATUS_COMPLETED
    pending_payment.save(update_fields=["status"])

    return pending_payment


@pytest.fixture
def completed_payment_with_receipt(pending_payment):
    """
    Payment finalized THROUGH service (receipt generated).
    """

    return PaymentService.finalize_payment(pending_payment)
