# apps/products/api/product_viewset.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django.db.models import OuterRef, Subquery, Value
from django.db.models.functions import Coalesce

from apps.products.models import Product, Inventory
from apps.products.serializers.product_serializer import ProductSerializer
from apps.products.serializers.pos_product_serializer import POSProductSerializer
from apps.products.permissions import IsBusinessManager, IsCashier
from apps.businesses.api.base import BusinessScopedViewSet


class ProductViewSet(BusinessScopedViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(
            business=self.request.business
        )

    def perform_create(self, serializer):
        """
        Harden: Save the product and then create a corresponding inventory record.
        """
        product = serializer.save(business=self.request.business)
        # Automatically create an inventory record for the new product
        Inventory.objects.get_or_create(
            business=product.business,
            product=product,
            defaults={'quantity': 0}
        )

    def perform_destroy(self, instance):
        """
        Harden: Perform a soft-delete instead of a hard-delete to preserve data integrity.
        """
        instance.is_active = False
        instance.save()

    # ... (pos_list action remains the same) ...
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