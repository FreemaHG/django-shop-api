import json
import logging

from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, mixins, generics
from rest_framework.views import APIView

from src.api_shop.models import Product
from src.api_shop.models.basket import Basket
from src.api_shop.serializers.basket import BasketSerializer
from src.api_shop.serializers.product import ProductShortSerializer
from src.api_shop.swagger import basket_data
from src.api_shop.services.basket import BasketService, BasketSessionService

logger = logging.getLogger(__name__)


class BasketView(APIView):

    @swagger_auto_schema(
        tags=['basket'],
        responses={
            200: BasketSerializer(many=True)
        }
    )
    def get(self, request):
        """
        Get items in basket
        """
        # TODO Возможно вынести (не дублировать)
        if request.user.is_authenticated:
            queryset = BasketService.get_basket(request)
        else:
            queryset = BasketSessionService.get_basket(request)

        serializer = BasketSerializer(queryset, many=True)

        return JsonResponse(serializer.data, safe=False)

    @swagger_auto_schema(
        tags=['basket'],
        manual_parameters=[basket_data],
        responses={
            200: BasketSerializer(many=True)
        }
    )
    def post(self, request):
        """
        Add item to basket
        """
        # TODO Возможно вынести (не дублировать)
        if request.user.is_authenticated:
            queryset = BasketService.add(request)
        else:
            queryset = BasketSessionService.add(request)

        serializer = BasketSerializer(queryset, many=True)

        return JsonResponse(serializer.data, safe=False)

    @swagger_auto_schema(
        tags=['basket'],
        manual_parameters=[basket_data],
        responses={
            200: BasketSerializer(many=True)
        },
    )
    def delete(self, request):
        """
        Remove item from basket
        """
        # TODO Возможно вынести (не дублировать)
        if request.user.is_authenticated:
            queryset = BasketService.delete(request)
        else:
            queryset = BasketSessionService.delete(request)

        serializer = BasketSerializer(queryset, many=True)

        return JsonResponse(serializer.data, safe=False)
