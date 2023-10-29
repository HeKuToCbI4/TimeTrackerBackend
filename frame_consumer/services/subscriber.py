from django.http import response

from frame_consumer.models import KnownHost
from modules.rpc_client_pool import RPCClientPool


class SubscriberService:
    # TODO: REWRITE LOGIC BEHIND CONSUMER ID. MAP SHOULD USE HOST-PORT REPRESENTATION! NOT THIS SHIT!
    def __init__(self):
        self.rpc_pool = RPCClientPool()

    def subscribe(self, host, port, consumer_id) -> response.JsonResponse:
        print(self.rpc_pool)
        # This thing should handle thread creation.
        # This thing should also create remote_host remote_host model obj.
        remote_host, created = KnownHost.objects.get_or_create(host=host, port=port)
        if created:
            print(f"Created a new remote_host instance {remote_host}")
        if remote_host.is_monitored and self.rpc_pool.is_monitored(remote_host):
            return response.JsonResponse(
                {"status_code": 403, "message": "Host is already monitored"}
            )
        print(f"Creating RPCClient service for {consumer_id} {remote_host}")
        if self.rpc_pool.start_monitoring(
            remote_host, consumer_id
        ):
            return response.JsonResponse({"status_code": 200, "message": "Success!"})
        else:
            # if monitoring failed to start we should return status.
            return response.JsonResponse(
                {"status_code": 500, "message": "Some shit happened!"}
            )

    def unsubscribe(self, host, port, consumer_id) -> response.JsonResponse:
        print(self.rpc_pool)
        # This thing should handle thread stopping.
        # This thing should also create remote_host remote_host model obj.
        print(host, port, consumer_id)
        if not KnownHost.objects.filter(host=host, port=port):
            return response.JsonResponse(
                {"status_code": 502, "message": "Host does not exist bruh!"}
            )
        remote_host = KnownHost.objects.get(host=host, port=port)
        # TODO: IT SHOULD CHECK FOR HOST!
        if not self.rpc_pool.is_monitored(remote_host):
            return response.JsonResponse(
                {"status_code": 502, "message": "Unknown remote_host bruh!"}
            )
        if self.rpc_pool.stop_monitoring(remote_host):
            return response.JsonResponse({"status_code": 200, "message": "Success!"})
        else:
            # if monitoring failed to start we should return status.
            return response.JsonResponse(
                {"status_code": 500, "message": "Some shit happened!"}
            )
