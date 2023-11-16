import datetime

from rest_framework import serializers

from frame_consumer.models import (
    ProcessExecutable,
)
from django.utils import timezone


class ProcessExecutableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessExecutable
        fields = "__all__"


class ProcessExecutableUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessExecutable
        fields = ["executable_categories"]


class PerProcessUtilizationRequestSerializer(serializers.Serializer):
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


class PerProcessUtilizationSerializer(serializers.ModelSerializer):
    duration = serializers.IntegerField()
    host = serializers.CharField(source="host.address")

    def get_duration(self, obj):
        try:
            return obj.duration
        except:
            return None

    class Meta:
        model = ProcessExecutable
        fields = ["executable_path", "executable_name", "duration", "host"]
