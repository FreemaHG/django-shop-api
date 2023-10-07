from django.db import models

# from src.api_shop.models.product import Product


class Specification(models.Model):
    """
    Модель для хранения данных о характеристиках товаров
    """
    name = models.CharField(max_length=100, verbose_name="характеристика")
    value = models.CharField(max_length=100, verbose_name="значение")

    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, verbose_name="товар", related_name="specifications"
    )

    class Meta:
        db_table = "specifications"
        verbose_name = "характеристика товара"
        verbose_name_plural = "характеристики товаров"

    def __str__(self) -> str:
        return str(self.name)
