

# apps/sales/api/payment_viewset.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.sales.models import Payment
from apps.sales.serializers import PaymentSerializer
from apps.businesses.api.permissions import IsBusinessOwner, IsBusinessManager

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsBusinessManager]

    def get_queryset(self):
        return Payment.objects.filter(business=self.request.business).select_related(
            "order", "customer"
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(business=self.request.business)

