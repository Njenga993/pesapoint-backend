from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth import get_user_model
from apps.accounts.serializers.user import UserSerializer
from core.pagination import StandardResultsSetPagination
from core.auth.permissions import HasPermission

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Users:
    - List, Retrieve, Create, Update
    - Disable user instead of delete
    """
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]  # base permission

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["is_active", "username", "email"]
    search_fields = ["username", "email", "first_name", "last_name"]
    ordering_fields = ["date_joined", "username", "email"]
    ordering = ["-date_joined"]

    def get_permissions(self):
        """
        Dynamic permission mapping per action
        """
        permission_map = {
            "list": HasPermission,       # sales.view_users
            "retrieve": HasPermission,   # sales.view_users
            "create": HasPermission,     # sales.create_user
            "update": HasPermission,     # sales.update_user
            "partial_update": HasPermission,
            "disable_user": HasPermission,
        }

        # Here, you would pass the domain string for the HasPermission check
        # e.g., HasPermission("users.create_user") etc.
        return [permission_map.get(self.action, HasPermission)()]

    @action(detail=True, methods=["post"])
    def disable_user(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({"status": "user disabled"}, status=status.HTTP_200_OK)
