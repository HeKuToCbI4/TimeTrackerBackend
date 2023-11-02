from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet

from frame_consumer.services.subscriber import SubscriberService
from .serializer import SubscriptionSerializer, UnsubscriptionSerializer


class SubscriberAPI(ViewSet):
    permission_classes = (AllowAny,)

    def __init__(self, **kwargs):
        self.service = SubscriberService()
        super().__init__(**kwargs)

    @action(methods=["post"], detail="Subscribe for frame updates of the remote_host")
    @swagger_auto_schema(request_body=SubscriptionSerializer)
    def subscribe(self, request: Request):
        serializer = SubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return self.service.subscribe(
            data.get("address"),
            data.get("port"),
            data.get("consumer_id"),
            data.get("auto_monitor", None),
        )

    @action(methods=["post"], detail="Unubscribe for frame updates of the remote_host")
    @swagger_auto_schema(request_body=UnsubscriptionSerializer)
    def unsubscribe(self, request: Request):
        serializer = UnsubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return self.service.unsubscribe(data.get("address"), data.get("port"))

    @action(methods=["get"], detail="get status of all hosts")
    @swagger_auto_schema()
    def status(self, request: Request):
        response_data = {
            "rpc_pool": {
                str(k): str(v)
                for k, v in self.service.rpc_pool.client_rpc_client_map.items()
            },
            "status": "success",
        }
        return JsonResponse(data=response_data, status=200)
