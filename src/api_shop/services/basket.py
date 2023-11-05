import json
import logging
from typing import List

from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.http import HttpRequest

from src.api_shop.models import Basket, Product

logger = logging.getLogger(__name__)


class BasketService:
    """
    Сервис для добавления, удаления и вывода товаров из корзины авторизованного пользователя.
    """

    @classmethod
    def get_basket(cls, request: HttpRequest) -> QuerySet:
        """
        Получение записей о товарах в корзине пользователя
        """
        logger.debug("Вывод корзины авторизованного пользователя")
        basket = Basket.objects.filter(user=request.user)

        return basket


    @classmethod
    def add(cls, request: HttpRequest) -> QuerySet:
        """
        Добавление товара в корзину
        """
        data = request.data
        logger.debug("Добавление товара в корзину авторизованного пользователя")

        try:
            basket = Basket.objects.get(
                user=request.user,
                product_id=data["id"]
            )
            basket.count += data["count"]
            basket.save()
            logger.info("Увеличение кол-ва товара в корзине")

        except ObjectDoesNotExist:
            Basket.objects.create(
                user = request.user,
                product_id=data["id"],
                count=data["count"]
            )
            logger.info("Новый товар добавлен в корзину")

        finally:
            return cls.get_basket(request)  # Возвращаем обновленную корзину с товарами


    @classmethod
    def delete(cls, request: HttpRequest) -> QuerySet:
        """
        Удаление товара из корзины
        """
        data = json.loads(request.body)

        logger.debug("Удаление товара из корзины авторизованного пользователя")
        basket = Basket.objects.get(product_id=data["id"])
        basket.count -= data["count"]

        if basket.count > 0:
            basket.save()
            logger.info("Кол-во товара уменьшено")
        else:
            logger.warning("Кол-во товара в корзине <= 0. Удаление товара из корзины")
            basket.delete()

        return cls.get_basket(request)  # Возвращаем обновленную корзину с товарами


    @classmethod
    def merger(cls, request: HttpRequest, user: User) -> None:
        """
        Объединение корзин при регистрации и авторизации пользователя
        """
        logger.debug("Объединение корзин")

        records = request.session.get("basket", False)
        new_records = []

        if records:
            logger.debug(f"Имеются данные для слияния: {records}")

            for prod_id, count in records.items():
                # Проверка, есть ли товар уже в корзине зарегистрированного пользователя
                try:
                    deferred_product = Basket.objects.get(user=user, product_id=prod_id)
                    deferred_product.count += count  # Суммируем кол-во товара
                    deferred_product.save(update_fields=["count"])
                    logger.debug("Кол-во товара увеличено")

                except ObjectDoesNotExist:
                    deferred_product = Basket.objects.create(
                        user=user,
                        product_id=prod_id,
                        count=count
                    )

                    new_records.append(deferred_product)
                    logger.debug("Новый товар добавлен в корзину")

            logger.info("Корзины объединены")

            del request.session["basket"]  # Удаляем записи из сессии
            request.session.save()

        else:
            logger.warning("Нет записей для слияния")


class BasketSessionService:
    """
    Сервис для добавления, удаления и вывода товаров из корзины неавторизованного пользователя.
    Сохранение данных в сессии.
    """

    @classmethod
    def get_basket(cls, request: HttpRequest) -> List:
        """
        Получение записей о товарах в корзине пользователя
        """
        logger.debug("Вывод корзины гостя")

        records_list = []
        session_key = request.session.session_key
        cart_cache_key = f"basket_{session_key}"

        if cart_cache_key not in cache:
            logger.warning("Нет данных в кэше")
            products = request.session.get("basket", False)

            if products:
                logger.debug(f"Корзина пользователя: {products}")

                for prod_id, count in products.items():
                    records_list.append(
                        Basket(
                            product=Product.objects.get(id=prod_id),
                            count=count,
                        )
                    )

                # FIXME Изменить время хранения сессии
                cache.set(cart_cache_key, records_list, 60 * 60)
                logger.info("Товары сохранены в кэш")

            else:
                logger.warning("Записи о товарах не найдены")
        else:
            records_list = cache.get(cart_cache_key)

        return records_list

    @classmethod
    def add(cls, request: HttpRequest) -> List:
        """
        Добавление товара в корзину гостя
        """
        logger.debug("Добавление товара в корзину гостя")

        product_id = str(request.data["id"])
        count = int(request.data["count"])
        cls.check_key(request)  # Проверка ключа в сессии

        record = request.session["basket"].get(product_id, False)

        if record:
            request.session["basket"][product_id] += count
            logger.info("Кол-во товара увеличено")
        else:
            request.session["basket"][product_id] = count
            logger.info("Новый товар добавлен")

        request.session.save()
        cls.clear_cache_cart(request=request)  # Очистка кэша с товарами корзины

        return cls.get_basket(request)  # Возврат всех товаров в корзине

    @classmethod
    def delete(cls, request: HttpRequest) -> List:
        """
        Удаление товара из корзины гостя
        """
        logger.debug("Удаление товара из корзины гостя")

        data = json.loads(request.body)
        product_id = str(data["id"])
        count = data["count"]
        count_record = request.session["basket"].get(product_id, None)

        if not count_record:
            logger.error(f'Не найден ключ в сессии')
        else:
            count_record -= count

            if count_record <= 0:
                del request.session["basket"][product_id]
                logger.info("Товар удален из сессии")
            else:
                request.session["basket"][product_id] = count_record

            request.session.save()
            cls.clear_cache_cart(request=request)  # Очистка кэша с товарами корзины

        return cls.get_basket(request)  # Возврат всех товаров в корзине

    @classmethod
    def check_key(cls, request: HttpRequest) -> None:
        """
        Проверка ключа в объекте сессии (создание при необходимости) для записи, чтения и удаления товаров
        """
        logger.debug('Проверка ключа в объекте сессии')

        if not request.session.get("basket", False):
            request.session["basket"] = {}
            logger.info("Ключ создан")

    @classmethod
    def clear_cache_cart(cls, request: HttpRequest) -> None:
        """
        Очистка кэша с товарами в сессии
        """
        session_key = request.session.session_key
        cart_cache_key = f"basket_{session_key}"

        if cache.delete(cart_cache_key):
            logger.info("Кэш с товарами успешно очищен")
        else:
            logger.error("Кэш с товарами не очищен")
