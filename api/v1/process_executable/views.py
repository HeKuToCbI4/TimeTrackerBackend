from rest_framework.generics import ListCreateAPIView
from frame_consumer.models import ProcessExecutable
from .serializer import ProcessExecutableSerializer
from rest_framework.permissions import AllowAny



class ProcessExecutableListCreateAPI(ListCreateAPIView):
    queryset = ProcessExecutable.objects.all()
    serializer_class = ProcessExecutableSerializer
    permission_classes = (AllowAny,)
