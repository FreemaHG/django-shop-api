import logging

from typing import List

from src.api_shop.models.category import Category


logger = logging.getLogger(__name__)


def soft_remove_child_records(categories: List[Category]) -> None:
    """
    Мягкое удаление дочерних категорий (смена статуса на неактивный)
    """
    logger.debug("Мягкое удаление дочерних записей")
    deleted_objects = []

    for record in categories:
        # Получаем все дочерние записи
        children = record.get_descendants(
            include_self=False
        )

        for child in children:
            child.deleted = True
            deleted_objects.append(child)

    # Сохраняем все измененные дочерние записи
    Category.objects.bulk_update(deleted_objects, ["deleted"])
