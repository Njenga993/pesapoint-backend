# apps/sales/serializers/order.py
from rest_framework import serializers
from apps.sales.models import Order
from .order_item import OrderItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    balance = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "total_amount",
            "balance",
            "created_at",
            "items",
        ]
        read_only_fields = fields
