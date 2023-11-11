import logging

from typing import Dict
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import QuerySet

from src.api_shop.models.review import Review
from src.api_shop.services.product import ProductService


logger = logging.getLogger(__name__)


class CommentsService:
    """
    Сервис для добавления комментариев к товару
    """

    @staticmethod
    def all_comments(product_id: int) -> QuerySet:
        """
        Вывод всех (активных) комментариев к товару
        """
        logger.debug("Вывод комментариев к товару")

        comments = cache.get_or_set(
            f"comments_{product_id}",
            Review.objects.filter(product__id=product_id, deleted=False),
        )

        return comments

    @staticmethod
    def add_new_comments(product_id: int, user: User, data: Dict) -> None:
        """
        Метод для добавления нового комментария к товару
        """
        logger.debug(f"Добавление комментария к товару")

        product = ProductService.get_product(product_id=product_id)
        author = data.get("author", None)
        email = data.get("email", None)

        if not author:
            if user.last_name or user.first_name:
                author = f"{user.last_name} {user.first_name}"
            else:
                author = user.username

        if not email:
            email = user.email

        Review.objects.create(
            user=user,
            product=product,
            author=author,
            email=email,
            text=data["text"],
            rate=data["rate"],
        )

        logger.info("Комментарий успешно создан")

        cache.delete(f"average_rating_{product_id}")  # Очистка кэша с средней оценкой товара
        cache.delete(f"comments_{product_id}")  # Очистка кэша с комментариями к текущему товару
