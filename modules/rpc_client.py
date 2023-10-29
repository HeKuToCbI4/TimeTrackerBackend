import dataclasses
import os
import threading
import time
from datetime import datetime

import grpc

from frame_consumer.models import ProcessWindow, ProcessExecutable, KnownHost
from proto import FrameInfoService_pb2 as frame_info_service
from proto import FrameInfoService_pb2_grpc as frame_info_service_grpc
from proto import FrameInfo_pb2 as frame_info


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

    def _prepare_subscription_request(
        self, consumer_id: str
    ) -> frame_info_service.StreamSubscribeRequest:
        return frame_info_service.StreamSubscribeRequest(consumer_id=self.consumer_id)

    def _update_remote_host_state(self, is_monitored: bool, status=""):
        # update state to "monitored"
        self.remote_host.is_monitored = is_monitored
        self.remote_host.status = status
        self.remote_host.save()

    def _extract_data_from_frame(self, frame: frame_info.TimeFrameInfo) -> tuple:
        cur_frame_id = frame.id
        process_path = frame.process_executable_path
        current_timestamp = frame.utc_timestamp
        process_window = frame.window_title
        if process_path:
            process_binary = process_path.split(os.sep)[-1]
            print(f"{process_path=} {process_binary=}")
        else:
            print("process path is none!")
            process_binary = None
        return (
            cur_frame_id,
            process_binary,
            process_path,
            process_window,
            current_timestamp,
        )

    def _initialize_data_to_write(
        self, frame: frame_info.TimeFrameInfo
    ) -> ProcessWindowData:
        (
            cur_frame_id,
            process_binary,
            process_path,
            process_window,
            current_timestamp,
        ) = self._extract_data_from_frame(frame)
        return ProcessWindowData(
            last_frame_id=cur_frame_id,
            window_title=process_window,
            utc_from=current_timestamp,
            process_path=process_path,
            process_executable=process_binary,
        )

    def _get_process_executable_object(
        self, process_executable: str, process_path: str
    ) -> ProcessExecutable:
        # Process executable may exist there.
        (
            process_executable_object,
            created,
        ) = ProcessExecutable.objects.get_or_create(
            executable_name=process_executable,
            executable_path=process_path,
        )
        if created:
            print(f"created new process executable entry: {process_executable_object}")
        print(f"{process_executable_object=}")

    def _write_data_to_db(self, process_data: ProcessWindowData, utc_to: int):
        process_executable_object = self._get_process_executable_object(
            process_data.process_executable, process_data.process_path
        )
        # Process window we always create from scratch.
        process_window_object = ProcessWindow.objects.create(
            process_window_title=process_data.window_title,
            executable=process_executable_object,
            utc_from=datetime.utcfromtimestamp(process_data.utc_from / 1000),
            utc_to=datetime.utcfromtimestamp(utc_to / 1000),
        )
        print(f"{process_window_object=}")

    def _process_incoming_frames(self):
        # Receive and write data?
        subscribe_request = self._prepare_subscription_request(self.consumer_id)
        incoming_frame: frame_info.TimeFrameInfo
        process_info: ProcessExecutable
        window_info: ProcessWindow
        data_to_write: ProcessWindowData | None = None
        for incoming_frame in self.service_stub.Subscribe(subscribe_request):
            # probably preprocess extracted data. Apply some filters.
            # TODO: execute self.preprocess data or some DataProcessor.process_data()
            if data_to_write is None:
                print(f"Received first frame for host {self.remote_host}")
                # Construct inital object. Date to is none and will be updated.
                data_to_write = self._initialize_data_to_write(incoming_frame)
                continue
            # Process incoming frame considering previous received.
            if incoming_frame.id != data_to_write.last_frame_id + 1:
                print(
                    f"Sequence error! Prev frame id = {data_to_write.last_frame_id}. Current {incoming_frame.id}."
                )
                data_to_write = None
                continue
            # Now we have process executable, binary, window and timestamp of snapshot + prev frame data.
            # If process binary and window titles match -> update data to write,
            # and continue, else write to db, create new data.
            # If window was not switched.
            if (
                incoming_frame.window_title == data_to_write.window_title
                and not self.stop_requested.is_set()
            ):
                data_to_write.last_frame_id = incoming_frame.id
                continue
            # We're in else section. We need to grab data from DB and write it.
            # Get process object to link against new frame.
            self._write_data_to_db(data_to_write, incoming_frame.utc_timestamp)
            # Update data to write for further actions.
            data_to_write = self._initialize_data_to_write(incoming_frame)

            # Check for exit condition
            if self.stop_requested.is_set():
                self._unsubscribe()
                break

    # TODO: add exception handling.
    def _subscription_thread(self):
        # we need to get data, after that process and save it into db.
        while not self.stop_requested.is_set():
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
            self._update_remote_host_state(True, "Connection established")
            self._process_incoming_frames()

    def start_monitoring(self) -> bool:
        try:
            self.subscription_thread = threading.Thread(
                target=self._subscription_thread,
                name=f"subscription thread client {self.consumer_id}",
                daemon=True,
            )
            print(f"{self} created {self.subscription_thread}")
            self.subscription_thread.start()
            print(f"{self} started {self.subscription_thread}")
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
        unsubscribe_req = frame_info_service.StreamUnsubscribeRequest(
            consumer_id=self.consumer_id
        )
        self.service_stub.Unsubscribe(unsubscribe_req)
        self._update_remote_host_state(
            is_monitored=False, status="Stopped due to unsubscribe request"
        )

    def __str__(self):
        return f"{self.remote_host} consumer {self.consumer_id}"
