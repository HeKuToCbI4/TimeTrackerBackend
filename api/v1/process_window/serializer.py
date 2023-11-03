from rest_framework import serializers

from frame_consumer.models import (
    ProcessWindow,
)


class ProcessWindowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessWindow
        fields = "__all__"


class FilterQuerySerializer(serializers.Serializer):
    utc_from = serializers.IntegerField(
        required=False, help_text="UTC timestamp to filter entries 'from time'"
    )
    utc_to = serializers.IntegerField(
        required=False, help_text="UTC timestamp to filter entries 'to time'"
    )
