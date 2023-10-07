from django.db import models

from src.config import STATUS_CHOICES


class Tag(models.Model):
    """
    Модель для хранения тегов для товаров
    """

    name = models.CharField(max_length=100, verbose_name="тег")
    # Мягкое удаление
    deleted = models.BooleanField(choices=STATUS_CHOICES, default=False, verbose_name="статус")

    class Meta:
        db_table = "tags"
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name
