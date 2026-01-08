from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import Sum, F

from apps.sales.models import Payment, Order
from apps.accounts.services.ledger_service import LedgerService


class PaymentService:
    """
    Handles all payment lifecycle logic.
    """

    @staticmethod
    def _get_locked_order(order: Order) -> Order:
        return Order.objects.select_for_update().get(pk=order.pk)

    # -------------------------
    # Totals
    # -------------------------

    @staticmethod
    def order_total_amount(order: Order) -> Decimal:
        return (
            order.items.aggregate(
                total=Sum(F("quantity") * F("price"))
            )["total"]
            or Decimal("0.00")
        )

    @staticmethod
    def is_order_fully_paid(order: Order) -> bool:
        """
        Returns True if the order has been fully settled.
        """
        return PaymentService.order_balance(order) == Decimal("0.00")

    @staticmethod
    def order_paid_total(order: Order) -> Decimal:
        return (
            Payment.objects.filter(
                order=order,
                status=Payment.STATUS_COMPLETED,
                direction=Payment.DIRECTION_IN,
            ).aggregate(total=Sum("amount"))["total"]
            or Decimal("0.00")
        )

    @staticmethod
    def order_refunded_total(order: Order) -> Decimal:
        return (
            Payment.objects.filter(
                order=order,
                status=Payment.STATUS_COMPLETED,
                direction=Payment.DIRECTION_OUT,
            ).aggregate(total=Sum("amount"))["total"]
            or Decimal("0.00")
        )

    @staticmethod
    def order_balance(order: Order) -> Decimal:
        net_paid = (
            PaymentService.order_paid_total(order)
            - PaymentService.order_refunded_total(order)
        )
        return max(
            PaymentService.order_total_amount(order) - net_paid,
            Decimal("0.00"),
        )

    # -------------------------
    # Payments
    # -------------------------

    @staticmethod
    @transaction.atomic
    def record_payment(*, order: Order, amount: Decimal, method: str, reference: str = "") -> Payment:
        order = PaymentService._get_locked_order(order)

        if order.status != Order.STATUS_COMPLETED:
            raise ValidationError("Payments can only be recorded for completed orders")

        if amount <= 0:
            raise ValidationError("Payment amount must be positive")

        if amount > PaymentService.order_balance(order):
            raise ValidationError("Payment exceeds outstanding order balance")

        return Payment.objects.create(
            order=order,
            method=method,
            amount=amount,
            reference=reference,
            direction=Payment.DIRECTION_IN,
            status=Payment.STATUS_PENDING,
        )

    @staticmethod
    @transaction.atomic
    def finalize_payment(payment: Payment) -> Payment:
        payment = Payment.objects.select_for_update().get(pk=payment.pk)

        if payment.status != Payment.STATUS_PENDING:
            raise ValidationError("Only pending payments can be finalized")

        payment.status = Payment.STATUS_COMPLETED
        payment.finalized_at = payment.finalized_at or payment.created_at
        payment.save(update_fields=["status", "finalized_at"])

        # 🔒 Ledger write (payment)
        LedgerService.record_payment(
              order=payment.order,
              payment=payment,
              amount=payment.amount,
)


        return payment

    # -------------------------
    # Refunds
    # -------------------------

    @staticmethod
    @transaction.atomic
    def refund_payment(payment: Payment, amount: Decimal | None = None) -> Payment:
        payment = Payment.objects.select_for_update().get(pk=payment.pk)

        if payment.status != Payment.STATUS_COMPLETED:
            raise ValidationError("Only completed payments can be refunded")

        refund_amount = amount or payment.amount

        refund = Payment.objects.create(
            order=payment.order,
            method=payment.method,
            amount=refund_amount,
            direction=Payment.DIRECTION_OUT,
            status=Payment.STATUS_COMPLETED,
            reference=f"Refund of payment #{payment.id}",
        )

        if refund_amount == payment.amount:
            payment.status = Payment.STATUS_REVERSED
            payment.save(update_fields=["status"])

        # 🔒 Ledger write (refund)
        LedgerService.record_refund(
            order=refund.order,
            payment=refund,
            amount=refund.amount,
)


        return refund
