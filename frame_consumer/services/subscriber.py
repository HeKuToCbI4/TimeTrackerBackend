from frame_consumer.models import KnownHost
from django.http import response


class SubscriberService:
    def __init__(self):
        pass

    def subscribe(self, remote_host: KnownHost):
        # This thing should handle thread creation.
        host = remote_host.host
        port = remote_host.port
        # TODO: add logic that will do actual monitoring there :)
        # It should start separate thread.
        if True:
            # Here if monitoring was successfully started we do some things.
            pass
        else:
            # if monitoring failed to start we should return status.
            return response.HttpResponseServerError()
