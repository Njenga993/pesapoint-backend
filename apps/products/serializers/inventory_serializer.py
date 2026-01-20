from rest_framework import serializers
from apps.products.models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    class Meta:
        model = Inventory
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "updated_at",
        ]
        read_only_fields = ["updated_at"]
        depth = 1