from typing import List

from rest_framework import serializers

from src.api_shop.models.product import Product
from src.api_shop.models.specification import Specification
from src.api_shop.serializers.image import ImageSerializer
from src.api_shop.serializers.review import ReviewOutSerializer
from src.api_shop.serializers.tag import TagSerializer


class SpecificationSerializer(serializers.ModelSerializer):
    """
    Схема для характеристик товара
    """
    class Meta:
        model = Specification
        fields = ['name', 'value']


class ProductShortSerializer(serializers.ModelSerializer):
    """
    Схема для товара (короткая)
    """

    date = serializers.SerializerMethodField('date_format')
    description = serializers.CharField(source="short_description")
    freeDelivery = serializers.BooleanField(source="free_delivery")
    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)
    reviews = serializers.IntegerField(source="reviews_count")  # Кол-во отзывов
    rating = serializers.FloatField(source="average_rating")

    def date_format(self, obj):
        """
        Изменяем формат времени
        """
        return obj.date.strftime(f"%a %b %Y %H:%M:%S %Z%z")

    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'price',
            'count',
            'date',
            'title',
            'description',
            'freeDelivery',
            'images',
            'tags',
            'reviews',
            'rating'
        ]


class ProductFullSerializer(ProductShortSerializer):
    """
    Схема для товара (полная). Для страницы товара.
    """
    fullDescription = serializers.CharField(source="description")
    reviews = ReviewOutSerializer(many=True)  # Список с отзывами
    specifications = SpecificationSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'
