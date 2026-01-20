from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.businesses.serializers.business_settings import BusinessSettingsSerializer
from apps.businesses.permissions import IsBusinessOwnerOrManager


class BusinessSettingsViewSet(viewsets.ViewSet):
    """
    Business settings (business-scoped).

    GET  /api/v1/businesses/settings/
    PATCH /api/v1/businesses/settings/
    """

    permission_classes = [
        IsAuthenticated,
        IsBusinessOwnerOrManager,
    ]

    def retrieve(self, request):
        serializer = BusinessSettingsSerializer(request.business)
        return Response(serializer.data)

    def partial_update(self, request):
        serializer = BusinessSettingsSerializer(
            request.business,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
