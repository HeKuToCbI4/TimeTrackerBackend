from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from frame_consumer.models import ProcessWindow
from .serializer import ProcessWindowSerializer


class ProcessWindowListCreateAPI(ListCreateAPIView):
    queryset = ProcessWindow.objects.all()
    serializer_class = ProcessWindowSerializer
    permission_classes = (AllowAny,)


class ProcessWindowRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = ProcessWindowSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        ProcessWindow.objects.filter(id=self.kwargs.get("pk", None))
