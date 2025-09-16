from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("", views.profile_view, name="profile"),
    path("list/", views.profile_list, name="list"),  # Liste des profils
    path("<int:pk>/", views.profile_detail, name="detail"),  # Détail d'un profil
    path("edit/<int:pk>/", views.profile_edit, name="edit"),  # Modifier son profil
    path("create/", views.create_profile, name="create_profile"),  # Créer son profil
]
