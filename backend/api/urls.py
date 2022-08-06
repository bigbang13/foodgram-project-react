from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from recipes.views import IngredientViewSet, RecipeViewSet, TagViewSet
from users.views import LoginView, UserAPIList, SubscriptionViewSet, SubscribeViewSet

app_name = "api"

router = DefaultRouter()
# router.register(r'follow', FollowViewSet, basename='follow')
# router.register(
#    'users/(<int:user_id>)/subscribe',
#    SubscribeViewSet,
#    basename='subscribe'
# )
# router.register('subscriptions', SubscriptionViewSet, basename='subscriptions')
# router.register(r'users', UserAPIList, basename='users')

urlpatterns = [
    path("", include(router.urls)),
    path("auth/token/login/", LoginView.as_view()),
    path("users/subscriptions/", SubscriptionViewSet.as_view()),
    path('users/<int:user_id>/subscribe/', SubscribeViewSet.as_view()),
    path("users/", UserAPIList.as_view()),
    path("", include('recipes.urls')),
    path("", include('djoser.urls')),
    re_path(r"^auth/", include('djoser.urls.authtoken')),
]
