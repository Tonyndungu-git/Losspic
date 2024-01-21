from rest_framework import serializers

class ImageCompressionSerializer(serializers.Serializer):
    original_image = serializers.ImageField()
