import logging

from django.db import models
from django.contrib.auth.models import User

from src.api_shop.models import Product


logger = logging.getLogger(__name__)


class Basket(models.Model):
    """
    Модель для хранения данных о корзине покупателя
    """

    # Warning null=True - для создания экземпляра корзины для анонимного пользователя из данных сессии
    user = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, verbose_name="покупатель"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="товар")
    count = models.PositiveIntegerField(default=1, verbose_name="кол-во")

    @property
    def price(self) -> int:
        """
        Стоимость одной позиции товара с учетом скидки и кол-ва товара (с округлением до целого)
        """
        price = int(self.product.price * self.count)
        return price

    class Meta:
        db_table = "basket"
        verbose_name = "Корзина покупателя"
        verbose_name_plural = "Корзины покупателей"

    def __str__(self) -> str:
        return f"Корзина покупателя"
