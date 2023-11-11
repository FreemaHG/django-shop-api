import logging

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Avg
from django.core.cache import cache

from src.config import STATUS_CHOICES
from src.api_shop.models.category import Category
from src.api_shop.models.tag import Tag
from src.api_shop.models.review import Review


logger = logging.getLogger(__name__)


# TODO Добавить кэширование товара!
class Product(models.Model):
    """
    Модель для хранения данных о товарах
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="категория")
    price = models.FloatField(validators=[MinValueValidator(0)], verbose_name="цена")
    count = models.PositiveIntegerField(default=0, verbose_name="кол-во")
    date = models.DateTimeField(auto_now_add=True, verbose_name="время добавления")
    title = models.CharField(max_length=250, verbose_name="название")
    short_description = models.CharField(max_length=500, verbose_name="краткое описание")
    description = models.TextField(max_length=1000, verbose_name="описание")
    tags = models.ManyToManyField(Tag, related_name="products", verbose_name="теги")

    # Мягкое удаление
    deleted = models.BooleanField(
        choices=STATUS_CHOICES, default=False, verbose_name="Статус"
    )

    @property
    def reviews_count(self) -> int:
        """
        Кол-во отзывов у товара
        """
        return self.reviews.all().count()

    def free_delivery(self) -> bool:
        """
        Определение стоимости доставки в зависимости от стоимости товара
        """
        # TODO Задать значение 2000 через конфиги сайта
        if self.price > 2000:
            return True

        return False

    @property
    def average_rating(self) -> int:
        """
        Расчет средней оценки товара на основе всех отзывов
        """
        res = Review.objects.filter(product_id=self.id).aggregate(average_rate=Avg('rate'))

        try:
            # Округляем рейтинг товара до 1 знака после запятой
            return round(res["average_rate"], 1)

        except TypeError:
            return 0

    class Meta:
        db_table = "products"
        verbose_name = "товар"
        verbose_name_plural = "товары"
        ordering = ["id"]

    def add_tags(self, *args, **kwargs):
        """
        Добавляем запись об используемых тегах в категорию товара
        (для быстрого вывода всех тегов товаров определенной категории)
        """
        chair_tags = self.category.tags.all()

        for tag in self.tags.all():
            if tag not in chair_tags:
                self.category.tags.add(tag)

        super(Product, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        try:
            self.add_tags()

        except ValueError:
            super(Product, self).save(*args, **kwargs)
            self.add_tags()

    def __str__(self) -> str:
        return str(self.title)
