from django.urls import path, include
from .views import account_view, register_view, post_register_profile

app_name = "users"

urlpatterns = [
    path("account", account_view, name="account"),
    path("register/", register_view, name="register"),
    path("", include("django.contrib.auth.urls")),
    path("register/profile", post_register_profile, name="register_profile")
]
