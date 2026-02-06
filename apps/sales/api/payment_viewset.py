from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.sales.models import Payment
from apps.sales.serializers import PaymentSerializer
from apps.businesses.api.permissions import IsBusinessOwner, IsBusinessManager

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsBusinessManager]

    def get_queryset(self):
        return Payment.objects.filter(order__business=self.request.business).select_related(
            "order"
        ).order_by("-created_at")

    # BUG FIX: REMOVED THE perform_create METHOD
    # The Payment model does not have a 'business' field.
    # The business context is correctly handled by the relationship to the Order.
    # def perform_create(self, serializer):
    #     serializer.save(business=self.request.business) # <-- THIS WAS INCORRECT