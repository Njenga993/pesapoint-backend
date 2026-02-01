# apps/sales/api/order_viewset.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.sales.models import Order
from apps.sales.serializers import OrderSerializer
from core.auth.permissions import HasPermission
from apps.businesses.api.permissions import IsBusinessOwner, IsBusinessManager

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsBusinessManager]

    def get_queryset(self):
        return Order.objects.filter(
            business=self.request.business
        ).select_related( "business")

    def perform_create(self, serializer):
        serializer.save(business=self.request.business)

