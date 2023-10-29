from frame_consumer.models import KnownHost
from django.http import response
from modules.rpc_client import RPCClientService
from typing import Dict


class SubscriberService:
    # TODO: REWRITE LOGIC BEHIND CONSUMER ID. MAP SHOULD USE HOST-PORT REPRESENTATION! NOT THIS SHIT!
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = cls.__new__(SubscriberService, args, kwargs)
        return cls.instance

    def __init__(self):
        self.client_rpc_client_map: Dict[str, RPCClientService] = {}

    def subscribe(self, host, port, consumer_id):
        # This thing should handle thread creation.
        # This thing should also create remote_host host model obj.
        remote_host, created = KnownHost.objects.get_or_create(host=host, port=port)
        if created:
            print(f"Created a new host instance {remote_host}")
        if remote_host.is_monitored:
            return response.JsonResponse(
                {"status_code": 403, "message": "Host is already monitored"}
            )
        self.client_rpc_client_map[consumer_id] = RPCClientService(
            remote_host, consumer_id
        )
        if self.client_rpc_client_map[consumer_id].start_monitoring():
            return response.JsonResponse({"status_code": 200, "message": "Success!"})
        else:
            # if monitoring failed to start we should return status.
            return response.JsonResponse(
                {"status_code": 500, "message": "Some shit happened!"}
            )

    def unsubscribe(self, host, port, consumer_id):
        # This thing should handle thread stopping.
        # This thing should also create remote_host host model obj.
        if not KnownHost.objects.filter(host=host, port=port):
            return response.JsonResponse(
                {"status_code": 502, "message": "Host does not exist bruh!"}
            )
        remote_host = KnownHost.objects.get(host=host, port=port)
        # TODO: IT SHOULD CHECK FOR HOST!
        if consumer_id not in self.client_rpc_client_map:
            return response.JsonResponse(
                {"status_code": 502, "message": "Unknown host bruh!"}
            )
        if self.client_rpc_client_map[consumer_id].stop_monitoring():
            return response.JsonResponse({"status_code": 200, "message": "Success!"})
        else:
            # if monitoring failed to start we should return status.
            return response.JsonResponse(
                {"status_code": 500, "message": "Some shit happened!"}
            )
