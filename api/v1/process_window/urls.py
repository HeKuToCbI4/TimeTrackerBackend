from django.urls import path, include
from . import views

urlpatterns = [
    path("''/", views.ProcessWindowListCreateAPI.as_view()),
]
