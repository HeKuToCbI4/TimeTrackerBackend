from django.urls import path, include

urlpatterns = [
    path("known_host/", include("api.v1.known_host.urls")),
    path("process_category/", include("api.v1.process_category.urls")),
    path("process_executable/", include("api.v1.process_executable.urls")),
    path("process_window/", include("api.v1.process_window.urls")),
    path("subscriber/", include("api.v1.subscriber.urls")),
]
