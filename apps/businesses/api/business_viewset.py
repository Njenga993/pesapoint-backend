from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from apps.businesses.models import Business, BusinessUser
from apps.businesses.serializers.business import BusinessSerializer
from apps.businesses.permissions import IsBusinessOwner
from apps.businesses.serializers.my_business import MyBusinessSerializer


class BusinessViewSet(ModelViewSet):
    """
    Business API

    - List businesses user belongs to
    - Create new business (auto assigns owner)
    - Retrieve business details
    - Update only if owner
    """

    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    # -------------------------
    # Queryset scoping
    # -------------------------
    def get_queryset(self):
        return Business.objects.filter(
            members__user=self.request.user,
            members__is_active=True,
        ).distinct()

    # -------------------------
    # Create business
    # -------------------------
    def perform_create(self, serializer):
        business = serializer.save(owner=self.request.user)

        # Auto-create owner membership
        BusinessUser.objects.create(
            user=self.request.user,
            business=business,
            role=BusinessUser.ROLE_OWNER,
        )

    # -------------------------
    # Permissions per action
    # -------------------------
    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsBusinessOwner()]
        return super().get_permissions()

    # -------------------------
    # Safety: prevent deleting businesses
    # -------------------------
    def destroy(self, request, *args, **kwargs):
        raise PermissionDenied("Businesses cannot be deleted.")
    
        # ------------------------------------------------
    # 🔹 My Businesses (Business Switcher)
    # ------------------------------------------------
    @action(detail=False, methods=["get"], url_path="my-businesses")
    def my_businesses(self, request):
        memberships = (
            BusinessUser.objects
            .select_related("business")
            .filter(user=request.user, is_active=True)
        )

        serializer = MyBusinessSerializer(memberships, many=True)
        return Response(serializer.data)
