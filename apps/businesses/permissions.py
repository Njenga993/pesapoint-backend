from rest_framework.permissions import BasePermission
from apps.businesses.models import BusinessUser


class IsBusinessOwner(BasePermission):
    """
    Allows access only to business owners.
    """
    def has_permission(self, request, view):
        return request.business_role == "owner"
    
    def has_object_permission(self, request, view, obj):
        return BusinessUser.objects.filter(
            user=request.user,
            business=obj,
            role=BusinessUser.ROLE_OWNER,
            is_active=True,
        ).exists()
class CanManageBusinessUsers(BasePermission):
    """
    Allows access to users who can manage business users.
    """

    def has_object_permission(self, request, view, obj):
        return BusinessUser.objects.filter(
            user=request.user,
            business=obj,
            role__in=[
                BusinessUser.ROLE_OWNER,
                BusinessUser.ROLE_MANAGER,
            ],
            is_active=True,
        ).exists()
    
class IsBusinessOwnerOrManager(BasePermission):
    """
    Owners & managers can manage staff.
    """
    def has_permission(self, request, view):
        return request.business_role in ["owner", "manager"]
    
    def has_permission(self, request, view):
        business_id = (
            request.data.get("business")
            or request.query_params.get("business")
        )

        if not business_id:
            return False

        return BusinessUser.objects.filter(
            user=request.user,
            business_id=business_id,
            role__in=[
                BusinessUser.ROLE_OWNER,
                BusinessUser.ROLE_MANAGER,
            ],
            is_active=True,
        ).exists()    