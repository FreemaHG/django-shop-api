from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User

# from src.api_shop.models.product import Product
from src.config import STATUS_CHOICES


class Review(models.Model):
    """
    Модель для хранения данных об отзывах о товарах
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="автор")
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, verbose_name="товар", related_name="reviews"
    )
    text = models.TextField(max_length=2000, verbose_name="отзыв")
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="оценка")
    date = models.DateTimeField(auto_created=True)

    # Мягкое удаление
    deleted = models.BooleanField(
        choices=STATUS_CHOICES, default=False, verbose_name="Статус"
    )

    class Meta:
        db_table = "reviews"
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"
        ordering = ["date"]

    def __str__(self) -> str:
        return str(self.author)
