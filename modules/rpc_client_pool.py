from typing import Dict

from frame_consumer.models import KnownHost
from .rpc_client import RPCClientService


class RPCClientPool:
    client_rpc_client_map: Dict[KnownHost, RPCClientService] = {}

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(RPCClientPool, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def start_monitoring(self, remote_host: KnownHost, consumer_id: str) -> bool:
        self.client_rpc_client_map[remote_host] = RPCClientService(
            remote_host, consumer_id
        )
        print(f"{self.client_rpc_client_map[remote_host]} created")
        print(self.client_rpc_client_map)
        return self.client_rpc_client_map[remote_host].start_monitoring()

    def stop_monitoring(self, remote_host: KnownHost) -> bool:
        print(self.client_rpc_client_map)
        return self.client_rpc_client_map[remote_host].stop_monitoring()

    def is_monitored(self, remote_host: KnownHost) -> bool:
        print(self.client_rpc_client_map)
        return remote_host in self.client_rpc_client_map
