# apps/products/api/inventory_transaction_viewset.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.products.models import Inventory, InventoryTransaction
from apps.products.serializers.inventory_transaction_serializer import InventoryTransactionSerializer
from apps.products.permissions import IsBusinessManager
from apps.businesses.api.base import BusinessScopedViewSet


class InventoryTransactionViewSet(BusinessScopedViewSet):
    """
    ViewSet for VIEWING inventory transaction history.
    This is now a read-only API. Transactions are created by other actions.
    """
    serializer_class = InventoryTransactionSerializer
    permission_classes = [IsAuthenticated] # Require manager to view history

    def get_queryset(self):
        return InventoryTransaction.objects.filter(
            business=self.request.business
        ).select_related("product").order_by("-created_at")

    # REMOVED perform_create. Transactions are now created internally by other actions.