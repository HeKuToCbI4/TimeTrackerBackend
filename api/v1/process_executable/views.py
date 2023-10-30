from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from frame_consumer.models import ProcessExecutable
from .serializer import ProcessExecutableSerializer


class ProcessExecutableListCreateAPI(ListCreateAPIView):
    queryset = ProcessExecutable.objects.all()
    serializer_class = ProcessExecutableSerializer
    permission_classes = (AllowAny,)


class ProcessExecutableRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = ProcessExecutableSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return ProcessExecutable.objects.filter(id=self.kwargs.get("pk", None))
