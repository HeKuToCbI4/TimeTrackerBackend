from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProcessCategoryListCreateAPI.as_view()),
    path("<int:pk>", views.ProcessCategoryRetrieveUpdateDestroyAPI.as_view()),
]
