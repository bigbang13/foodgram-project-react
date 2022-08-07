from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from users.views import (LoginView, SubscribeViewSet, SubscriptionViewSet,
                         UserAPIList)

app_name = "api"

router = DefaultRouter()

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
