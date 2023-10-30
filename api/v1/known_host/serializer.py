from rest_framework import serializers

from frame_consumer.models import (
    KnownHost,
)


class KnownHostSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnownHost
        fields = "__all__"
