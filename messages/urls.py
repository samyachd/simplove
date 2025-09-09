from django.urls import path
<<<<<<< HEAD
from . import views

urlpatterns = [path("", views.index, name="messages")]
=======
from .views import messages_view

urlpatterns = [
    path('', messages_view, name='messages'),
]
>>>>>>> users
