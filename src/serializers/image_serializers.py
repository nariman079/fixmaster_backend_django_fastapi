from rest_framework import serializers
from src.models import Image
from src.services.image_services import get_full_url


class ImageSerializer(serializers.ModelSerializer):
    """
    A serializer for image model
    """

    image = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ("id", "image", "priority")

    def get_image(self, obj):
        return get_full_url(self, obj, "image")
