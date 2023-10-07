from rest_framework import serializers

from src.api_shop.models.review import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Схема для отзывов
    """
    author = serializers.SerializerMethodField('get_author')
    email = serializers.SerializerMethodField('get_email')
    date = serializers.SerializerMethodField('date_format')

    def date_format(self, obj):
        """
        Изменяем формат времени
        """
        return obj.date.strftime("%Y-%m-%d %H:%M")

    def get_author(self, obj) -> str:
        """
        Возвращаем имя пользователя
        """
        last_name = obj.author.last_name
        first_name = obj.author.first_name

        if last_name or first_name:
            return f"{obj.author.last_name} {obj.author.first_name}"

        return obj.author.username

    def get_email(self, obj) -> str:
        """
        Возвращаем email пользователя, оставившего отзыв
        """
        return obj.author.email

    class Meta:
        model = Review
        fields = [
            'author',
            'email',
            'text',
            'rate',
            'date',
        ]