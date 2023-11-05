from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProcessWindowListCreateAPI.as_view()),
    path("<int:pk>", views.ProcessWindowRetrieveUpdateDestroyAPI.as_view()),
]
