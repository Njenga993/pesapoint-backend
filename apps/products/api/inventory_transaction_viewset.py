# apps/products/api/inventory_viewset.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.products.models import Inventory, InventoryTransaction
from apps.products.serializers.inventory_transaction_serializer import InventoryTransactionSerializer
from apps.products.permissions import IsBusinessManager
from apps.businesses.api.base import BusinessScopedViewSet  # Import the base class


class InventoryTransactionViewSet(BusinessScopedViewSet):
    serializer_class = InventoryTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InventoryTransaction.objects.filter(
            business=self.request.business
        ).select_related("product")

    def perform_create(self, serializer):
        transaction = serializer.save(business=self.request.business)

        # Get or create inventory record
        inventory, _ = Inventory.objects.get_or_create(
            business=self.request.business,
            product=transaction.product,
        )

        # Apply stock logic
        if transaction.transaction_type == "in":
            inventory.quantity += transaction.quantity

        elif transaction.transaction_type == "out":
            inventory.quantity -= transaction.quantity

        elif transaction.transaction_type == "adjust":
            # Only owner allowed to adjust
            if self.request.business_role != "owner":
                raise PermissionError("Only owners can adjust stock")
            inventory.quantity = transaction.quantity

        inventory.save()