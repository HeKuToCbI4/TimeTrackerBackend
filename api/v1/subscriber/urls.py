from django.urls import path, include
from . import views

urlpatterns = [
    path("subscribe", views.SubscriberAPI.as_view(actions={'post': 'subscribe'})),
    path("unsubscribe", views.SubscriberAPI.as_view(actions={'post': 'unsubscribe'})),
]
