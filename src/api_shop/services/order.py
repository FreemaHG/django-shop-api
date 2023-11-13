import logging
from typing import List, Dict

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from src.api_shop.models import Basket
from src.api_shop.models.order import Order, PurchasedProduct
from src.api_shop.services.basket import BasketService

logger = logging.getLogger(__name__)


class OrderService:
    """
    Сервис для оформления и вывода данных о заказах
    """

    @classmethod
    def get(cls, order_id: int):
        """
        Поиск и возврат заказа по id
        """
        try:
            return Order.objects.get(id=order_id)

        except ObjectDoesNotExist:
            logger.error("Заказ не найден")
            raise Http404

    @classmethod
    def create(cls, data: List[Basket], user: User) -> int:
        """
        Создание заказа
        """
        logger.debug("Создание заказа")

        order = Order.objects.create(user=user)
        new_records = []

        for product in data:
            product = dict(product)

            record = PurchasedProduct(
                order=order,
                product_id=product["product"]["id"],
                count=product["count"],
                price=product["price"],
            )

            new_records.append(record)

        PurchasedProduct.objects.bulk_create(new_records)
        BasketService.clear(user)  # Очистка корзины

        return order.id

    @classmethod
    def update(cls, data: Dict) -> None:
        """
        Подтверждение заказа (обновление введенных данных)
        """

        order = cls.get(order_id=data["orderId"])

        order.full_name = data["fullName"]
        order.email = data["email"]
        order.email = data["phone"]
        order.city = data["city"]
        order.address = data["address"]

        if data["deliveryType"] == "Обычная доставка":
            order.delivery = 1
        else:
            order.delivery = 2

        if data["paymentType"] == "Онлайн картой":
            order.payment = 1
        else:
            order.payment = 2

        order.status = 2
        order.save()
