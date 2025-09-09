from django.urls import path, include
from .views import account_view, logout_view, register_view

app_name = "users"

urlpatterns = [
    path("account", account_view, name="users"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("", include("django.contrib.auth.urls")),
]
