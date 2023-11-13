import json
import logging

from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from src.api_shop.services.basket import BasketService
from src.api_user.serializers.login_and_register import UserRegisterSerializer
from src.api_user.serializers.login_and_register import UserLoginSerializer


logger = logging.getLogger(__name__)


@swagger_auto_schema(
    tags=["auth"],
    method="post",
    request_body=UserRegisterSerializer,
    responses={201: "The user is registered", 400: "Invalid data"},
)
@api_view(["POST"])
@permission_classes([AllowAny])  # Разрешено любому пользователю
def register_user(request):
    """
    Регистрация пользователя
    """
    logging.debug("Регистрация пользователя")

    data = json.loads(request.body)
    serializer = UserRegisterSerializer(data=data)

    if serializer.is_valid():
        user = (
            serializer.save()
        )  # Создаем и возвращаем нового пользователя в методе create() в схеме
        # Аутентификация
        user = authenticate(
            username=user.username, password=serializer.validated_data["password"]
        )
        login(request, user)  # Авторизация нового пользователя

        BasketService.merger(request=request, user=user)  # Слияние корзин

        return Response(status=status.HTTP_201_CREATED)

    logging.error(f"Невалидные данные: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    tags=["auth"],
    method="post",
    request_body=UserLoginSerializer,
    responses={200: "The user is authenticated", 400: "Invalid data"},
)
@api_view(["POST"])
@permission_classes([AllowAny])  # Разрешено любому пользователю
def user_login(request):
    """
    Авторизация пользователя
    """
    logging.debug("Авторизация пользователя")

    data = json.loads(request.body)
    serializer = UserLoginSerializer(data=data)

    if serializer.is_valid(raise_exception=True):
        user = authenticate(
            username=data["username"], password=data["password"]
        )  # Аутентификация
        login(request, user)  # Авторизация нового пользователя
        logging.info(f"Пользователь аутентифицирован")

        BasketService.merger(request=request, user=user)  # Слияние корзин

        return Response(None, status=status.HTTP_200_OK)

    else:
        logging.error(f"Невалидные данные: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    tags=["auth"],
    method="post",
    responses={
        200: "The user logged out of the account",
        403: "The user is not logged in",
    },
)
@api_view(["POST"])
@permission_classes(
    [IsAuthenticated]
)  # Разрешено только аутентифицированным пользователям
def user_logout(request):
    """
    Выход из учетной записи пользователя
    """
    logging.debug("Выход из учетной записи")
    logout(request)

    return Response(None, status=status.HTTP_200_OK)
