from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from frame_consumer.models import KnownHost
from .serializer import KnownHostListCreateSerializer, KnownHostUpdateDeleteSerializer


class KnownHostsListCreateAPI(ListCreateAPIView):
    queryset = KnownHost.objects.all()
    serializer_class = KnownHostListCreateSerializer
    permission_classes = (AllowAny,)


class KnownHostRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = KnownHostUpdateDeleteSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return KnownHost.objects.filter(id=self.kwargs.get("pk", None))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(
            {
                "success:": True,
                "message": "address data successfully updated",
                "data": serializer.data,
            }
        )
