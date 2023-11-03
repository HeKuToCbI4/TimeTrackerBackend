import datetime

from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework.permissions import AllowAny

from frame_consumer.models import ProcessWindow
from .serializer import ProcessWindowSerializer, FilterQuerySerializer


class ProcessWindowListCreateAPI(ListCreateAPIView):
    serializer_class = ProcessWindowSerializer
    permission_classes = (AllowAny,)
    queryset = ProcessWindow.objects.all()


class ProcessWindowRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = ProcessWindowSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return ProcessWindow.objects.filter(id=self.kwargs.get("pk", None))


class ProcessWindowListFilteredAPI(ListAPIView):
    serializer_class = ProcessWindowSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(query_serializer=FilterQuerySerializer())
    @action(
        methods=["get"],
        detail="List filtered items based on timestamps from-to",
        url_path="/filter",
        url_name="list_filtered",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = ProcessWindow.objects.all()
        if self.request.method == "GET":
            print(self.request.query_params)
            if utc_from := self.request.query_params.get("utc_from"):
                from_time_obj = datetime.datetime.fromtimestamp(
                    int(utc_from) / 1000, tz=timezone.utc
                )
                print(f"{from_time_obj=}")
                queryset = queryset.filter(utc_to__gte=from_time_obj)
            if utc_to := self.request.query_params.get("utc_to"):
                to_time_obj = datetime.datetime.fromtimestamp(
                    int(utc_to[0]) / 1000, tz=timezone.utc
                )
                print(to_time_obj)
                queryset = queryset.filter(utc_to__lte=to_time_obj)
        return queryset
