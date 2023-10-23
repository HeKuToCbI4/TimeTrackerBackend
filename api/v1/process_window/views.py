from rest_framework.generics import ListCreateAPIView
from frame_consumer.models import ProcessWindow
from .serializer import ProcessWindowSerializer
from rest_framework.permissions import AllowAny


class ProcessCategoryListCreateAPI(ListCreateAPIView):
    queryset = ProcessWindow.objects.all()
    serializer_class = ProcessWindowSerializer
    permission_classes = (AllowAny,)
