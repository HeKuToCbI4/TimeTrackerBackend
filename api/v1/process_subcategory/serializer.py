from rest_framework import serializers

from frame_consumer.models import ProcessSubCategory


class ProcessSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessSubCategory
        fields = "__all__"
