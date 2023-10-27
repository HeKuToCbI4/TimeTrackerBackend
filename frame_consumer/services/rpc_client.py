import dataclasses
import os
import threading
import time

import grpc
import re
from frame_consumer.models import ProcessWindow, ProcessExecutable, KnownHost
from proto import FrameInfo_pb2 as frame_info
from proto import FrameInfoService_pb2 as frame_info_service
from proto import FrameInfoService_pb2_grpc as frame_info_service_grpc


class RPCClientServiceException(Exception):
    pass


@dataclasses.dataclass
class ProcessWindowData(object):
    last_frame_id: int
    window_title: str
    utc_from: int
    process_path: str
    process_executable: str


class RPCClientService(object):
    def __init__(self, remote_host: KnownHost, consumer_id):
        self.subscription_thread: threading.Thread | None = None
        self.remote_host = remote_host
        self.consumer_id = consumer_id
        self.channel: grpc.Channel | None = None
        self.service_stub: frame_info_service_grpc.FrameInfoServiceStub | None = None
        self.stop_requested = threading.Event()

    def connect(self):
        # we need to create channel
        if self.channel is None:
            self.channel = grpc.insecure_channel(
                f"{self.remote_host.host}:{self.remote_host.port}"
            )

    def create_stub(self):
        if self.channel is None:
            raise RPCClientServiceException(
                "Client is not connected. Channel is not initialized."
            )
        self.service_stub = frame_info_service_grpc.FrameInfoServiceStub(self.channel)

    # TODO: decompose.
    # TODO: add exception handling.
    def _subscription_thread(self):
        subscribe_request = frame_info_service.StreamSubscribeRequest(self.consumer_id)
        incoming_frame: frame_info.TimeFrameInfo
        # we need to get data, after that process and save it into db.
        while not self.stop_requested:
            try:
                # attempt to connect. Some issues may be raised during connection.
                self.connect()
            except Exception as e:
                print(
                    f"Exception {e} encountered during connection to remote host {self.remote_host}."
                )
                retry_interval = 5
                print(f"Retrying after {retry_interval}")
                time.sleep(retry_interval)
                continue

            self.create_stub()
            # update state to "monitored"
            self.remote_host.is_monitored = True
            self.remote_host.status = "Success"
            self.remote_host.save()
            # Receive and write data?
            process_info: ProcessExecutable
            window_info: ProcessWindow
            data_to_write: ProcessWindowData | None = None
            for incoming_frame in self.service_stub.Subscribe(subscribe_request):
                print(data_to_write)
                # Extract data from frame.
                cur_frame_id = incoming_frame.id
                process_path = incoming_frame.process_executable_path
                current_timestamp = incoming_frame.utc_timestamp
                process_window = incoming_frame.window_title
                if process_path:
                    process_binary = process_path.split(os.sep)[0]
                else:
                    process_binary = None
                # probably preprocess extracted data. Apply some filters.
                # TODO: execute self.preprocess data or some DataProcessor.process_data()
                if data_to_write is None:
                    print(f"Received first frame for host {self.remote_host}")
                    # Construct inital object. Date to is none and will be updated.
                    data_to_write = ProcessWindowData(
                        last_frame_id=cur_frame_id,
                        window_title=process_window,
                        utc_from=current_timestamp,
                        process_path=process_path,
                        process_executable=process_binary,
                    )
                    continue
                # Process incoming frame considering previous received.
                if cur_frame_id != data_to_write.last_frame_id + 1:
                    print(
                        f"Sequnce error! Prev frame id = {data_to_write.last_frame_id}. Current {id=}."
                    )
                    print(f"Clearing data.")
                    data_to_write = None
                    continue
                # Now we have process executable, binary, window and timestamp of snapshot + prev frame data.
                # If process binary and window titles match -> update data to write,
                # and continue, else write to db, create new data.
                # If window was not switched.
                if process_window == data_to_write.window_title:
                    continue
                # We're in else section. We need to grab data from DB and write it.
                # Process executable may exist there.
                process_executable_object = ProcessExecutable.objects.get_or_create(
                    executable_name=data_to_write.process_executable,
                    executable_path=data_to_write.process_path,
                )
                print(f"{process_executable_object=}")
                # Process window we always create from scratch.
                process_window_object = ProcessWindow.objects.create(
                    process_window_title=data_to_write.window_title,
                    executable=process_executable_object,
                    utc_from=data_to_write.utc_from,
                    utc_to=current_timestamp,
                )
                print(f"{process_window_object=}")
                # Update data to write for further actions.
                data_to_write = ProcessWindowData(
                    last_frame_id=cur_frame_id,
                    window_title=process_window,
                    utc_from=current_timestamp,
                    process_path=process_path,
                    process_executable=process_binary,
                )
                if self.stop_requested:
                    self._unsubscribe()
                    break

    def start_monitoring(self) -> bool:
        try:
            self.subscription_thread = threading.Thread(
                target=self._subscription_thread,
                name=f"subscription thread client {self.consumer_id}",
                daemon=True,
            )
            self.subscription_thread.start()
            return True
        except:
            return False

    def stop_monitoring(self) -> bool:
        try:
            print(f"Stop requested for {self.consumer_id}")
            self.stop_requested.set()
            self.subscription_thread.join(timeout=30)
            return True
        except:
            return False

    def _unsubscribe(self):
        unsubscribe_req = frame_info_service.StreamUnsubscribeRequest(self.consumer_id)
        self.service_stub.Unsubscribe(unsubscribe_req)
