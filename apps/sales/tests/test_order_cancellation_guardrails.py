import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError

from apps.sales.services.sales_service import SalesService
from apps.sales.services.payment_service import PaymentService
from apps.products.models import Inventory


@pytest.mark.django_db
def test_cannot_cancel_fully_paid_order(
    business,
    product,
    order_with_items,
    chart_of_accounts
):

    Inventory.objects.create(
        business=business,
        product=product,
        quantity=20
    )

    SalesService.finalize_order(order_with_items)

    payment = PaymentService.record_payment(
        order=order_with_items,
        amount=Decimal("200.00"),
        method="cash"
    )
    PaymentService.finalize_payment(payment)

    with pytest.raises(ValidationError):
        SalesService.cancel_order(order_with_items)


@pytest.mark.django_db
def test_can_cancel_completed_but_unpaid_order(
    business,
    product,
    order_with_items,
    chart_of_accounts
):

    inventory = Inventory.objects.create(
        business=business,
        product=product,
        quantity=20
    )

    SalesService.finalize_order(order_with_items)
    SalesService.cancel_order(order_with_items)

    inventory.refresh_from_db()

    assert inventory.quantity == 20
    assert order_with_items.status == order_with_items.STATUS_CANCELLED

