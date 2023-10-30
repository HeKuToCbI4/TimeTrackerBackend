from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from frame_consumer.models import KnownHost
from .serializer import KnownHostSerializer


class KnownHostsListCreateAPI(ListCreateAPIView):
    queryset = KnownHost.objects.all()
    serializer_class = KnownHostSerializer
    permission_classes = (AllowAny,)


class KnownHostRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = KnownHostSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return KnownHost.objects.filter(id=self.kwargs.get("pk", None))
