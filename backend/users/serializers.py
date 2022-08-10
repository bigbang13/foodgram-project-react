from recipes.models import Recipe
from rest_framework import serializers

from .models import Subscription, User


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(required=True, max_length=150)
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=True, max_length=150)

    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email=lower_email).exists():
            raise serializers.ValidationError('Email должен быть уникальным')
        return lower_email

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Username должен быть уникальным'
            )
        return value

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class UserIDSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous or request is None:
            return False
        return User.objects.filter(
            following__user=request.user,
            follower__author=obj
        ).exists()

#        return Subscription.objects.filter(
#            user=request.user,
#            author=obj.id
#        ).exists()


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
    email = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous or request is None:
            return False
        return User.objects.filter(
            following__user=request.user,
            follower__author=obj
        ).exists()

#    def get_is_subscribed(self, obj):
#        request = self.context.get('request')
#        if request.user.is_anonymous or request is None:
#            return False
#        return Subscription.objects.filter(
#            user=request.user,
#            author=obj.id
#        ).exists()

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        return SubscriptionRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
