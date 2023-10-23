from rest_framework import serializers

from frame_consumer.models import ProcessCategory, ProcessExecutable, ProcessWindow, KnownHost


class ProcessCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessCategory
        fields = '__all__'
