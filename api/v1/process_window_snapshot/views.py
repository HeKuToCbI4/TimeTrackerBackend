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

from frame_consumer.models import ProcessWindowSnapshot
from .serializer import ProcessWindowSnapshotSerializer, FilterQuerySerializer


class ProcessWindowSnapshotListCreateAPI(ListCreateAPIView):
    serializer_class = ProcessWindowSnapshotSerializer
    permission_classes = (AllowAny,)
    queryset = ProcessWindowSnapshot.objects.all()


class ProcessWindowSnapshotRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = ProcessWindowSnapshotSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return ProcessWindowSnapshot.objects.filter(id=self.kwargs.get("pk", None))


class ProcessWindowSnapshotListFilteredAPI(ListAPIView):
    serializer_class = ProcessWindowSnapshotSerializer
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
        queryset = ProcessWindowSnapshot.objects.all()
        if self.request.method == "GET":
            request_serializer = FilterQuerySerializer(data=self.request.query_params)
            request_serializer.is_valid()
            data = request_serializer.data
            if utc_from := data.get("utc_from_ts"):
                from_time_obj = datetime.datetime.fromtimestamp(
                    int(utc_from) / 1000, tz=timezone.utc
                )
                queryset = queryset.filter(utc_to__gte=from_time_obj)
            if utc_to := data.get("utc_to_ts"):
                to_time_obj = datetime.datetime.fromtimestamp(
                    int(utc_to) / 1000, tz=timezone.utc
                )
                queryset = queryset.filter(utc_to__lte=to_time_obj)
        return queryset
