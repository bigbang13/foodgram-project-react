from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from users.views import LoginView, PasswordChangeView, UserAPIList
app_name = "api"

router = DefaultRouter()

# router.register("recipes", RecipeViewSet)
# router.register("tags", TagViewSet)
# router.register("ingredients", IngredientViewSet)
# router.register(
#    r"recipes/(?P<recipe_id>\d+)/asdsad", ReviewViewSet, basename="reviews"
# )
# router.register(
#    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
#    CommentViewSet,
#    basename="comments",
# )
# router.register("users", UserViewSet, basename="users")


urlpatterns = [
    path("auth/token/login/", LoginView.as_view()),
    path("users/", UserAPIList.as_view()),
    path("", include(router.urls)),
    path("", include('djoser.urls')),
    re_path(r"^auth/", include('djoser.urls.authtoken')),
]
