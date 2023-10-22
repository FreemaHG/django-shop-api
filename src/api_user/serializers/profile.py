import logging

from rest_framework import serializers

from src.api_user.models import Profile
from src.api_shop.serializers.image import ImageSerializer


logger = logging.getLogger(__name__)


class ProfileSerializer(serializers.ModelSerializer):
    """
    Схема для профиля пользователя
    """
    fullName = serializers.CharField(source="full_name")
    email = serializers.SerializerMethodField('get_email')
    phone = serializers.CharField()
    avatar = ImageSerializer(read_only=True)

    def get_email(self, obj) -> str:
        """
        Вывод email пользователя
        """
        return obj.user.email

    def validate_title(self, value):
        if self.phone == value:
            pass

    class Meta:
        model = Profile
        fields = ['fullName', 'email', 'phone', 'avatar']
        