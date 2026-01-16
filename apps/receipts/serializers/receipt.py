# apps/receipts/serializers/receipt.py
from rest_framework import serializers
from apps.receipts.models import Receipt


class ReceiptSerializer(serializers.ModelSerializer):
    has_pdf = serializers.BooleanField(read_only=True)

    class Meta:
        model = Receipt
        fields = [
            "id",
            "receipt_number",
            "created_at",
            "has_pdf",
        ]
        read_only_fields = fields
