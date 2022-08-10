import io

import reportlab
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.colors import black, grey, orange
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.response import Response

from .models import Recipe, RecipeIngredient, Tag

reportlab.rl_config.TTFSearchPath.append(
    str(settings.BASE_DIR) + '/reportlab/fonts'
)

def save_tags_and_ingredients(self, obj):
    tags = self.initial_data.get('tags')
    for tag in tags:
        obj.tags.add(get_object_or_404(Tag, pk=tag))
    ingredients = self.initial_data.get('ingredients')
    for ingredient in ingredients:
        RecipeIngredient.objects.create(
            ingredient_id=ingredient.get('id'),
            recipe=obj,
            amount=ingredient.get('amount'),
        )


def create_delete(
    self, models_class, save_serial, post_serial, request, **kwargs
):
    in_shop_cart = models_class.objects.filter(
        user=self.request.user, recipe=kwargs['recipe_id']
    ).exists()
    if request.method == 'POST':
        if in_shop_cart:
            return Response(
                'Рецепт уже был добавлен', status=status.HTTP_400_BAD_REQUEST
            )
        user = self.request.user
        request.data.update({'user': user.id, 'recipe': kwargs['recipe_id']})
        serializer = save_serial(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        recipe = get_object_or_404(Recipe, id=kwargs['recipe_id'])
        serializer = post_serial(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if request.method == 'DELETE':
        if not in_shop_cart:
            return Response(
                'Рецепта нет в списке',
                status=status.HTTP_400_BAD_REQUEST
            )
        get_object_or_404(
            models_class, user=self.request.user, recipe=kwargs['recipe_id']
        ).delete()
        return Response('Рецепт удален', status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def to_pdf(self, spisok, data):
    pdfmetrics.registerFont(TTFont('Vlashu', 'Vlashu.otf'))
    pdfmetrics.registerFont(TTFont('Gunny', 'Gunny.ttf'))
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    font_size = 6
    p.setFont('Vlashu', font_size * mm)
    x = 15 * mm
    y = 270 * mm
    p.setFillColor(black)
    top = 'Список покупок для рецептов'
    p.drawString(x, y, top)
    y -= font_size * mm + 15
    color = 1
    p.setFont('Gunny', font_size * mm)
    for key in spisok:
        p.drawString(x, y, key.name)
        y -= font_size * mm
        if y < 25 * mm:
            y = 270 * mm
            p.showPage()
            p.setFillColor(black)
            p.setFont('Gunny', font_size * mm)
    y -= 15
    for key in data:
        if color % 2:
            p.setFillColor(grey)
        else:
            p.setFillColor(orange)
        color += 1
        p.drawString(x, y, key)
        x += 380
        p.drawString(x, y, str(data[key]["amount"]))
        x += 60
        p.drawString(x, y, data[key]["measurement_unit"])
        x -= 440
        y -= font_size * mm
        if y < 25 * mm:
            y = 270 * mm
            p.showPage()
            p.setFillColor(black)
            p.setFont('Gunny', font_size * mm)
    p.setTitle('Data')
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(
        buffer, as_attachment=True,
        filename='shopping_cart.pdf'
    )
