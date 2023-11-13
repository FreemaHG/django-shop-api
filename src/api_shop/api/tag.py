import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from src.api_shop.models import Category
from src.api_shop.serializers.tag import TagSerializer
from src.api_shop.swagger import category


logger = logging.getLogger(__name__)


class TagListView(viewsets.ViewSet):
    """
    Вывод тегов
    """

    @swagger_auto_schema(
        tags=["tags"],
        manual_parameters=[category],
        responses={200: TagSerializer(many=True)},
    )
    def list(self, request):
        category_id = request.query_params.get(
            "category", None
        )  # Извлекаем id категории из URL

        # Все теги, встречающиеся в данной категории товара
        try:
            tags = Category.objects.get(id=category_id).tags.filter(deleted=False)
        except ObjectDoesNotExist:
            logger.error("Теги не найдены")
            return HttpResponse("Теги не найдены")

        serializer = TagSerializer(tags, many=True)
        return JsonResponse(serializer.data, safe=False)
