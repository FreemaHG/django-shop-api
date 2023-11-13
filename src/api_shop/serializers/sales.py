import logging

from rest_framework import serializers

from src.api_shop.models.sales import SaleItem
from src.api_shop.serializers.image import ImageSerializer
from src.api_shop.serializers.pagination import PaginationSerializerMixin

logger = logging.getLogger(__name__)


class SaleItemSerializer(serializers.ModelSerializer):
    """
    Схема для записей о распродажах товаров
    """

    id = serializers.CharField(source="product.id")
    price = serializers.IntegerField(source="product.price")
    salePrice = serializers.FloatField(source="sale_price")
    dateFrom = serializers.SerializerMethodField("date_from_format")
    dateTo = serializers.SerializerMethodField("date_to_format")
    title = serializers.CharField(source="product.title")
    images = serializers.SerializerMethodField("get_images")

    def date_from_format(self, obj):
        """
        Изменяем формат времени
        """
        return obj.date_from.strftime("%Y-%m-%d")

    def date_to_format(self, obj):
        """
        Изменяем формат времени
        """
        return obj.date_to.strftime("%Y-%m-%d")

    def get_images(self, obj):
        """
        Возвращаем изображения товара
        """
        images = obj.product.images.all()
        serializer = ImageSerializer(images, many=True)

        return serializer.data

    class Meta:
        model = SaleItem
        fields = [
            "id",
            "price",
            "salePrice",
            "dateFrom",
            "dateTo",
            "title",
            "images",
        ]


class SalesSerializer(PaginationSerializerMixin):
    """
    Схема для вывода списка предложений с товарами на распродаже
    """

    items = SaleItemSerializer(many=True)
