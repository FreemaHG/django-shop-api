import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView, GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api_shop.models.product import Product
from src.api_shop.models.category import Category
from src.api_shop.models.tag import Tag
from src.api_shop.models.image import ImageForCategory
from src.api_shop.serializers.category import CategorySerializer
from src.api_shop.serializers.product import ProductSerializer
from src.api_shop.serializers.tag import TagSerializer

logger = logging.getLogger(__name__)


class ProductDetail(RetrieveAPIView):
    """
    Вывод данных о товаре (по pk в url)
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoriesList(ListModelMixin, GenericAPIView):
    """
    Вывод категорий
    """
    serializer_class = CategorySerializer

    def get_queryset(self):
        """
        Вывод родительских категорий товаров
        """
        queryset = Category.objects.filter(deleted=False, parent=None)
        return queryset

    def get(self, request):
        return self.list(request)


class TagList(ListModelMixin, GenericAPIView):
    """
    Вывод тегов
    """
    serializer_class = TagSerializer

    def get_queryset(self):
        """
        Вывод родительских категорий товаров
        """
        queryset = Tag.objects.filter(deleted=False)
        return queryset

    def get(self, request):
        return self.list(request)