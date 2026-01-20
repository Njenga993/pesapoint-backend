from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.receipts.models import Receipt
from apps.receipts.services.print_audit_service import ReceiptPrintAuditService
from apps.receipts.permissions import (
    IsBusinessManager,
    IsBusinessStaff,
)


class ReceiptPrintViewSet(viewsets.ViewSet):
    """
    Receipt printing endpoints (business-scoped).
    """

    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "print_pdf":
            permission_classes = [IsAuthenticated, IsBusinessManager]
        elif self.action == "print_thermal":
            permission_classes = [IsAuthenticated, IsBusinessStaff]
        else:
            permission_classes = self.permission_classes

        return [permission() for permission in permission_classes]

    # -------------------------------------------------
    # PDF Printing
    # -------------------------------------------------

    @action(detail=False, methods=["post"], url_path="pdf")
    def print_pdf(self, request):
        receipt_id = request.data.get("receipt_id")

        if not receipt_id:
            return Response(
                {"detail": "receipt_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        receipt = Receipt.objects.filter(
            id=receipt_id,
            business=request.business
        ).first()

        if not receipt:
            return Response(
                {"detail": "Receipt not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        ReceiptPrintAuditService.log_print(
            receipt_id=receipt.id,
            method="pdf",
            printed_by=request.user,
        )

        return Response(
            {"status": "pdf_printed"},
            status=status.HTTP_201_CREATED,
        )

    # -------------------------------------------------
    # Thermal Printing
    # -------------------------------------------------

    @action(detail=False, methods=["post"], url_path="thermal")
    def print_thermal(self, request):
        receipt_id = request.data.get("receipt_id")
        printer_name = request.data.get("printer_name", "")

        if not receipt_id:
            return Response(
                {"detail": "receipt_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        receipt = Receipt.objects.filter(
            id=receipt_id,
            business=request.business
        ).first()

        if not receipt:
            return Response(
                {"detail": "Receipt not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        ReceiptPrintAuditService.log_print(
            receipt_id=receipt.id,
            method="thermal",
            printed_by=request.user,
            printer_name=printer_name,
        )

        return Response(
            {"status": "thermal_printed"},
            status=status.HTTP_201_CREATED,
        )
