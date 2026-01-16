# apps/receipts/serializers/print_log.py
from rest_framework import serializers
from apps.receipts.models import ReceiptPrintLog


class ReceiptPrintLogSerializer(serializers.ModelSerializer):
    receipt_number = serializers.CharField(
        source="receipt.receipt_number",
        read_only=True,
    )

    class Meta:
        model = ReceiptPrintLog
        fields = [
            "id",
            "receipt_number",
            "method",
            "printer_name",
            "printed_by",
            "created_at",
        ]
        read_only_fields = fields
