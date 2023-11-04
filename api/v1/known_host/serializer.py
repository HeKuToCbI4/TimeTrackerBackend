from rest_framework import serializers

from frame_consumer.models import (
    KnownHost,
)


class KnownHostListCreateSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = KnownHost
        fields = "__all__"


class KnownHostUpdateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnownHost
        fields = [
            "consumer_id",
            "is_monitored",
            "status",
            "auto_start_monitor",
        ]
