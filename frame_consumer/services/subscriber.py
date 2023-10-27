from frame_consumer.models import KnownHost
from django.http import response
from .rpc_client import RPCClientService
from typing import Dict


class SubscriberService:
    def __init__(self):
        self.client_rpc_client_map: Dict[str, RPCClientService] = {}

    def subscribe(self, host, port, consumer_id):
        # This thing should handle thread creation.
        # This thing should also create remote_host host model obj.
        remote_host = KnownHost.objects.filter(host=host, port=port)
        print(remote_host)
        self.client_rpc_client_map[consumer_id] = RPCClientService(
            remote_host, consumer_id
        )
        if self.client_rpc_client_map[consumer_id].start_monitoring():
            return response.JsonResponse({"status_code": 200, "message": "Success!"})
        else:
            # if monitoring failed to start we should return status.
            return response.JsonResponse({"status_code": 500, "message": "Some shit happened!"})
