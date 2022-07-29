from django.contrib.auth.tokens import PasswordResetTokenGenerator
from djoser.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import User, ROLE_CHOICES


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

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
        return value

    class Meta:
        model = User
        fields = (
            "email",
            "username",
        )


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    role = serializers.ChoiceField(
        choices=ROLE_CHOICES,
        default="user",
    )

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
        return value

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "email",
            "first_name",
            "last_name",
        )


class UserMeSerializer(UserSerializer):
    role = serializers.ChoiceField(
        choices=ROLE_CHOICES,
        read_only=True,
    )


class CustomTokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=200,
        required=True,
    )
    confirmation_code = serializers.CharField(
        max_length=200,
        required=True,
    )

    def validate_username(self, value):
        """Пользователь должен существовать, иначе ошибка 404"""
        get_object_or_404(User, username=value.lower())
        return value.lower()

    def validate_confirmation_code(self, value):
        """Валидация confirmation_code"""
        lower_confirmation_code = value.lower()
        if self.initial_data.get("username") is None:
            raise serializers.ValidationError(
                "Нельзя делать запрос без username"
            )
        username = self.initial_data.get("username")
        user = get_object_or_404(User, username=username)
        if not PasswordResetTokenGenerator().check_token(
            user, lower_confirmation_code
        ):
            raise serializers.ValidationError("Неверный код подтверждения")
        return lower_confirmation_code
