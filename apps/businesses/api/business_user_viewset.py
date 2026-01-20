from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from apps.businesses.models import BusinessUser
from apps.businesses.serializers.business_user import BusinessUserSerializer
from apps.businesses.permissions import (
    IsBusinessOwner,
    IsBusinessOwnerOrManager,
)


class BusinessUserViewSet(ModelViewSet):
    """
    Business Staff Management API
    """

    serializer_class = BusinessUserSerializer
    permission_classes = [IsAuthenticated]

    # -------------------------
    # Queryset
    # -------------------------
    def get_queryset(self):
        return BusinessUser.objects.filter(
            business__members__user=self.request.user,
            business__members__is_active=True,
        ).select_related("user", "business")

    # -------------------------
    # Permissions
    # -------------------------
    def get_permissions(self):
        if self.action in ["create"]:
            return [IsAuthenticated(), IsBusinessOwnerOrManager()]

        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsBusinessOwner()]

        return super().get_permissions()

    # -------------------------
    # Prevent owners from being removed
    # -------------------------
    def perform_destroy(self, instance):
        if instance.role == BusinessUser.ROLE_OWNER:
            raise PermissionDenied("Business must have at least one owner.")

        instance.is_active = False
        instance.save()
