from rest_framework import serializers

from frame_consumer.models import ProcessCategory


class ProcessCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessCategory
        fields = "__all__"
