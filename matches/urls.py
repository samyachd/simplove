from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path("like/<int:user_id>/", views.like_user, name="like_user"),
    path("unlike/<int:user_id>/", views.unlike_user, name="unlike_user"),
    path("", views.my_matches, name="my_matches"),
]
