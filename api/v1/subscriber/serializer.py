from rest_framework import serializers


class SubscriptionSerializer(serializers.Serializer):
    host = serializers.CharField(max_length=64)
    port = serializers.IntegerField()
    consumer_id = serializers.CharField(max_length=256)

    class Meta:
        fields = "__all__"
