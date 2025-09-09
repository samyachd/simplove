from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
]
from .views import core_view

urlpatterns = [
    path('' , core_view, name='core'),
]
