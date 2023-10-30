import logging


from django.http import JsonResponse, HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView, GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework import pagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from src.api_shop.models import SaleItem
from src.api_shop.models.product import Product
from src.api_shop.models.category import Category
from src.api_shop.models.review import Review
from src.api_shop.models.tag import Tag
from src.api_shop.serializers.category import CategorySerializer
from src.api_shop.serializers.product import ProductShortSerializer, ProductFullSerializer
from src.api_shop.serializers.review import ReviewInSerializer, ReviewOutSerializer
from src.api_shop.serializers.sales import SaleItemSerializer, SalesSerializer
from src.api_shop.serializers.tag import TagSerializer
from src.api_shop.services.comment import CommentsService
from src.megano.utils.pagination import SalePagination


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


class TagListView(ListModelMixin, GenericAPIView):
    """
    Вывод тегов
    """
    queryset = Tag.objects.filter(deleted=False)  # Только активные теги
    serializer_class = TagSerializer

    @swagger_auto_schema(tags=['tags'])
    def get(self, request):
        return self.list(request)


class ProductDetailView(RetrieveAPIView):
    """
    Вывод данных о товаре (по pk в url)
    """
    queryset = Product.objects.filter(deleted=False)  # Активные товары
    serializer_class = ProductFullSerializer


class ReviewCreateView(CreateModelMixin, GenericAPIView):
    """
    Добавление отзыва к товару
    """
    queryset = Review.objects.all()
    serializer_class = ReviewInSerializer
    # permission_classes = [IsAuthenticated]  # Разрешено только авторизованным пользователям

    def post(self, request, format=None, *args, **kwargs):
        self.product_id = kwargs["pk"]  # id товара

        # Создаем новый комментарий
        CommentsService.add_new_comments(
            product_id=self.product_id,
            user=request.user,
            data=request.data
        )

        comments = CommentsService.all_comments(product_id=self.product_id)  # Все комментарии товара
        serializer = ReviewOutSerializer(comments, many=True)  # Валидация данных (many=True - список)

        # Сериализуем данные и отправляем Json
        # safe=False - разрешаем сериализацию данных, не являющихся словарем (получаем список с OrderedDict)
        return JsonResponse(serializer.data, safe=False)


class LimitedProductsView(viewsets.ViewSet):
    """
    Вывод товаров ограниченной серии
    """

    @swagger_auto_schema(
        tags=['catalog'],
        responses={
            200: ProductShortSerializer(many=TagSerializer)
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
            200: SalesSerializer
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
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = SalesSerializer({"items": queryset})

        return JsonResponse(serializer.data, safe=False)
