# apps/sales/serializers/order_item.py
from rest_framework import serializers
from apps.sales.models import OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            
        ]
        read_only_fields = ["total_price"]
