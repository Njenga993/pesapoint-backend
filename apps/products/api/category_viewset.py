# apps/products/api/category_viewset.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.businesses.api.base import BusinessScopedViewSet
from apps.products.models import Category
from apps.products.serializers.category_serializer import CategorySerializer


class CategoryViewSet(BusinessScopedViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(business=self.request.business)

    def perform_create(self, serializer):
        serializer.save(business=self.request.business)

    def perform_destroy(self, instance):
        """
        Harden: Prevent deletion if the category is being used by any active products.
        """
        if instance.products.filter(is_active=True).exists():
            raise serializers.ValidationError(
                "Cannot delete a category that is in use by active products."
            )
        instance.delete()