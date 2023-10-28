from rest_framework.generics import ListCreateAPIView
from frame_consumer.models import KnownHost
from .serializer import KnownHostSerializer
from rest_framework.permissions import AllowAny


class KnownHostsListCreateAPI(ListCreateAPIView):
    queryset = KnownHost.objects.all()
    serializer_class = KnownHostSerializer
    permission_classes = (AllowAny,)
