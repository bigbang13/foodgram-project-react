from api.permissions import IsAdminOrReadOnly, IsAuthorOrStaff
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import RecipeFilter
from .models import (FavoriteRecipes, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)
from .paginations import RecipePagination
from .serializers import (FavoriteRecipesSerializer, IngredientSerializer,
                          RecipePostSerializer, RecipeSerializer,
                          ShoppingCartSerializer, TagSerializer)
from .utils import create_delete


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name']


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrStaff)
    pagination_class = RecipePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    @action(
        methods=["post", "delete"],
        url_path="(?P<recipe_id>[0-9]+)/shopping_cart",
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, **kwargs):
        return create_delete(
            self,
            ShoppingCart,
            ShoppingCartSerializer,
            RecipePostSerializer,
            request,
            **kwargs
        )

    @action(
        methods=["post", "delete"],
        url_path="(?P<recipe_id>[0-9]+)/favorite",
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def favorite_recipes(self, request, **kwargs):
        return create_delete(
            self,
            FavoriteRecipes,
            FavoriteRecipesSerializer,
            RecipePostSerializer,
            request,
            **kwargs
        )

    @action(
        methods=["get"],
        url_path="download_shopping_cart",
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        spisok = Recipe.objects.filter(
            shopping_cart__user=self.request.user
        ).all()
        data = dict()
        if not spisok:
            raise ParseError('Нет рецептов в корзине')
        for recipe in spisok:
            ingredients = RecipeIngredient.objects.filter(
                recipe=recipe
            ).all()
            for i in ingredients:
                if f'{i.ingredient.id}' in data:

                    data[
                        f'{i.ingredient.id}'
                    ]['amount'] += i.amount
                else:
                    data.update(
                        {
                            f'{i.ingredient.id}': {
                                'name': i.ingredient.name,
                                'measurement_unit':
                                    i.ingredient.measurement_unit,
                                'amount': i.amount
                            }
                        }
                    )
        data = dict(sorted(data.items(), key=lambda item: item[1]['name']))
        data = HttpResponse(data, content_type='text/plain')
        data['Content-Disposition'] = (
            'attachment; filename="shopping_cart"'
        )
        return data
