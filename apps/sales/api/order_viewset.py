# apps/sales/api/order_viewset.py
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from apps.sales.models import Order
from apps.sales.serializers.order import OrderSerializer
from apps.sales.services.sales_service import SaleService
from core.auth.permissions import HasPermission
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.sales.models import Order
from apps.sales.serializers import OrderSerializer
from core.pagination import StandardResultsSetPagination
from core.permissions import IsPermitted


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsPermitted]

    # Filters & search
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_status', 'business']
    search_fields = ['id', 'customer__name']
    ordering_fields = ['created_at', 'id']
    ordering = ['-created_at']



class OrderViewSet(ReadOnlyModelViewSet):
    queryset = Order.objects.prefetch_related("items").order_by("-created_at")
    serializer_class = OrderSerializer
    permission_classes = [
        IsAuthenticated,
        HasPermission("sales.view_order"),
    ]

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[
            IsAuthenticated,
            HasPermission("sales.create_order"),
        ],
    )
    def create_order(self, request):
        order = SaleService.create_order(
            user=request.user,
            items=request.data.get("items", []),
        )

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )
