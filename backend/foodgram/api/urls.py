from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (RecipeViewSet, IngredientViewSet, CustomTokenObtainView,
                    TagViewSet, SignUpAPIView,
                    UserViewSet)

app_name = "api"

router = DefaultRouter()

router.register("recipes", RecipeViewSet)
router.register("tags", TagViewSet)
router.register("ingredients", IngredientViewSet)
# router.register(
#    r"recipes/(?P<recipe_id>\d+)/asdsad", ReviewViewSet, basename="reviews"
# )
# router.register(
#    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
#    CommentViewSet,
#    basename="comments",
# )
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/signup/", SignUpAPIView.as_view()),
    path(
        "auth/token/login/",
        CustomTokenObtainView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "auth/token/logout/",
        CustomTokenObtainView.as_view(),
        name="token_obtain_pair",
    ),
]
