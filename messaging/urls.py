from django.urls import path
from . import views

app_name = "messaging"

urlpatterns = [
    path("", views.thread_list, name="thread_list"),
    path("<int:pk>/", views.thread_detail, name="thread_detail"),
    path("new/<int:user_id>/", views.new_thread, name="new_thread"),
]
