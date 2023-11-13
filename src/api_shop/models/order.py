from django.db import models
from django.contrib.auth.models import User

from src.api_shop.models import Product


class Order(models.Model):
    """
    Модель для хранения данных о заказах
    """

    STATUS_CHOICES = (
        (1, "Оформление"),
        (2, "Оформлен"),
        (3, "Не оплачен"),
        (4, "Подтверждение оплаты"),
        (5, "Оплачен"),
        (6, "Доставляется"),
    )

    DELIVERY_CHOICES = (
        (1, "Обычная доставка"),
        (2, "Экспресс доставка"),
    )

    PAYMENT_CHOICES = (
        (1, "Онлайн картой"),
        (2, "Онлайн со случайного чужого счета"),
    )

    # WARNING: многие поля null, т.к. по фронту сначала создается заказ, после обновляется подтвержденными данными
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="покупатель")
    full_name = models.CharField(max_length=150, null=True, verbose_name="ФИО")
    email = models.EmailField(null=True, verbose_name="email")
    phone_number = models.CharField(max_length=10, null=True, verbose_name="телефон")
    data_created = models.DateTimeField(
        auto_now_add=True, verbose_name="дата оформления"
    )
    delivery = models.IntegerField(
        choices=DELIVERY_CHOICES, null=True, verbose_name="тип доставки"
    )
    payment = models.IntegerField(
        choices=PAYMENT_CHOICES, null=True, verbose_name="оплата"
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES, default=1, verbose_name="cтатус"
    )
    city = models.CharField(max_length=150, null=True, verbose_name="город")
    address = models.CharField(max_length=300, null=True, verbose_name="адрес")

    @property
    def total_cost(self) -> float:
        """
        Общая стоимость всех товаров в заказе
        """
        res = sum((product.price * product.count) for product in self.products.all())
        return res

    class Meta:
        db_table = "orders"
        verbose_name = "заказ"
        verbose_name_plural = "заказы"
        ordering = ["-data_created"]

    def __str__(self) -> str:
        return f"Заказ №{self.id}"


class PurchasedProduct(models.Model):
    """
    Модель для хранения товаров, их кол-ва и стоимости на момент покупки с привязкой к номеру заказа
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="номер заказа",
    )
    # models.PROTECT - нельзя удалить, пока есть связанные ссылки
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="товар")
    count = models.PositiveIntegerField(verbose_name="кол-во")
    price = models.PositiveIntegerField(
        verbose_name="цена"
    )  # На момент оформления заказа

    class Meta:
        db_table = "purchased_products"
        verbose_name = "товар в заказе"
        verbose_name_plural = "товары в заказе"

    def __str__(self) -> str:
        return self.product.title
