import logging
import os

logger = logging.getLogger(__name__)

_PRODUCTS_PATH = os.path.join("images", "products")
_CATEGORIES_PATH = os.path.join("images", "categories")


def save_img_for_product(instance, filename: str) -> str:
    """
    Сохранение изображения товара

    @param instance: объект изображения
    @param filename: название файла
    @return: строка - место хранения изображения
    """
    logger.debug("Сохранение изображения товара")

    # Сохраняем файлы в директорию с фронтендом
    return os.path.join("static", _PRODUCTS_PATH, f"{instance.product.id}", f"{filename}")


def save_img_for_category(instance, filename: str) -> str:
    """
    Сохранение изображения к категории

    @param instance: объект изображения
    @param filename: название файла
    @return: строка - место хранения изображения
    """
    logger.debug("Сохранение изображения категории")

    # Сохраняем файлы в директорию с фронтендом
    return os.path.join("static", _CATEGORIES_PATH, f"{instance.category.id}", f"{filename}")