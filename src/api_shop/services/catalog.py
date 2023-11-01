import logging
from typing import Dict

logger = logging.getLogger(__name__)


class CatalogService:
    """
    Сервис для вывода каталога с товарами.
    Фильтрация и сортировка товаров по переданным параметрам.
    """

    @staticmethod
    def get_products(query_params: Dict):
        logger.debug(f"Вывод товаров по параметрам: {query_params}")

        # ?filter[name]=aefeafae&filter[minPrice]=56339&filter[maxPrice]=192605&filter[freeDelivery]=false&filter[available]=true&currentPage=1&category=5&sort=price&sortType=inc&tags[]=4&tags[]=5&limit=20

        pass


    @staticmethod
    def by_category(category_id: int):
        """
        Возврат товаров по id категории
        """

