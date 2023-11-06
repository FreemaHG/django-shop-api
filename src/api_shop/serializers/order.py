import logging

from rest_framework import serializers

from src.api_shop.models.order import Order
from src.api_shop.serializers.basket import BasketSerializer


logger = logging.getLogger(__name__)


class OrderIdSerializer(serializers.Serializer):
    """
    Схема для вывода id заказа
    """
    orderId = serializers.IntegerField()

    class Meta:
        fields = ["orderId"]


class OrderSerializer(serializers.ModelSerializer):
    """
    Схема для оформления заказа
    """
    createdAt = serializers.SerializerMethodField("date_format")
    fullName = serializers.CharField(source="user.profile.full_name")
    email = serializers.CharField(source="user.email")
    phone = serializers.CharField(source="user.profile.phone")
    deliveryType = serializers.IntegerField(source="delivery")
    paymentType = serializers.IntegerField(source="payment")
    totalCost = serializers.FloatField(source="total_cost")
    products = BasketSerializer(many=True, read_only=True)

    def date_format(self, obj):
        """
        Изменяем формат времени
        """
        return obj.data_created.strftime("%Y-%m-%d %H:%M")  # 2023-05-05 12:12

    class Meta:
        model = Order
        fields = [
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products"
        ]
