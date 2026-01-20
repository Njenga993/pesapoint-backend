from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.business_role == "owner"


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.business_role in ["owner", "manager"]


class IsCashier(BasePermission):
    def has_permission(self, request, view):
        return request.business_role in ["owner", "manager", "cashier"]
