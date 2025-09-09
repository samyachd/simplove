# matches/urls.py
from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path("", views.my_matches, name="my_matches"),
    path("browse/", views.browse_profiles, name="browse_profiles"),
    path("like/<int:user_id>/", views.like_user, name="like_user"),
    path("pass/<int:user_id>/", views.pass_user, name="pass_user"),
    path("remove-like/<int:user_id>/", views.remove_like, name="remove_like"),
]
