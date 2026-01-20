from rest_framework import serializers
from apps.businesses.models import Business


class BusinessSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = [
            "id",
            "name",
        ]
        read_only_fields = ["id"]
class BusinessUpdateSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = [
            "name",
            "address",
            "phone_number",
            "email",
            "website",
        ]