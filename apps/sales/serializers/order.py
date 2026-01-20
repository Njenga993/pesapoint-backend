from decimal import Decimal

from django.db.models import Sum, F
from rest_framework import serializers

from apps.sales.models import Order, Payment
from .order_item import OrderItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    total_amount = serializers.SerializerMethodField()
    paid_amount = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "payment_status",
            "total_amount",
            "paid_amount",
            "balance",
            "created_at",
            "items",
        ]
        read_only_fields = fields

    def get_total_amount(self, obj):
        """
        Sum of (quantity * price) for all order items.
        """
        result = obj.items.aggregate(
            total=Sum(F("quantity") * F("price"))
        )["total"]

        return result or Decimal("0.00")

    def get_paid_amount(self, obj):
        """
        Sum of completed incoming payments.
        """
        result = obj.payments.filter(
            status=Payment.STATUS_COMPLETED,
            direction=Payment.DIRECTION_IN,
        ).aggregate(
            total=Sum("amount")
        )["total"]

        return result or Decimal("0.00")

    def get_balance(self, obj):
        return self.get_total_amount(obj) - self.get_paid_amount(obj)
