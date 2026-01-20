# core/auth/permissions.py

from rest_framework.permissions import BasePermission


class HasPermission(BasePermission):
    """
    Permission checker using domain-style permission strings.
    """

    required_permission = None

    def has_permission(self, request, view):
        if not self.required_permission:
            return True

        codename = self.required_permission.replace(".", "_")
        return request.user.has_perm(f"core.{codename}")
    
class CanViewFinancialReports(HasPermission):
    required_permission = "accounts.view_financial_reports"

