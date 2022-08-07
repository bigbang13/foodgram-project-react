from recipes.models import Recipe
from rest_framework import serializers

from .models import Subscription, User


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(required=True, max_length=150)
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=True, max_length=150)
    password = serializers.CharField(
        write_only=True,
        required=True,
        max_length=150
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
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username должен быть уникальным"
            )
        return value

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password"
        )


class UserIDSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed"
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous or request is None:
            return False
        return Subscription.objects.filter(
            user=request.user,
            author=obj
        ).exists()


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
            raise serializers.ValidationError(
                "Новый пароль не должен совпадать с действующим"
            )
        return value


class SubscriptionRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscriptionSerializer(serializers.Serializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user=obj.user,
            author=obj.author
        ).exists()

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        return SubscriptionRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
