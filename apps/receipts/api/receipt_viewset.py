# apps/sales/api/receipt_viewset.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.receipts.models import Receipt
from apps.receipts.serializers import ReceiptSerializer
from apps.businesses.api.permissions import IsBusinessOwner, IsBusinessManager

class ReceiptViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReceiptSerializer
    permission_classes = [IsAuthenticated, IsBusinessManager]

    def get_queryset(self):
        return Receipt.objects.filter(business=self.request.business).select_related(
            "order", "payment"
        ).order_by("-created_at")
