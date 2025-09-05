from django.urls import path
from .views import core_view

urlpatterns = [
    path('' , core_view, name='core'),
]