from rest_framework import serializers

from src.api_shop.models import Basket, Product
from src.api_shop.serializers.image import ImageSerializer
from src.api_shop.serializers.tag import TagSerializer


class BasketSerializer(serializers.Serializer):
    """
    Схема для корзины с товарами
    """
    id = serializers.IntegerField(source='product.id')
    category = serializers.IntegerField(source='product.category.id')
    price = serializers.FloatField()
    count = serializers.IntegerField()
    date = serializers.DateTimeField(source='product.date')
    title = serializers.CharField(source='product.title')
    description = serializers.CharField(source='product.short_description')
    freeDelivery = serializers.BooleanField(source='product.free_delivery')
    images = ImageSerializer(source='product.images', many=True)
    tags = TagSerializer(source='product.tags',many=True)
    reviews = serializers.IntegerField(source='product.reviews_count')
    rating = serializers.FloatField(source='product.average_rating')

    class Meta:
        model = Basket
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
