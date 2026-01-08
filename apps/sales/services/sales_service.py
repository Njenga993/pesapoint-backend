from django.db import transaction
from django.core.exceptions import ValidationError

from apps.sales.models import Order
from apps.products.services.inventory_service import InventoryService
from apps.products.models import InventoryTransaction
from apps.sales.services.payment_service import PaymentService
from apps.accounts.services.ledger_service import LedgerService



class SalesService:
    """
    Handles order lifecycle.
    """

    @staticmethod
    @transaction.atomic
    def finalize_order(order: Order) -> Order:
        order = Order.objects.select_for_update().get(pk=order.pk)

        if order.status != Order.STATUS_DRAFT:
            raise ValueError("Only draft orders can be finalized")

        for item in order.items.select_related("product"):
            InventoryService.adjust_stock(
                business=order.business,
                product=item.product,
                quantity=-item.quantity,
                transaction_type=InventoryTransaction.TRANSACTION_OUT,
                note=f"Sale Order #{order.id}",
            )

        order.status = Order.STATUS_COMPLETED
        order.payment_status = Order.PAYMENT_UNPAID
        order.save(update_fields=["status", "payment_status"])

        # 🔒 Ledger write (sale)
        LedgerService.record_sale(
           order=order,
           amount=PaymentService.order_total_amount(order),
          )

        return order

    @staticmethod
    @transaction.atomic
    def cancel_order(order: Order) -> Order:
        locked_order = Order.objects.select_for_update().get(pk=order.pk)

        if locked_order.status != Order.STATUS_COMPLETED:
            raise ValidationError("Only completed orders can be cancelled")

        if PaymentService.order_paid_total(locked_order) > 0:
            raise ValidationError(
                "Paid or partially paid orders must be refunded before cancellation"
            )

        for item in locked_order.items.select_related("product"):
            InventoryService.adjust_stock(
                business=locked_order.business,
                product=item.product,
                quantity=item.quantity,
                transaction_type=InventoryTransaction.TRANSACTION_IN,
                note=f"Order #{locked_order.id} cancellation",
            )

        locked_order.status = Order.STATUS_CANCELLED
        locked_order.save(update_fields=["status"])

        order.status = locked_order.status
        return order
