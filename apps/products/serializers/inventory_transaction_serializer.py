from rest_framework import serializers
from apps.products.models import InventoryTransaction


class InventoryTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTransaction
        fields = [
            "id",
            "product",
            "transaction_type",
            "quantity",
            "note",
            "created_at",
        ]
