# apps/sales/api/payment_viewset.py
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from apps.sales.models import Payment
from apps.sales.serializers.payment import PaymentSerializer
from apps.sales.services.payment_service import PaymentService
from core.auth.permissions import HasPermission
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.sales.models import Payment
from apps.sales.serializers import PaymentSerializer
from core.pagination import StandardResultsSetPagination
from core.permissions import IsPermitted


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsPermitted]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'method', 'order']
    search_fields = ['id', 'order__id']
    ordering_fields = ['created_at', 'id', 'amount']
    ordering = ['-created_at']



class PaymentViewSet(ReadOnlyModelViewSet):
    queryset = Payment.objects.all().order_by("-created_at")
    serializer_class = PaymentSerializer
    permission_classes = [
        IsAuthenticated,
        HasPermission("sales.view_payment"),
    ]

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[
            IsAuthenticated,
            HasPermission("sales.create_payment"),
        ],
    )
    def create_payment(self, request):
        payment = PaymentService.record_payment(
            order_id=request.data.get("order_id"),
            amount=request.data.get("amount"),
            method=request.data.get("method"),
            user=request.user,
        )

        return Response(
            PaymentSerializer(payment).data,
            status=status.HTTP_201_CREATED,
        )
