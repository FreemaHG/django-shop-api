import logging

from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

from src.api_shop.models import SaleItem
from src.api_shop.models.product import Product
from src.api_shop.models.category import Category
from src.api_shop.serializers.category import CategorySerializer
from src.api_shop.serializers.product import ProductShortSerializer, CatalogSerializer
from src.api_shop.serializers.sales import SaleItemSerializer, SalesSerializer
from src.api_shop.serializers.tag import TagSerializer
from src.api_shop.pagination import SalePagination, CatalogPagination
from src.api_shop.services.catalog import CatalogService
from src.api_shop.swagger import filter_param, category, sort, sortType, limit

logger = logging.getLogger(__name__)


class CategoriesListView(ListModelMixin, GenericAPIView):
    """
    Вывод категорий
    """
    queryset = Category.objects.filter(deleted=False, parent=None)  # Активные родительские категории
    serializer_class = CategorySerializer

    @swagger_auto_schema(tags=['catalog'])
    def get(self, request):
        return self.list(request)


class LimitedProductsView(viewsets.ViewSet):
    """
    Вывод товаров ограниченной серии
    """

    @swagger_auto_schema(
        tags=['catalog'],
        responses={
            200: ProductShortSerializer(many=True)
        }
    )
    def list(self, request):
        """
        Get catalog limeted items
        """
        logger.debug("Вывод лимитированных товаров")

        queryset = Product.objects.filter(count__lte=50)[:10]
        serializer = ProductShortSerializer(queryset, many=True)

        return JsonResponse(serializer.data, safe=False)


class BannersProductsView(viewsets.ViewSet):
    """
    Вывод товаров для банера (акции)
    """

    @swagger_auto_schema(
        tags=['catalog'],
        responses={
            200: ProductShortSerializer(many=True)
        }
    )
    def list(self, request):
        """
        Get banner items
        """
        logger.debug("Вывод товаров для баннера")

        # FIXME Задать условие для вывода 3 случайных товаров для акций
        queryset = Product.objects.filter(count__lte=50)[:3]
        serializer = ProductShortSerializer(queryset, many=True)

        return JsonResponse(serializer.data, safe=False)


class PopularProductsView(viewsets.ViewSet):
    """
    Вывод популярных товаров
    """

    @swagger_auto_schema(
        tags=['catalog'],
        responses={
            200: ProductShortSerializer(many=True)
        }
    )
    def list(self, request):
        """
        Get catalog popular items
        """
        logger.debug("Вывод популярных товаров")

        # FIXME Задать условие для вывода товаров (сортировка по средней оценке отзывов и кол-ву продаж)
        queryset = Product.objects.all()
        serializer = ProductShortSerializer(queryset, many=True)

        return JsonResponse(serializer.data, safe=False)


class SalesView(ListModelMixin, viewsets.GenericViewSet):
    """
    Вывод товаров по распродаже
    """
    serializer_class = SaleItemSerializer  # Схема для сериализации данных
    pagination_class = SalePagination  # Кастомная пагинация

    @swagger_auto_schema(
        tags=['catalog'],
        responses={
            200: SalesSerializer()
        }
    )
    def list(self, request):
        """
        Get sales items
        """
        logger.debug("Вывод товаров на распродаже")

        # FIXME Проверить оптимизацию запроса
        # WARNING Ограничение в 40 записей, чтобы пагинация не ломала верстку (корявый фронт)
        queryset = SaleItem.objects.select_related("product").filter(deleted=False)[:40]  # Только активные акции

        # Пагинация
        # FIXME Вынести, не дублировать
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = SaleItemSerializer(queryset, many=True)

        return JsonResponse(serializer.data, safe=False)


class CatalogView(ListModelMixin, viewsets.GenericViewSet):
    """
    Вывод товаров по переданным параметрам
    """
    serializer_class = ProductShortSerializer  # Схема для сериализации данных
    pagination_class = CatalogPagination  # Кастомная пагинация

    @swagger_auto_schema(
        tags=['catalog'],
        manual_parameters=[filter_param, category, sort, sortType, limit],
        responses={
            200: CatalogSerializer()
        }
    )
    def list(self, request):
        """
        Get catalog items
        """
        logger.debug("Вывод каталога с товарами")

        query_params = request.query_params.dict()
        tags = request.GET.getlist('tags[]')

        # Получаем отфильтрованные товары
        queryset = CatalogService.get_products(query_params=query_params, tags=tags)

        # Пагинация
        # FIXME Вынести, не дублировать!!!
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ProductShortSerializer(queryset, many=True)

        return JsonResponse(serializer.data, safe=False)
