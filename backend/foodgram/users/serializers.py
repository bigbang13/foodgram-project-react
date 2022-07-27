from django.contrib.auth.tokens import PasswordResetTokenGenerator
from djoser.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from users.models import User, ROLE_CHOICES


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()


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
        fields = ("email", "id", "username", "first_name", "last_name", "password")


class UserIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "id", "username", "first_name", "last_name")


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, value):
        """Проверка соответствия пары email-pwd"""
        password = value.get("password")
        email = value.get("email")
        
        if email and password:
            user = User.objects.filter(email=email).first()
            if user:
                if user.password == password:
                    return user
                else:
                    raise serializers.ValidationError("Неправильный пароль")
            else:
                raise serializers.ValidationError("Пользователь с указанным email не найден")


    class Meta:
        model = User
        fields = ["password", "email"]


class PasswordChangeSerializer(serializers.Serializer):
    new_password =  serializers.CharField()
    current_password = serializers.CharField()

    def validate(self, value):
        """Current_password должен совпадать с текущим паролем."""
        current_password = value.get("current_password")
        new_password = value.get("new_password")
        if current_password==new_password:
            raise serializers.ValidationError("Новый пароль не должен совпадать с действующим")
        return value
