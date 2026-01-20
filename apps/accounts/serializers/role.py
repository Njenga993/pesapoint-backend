from django.contrib.auth.models import Group, Permission
from rest_framework import serializers


class RoleSerializer(serializers.ModelSerializer):
    """
    Serializer for Roles (Django Groups).
    """
    permissions = serializers.SlugRelatedField(
        many=True,
        slug_field="codename",
        queryset=Permission.objects.all(),
        required=False,
    )

    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "permissions",
        ]
