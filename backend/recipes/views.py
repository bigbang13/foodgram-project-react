import io

import reportlab
from api.permissions import IsAdminOrReadOnly, IsAuthorOrStaff
from django.conf import settings
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.lib.colors import black
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
# from reportlab.platypus import SimpleDocTemplate
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientSearchFilter, RecipeFilter
from .models import FavoriteRecipes, Ingredient, Recipe, ShoppingCart, Tag
from .paginations import RecipePagination
from .serializers import (FavoriteRecipesSerializer, IngredientSerializer,
                          RecipePostSerializer, RecipeSerializer,
                          ShoppingCartSerializer, TagSerializer)
from .utils import create_delete

reportlab.rl_config.TTFSearchPath.append(
    str(settings.BASE_DIR) + '/reportlab/fonts'
)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientSearchFilter, )
    search_fields = ('^name', )


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrStaff)
    pagination_class = RecipePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    @action(
        methods=['post', 'delete'],
        url_path='(?P<recipe_id>[0-9]+)/shopping_cart',
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
        methods=['post', 'delete'],
        url_path='(?P<recipe_id>[0-9]+)/favorite',
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
        methods=['get'],
        url_path='download_shopping_cart',
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
#        data_list = []
#        for index, key in enumerate(data, start=1):
#            data_list.append(
#                f'{index}. {key} - {data[key]["amount"]} '
#                f'{data[key]["measurement_unit"]}\n')
        pdfmetrics.registerFont(TTFont('Vlashu', 'Vlashu.otf'))
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        font_size = 6
        p.setFont('Vlashu', font_size * mm)
        x = 15 * mm
        y = 25 * mm
        p.setFillColor(black)
        for key in data:
            p.drawString(x, y, key)
            x += 320
            p.drawString(x, y, str(data[key]["amount"]))
            x += 60
            p.drawString(x, y, data[key]["measurement_unit"])
            x -= 380
            y += font_size * mm
            if y > 280 * mm:
                y = 25 * mm
                p.showPage()
                p.setFillColor(black)
                p.setFont('Vlashu', font_size * mm)
        p.setTitle('Data')
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(
            buffer, as_attachment=True,
            filename='shopping_cart.pdf'
        )

#        p.drawString(10, 10, "Список покупок.")
#        p.showPage()
#        p.save()
#        buffer.seek(0)
#        return FileResponse(
#            buffer, as_attachment=True,
#            filename='shopping_cart.pdf'
#        )

#        out_data = HttpResponse(data_list, content_type='application/pdf')
#        out_data['Content-Disposition'] = (
#            'attachment; filename="shopping_cart.pdf"'
#        )
#        p = canvas.Canvas(out_data)
#        p.setFont("Times-Roman", 14)
#        p.showPage()
#        p.save()
#        return out_data

#       out_data = HttpResponse(data_list, content_type='text/plain')
#       out_data = HttpResponse(data_list, 'Content-Type: application/pdf')
#       out_data['Content-Disposition'] = (
#           'attachment; filename="shopping_cart"'
#       )
