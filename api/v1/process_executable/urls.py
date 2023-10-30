from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProcessExecutableListCreateAPI.as_view()),
    path("<int:pk>", views.ProcessExecutableRetrieveUpdateDestroyAPI.as_view()),
]
