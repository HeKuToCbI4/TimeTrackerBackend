from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet

from frame_consumer.services.subscriber import SubscriberService
from .serializer import SubscriptionSerializer
from drf_yasg.utils import swagger_auto_schema


class SubscriberAPI(ViewSet):
    permission_classes = (AllowAny,)

    @action(methods=["post"], detail="Subscribe for frame updates of the host")
    @swagger_auto_schema(request_body=SubscriptionSerializer)
    def subscribe(self, request: Request):
        serializer = SubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        service = SubscriberService()
        return service.subscribe(data["host"], data["port"], data["consumer_id"])

    @action(methods=["post"], detail="Unubscribe for frame updates of the host")
    @swagger_auto_schema(request_body=SubscriptionSerializer)
    def unsubscribe(self, request: Request):
        serializer = SubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        service = SubscriberService()
        return service.unsubscribe(data["host"], data["port"], data["consumer_id"])
