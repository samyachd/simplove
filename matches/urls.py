from django.urls import path
from . import views
from django.http import HttpResponse

app_name = "matches"

urlpatterns = [
    path(
        "like/<int:pk>/", lambda request, pk: HttpResponse("Temporaire"), name="like"
    ),  # TODO Chemin URL à corriger une fois matches prêt
]
