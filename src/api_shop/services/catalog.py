import logging
from typing import Dict, List

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, QuerySet, Count, Avg

from src.api_shop.models import Product, Category

logger = logging.getLogger(__name__)


class CatalogService:
    """
    Сервис для вывода каталога с товарами.
    Фильтрация и сортировка товаров по переданным параметрам.
    """

    @classmethod
    def get_products(cls, query_params: Dict, tags: List = None):
        logger.debug(f"Вывод товаров по параметрам: {query_params}")

        category_id = query_params.get("category", None)

        if category_id:
            logger.debug(f"Фильтрация товаров категории: {category_id}")
            products = cls.by_category(category_id=int(category_id))
        else:
            logger.debug(f"Вывод всех товаров")
            products = Product.objects.all()

        name = query_params.get("filter[name]", None)

        if name:
            products = cls.by_name(name=name, products=products)

        min_price = query_params.get("filter[minPrice]", None)
        max_price = query_params.get("filter[maxPrice]", None)

        if min_price or max_price:
            products = cls.by_price(products=products, min_price=int(min_price), max_price=int(max_price))

        available = query_params.get("filter[available]", "true")

        if available == "true":
            products = cls.by_available(products=products)

        sort = query_params.get("sort", None)
        sort_type = query_params.get("sortType", "inc")

        if sort:
            products = cls.by_sort(products=products, sort=sort)

            if sort_type == "dec":
                logger.debug("Обратный порядок товаров")
                products = products.reverse()

        if tags:
            products = cls.by_tags(products=products, tags=tags)

        free_delivery = query_params.get("filter[freeDelivery]", "false")

        if free_delivery == "true":
            products = cls.be_free_delivery(products=products)

        logger.info(f"Возвращаемые товары: {products}")
        return products[:100]


    @classmethod
    def by_category(cls, category_id: int):
        """
        Возврат товаров по id категории
        """
        logger.debug(f"Вывод товаров категории: id - {category_id}")

        try:
            category = Category.objects.get(id = category_id)

        except ObjectDoesNotExist:
            logger.error("Категория не найдена")
            return []

        # Дочерние категории
        sub_categories = category.get_descendants(include_self=True)
        products = Product.objects.select_related("category").filter(category__in=sub_categories, deleted=False)

        logger.info(f"Возврат {products.count()} товаров")
        return products

    @classmethod
    def by_name(cls, name: str, products: QuerySet = None):
        """
        Поиск товаров по названию
        """
        logger.debug(f"Поиск товаров по названию: {name}")

        if not products:
            logger.debug("Поиск по всем товарам")
            products = Product.objects.all()[:100]

        logger.debug("Поиск по переданным товарам")
        res = products.filter(title__iregex=fr'.*({name}).*')

        logger.warning(f"Возврат {res.count()} товаров: {products}")
        return res

    @classmethod
    def by_price(cls, products: QuerySet, min_price: int, max_price: int):
        """
        Фильтрация товаров по минимальной цене
        """
        logger.debug(f"Фильтрация товаров по цене: min - {min_price}, max - {max_price}")
        res = products.filter(price__lte=max_price, price__gte=min_price)

        logger.info(f"Возврат {res.count()} товаров")
        return res

    @classmethod
    def be_free_delivery(cls, products: QuerySet):
        """
        Фильтрация товаров по бесплатной доставке
        """
        logger.debug(f"Фильтрация товаров по бесплатной доставке")

        # FIXME Сделать сравнение со значением из настроек
        res = products.filter(price__gt=2000)

        # res = list(filter(lambda prod: prod.free_delivery is True, products))

        logger.info(f"Возврат {res.count()} товаров")
        return res

    @classmethod
    def by_available(cls, products: QuerySet):
        """
        Фильтрация товаров по наличию
        """
        logger.debug(f"Фильтрация товаров по наличию")
        res = products.filter(count__gt=0)

        logger.info(f"Возврат {res.count()} товаров")
        return res

    @classmethod
    def by_tags(cls, products: QuerySet, tags: List):
        """
        Фильтрация по тегам
        """
        logger.debug(f"Фильтрация товаров по тегам")
        res = list(set(products.filter(tags__in=tags)))

        logger.info(f"Возврат {len(res)} товаров")
        return res


    @classmethod
    def by_sort(cls, products: QuerySet, sort: str):
        """
        Сортировка товара: по цене, средней оценке, кол-ву отзывов, дате
        """
        if sort == "price":
            logger.debug("Сортировка по цене")
            return products.order_by("-price")

        elif sort == "rating":
            logger.debug("Сортировка по средней оценке")
            products = products.annotate(rating=Avg("reviews__rate")).order_by("-rating")
            return products

        elif sort == "reviews":
            logger.debug("Сортировка по кол-ву отзывов")
            products = products.annotate(count_comments=Count("reviews")).order_by("-count_comments")
            return products

        elif sort == "date":
            logger.debug("Сортировка по дате добавления товара")
            return products.order_by("-date")
