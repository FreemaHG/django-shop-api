import logging

from django.db import models

from src.megano.utils.save_img import save_img_for_product, save_img_for_category


logger = logging.getLogger(__name__)


class ImageForProduct(models.Model):
    """
    Модель для хранения данных об изображениях товаров
    """

    path = models.ImageField(upload_to=save_img_for_product, verbose_name="изображение")
    alt = models.CharField(max_length=250, verbose_name="alt")
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, verbose_name="товар", related_name="images"
    )

    class Meta:
        db_table = "images_for_products"
        verbose_name = "изображение"
        verbose_name_plural = "изображения"

    @property
    def src(self) -> str:
        """
        Переопределяем path для подстановки в frontend и корректного отображения картинки
        """
        return f"/{self.path}"

    def __str__(self) -> str:
        return str(self.path)


class ImageForCategory(models.Model):
    """
    Модель для хранения данных об изображениях для категорий товаров
    """

    path = models.ImageField(
        upload_to=save_img_for_category, verbose_name="изображение"
    )
    alt = models.CharField(max_length=250, verbose_name="alt")
    category = models.OneToOneField(
        "Category",
        on_delete=models.CASCADE,
        verbose_name="категория",
        related_name="image",
    )

    class Meta:
        db_table = "images_for_category"
        verbose_name = "изображение"
        verbose_name_plural = "изображения"

    @property
    def src(self) -> str:
        """
        Переопределяем path для подстановки в frontend и корректного отображения картинки
        """
        return f"/{self.path}"

    def __str__(self) -> str:
        return str(self.path)
