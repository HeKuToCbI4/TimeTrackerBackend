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
from .serializer import ProcessWindowSerializer


class ProcessWindowListCreateAPI(ListCreateAPIView):
    serializer_class = ProcessWindowSerializer
    permission_classes = (AllowAny,)
    queryset = ProcessWindow.objects.all()


class ProcessWindowRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = ProcessWindowSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return ProcessWindow.objects.filter(id=self.kwargs.get("pk", None))
