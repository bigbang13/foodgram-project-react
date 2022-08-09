from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin

from .models import Ingredient, Recipe, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "author",
    )
    list_filter = ['name', 'author', 'tags', ]
    readonly_fields = ('count_favorite',)

    def count_favorite(self, obj):
        return obj.favorite.count()


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "color",
        "slug",
    )


class IngredientResource(resources.ModelResource):

    class Meta:
        model = Ingredient


class IngredientAdmin(ImportExportActionModelAdmin):
    resource_class = IngredientResource
    list_display = (
        "id",
        "name",
        "measurement_unit",
    )
    list_filter = ['name', ]


# class IngredientAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "name",
#         "measurement_unit",
#     )
#     list_filter = ['name', ]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
