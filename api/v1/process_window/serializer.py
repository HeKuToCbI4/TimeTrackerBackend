import datetime

from rest_framework import serializers
from django.utils import timezone
from frame_consumer.models import (
    ProcessWindow,
)


class ProcessWindowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessWindow
        fields = "__all__"


class ProcessWindowUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessWindow
        fields = ["process_subcategory"]


class PerProcessWindowUtilizationRequestSerializer(serializers.Serializer):
    from_utc = serializers.DateTimeField(
        default_timezone=timezone.utc,
        required=False,
        default=datetime.datetime(1970, 1, 1, tzinfo=timezone.utc),
    )
    to_utc = serializers.DateTimeField(
        default_timezone=timezone.utc,
        required=False,
        default=None,
    )
    host = serializers.CharField(required=False, max_length=128)


class PerProcessWindowUtilizationSerializer(serializers.ModelSerializer):
    executable_path = serializers.CharField(
        source="executable.executable_path", read_only=True
    )
    executable_name = serializers.CharField(
        source="executable.executable_name", read_only=True
    )
    host = serializers.CharField(source='executable.host.address', read_only=True)
    duration = serializers.DurationField()

    def get_duration(self, obj):
        try:
            return obj.duration
        except:
            return None

    class Meta:
        model = ProcessWindow
        fields = [
            "executable_path",
            "executable_name",
            "process_window_title",
            "duration",
            "host",
        ]
