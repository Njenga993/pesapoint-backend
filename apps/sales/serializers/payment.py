from rest_framework import serializers
from apps.sales.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(source="order.id", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "direction",
            "method",
            "amount",
            "status",
            "created_at",
        ]
        read_only_fields = fields
