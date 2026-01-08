from django.db import transaction
from apps.products.models import Inventory, InventoryTransaction


class InventoryService:
    """
    Handles all inventory mutations.
    """

    @staticmethod
    @transaction.atomic
    def adjust_stock(
        *,
        business,
        product,
        quantity,
        transaction_type,
        note=''
    ):
        inventory, _ = Inventory.objects.select_for_update().get_or_create(
            business=business,
            product=product,
            defaults={'quantity': 0}
        )

        inventory.quantity += quantity
        inventory.save()

        InventoryTransaction.objects.create(
            business=business,
            product=product,
            transaction_type=transaction_type,
            quantity=quantity,
            note=note
        )

        return inventory
