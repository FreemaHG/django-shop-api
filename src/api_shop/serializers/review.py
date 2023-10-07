from rest_framework import serializers

from src.api_shop.models.review import Review


class ReviewInSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['author', 'email', 'text', 'date', 'rate']


class ReviewOutSerializer(serializers.ModelSerializer):
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
        Возвращаем имя автора
        """
        if not obj.author:
            last_name = obj.user.last_name
            first_name = obj.user.first_name

            if last_name or first_name:
                return f"{last_name} {first_name}"

            return obj.user.username

        else:
            return obj.author

    def get_email(self, obj) -> str:
        """
        Возвращаем email пользователя, оставившего отзыв
        """
        if not obj.email:
            return obj.user.email

        return obj.email

    class Meta:
        model = Review
        fields = [
            'author',
            'email',
            'text',
            'rate',
            'date',
        ]