import logging
import random

from django.http import JsonResponse
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
from src.api_shop.pagination import SalePagination, CatalogPagination
from src.api_shop.services.catalog import CatalogService
from src.api_shop.swagger import filter_param, category, sort, sortType, limit


logger = logging.getLogger(__name__)


class CategoriesListView(ListModelMixin, GenericAPIView):
    """
    Вывод категорий
    """

    queryset = Category.objects.filter(
        deleted=False, parent=None
    )  # Активные родительские категории
    serializer_class = CategorySerializer

    @swagger_auto_schema(tags=["catalog"])
    def get(self, request):
        return self.list(request)


class LimitedProductsView(viewsets.ViewSet):
    @swagger_auto_schema(
        tags=["catalog"], responses={200: ProductShortSerializer(many=True)}
    )
    def list(self, request):
        """
        Вывод товаров ограниченной серии
        """
        logger.debug("Вывод лимитированных товаров")

        # TODO Обработать ошибку, когда нет товаров!!!
        queryset = list(Product.objects.filter(count__lte=50))

        if len(queryset) > 4:
            queryset = random.sample(queryset, 4)  # 4 случайные записи

        serializer = ProductShortSerializer(queryset, many=True)

        return JsonResponse(serializer.data, safe=False)


class BannersProductsView(viewsets.ViewSet):
    @swagger_auto_schema(
        tags=["catalog"], responses={200: ProductShortSerializer(many=True)}
    )
    def list(self, request):
        """
        Вывод товаров для банера (акции)
        """
        logger.debug("Вывод товаров для баннера")
        sales_id = list(
            SaleItem.objects.values_list("id", flat=True)
        )  # Все id записей с акциями

        if len(sales_id) > 3:
            sales_id = random.sample(sales_id, 3)  # 3 случайные записи

        # Получаем товары по акции
        queryset = Product.objects.filter(
            saleitem__id__in=sales_id
        )

        serializer = ProductShortSerializer(queryset, many=True)

        return JsonResponse(serializer.data, safe=False)


class PopularProductsView(viewsets.ViewSet):
    @swagger_auto_schema(
        tags=["catalog"], responses={200: ProductShortSerializer(many=True)}
    )
    def list(self, request):
        """
        Вывод популярных товаров
        """
        logger.debug("Вывод популярных товаров")
        queryset = Product.objects.all()[:8]
        serializer = ProductShortSerializer(queryset, many=True)

        return JsonResponse(serializer.data, safe=False)


class SalesView(ListModelMixin, viewsets.GenericViewSet):
    serializer_class = SaleItemSerializer  # Схема для сериализации данных
    pagination_class = SalePagination  # Кастомная пагинация

    @swagger_auto_schema(tags=["catalog"], responses={200: SalesSerializer()})
    def list(self, request):
        """
        Вывод товаров на распродаже
        """
        logger.debug("Вывод товаров на распродаже")

        # WARNING Ограничение в 40 записей, чтобы пагинация не ломала верстку (корявый фронт)
        queryset = SaleItem.objects.select_related("product").filter(deleted=False)[
            :40
        ]  # Только активные акции

        # Пагинация
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
        tags=["catalog"],
        manual_parameters=[filter_param, category, sort, sortType, limit],
        responses={200: CatalogSerializer()},
    )
    def list(self, request):
        """
        Get catalog items
        """
        logger.debug("Вывод каталога с товарами")

        query_params = request.query_params.dict()
        tags = request.GET.getlist("tags[]")

        # Получаем отфильтрованные товары
        queryset = CatalogService.get_products(query_params=query_params, tags=tags)

        # Пагинация
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = ProductShortSerializer(queryset, many=True)

        # return JsonResponse(serializer.data, safe=False)
        return self.get_paginated_response(serializer.data)
