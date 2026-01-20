# apps/businesses/api/permissions.py
from rest_framework.permissions import BasePermission

class IsBusinessOwner(BasePermission):
    """
    Only allows access if the user is the owner of the business.
    """
    def has_permission(self, request, view):
        return request.business_role == "owner"


class IsBusinessManager(BasePermission):
    """
    Allows access if the user is the owner or manager of the business.
    """
    def has_permission(self, request, view):
        return request.business_role in ["owner", "manager"]
class IsBusinessOwnerOrManager(BasePermission):
    """
    Owners & managers can manage staff.
    """

    def has_permission(self, request, view):
        return request.business_role in [
            "owner",
            "manager",
        ]