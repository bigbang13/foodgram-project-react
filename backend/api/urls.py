from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import SubscribeViewSet
from recipes.views import TagViewSet, IngredientViewSet, RecipeViewSet

app_name = "api"

router = DefaultRouter()

router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)
router.register('users', SubscribeViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
