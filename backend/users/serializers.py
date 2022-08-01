from django.contrib.auth import authenticate
from djoser.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.fields import CurrentUserDefault

from users.models import User, ROLE_CHOICES


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(required=True, max_length=150)
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=True, max_length=150)
    password = serializers.CharField(write_only=True, required=True, max_length=150)

    def validate_email(self, value):
        """Email должен быть уникальным."""
        lower_email = value.lower()
        if User.objects.filter(email=lower_email).exists():
            raise serializers.ValidationError("Email должен быть уникальным")
        return lower_email

    def validate_username(self, value):
        """Использовать имя 'me' в качестве username запрещено."""
        if value.lower() == "me":
            raise serializers.ValidationError(
                "Использовать имя 'me' в качестве username запрещено."
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username должен быть уникальным")
        return value

    class Meta:
        model = User
        fields = ("email", "id", "username", "first_name", "last_name", "password")


class UserIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "id", "username", "first_name", "last_name", "password")


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField()
    email = serializers.EmailField()


class PasswordChangeSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    current_password = serializers.CharField()

    def validate(self, value):
        """Current_password должен совпадать с текущим паролем."""
        current_password = value.get("current_password")
        new_password = value.get("new_password")
        if current_password == new_password:
            raise serializers.ValidationError("Новый пароль не должен совпадать с действующим")
        return value
