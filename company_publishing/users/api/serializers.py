from django.contrib.auth import get_user_model
from rest_framework import serializers

from company_publishing.users.models import User as UserType

User = get_user_model()


class EmbeddedUserSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = ["username", "name", "image"]


class UserSerializer(serializers.ModelSerializer[UserType]):
    added_by = EmbeddedUserSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["username", "name", "type", "image", "password", "added_by"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
            "password": {"write_only": True, "required": False},
        }

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        data = super().validate(attrs)
        if not self.instance and not data.get("password"):
            raise serializers.ValidationError({"password": ["This field is required."]})
        return data

    def create(self, validated_data: dict[str, str]) -> User:
        password = validated_data.pop("password")
        user = User.objects.create_user(added_by=self.context["request"].user, **validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance: User, validated_data: dict[str, str]) -> User:
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class SignupSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = ["username", "name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict[str, str]) -> User:
        return User.objects.create_user(**validated_data)
