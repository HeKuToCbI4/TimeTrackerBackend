import datetime

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework.permissions import AllowAny

from frame_consumer.models import ProcessExecutable
from .serializer import (
    ProcessExecutableSerializer,
    ProcessExecutableUpdateSerializer,
    PerProcessUtilizationSerializer,
    PerProcessUtilizationRequestSerializer,
)
from django.db.models import Sum, F, ExpressionWrapper, fields
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from django.utils import timezone


class ProcessExecutableListCreateAPI(ListCreateAPIView):
    queryset = ProcessExecutable.objects.all()
    serializer_class = ProcessExecutableSerializer
    permission_classes = (AllowAny,)


class ProcessExecutableRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = ProcessExecutableUpdateSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return ProcessExecutable.objects.filter(id=self.kwargs.get("pk", None))


class PerProcessUtilizationAPI(ListAPIView):
    serializer_class = PerProcessUtilizationSerializer

    @swagger_auto_schema(query_serializer=PerProcessUtilizationRequestSerializer())
    @action(
        methods=["get"],
        detail="List filtered items based on timestamps from-to",
        url_name="list_filtered",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = ProcessExecutable.objects.all()
        if self.request.method == "GET":
            request_serializer = PerProcessUtilizationRequestSerializer(
                data=self.request.query_params
            )
            request_serializer.is_valid()
            data = request_serializer.data
            utc_from = data.get("from_utc")
            utc_to = data.get("to_utc") or datetime.datetime.now(tz=timezone.utc)
            queryset = queryset.filter(
                processwindow__processwindowsnapshot__utc_from__gte=utc_from,
                processwindow__processwindowsnapshot__utc_to__lte=utc_to,
            )
            # This is to wrap.
            duration_agg = ExpressionWrapper(
                F("processwindow__processwindowsnapshot__utc_to")
                - F("processwindow__processwindowsnapshot__utc_from"),
                output_field=fields.BigIntegerField(),
            )
            queryset = queryset.annotate(duration=Sum(duration_agg)).order_by(
                "-duration"
            )
            return queryset
        else:
            print(self.request.method)
            return queryset
