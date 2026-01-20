from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django.db.models import OuterRef, Subquery, Value
from django.db.models.functions import Coalesce

from apps.products.models import Product, Inventory
from apps.products.serializers.product_serializer import ProductSerializer
from apps.products.serializers.pos_product_serializer import POSProductSerializer
from apps.products.permissions import IsManager


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsManager]

    def get_queryset(self):
        return Product.objects.filter(
            business=self.request.business
        )

    def perform_create(self, serializer):
        serializer.save(business=self.request.business)

    # -------------------------------------------
    # POS PRODUCT LIST (FAST QUERY)
    # -------------------------------------------
    @action(
        detail=False,
        methods=["get"],
        url_path="pos",
        permission_classes=[IsAuthenticated],
    )
    def pos_list(self, request):
        inventory_subquery = Inventory.objects.filter(
            business=request.business,
            product=OuterRef("pk"),
        ).values("quantity")[:1]

        qs = (
            Product.objects
            .filter(
                business=request.business,
                is_active=True,
            )
            .select_related("category")
            .annotate(
                stock=Coalesce(Subquery(inventory_subquery), Value(0)),
                category_name=Coalesce("category__name", Value("")),
            )
            .values(
                "id",
                "name",
                "sku",
                "price",
                "stock",
                "category_name",
            )
            .order_by("name")
        )

        serializer = POSProductSerializer(qs, many=True)
        return Response(serializer.data)
