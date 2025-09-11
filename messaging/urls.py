from django.urls import path
from .views import messages_view

app_name = "messaging"

urlpatterns = [
    path("", messages_view, name="messaging"),
]
