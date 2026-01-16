# apps/accounts/api/ledger_viewset.py
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import LedgerEntry
from apps.accounts.serializers.ledger import LedgerEntrySerializer
from core.auth.permissions import HasPermission


class LedgerViewSet(ReadOnlyModelViewSet):
    queryset = LedgerEntry.objects.select_related("account").order_by("-created_at")
    serializer_class = LedgerEntrySerializer
    permission_classes = [
        IsAuthenticated,
        HasPermission("accounts.view_ledger"),
    ]
