# apps/products/serializers/inventory_transaction_serializer.py
from rest_framework import serializers
from apps.products.models import InventoryTransaction


class InventoryTransactionSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_sku = serializers.CharField(source="product.sku", read_only=True)
    
    class Meta:
        model = InventoryTransaction
        fields = [
            "id",
            "product",
            "product_name",
            "product_sku",
            "transaction_type",
            "quantity",
            "note",
            "created_at",
        ]
        read_only_fields = ["created_at"]