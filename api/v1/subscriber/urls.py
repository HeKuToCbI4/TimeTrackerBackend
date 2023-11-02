from django.urls import path

from . import views

urlpatterns = [
    path("subscribe", views.SubscriberAPI.as_view(actions={"post": "subscribe"})),
    path("unsubscribe", views.SubscriberAPI.as_view(actions={"post": "unsubscribe"})),
    path("", views.SubscriberAPI.as_view(actions={"get": "status"})),
]
