import dataclasses
import os
import threading
import time
from datetime import datetime

import grpc
from django.utils import timezone

from frame_consumer.models import (
    ProcessWindow,
    ProcessExecutable,
    KnownHost,
    ProcessWindowSnapshot,
)
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
    utc_to: int | None
    process_path: str
    process_executable: str


class RPCClientService(object):
    def __init__(self, remote_host: KnownHost):
        self.subscription_thread: threading.Thread | None = None
        self.remote_host = remote_host
        self.channel: grpc.Channel | None = None
        self.service_stub: frame_info_service_grpc.FrameInfoServiceStub | None = None
        self.stop_requested = threading.Event()

    def connect(self):
        # we need to create channel
        if self.channel is None:
            self.channel = grpc.insecure_channel(
                f"{self.remote_host.address}:{self.remote_host.port}"
            )

    def create_stub(self):
        if self.channel is None:
            raise RPCClientServiceException(
                "Client is not connected. Channel is not initialized."
            )
        self.service_stub = frame_info_service_grpc.FrameInfoServiceStub(self.channel)

    def _prepare_subscription_request(
        self,
    ) -> frame_info_service.StreamSubscribeRequest:
        return frame_info_service.StreamSubscribeRequest(
            consumer_id=self.remote_host.consumer_id
        )

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
            utc_to=None,
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
            host=self.remote_host,
        )
        if created:
            print(f"created new process executable entry: {process_executable_object}")
        return process_executable_object

    def _write_data_to_db(self, process_data: ProcessWindowData):
        process_executable_object = self._get_process_executable_object(
            process_data.process_executable, process_data.process_path
        )
        # Try to find process window object
        process_window_object, created = ProcessWindow.objects.get_or_create(
            process_window_title=process_data.window_title,
            executable=process_executable_object,
        )
        if created:
            print(f"Created new {str(process_window_object).encode()}")
        # Store snapshot data.
        (
            process_window_snapshot_object,
            created,
        ) = ProcessWindowSnapshot.objects.get_or_create(
            defaults={"utc_to": datetime(1970, 1, 1, tzinfo=timezone.utc)},
            utc_from=datetime.fromtimestamp(
                process_data.utc_from / 1000, tz=timezone.utc
            ),
            process_window=process_window_object,
        )
        if created:
            # This is weird. but it's fixing encoding if we want to get rid of some exceptions :D
            print(f"Created snapshot object {str(process_window_snapshot_object).encode()}")

        process_window_snapshot_object.utc_to = datetime.fromtimestamp(
            process_data.utc_to / 1000, tz=timezone.utc
        )
        process_window_snapshot_object.save()
        print(f"Updated {str(process_window_snapshot_object).encode()}")

    def _process_incoming_frames(self):
        # Receive and write data?
        subscribe_request = self._prepare_subscription_request()
        incoming_frame: frame_info.TimeFrameInfo
        process_info: ProcessExecutable
        window_info: ProcessWindow
        data_to_write: ProcessWindowData | None = None
        self._update_remote_host_state(is_monitored=True, status="Receiving frames")
        try:
            for incoming_frame in self.service_stub.Subscribe(subscribe_request):
                print(incoming_frame.SerializeToString())
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
                # If process binary and window titles match -> update data adn write,
                data_to_write.last_frame_id = incoming_frame.id
                # We're in else section. We need to grab data from DB and write it.
                # Get process object to link against new frame.
                data_to_write.utc_to = incoming_frame.utc_timestamp
                self._write_data_to_db(data_to_write)
                # Update data to write for further actions in case window switched.
                if (
                    incoming_frame.window_title != data_to_write.window_title
                    and not self.stop_requested.is_set()
                ):
                    data_to_write = self._initialize_data_to_write(incoming_frame)
                # Check for exit condition
                if self.stop_requested.is_set():
                    self._unsubscribe()
                    break
        except Exception as e:
            self._update_remote_host_state(
                is_monitored=False, status=f"Not active due to {e}"
            )
            print(
                f"Exception during processing frames for {self.remote_host.address}:{self.remote_host.port}, {e}"
            )
            raise

    # TODO: add exception handling.
    def _subscription_thread(self):
        RETRY_INTERVAL = 5
        # we need to get data, after that process and save it into db.
        while not self.stop_requested.is_set():
            try:
                # attempt to connect. Some issues may be raised during connection.
                self.connect()
            except Exception as e:
                print(
                    f"Exception {e} encountered during connection to remote host {self.remote_host}."
                )
                print(f"Retrying after {RETRY_INTERVAL}")
                time.sleep(RETRY_INTERVAL)
                continue

            self.create_stub()
            # update state to "monitored"
            self._update_remote_host_state(True, "Connection established")
            try:
                self._process_incoming_frames()
            except Exception as e:
                print(
                    f"Handling exception for {self.remote_host}, retrying after {RETRY_INTERVAL}"
                )
                time.sleep(RETRY_INTERVAL)

    def start_monitoring(self) -> bool:
        try:
            self.subscription_thread = threading.Thread(
                target=self._subscription_thread,
                name=f"subscription thread client {self.remote_host.address}|{self.remote_host.port}",
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
            print(f"Stop requested for {self.remote_host}")
            self.stop_requested.set()
            self.subscription_thread.join(timeout=30)
            return True
        except:
            return False

    def _unsubscribe(self):
        unsubscribe_req = frame_info_service.StreamUnsubscribeRequest(
            consumer_id=self.remote_host.consumer_id
        )
        self.service_stub.Unsubscribe(unsubscribe_req)
        self._update_remote_host_state(
            is_monitored=False, status="Stopped due to unsubscribe request"
        )

    def __str__(self):
        return (
            f"{self.remote_host.address}:{self.remote_host.port} RPC consumer with "
            f"client_id {self.remote_host.consumer_id}"
        )
