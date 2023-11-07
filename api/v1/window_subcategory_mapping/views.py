from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from frame_consumer.models import WindowSubCategoryMapping
from .serializer import WindowSubCategoryMappingSerializer


class ProcessCategoryListCreateAPI(ListCreateAPIView):
    queryset = WindowSubCategoryMapping.objects.all()
    serializer_class = WindowSubCategoryMappingSerializer
    permission_classes = (AllowAny,)


class ProcessCategoryRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = WindowSubCategoryMappingSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return WindowSubCategoryMapping.objects.filter(id=self.kwargs.get("pk", None))
