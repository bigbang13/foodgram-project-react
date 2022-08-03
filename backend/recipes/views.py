import base64

from django.contrib.auth.hashers import check_password
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import (CharFilter, DjangoFilterBackend,
                                           FilterSet, NumberFilter)
from rest_framework import filters, generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.permissions import IsAdminOrReadOnly, UserPermission
from users.models import User

from .models import FavoriteRecipes, Ingredient, Recipe, Tag, ShoppingCart
from .serializers import FavoriteRecipesSerializer, IngredientSerializer, RecipeSerializer, TagSerializer, ShoppingCartSerializer
from .utils import create_delete


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

#    def get_image(self, request):
#        data = request.get("image")
#        img_name = request.get("name")
#        format, imgstr = data.split(';base64,')
#        ext = format.split('/')[-1]
#        image_file = ContentFile(base64.b64decode(imgstr), name=img_name + ext)
#        return image_filer

    @action(
        methods=["post", "delete"],
        url_path="(?P<id>[0-9]+)/shopping_cart",
        detail=False
    )
    def shopping_cart(self, request, **kwargs):
        return create_delete(self, ShoppingCart, ShoppingCartSerializer, request, **kwargs)

    @action(
        methods=["post", "delete"],
        url_path="(?P<id>[0-9]+)/favorite",
        detail=False
    )
    def favorite_recipes(self, request, **kwargs):
        return create_delete(self, FavoriteRecipes, FavoriteRecipesSerializer, request, **kwargs)
