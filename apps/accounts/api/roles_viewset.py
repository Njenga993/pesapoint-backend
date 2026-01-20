from django.contrib.auth.models import Group
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.serializers.role import RoleSerializer
from core.auth.permissions import HasPermission


# ---- Permission subclasses (OPTION 1 – safe & explicit) ----
class CanManageRoles(HasPermission):
    required_permission = "users.assign_roles"


class RoleViewSet(viewsets.ModelViewSet):
    """
    API for managing roles (Django Groups).
    """
    queryset = Group.objects.prefetch_related("permissions").order_by("name")
    serializer_class = RoleSerializer
    permission_classes = [
        IsAuthenticated,
        CanManageRoles,
    ]

    def create(self, request, *args, **kwargs):
        """
        Create a role with optional permissions.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        role = Group.objects.create(name=serializer.validated_data["name"])

        permissions = serializer.validated_data.get("permissions", [])
        if permissions:
            role.permissions.set(permissions)

        return Response(
            RoleSerializer(role).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        """
        Update role name and permissions.
        """
        role = self.get_object()
        serializer = self.get_serializer(role, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if "name" in serializer.validated_data:
            role.name = serializer.validated_data["name"]
            role.save()

        if "permissions" in serializer.validated_data:
            role.permissions.set(serializer.validated_data["permissions"])

        return Response(RoleSerializer(role).data)
