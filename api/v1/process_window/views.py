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

from frame_consumer.models import ProcessWindow, ProcessWindowSnapshot
from .serializer import (
    ProcessWindowSerializer,
    PerProcessWindowUtilizationRequestSerializer,
    PerProcessWindowUtilizationSerializer,
)
from django.db.models import Sum, F, ExpressionWrapper, fields, Q



class ProcessWindowListCreateAPI(ListCreateAPIView):
    serializer_class = ProcessWindowSerializer
    permission_classes = (AllowAny,)
    queryset = ProcessWindow.objects.all()


class ProcessWindowRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = ProcessWindowSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return ProcessWindow.objects.filter(id=self.kwargs.get("pk", None))


class PerProcessWindowUtilizationAPI(ListAPIView):
    serializer_class = PerProcessWindowUtilizationSerializer

    @swagger_auto_schema(
        query_serializer=PerProcessWindowUtilizationRequestSerializer()
    )
    @action(
        methods=["get"],
        detail="List filtered items based on timestamps from-to",
        url_name="list_filtered",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = ProcessWindow.objects.all()
        if self.request.method == "GET":
            request_serializer = PerProcessWindowUtilizationRequestSerializer(
                data=self.request.query_params
            )
            request_serializer.is_valid()
            data = request_serializer.data
            utc_from = data.get("from_utc")
            utc_to = data.get("to_utc") or datetime.datetime.now(tz=timezone.utc)
            host = data.get("host")
            filters = None
            if utc_from is not None:
                filters = Q(
                    processwindowsnapshot__utc_from__gte=utc_from
                )
            if utc_to is not None:
                filters &= Q(processwindowsnapshot__utc_to__lte=utc_to)
            if host is not None:
                filters &= Q(executable__host__address__exact=host)
            queryset = queryset.filter(filters)
            # This is to wrap.
            duration_agg = ExpressionWrapper(
                F("processwindowsnapshot__utc_to")
                - F("processwindowsnapshot__utc_from"),
                output_field=fields.DurationField(),
            )
            queryset = queryset.annotate(duration=Sum(duration_agg)).order_by(
                "-duration"
            )
            return queryset
        raise Exception("You should not be there!")
