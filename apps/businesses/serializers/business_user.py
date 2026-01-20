from rest_framework import serializers
from apps.businesses.models import BusinessUser


class BusinessUserSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    class Meta:
        model = BusinessUser
        fields = [
            "id",
            "user",
            "user_email",
            "business",
            "role",
            "is_active",
            "joined_at",
        ]
        read_only_fields = [
            "id",
            "joined_at",
        ]
