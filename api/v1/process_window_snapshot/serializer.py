from rest_framework import serializers

from frame_consumer.models import (
    ProcessWindowSnapshot,
)


class ProcessWindowSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessWindowSnapshot
        fields = "__all__"


class FilterQuerySerializer(serializers.Serializer):
    utc_from_ts = serializers.IntegerField(
        help_text="UTC timestamp to filter entries 'from time'", required=False
    )
    utc_to_ts = serializers.IntegerField(
        help_text="UTC timestamp to filter entries 'to time'", required=False
    )

    def validate_utc_from_ts(self, data):
        print(f"Validate utc from. {data=}")
        return data

    def validate_utc_to_ts(self, data):
        print(f"Validate utc from. {data}")
        return data
