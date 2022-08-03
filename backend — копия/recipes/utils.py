from django.shortcuts import get_object_or_404

from .models import RecipeIngredient, Tag


def save_tags_and_ingredients(self, obj):
    tags = self.initial_data.get('tags')
    for tag in tags:
        obj.tags.add(get_object_or_404(Tag, pk=tag))
    ingredients = self.initial_data.get('ingredients')
    for ingredient in ingredients:
        RecipeIngredient.objects.create(
            ingredient_id=ingredient.get('id'),
            recipe=obj,
            amount=ingredient.get('amount')
        )
