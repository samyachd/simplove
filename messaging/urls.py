from django.urls import path
<<<<<<< HEAD
from .views import messages_view
=======
from . import views
>>>>>>> origin/messaging

app_name = "messaging"

urlpatterns = [
<<<<<<< HEAD
    path("", messages_view, name="messaging"),
]
=======
    path("", views.thread_list, name="thread_list"),
    path("<int:pk>/", views.thread_detail, name="thread_detail"),
]
>>>>>>> origin/messaging
