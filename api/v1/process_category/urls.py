from django.urls import path, include
from . import views

urlpatterns = [
    path("''/", views.ProcessCategoryListCreateAPI.as_view()),
]
