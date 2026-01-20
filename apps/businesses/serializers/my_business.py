from rest_framework import serializers
from apps.businesses.models import BusinessUser


class MyBusinessSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="business.id")
    name = serializers.CharField(source="business.name")

    class Meta:
        model = BusinessUser
        fields = ["id", "name", "role"]
