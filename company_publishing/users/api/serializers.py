from django.contrib.auth import get_user_model
from rest_framework import serializers

from company_publishing.users.models import User as UserType

User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = ["username", "name"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }


class SignupSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = ["username", "name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict[str, str]) -> User:
        return User.objects.create_user(**validated_data)
