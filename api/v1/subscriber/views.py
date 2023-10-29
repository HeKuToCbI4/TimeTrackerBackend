from rest_framework.request import Request
from rest_framework.viewsets import ViewSet

from frame_consumer.services.subscriber import SubscriberService
from .serializer import SubscriptionSerializer, UnsubscriptionSerializer
from rest_framework.permissions import AllowAny


class SubscriberAPI(ViewSet):
    permission_classes = (AllowAny,)

    def subscribe(self, request: Request):
        serializer = SubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        service = SubscriberService()
        service.subscribe(data["host"], data["port"], data["consumer_id"])

    def unsubscribe(self, request: Request):
        serializer = UnsubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        service = SubscriberService()
        service.unsubscribe(data["host"], data["port"], data["consumer_id"])
