from rest_framework.permissions import BasePermission


class IsBusinessOwner(BasePermission):
    def has_permission(self, request, view):
        return request.business_role == "owner"


class IsBusinessManager(BasePermission):
    def has_permission(self, request, view):
        return request.business_role in ["owner", "manager"]


class IsBusinessStaff(BasePermission):
    def has_permission(self, request, view):
        return request.business_role in ["owner", "manager", "cashier"]
