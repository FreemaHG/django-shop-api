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


class ProductSerializer(serializers.ModelSerializer):
    """
    Схема для товара
    """

    description = serializers.CharField(source="short_description")
    fullDescription = serializers.CharField(source="description")
    freeDelivery = serializers.BooleanField(source="free_delivery")
    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)
    reviews = ReviewOutSerializer(many=True)
    specifications = SpecificationSerializer(many=True)
    rating = serializers.FloatField(source="average_rating")
    date = serializers.SerializerMethodField('date_format')

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
            'fullDescription',
            'freeDelivery',
            'images',
            'tags',
            'reviews',
            'specifications',
            'rating'
        ]
