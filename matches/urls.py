from django.urls import path
from .views import matches_view

urlpatterns = [
    path('', matches_view, name='matches'),
]