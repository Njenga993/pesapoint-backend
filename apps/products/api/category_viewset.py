from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.products.models import Category
from apps.products.serializers.category_serializer import CategorySerializer
from apps.products.permissions import IsManager


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsManager]

    def get_queryset(self):
        return Category.objects.filter(
            business=self.request.business
        )

    def perform_create(self, serializer):
        serializer.save(business=self.request.business)
