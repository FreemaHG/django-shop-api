from rest_framework import serializers

from src.api_user.models import Profile
from src.api_shop.serializers.image import ImageSerializer


class ProfileSerializer(serializers.ModelSerializer):
    """
    Схема для профиля пользователя
    """
    fullName = serializers.CharField(source="full_name")
    email = serializers.SerializerMethodField('get_email')
    avatar = ImageSerializer()

    def get_email(self, obj) -> str:
        """
        Вывод email пользователя
        """
        return obj.user.email

    class Meta:
        model = Profile
        fields = ['fullName', 'email', 'phone', 'avatar']
        