from django.urls import include, path
from .views import (RegisterView, UserMeView, UserIDView, LoginView, LogoutView, PasswordChangeView)

app_name = "users"


urlpatterns = [
    path("", RegisterView.as_view()),
    path("<int:user_id>/", UserIDView.as_view()),
    path("me/", UserMeView.as_view()),
    path("set_password/", PasswordChangeView.as_view()),
    path(
        "auth/token/login/",
        LoginView.as_view()
    ),
    path(
        "auth/token/logout/",
        LogoutView.as_view(),
    ),
]
