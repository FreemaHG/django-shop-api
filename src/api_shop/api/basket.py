import logging

from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from src.api_shop.serializers.basket import BasketSerializer
from src.api_shop.swagger import basket_data
from src.api_shop.services.basket import BasketService, BasketSessionService


logger = logging.getLogger(__name__)


class BasketView(APIView):
    @swagger_auto_schema(tags=["basket"], responses={200: BasketSerializer(many=True)})
    def get(self, request):
        """
        Получить товары в корзине пользователя
        """
        if request.user.is_authenticated:
            queryset = BasketService.get_basket(
                request
            )  # Товары аутентифицированного пользователя из БД
        else:
            queryset = BasketSessionService.get_basket(
                request
            )  # Товары гостя из сессии

        serializer = BasketSerializer(queryset, many=True)

        return JsonResponse(serializer.data, safe=False)

    @swagger_auto_schema(
        tags=["basket"],
        manual_parameters=[basket_data],
        responses={200: BasketSerializer(many=True)},
    )
    def post(self, request):
        """
        Добавить товар в корзину
        """
        if request.user.is_authenticated:
            queryset = BasketService.add(
                request
            )  # Добавить товар в корзину аутентифицированного пользователя (в БД)
        else:
            queryset = BasketSessionService.add(request)  # Записать данные в сессию

        serializer = BasketSerializer(queryset, many=True)

        return JsonResponse(serializer.data, safe=False)

    @swagger_auto_schema(
        tags=["basket"],
        manual_parameters=[basket_data],
        responses={200: BasketSerializer(many=True)},
    )
    def delete(self, request):
        """
        Удалить товар из корзины
        """
        if request.user.is_authenticated:
            queryset = BasketService.delete(request)  # Удалить товар из БД
        else:
            queryset = BasketSessionService.delete(request)  # Удалить из сессии

        serializer = BasketSerializer(queryset, many=True)

        return JsonResponse(serializer.data, safe=False)
