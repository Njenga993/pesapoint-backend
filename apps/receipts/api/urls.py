from rest_framework.routers import DefaultRouter

from apps.receipts.api.receipt_viewset import ReceiptViewSet
from apps.receipts.api.print_viewset import ReceiptPrintViewSet, ReceiptPrintViewSet

router = DefaultRouter()
router.register(r"receipts", ReceiptViewSet, basename="receipt")
router.register(r"print", ReceiptPrintViewSet, basename="receipt-print")
router.register("print-logs", ReceiptPrintViewSet, basename="receipt-print-log")

urlpatterns = router.urls
