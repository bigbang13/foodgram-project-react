from django_filters.rest_framework import (AllValuesMultipleFilter,
                                           BooleanFilter, FilterSet)
from django_filters.widgets import BooleanWidget

from .models import Recipe


class RecipeFilter(FilterSet):

    is_favorited = BooleanFilter(widget=BooleanWidget)
    author = AllValuesMultipleFilter(field_name="author__id")
    is_in_shopping_cart = BooleanFilter(widget=BooleanWidget)
    tags = AllValuesMultipleFilter(field_name="tags__slug")

    class Meta:
        model = Recipe
        fields = ("is_favorited", "author", "is_in_shopping_cart", "tags")