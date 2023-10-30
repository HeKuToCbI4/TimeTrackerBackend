from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from frame_consumer.models import ProcessCategory
from .serializer import ProcessCategorySerializer


class ProcessCategoryListCreateAPI(ListCreateAPIView):
    queryset = ProcessCategory.objects.all()
    serializer_class = ProcessCategorySerializer
    permission_classes = (AllowAny,)


class ProcessCategoryRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = ProcessCategorySerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return ProcessCategory.objects.filter(id=self.kwargs.get("pk", None))
