# apps/products/api/category_viewset.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
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