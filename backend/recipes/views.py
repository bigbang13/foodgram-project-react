from api.permissions import IsAdminOrReadOnly, IsAuthorOrStaff
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import RecipeFilter
from .models import FavoriteRecipes, Ingredient, Recipe, ShoppingCart, Tag
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
    pagination_class = None
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
        data = {}
        if not spisok:
            raise ParseError('Нет рецептов в корзине')
        for recept in spisok:
            ingredients = recept.recipeingr.all()
            for i in ingredients:
                name = i.ingredient.name
                amount = i.amount
                measurement_unit = i.ingredient.measurement_unit
                if name not in data:
                    data[name] = {
                        'measurement_unit': measurement_unit,
                        'amount': amount}
                else:
                    data[name]['amount'] = (
                        data[name]['amount'] + amount)
        data_list = []
        for index, key in enumerate(data, start=1):
            data_list.append(
                f'{index}. {key} - {data[key]["amount"]} '
                f'{data[key]["measurement_unit"]}\n')
        out_data = HttpResponse(data_list, content_type='text/plain')
        out_data['Content-Disposition'] = (
            'attachment; filename="shopping_cart"'
        )
        return out_data
