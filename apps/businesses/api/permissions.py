# apps/businesses/api/permissions.py
from rest_framework.permissions import BasePermission
from apps.businesses.models import BusinessUser

class IsBusinessOwner(BasePermission):
    """
    Only allows access if the user is the owner of the business.
    """
    def has_permission(self, request, view):
        return request.business_role == "owner"




class IsBusinessManager(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        business_id = getattr(request, "business_id", None)
        if not business_id:
            return False

        try:
            membership = BusinessUser.objects.select_related("business").get(
                user=user,
                business_id=business_id,
                is_active=True,
            )
        except BusinessUser.DoesNotExist:
            return False

        # Attach context once
        request.business = membership.business
        request.business_role = membership.role

        # 🔥 FIX: lowercase roles
        return membership.role in ["owner", "manager"]



class IsBusinessOwnerOrManager(BasePermission):
    """
    Owners & managers can manage staff.
    """

    def has_permission(self, request, view):
        return request.business_role in [
            "owner",
            "manager",
        ]