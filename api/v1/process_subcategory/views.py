from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from frame_consumer.models import ProcessSubCategory
from .serializer import ProcessSubCategorySerializer


class ProcessSubCategoryListCreateAPI(ListCreateAPIView):
    queryset = ProcessSubCategory.objects.all()
    serializer_class = ProcessSubCategorySerializer
    permission_classes = (AllowAny,)


class ProcessSubCategoryRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = ProcessSubCategorySerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return ProcessSubCategory.objects.filter(id=self.kwargs.get("pk", None))
