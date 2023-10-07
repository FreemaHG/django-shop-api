import logging

from typing import Dict, List, Union
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

from src.api_shop.models.product import Product


logger = logging.getLogger(__name__)


class ProductService:
    """
    Сервис для вывода товаров
    """

    @staticmethod
    def get_product(product_id: int) -> Product | None:
        """
        Возврат товара по id
        :param product_id: id товара для поиска
        :return:
        """
        logger.debug(f"Поиск товара по id: {product_id}")

        # TODO Обработка исключения, если товар не найден
        product = Product.objects.get(id=product_id)
        return product
