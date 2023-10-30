from django.urls import path

from . import views

urlpatterns = [
    path("", views.KnownHostsListCreateAPI.as_view()),
    path("<int:pk>", views.KnownHostRetrieveUpdateDestroyAPI.as_view()),
]
