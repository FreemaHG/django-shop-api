from rest_framework import serializers


class ImageSerializer(serializers.Serializer):
    """
    Схема для изображений
    """
    src = serializers.CharField()
    alt = serializers.CharField(max_length=250)

    class Meta:
        fields = ['src', 'alt']
