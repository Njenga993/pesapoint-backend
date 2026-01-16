# apps/receipts/api/print_viewset.py
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.receipts.services.print_audit_service import ReceiptPrintAuditService
from core.auth.permissions import HasPermission
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.receipts.models import ReceiptPrintLog
from apps.receipts.serializers import ReceiptPrintLogSerializer
from core.pagination import StandardResultsSetPagination
from core.permissions import IsPermitted


class ReceiptPrintLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only audit logs for printed receipts.
    """
    queryset = ReceiptPrintLog.objects.all()
    serializer_class = ReceiptPrintLogSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsPermitted]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['receipt__receipt_number', 'method', 'printed_by']
    search_fields = ['receipt__receipt_number', 'printed_by__username']
    ordering_fields = ['created_at', 'receipt__receipt_number']
    ordering = ['-created_at']


class ReceiptPrintViewSet(ViewSet):
    permission_classes = [
        IsAuthenticated,
        HasPermission("receipts.print_receipt"),
    ]

    def create(self, request):
        receipt_id = request.data.get("receipt_id")
        method = request.data.get("method")  # pdf | thermal

        ReceiptPrintAuditService.print_receipt(
            receipt_id=receipt_id,
            method=method,
            user=request.user,
        )

        return Response(
            {"status": "printed"},
            status=status.HTTP_201_CREATED,
        )
