import threading
import time

import grpc
import re
from frame_consumer.models import ProcessWindow, ProcessExecutable
from proto import FrameInfo_pb2 as frame_info
from proto import FrameInfoService_pb2 as frame_info_service
from proto import FrameInfoService_pb2_grpc as frame_info_service_grpc


class RPCClientServiceException(Exception):
    pass


class RPCClientService:
    def __init__(self, host, port, consumer_id):
        self.host = host
        self.port = port
        self.consumer_id = consumer_id
        self.channel = None
        self.service_stub = None
        self.stop_requested = threading.Event()

    def connect(self):
        # we need to create channel
        if self.channel is None:
            self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")

    def _subscription_thread(self):
        subscribe_request = frame_info_service.StreamSubscribeRequest(self.consumer_id)
        incoming_frame = frame_info.TimeFrameInfo
        # we need to get data, after that process and save it into db.
        while not self.stop_requested:
            try:
                # attempt to connect. Some issues may be raised during connection.
                self.connect()
            except Exception as e:
                print(
                    f"Exception {e} encountered during connection to remote host {self.host}."
                )
                retry_interval = 5
                print(f"Retrying after {retry_interval}")
                time.sleep(retry_interval)
