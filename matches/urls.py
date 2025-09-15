# matches/urls.py
from django.urls import path
from . import views

app_name = "matches"

urlpatterns = [
    path("", views.my_matches, name="my_matches"),
    path("browse/", views.browse_profiles, name="browse_profiles"),
    path("like/<int:user_id>/", views.like_user, name="like"),
    path("pass/<int:user_id>/", views.pass_user, name="pass"),
    path("remove-like/<int:user_id>/", views.remove_like, name="remove_like"),
]
