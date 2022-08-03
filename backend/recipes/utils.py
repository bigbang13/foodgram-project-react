from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import RecipeIngredient, Tag, Recipe
from rest_framework.response import Response


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


def create_delete(self, models_class, save_serial, post_serial, request, **kwargs):
    in_shop_cart = models_class.objects.filter(user=self.request.user, recipe=kwargs["id"]).exists()
    if request.method == "POST":
        if in_shop_cart:
            return Response("Рецепт уже был добавлен", status=status.HTTP_400_BAD_REQUEST)
        user = self.request.user
        request.data.update({"user": user.id, "recipe": kwargs["id"]})
        serializer = save_serial(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        recipe = get_object_or_404(Recipe, id=kwargs['id'])
        serializer = post_serial(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if request.method == "DELETE":
        if not in_shop_cart:
            return Response("Рецепта нет в списке", status=status.HTTP_400_BAD_REQUEST)
        get_object_or_404(models_class, user=self.request.user, recipe=kwargs["id"]).delete()
        return Response("Рецепт удален", status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
