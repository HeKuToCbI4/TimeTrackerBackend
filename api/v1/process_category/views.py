from rest_framework.generics import ListCreateAPIView
from frame_consumer.models import ProcessCategory
from .serializer import ProcessCategorySerializer
from rest_framework.permissions import AllowAny


class ProcessCategoryListCreateAPI(ListCreateAPIView):
    queryset = ProcessCategory.objects.all()
    serializer_class = ProcessCategorySerializer
    permission_classes = (AllowAny,)
