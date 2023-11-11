import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

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
        """
        logger.debug(f"Поиск товара по id: {product_id}")

        try:
            return Product.objects.get(id=product_id)

        except ObjectDoesNotExist:
            logger.error("Товар не найден")
            raise Http404
