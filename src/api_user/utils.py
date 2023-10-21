import os
import logging

logger = logging.getLogger(__name__)

_AVATARS_PATH = os.path.join("images", "avatars")


def save_avatar(instance, filename: str) -> str:
    """
    Функция для сохранения аватара пользователя

    @param instance: объект профайла
    @param filename: название файла
    @return: path
    """
    logger.debug("Сохранение аватара пользователя")

    return os.path.join(
        _AVATARS_PATH, f"{instance.user.username}", f"{filename}"
    )
