from django_filters.rest_framework import (AllValuesMultipleFilter,
                                           BooleanFilter, FilterSet)

from .models import Recipe


class RecipeFilter(FilterSet):

    is_favorited = BooleanFilter(
        method='get_is_favorited'
    )
    author = AllValuesMultipleFilter(field_name="author__id")
    is_in_shopping_cart = BooleanFilter(
        method='get_is_in_shopping_cart'
    )
    tags = AllValuesMultipleFilter(field_name="tags__slug")

    class Meta:
        model = Recipe
        fields = ("is_favorited", "author", "is_in_shopping_cart", "tags")

    def get_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset
