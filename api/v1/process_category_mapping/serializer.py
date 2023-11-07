from rest_framework import serializers

from frame_consumer.models import ProcessCategoryMapping


class ProcessCategoryMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessCategoryMapping
        fields = "__all__"
