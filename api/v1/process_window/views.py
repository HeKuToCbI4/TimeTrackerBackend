import datetime

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    CreateAPIView,
)
from rest_framework.permissions import AllowAny

from frame_consumer.models import ProcessWindow
from .serializer import ProcessWindowSerializer
from django.utils import timezone


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

    def get_queryset(self):
        queryset = ProcessWindow.objects.all()
        if self.request.method == "GET":
            if from_utc := self.request.query_params.get("from_time"):
                from_time_obj = datetime.datetime.fromtimestamp(
                    from_utc / 1000, tz=timezone.utc
                )
                queryset.filter(utc_to__gte=from_time_obj)
            if to_utc := self.request.query_params.get("to_time"):
                to_time_obj = datetime.datetime.fromtimestamp(
                    to_utc / 1000, tz=timezone.utc
                )
                queryset.filter(utc_to__lte=to_time_obj)
        return queryset
