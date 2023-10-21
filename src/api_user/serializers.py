from django.contrib.auth import get_user_model
from rest_framework import serializers

from src.api_user.models import Profile


User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    """
    Схема для ввода данных для авторизации
    """
    username = serializers.CharField(max_length=300, required=True, label="username")
    password = serializers.CharField(required=True, write_only=True, label="password",
                                     style={'input_type': 'password'}, trim_whitespace=False,)


class UserRegisterSerializer(UserLoginSerializer):
    """
    Схема для ввода данных при регистрации
    """
    name = serializers.CharField(max_length=300, required=True)

    def create(self, validated_data):
        """
        Регистрация пользователя
        """
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        Profile.objects.create(full_name=validated_data['name'], user=user)

        return user



