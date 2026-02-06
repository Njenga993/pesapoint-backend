# apps/products/api/inventory_viewset.py
from rest_framework import viewsets, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction

from apps.products.models import Inventory, Product, InventoryTransaction
from apps.products.serializers.inventory_serializer import InventorySerializer
from apps.products.permissions import IsBusinessManager # Ensure this is imported
from apps.businesses.api.base import BusinessScopedViewSet


class InventoryViewSet(BusinessScopedViewSet):
    """
    ViewSet for viewing and managing current inventory levels.
    This shows the current stock for each product.
    """
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated] # Harden: Require manager permissions

    def get_queryset(self):
        return Inventory.objects.filter(
            business=self.request.business
        ).select_related("product")

    # -------------------------------------------
    # NEW ACTION: ADJUST STOCK FOR A SINGLE ITEM
    # -------------------------------------------
    @action(detail=True, methods=['post'], url_path='adjust-stock')
    def adjust_stock(self, request, pk=None):
        """
        Manually adjusts the stock for a single product.
        This creates an 'adjustment' transaction to log the change.
        Expected Payload:
        {
            "new_quantity": 150,
            "note": "Found extra box in the back room."
        }
        """
        inventory = self.get_object()
        new_quantity = request.data.get('new_quantity')
        note = request.data.get('note', 'Manual adjustment')

        if not isinstance(new_quantity, int) or new_quantity < 0:
            raise serializers.ValidationError("new_quantity must be a non-negative integer.")

        with transaction.atomic():
            # Lock the row to prevent race conditions
            inventory = Inventory.objects.select_for_update().get(pk=inventory.pk)
            old_quantity = inventory.quantity
            difference = new_quantity - old_quantity

            if difference == 0:
                return Response({"detail": "No change in quantity."}, status=status.HTTP_200_OK)

            # Update the inventory level
            inventory.quantity = new_quantity
            inventory.save()

            # Create a transaction record for the adjustment
            InventoryTransaction.objects.create(
                business=inventory.business,
                product=inventory.product,
                transaction_type=InventoryTransaction.TRANSACTION_ADJUST,
                quantity=difference, # Positive for stock in, negative for stock out
                note=note
            )

        return Response({
            "detail": f"Stock for {inventory.product.name} adjusted from {old_quantity} to {new_quantity}.",
            "old_quantity": old_quantity,
            "new_quantity": new_quantity,
            "difference": difference
        }, status=status.HTTP_200_OK)

    # -------------------------------------------
    # HARDENED: BULK UPDATE WITH TRANSACTION LOGGING
    # -------------------------------------------
    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        """
        Bulk update inventory for multiple products.
        Creates an 'adjustment' transaction for each change.
        Expected payload: [
            {"product_id": 1, "quantity": 10},
            {"product_id": 2, "quantity": 5}
        ]
        """
        if not isinstance(request.data, list):
            return Response(
                {"error": "Expected a list of product updates"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        updated_items = []
        errors = []
        
        with transaction.atomic():
            for item in request.data:
                try:
                    product_id = item.get('product_id')
                    new_quantity = item.get('quantity')
                    
                    if not product_id or new_quantity is None:
                        errors.append({
                            "product_id": product_id,
                            "error": "product_id and quantity are required"
                        })
                        continue
                    
                    # Get or create inventory record, and lock it
                    inventory, created = Inventory.objects.select_for_update().get_or_create(
                        business=self.request.business,
                        product_id=product_id,
                        defaults={'quantity': new_quantity}
                    )
                    
                    old_quantity = 0 if created else inventory.quantity
                    difference = new_quantity - old_quantity

                    if not created and difference != 0:
                        inventory.quantity = new_quantity
                        inventory.save()
                        
                        # Log the adjustment
                        InventoryTransaction.objects.create(
                            business=inventory.business,
                            product=inventory.product,
                            transaction_type=InventoryTransaction.TRANSACTION_ADJUST,
                            quantity=difference,
                            note="Bulk stock update"
                        )
                    
                    updated_items.append({
                        "product_id": product_id,
                        "old_quantity": old_quantity,
                        "new_quantity": new_quantity,
                        "difference": difference
                    })
                except Exception as e:
                    errors.append({
                        "product_id": item.get('product_id'),
                        "error": str(e)
                    })
        
        return Response({
            "updated": updated_items,
            "errors": errors
        })