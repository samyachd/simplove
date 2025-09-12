from django.urls import path, include
from .views import (
    account_view,
    logout_view,
    register_view,
    manage_account,
    welcome_back,
)

app_name = "users"

urlpatterns = [
    path("account", account_view, name="account"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("", include("django.contrib.auth.urls")),
    path("manage/", manage_account, name="manage_account"),
    path("welcome-back/", welcome_back, name="welcome_back"),
]
