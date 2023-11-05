from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProcessWindowSnapshotListCreateAPI.as_view()),
    path("filter", views.ProcessWindowSnapshotListFilteredAPI.as_view()),
    path("<int:pk>", views.ProcessWindowSnapshotRetrieveUpdateDestroyAPI.as_view()),
]
