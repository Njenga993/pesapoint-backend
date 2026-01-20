# apps/accounts/api/account_viewset.py
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.accounts.models import Account
from apps.accounts.serializers.ledger import AccountSerializer  # we will create this
from core.auth.permissions import HasPermission
from core.pagination import StandardResultsSetPagination


class AccountViewSet(ReadOnlyModelViewSet):
    """
    Read-only API for Chart of Accounts.
    """
    queryset = Account.objects.all().order_by("code")
    serializer_class = AccountSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [
        IsAuthenticated,
        HasPermission,  # class-based permission
    ]

    # Filtering, search, ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['code', 'name']
    search_fields = ['code', 'name']
    ordering_fields = ['code', 'name']
    ordering = ['code']

    def get_permissions(self):
        """
        Assign specific permission per action.
        """
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated(), HasPermission()]
        return super().get_permissions()
