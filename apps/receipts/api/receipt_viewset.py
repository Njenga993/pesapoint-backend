# apps/receipts/api/receipt_viewset.py
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.receipts.models import Receipt
from apps.receipts.serializers.receipt import ReceiptSerializer
from core.auth.permissions import HasPermission
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.receipts.models import Receipt
from apps.receipts.serializers import ReceiptSerializer
from core.pagination import StandardResultsSetPagination
from core.permissions import IsPermitted


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsPermitted]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['payment__id', 'receipt_number']
    search_fields = ['receipt_number', 'payment__order__id']
    ordering_fields = ['created_at', 'receipt_number']
    ordering = ['-created_at']



class ReceiptViewSet(ReadOnlyModelViewSet):
    queryset = Receipt.objects.all().order_by("-created_at")
    serializer_class = ReceiptSerializer
    permission_classes = [
        IsAuthenticated,
        HasPermission("receipts.view_receipt"),
    ]
