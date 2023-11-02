from typing import Dict

from frame_consumer.models import KnownHost
from .rpc_client import RPCClientService


class RPCClientPool(object):
    client_rpc_client_map: Dict[KnownHost, RPCClientService] = {}

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(RPCClientPool, cls).__new__(cls, *args, **kwargs)
            cls.instance._do_restore()
        return cls.instance

    def start_monitoring(self, remote_host: KnownHost) -> bool:
        self.client_rpc_client_map[remote_host] = RPCClientService(remote_host)
        print(f"{self.client_rpc_client_map[remote_host]} created")
        print(self.client_rpc_client_map)
        return self.client_rpc_client_map[remote_host].start_monitoring()

    def stop_monitoring(self, remote_host: KnownHost) -> bool:
        return self.client_rpc_client_map[remote_host].stop_monitoring()

    def is_monitored(self, remote_host: KnownHost) -> bool:
        return remote_host in self.client_rpc_client_map

    def _do_restore(self):
        hosts = KnownHost.objects.filter(auto_start_monitor__exact=True)
        for auto_started_host in hosts:
            self.start_monitoring(auto_started_host)
