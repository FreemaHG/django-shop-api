from rest_framework import serializers


class ReviewSerializer(serializers.Serializer):
    """
    Схема для отзывов
    """
    author = serializers.CharField(min_length=1, max_length=150)
    email = serializers.EmailField(max_length=250)
    text = serializers.CharField(max_length=2000)
    rate = serializers.IntegerField(min_value=1, max_value=5)
    date = serializers.DateTimeField()
