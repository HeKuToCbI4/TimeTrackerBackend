from rest_framework import serializers

from frame_consumer.models import (
    ProcessExecutable,
)


class ProcessExecutableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessExecutable
        fields = "__all__"


class ProcessExecutableUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessExecutable
        fields = ["executable_categories"]
