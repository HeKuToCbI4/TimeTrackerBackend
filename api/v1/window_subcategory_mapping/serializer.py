from rest_framework import serializers

from frame_consumer.models import WindowSubCategoryMapping


class WindowSubCategoryMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindowSubCategoryMapping
        fields = "__all__"
