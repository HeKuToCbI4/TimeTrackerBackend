from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProcessSubCategoryListCreateAPI.as_view()),
    path("<int:pk>", views.ProcessSubCategoryRetrieveUpdateDestroyAPI.as_view()),
]
