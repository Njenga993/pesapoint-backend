import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError

from apps.sales.models import Payment, Order
from apps.sales.services.payment_service import PaymentService
from apps.products.models import Inventory
from apps.sales.services.sales_service import SalesService


@pytest.mark.django_db
def test_partial_payments_accumulate_correctly(
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

    p1 = PaymentService.record_payment(
        order=order_with_items,
        amount=Decimal("50.00"),
        method="cash"
    )
    PaymentService.finalize_payment(p1)

    p2 = PaymentService.record_payment(
        order=order_with_items,
        amount=Decimal("150.00"),
        method="mpesa"
    )
    PaymentService.finalize_payment(p2)

    assert PaymentService.order_paid_total(order_with_items) == Decimal("200.00")
    assert PaymentService.order_balance(order_with_items) == Decimal("0.00")
    assert PaymentService.is_order_fully_paid(order_with_items) is True

@pytest.mark.django_db
def test_split_payment_multiple_methods(
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

    cash = PaymentService.record_payment(
        order=order_with_items,
        amount=Decimal("100.00"),
        method="cash"
    )
    mpesa = PaymentService.record_payment(
        order=order_with_items,
        amount=Decimal("100.00"),
        method="mpesa"
    )

    PaymentService.finalize_payment(cash)
    PaymentService.finalize_payment(mpesa)

    methods = set(
        Payment.objects.filter(order=order_with_items)
        .values_list("method", flat=True)
    )

    assert methods == {"cash", "mpesa"}

@pytest.mark.django_db
def test_overpayment_is_blocked(
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

    PaymentService.finalize_payment(
        PaymentService.record_payment(
            order=order_with_items,
            amount=Decimal("150.00"),
            method="cash"
        )
    )

    with pytest.raises(ValidationError):
        PaymentService.record_payment(
            order=order_with_items,
            amount=Decimal("100.00"),
            method="mpesa"
        )

@pytest.mark.django_db
def test_refund_restores_order_balance(
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

    refund = PaymentService.refund_payment(
        payment,
        amount=Decimal("50.00")
    )

    assert refund.direction == "out"
    assert refund.status == "completed"
    assert PaymentService.order_balance(order_with_items) == Decimal("50.00")

@pytest.mark.django_db
def test_cannot_finalize_payment_twice(
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
        amount=Decimal("100.00"),
        method="cash"
    )

    PaymentService.finalize_payment(payment)

    with pytest.raises(ValidationError):
        PaymentService.finalize_payment(payment)

@pytest.mark.django_db
def test_cannot_refund_pending_or_reversed_payment(
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
        amount=Decimal("100.00"),
        method="cash"
    )

    with pytest.raises(ValidationError):
        PaymentService.refund_payment(payment)

    PaymentService.finalize_payment(payment)
    PaymentService.refund_payment(payment)

    with pytest.raises(ValidationError):
        PaymentService.refund_payment(payment)

@pytest.mark.django_db
def test_receipt_is_generated_on_payment_finalization(
    business,
    product,
    order_with_items,
    chart_of_accounts
):
    from apps.receipts.models import Receipt

    Inventory.objects.create(
        business=business,
        product=product,
        quantity=20
    )

    SalesService.finalize_order(order_with_items)

    payment = PaymentService.record_payment(
        order=order_with_items,
        amount=Decimal("100.00"),
        method="cash"
    )

    PaymentService.finalize_payment(payment)

    receipt = Receipt.objects.get(payment=payment)

    assert receipt.receipt_number.startswith("RCT-")
