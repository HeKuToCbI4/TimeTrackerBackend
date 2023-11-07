from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from frame_consumer.models import ProcessCategoryMapping
from .serializer import ProcessCategoryMappingSerializer


class ProcessCategoryListCreateAPI(ListCreateAPIView):
    queryset = ProcessCategoryMapping.objects.all()
    serializer_class = ProcessCategoryMappingSerializer
    permission_classes = (AllowAny,)


class ProcessCategoryRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = ProcessCategoryMappingSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return ProcessCategoryMapping.objects.filter(id=self.kwargs.get("pk", None))
