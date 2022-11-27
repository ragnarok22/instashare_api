from rest_framework import serializers
from .models import File


class FileSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source="creator.username")
    creator_id = serializers.ReadOnlyField(source="creator.id")
    file = serializers.FileField()

    class Meta:
        model = File
        fields = ["id", "creator", "creator_id", "title", "file", "size", "created_at"]
