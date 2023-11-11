from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from src.config import STATUS_CHOICES


class Category(MPTTModel):
    """
    Модель для хранения данных о категориях товаров с возможностью вложенных категорий
    """

    title = models.CharField(max_length=100, verbose_name="название")
    tags = models.ManyToManyField("Tag", related_name="categories", verbose_name="теги")

    # Вложенные категории
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories",
        verbose_name="родительская категория",
    )

    # Мягкое удаление
    deleted = models.BooleanField(
        choices=STATUS_CHOICES, default=False, verbose_name="статус"
    )

    class MPTTMeta:
        """
        Сортировка по вложенности
        """
        order_insertion_by = ("title",)

    class Meta:
        db_table = "categories"
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self) -> str:
        return self.title
