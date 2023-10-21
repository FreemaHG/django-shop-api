import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.api_user.models import Profile
from src.api_user.serializers.profile import ProfileSerializer


logger = logging.getLogger(__name__)


@swagger_auto_schema(
    tags=['profile'],
    methods=['get', 'post'],
    responses={
        200: ProfileSerializer,
        404: "No data found"
    }
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # Разрешено только аутентифицированным пользователям
def profile(request):
    """
    Выход из учетной записи пользователя
    """
    if request.method == "GET":
        logging.debug("Вывод данных профайла")

        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)  # Сериализация данных

            return JsonResponse(serializer.data)  # Преобразуем и отправляем JSON

        except ObjectDoesNotExist:
            logger.error("Нет данных профайла")
            return Response(status=status.HTTP_404_NOT_FOUND)

    else:
        logging.debug("Обновление данных профайла")

        ...





