from rest_framework import serializers

from src.api_shop.models.category import Category
from src.api_shop.serializers.image import ImageSerializer


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Схема для вложенной категорий товаров
    """
    # Вложенная схема с изображением
    image = ImageSerializer()

    class Meta:
        model = Category
        fields = ['id', 'title', 'image']


class CategorySerializer(SubCategorySerializer):
    """
    Схема для категорий товаров
    """
    # Вложенная схема (подкатегория товаров)
    subcategories = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'subcategories']
