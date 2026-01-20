# apps/accounts/api/permission_viewset.py
from django.contrib.auth.models import Permission, Group
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.accounts.serializers.permission import PermissionSerializer
from apps.accounts.permissions import HasPermission


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API for viewing and assigning permissions.
    """

    queryset = Permission.objects.select_related("content_type")
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Limit to this project’s app permissions only.
        """
        return Permission.objects.filter(
            content_type__app_label="accounts"
        )

    @action(detail=False, methods=["post"], url_path="assign")
    def assign_permission(self, request):
        """
        Assign a permission to a role (group).

        Payload:
        {
            "group_id": 1,
            "permission_id": 5
        }
        """
        group_id = request.data.get("group_id")
        permission_id = request.data.get("permission_id")

        if not group_id or not permission_id:
            return Response(
                {"detail": "group_id and permission_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            group = Group.objects.get(id=group_id)
            permission = Permission.objects.get(id=permission_id)
        except (Group.DoesNotExist, Permission.DoesNotExist):
            return Response(
                {"detail": "Invalid group or permission"},
                status=status.HTTP_404_NOT_FOUND
            )

        group.permissions.add(permission)

        return Response(
            {"detail": "Permission assigned successfully"},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"], url_path="remove")
    def remove_permission(self, request):
        """
        Remove a permission from a role (group).
        """
        group_id = request.data.get("group_id")
        permission_id = request.data.get("permission_id")

        try:
            group = Group.objects.get(id=group_id)
            permission = Permission.objects.get(id=permission_id)
        except (Group.DoesNotExist, Permission.DoesNotExist):
            return Response(
                {"detail": "Invalid group or permission"},
                status=status.HTTP_404_NOT_FOUND
            )

        group.permissions.remove(permission)

        return Response(
            {"detail": "Permission removed successfully"},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["get"], url_path="groups")
    def permission_groups(self, request, pk=None):
        """
        List all roles (groups) that have this permission.
        """
        permission = self.get_object()
        groups = permission.group_set.all()

        return Response(
            [{"id": g.id, "name": g.name} for g in groups],
            status=status.HTTP_200_OK
        )
