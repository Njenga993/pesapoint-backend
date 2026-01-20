from rest_framework import serializers
from apps.businesses.models import Business


class BusinessSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(
        source="owner.email",
        read_only=True
    )

    class Meta:
        model = Business
        fields = [
            "id",
            "name",
            "owner",
            "owner_email",
            "is_active",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "owner",
            "created_at",
        ]
