from django.db import transaction
from django.db.models import F
from django.core.exceptions import ValidationError

from apps.products.models import Inventory, InventoryTransaction


class InventoryService:

    @staticmethod
    @transaction.atomic
    def adjust_stock(
        *,
        business,
        product,
        quantity,
        transaction_type,
        note=""
    ):
        inventory = (
            Inventory.objects
            .select_for_update()
            .get(business=business, product=product)
        )

        new_quantity = inventory.quantity + quantity

        if new_quantity < 0:
            raise ValidationError(
                f"Insufficient stock for product '{product.name}'. "
                f"Available: {inventory.quantity}, requested: {-quantity}"
            )

        inventory.quantity = new_quantity
        inventory.save(update_fields=["quantity", "updated_at"])

        InventoryTransaction.objects.create(
            business=business,
            product=product,
            transaction_type=transaction_type,
            quantity=quantity,
            note=note,
        )

        return inventory
