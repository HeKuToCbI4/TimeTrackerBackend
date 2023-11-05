from rest_framework import serializers

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
