# apps/products/serializers/inventory_serializer.py
from rest_framework import serializers
from apps.products.models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_sku = serializers.CharField(source="product.sku", read_only=True)
    product_price = serializers.DecimalField(
        source="product.price", 
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    product_category = serializers.CharField(
        source="product.category.name", 
        read_only=True
    )
    
    class Meta:
        model = Inventory
        fields = [
            "id",
            "product",
            "product_name",
            "product_sku",
            "product_price",
            "product_category",
            "quantity",
            "updated_at",
        ]
        read_only_fields = ["updated_at"]