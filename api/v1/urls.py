from django.urls import path, include

urlpatterns = [
    path("known_hosts/", include("api.v1.known_hosts.urls")),
    path("process_category/", include("api.v1.process_category.urls")),
    path("process_executable/", include("api.v1.process_executable.urls")),
    path("process_window/", include("api.v1.process_window.urls")),
]
