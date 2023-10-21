import logging

from typing import List, Dict
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

from src.api_shop.models.review import Review
from src.api_shop.services.product import ProductService


logger = logging.getLogger(__name__)


class CommentsService:
    """
    Сервис для добавления комментариев к товару
    """

    # TODO После добавления комментария -> вывод всех комментариев к товару
    @staticmethod
    def all_comments(product_id: int) -> QuerySet:
        """
        Вывод всех (активных) комментариев к товару

        :param product_id: id товара
        :return: все отзывы товара
        """
        logger.debug("Вывод комментариев к товару")

        # config = get_config()

        comments = Review.objects.filter(product__id=product_id, deleted=False)

        # TODO Кэширование отзывов (в отдельной фунции) и оптимизация запроса
        # comments = cache.get_or_set(
        #     f"comments_product_{product_id}",
        #     Review.objects.select_related(
        #         "buyer__profile", "buyer__profile__user"
        #     )
        #     .only(
        #         "created_at",
        #         "review",
        #         "buyer__profile__full_name",
        #         "buyer__profile__avatar",
        #         "buyer__profile__user__id",
        #     )
        #     .filter(product__id=product_id, deleted=False),
        #     60 * config.caching_time,
        # )

        logger.debug(f"Кол-во комментариев: {len(comments)}")

        return comments

    @staticmethod
    def add_new_comments(product_id: int, user: User, data: Dict) -> None:
        """
        Метод для добавления нового комментария к товару

        :param product_id: id товара, к которому оставляется комментарий
        :param user: текущий пользователь
        :param data: данные нового комментария
        :return: True / False в зависимости от успешности
        """
        # TODO Сбросить кэш с отзывами для указанного товара (в отдельной функции)
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
