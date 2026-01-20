# apps/accounts/permissions.py
from rest_framework.permissions import BasePermission


class HasPermission(BasePermission):
    """
    Base permission checker.
    Subclasses must define `required_permission`
    as a Django permission codename (without app label).
    """

    required_permission = None

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if not self.required_permission:
            return False

        return request.user.has_perm(
            f"accounts.{self.required_permission}"
        )
    
class CanViewFinancialReports(HasPermission):
    required_permission = "view_financial_reports"
