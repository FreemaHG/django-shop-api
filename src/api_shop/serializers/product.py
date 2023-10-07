from rest_framework import serializers

from src.api_shop.models.product import Product
from src.api_shop.models.specification import Specification


class SpecificationSerializer(serializers.ModelSerializer):
    """
    Схема для характеристик товара
    """
    class Meta:
        model = Specification
        fields = ['name', 'value']


# TODO Настроить вывод полей с другими названиями согласно документации
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
