from rest_framework import serializers


class SubscriptionSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=64)
    port = serializers.IntegerField()
    consumer_id = serializers.CharField(max_length=256)
    auto_monitor = serializers.BooleanField(required=False)

    class Meta:
        fields = "__all__"


class UnsubscriptionSerializer(serializers.Serializer):
    host = serializers.CharField(max_length=64)
    port = serializers.IntegerField()

    class Meta:
        fields = "__all__"
