from django.db import models
from django.contrib.auth.models import User

from src.megano.utils.save_img import save_avatar
from src.config import STATUS_CHOICES
from django.db import models


class Profile(models.Model):
    """
    Модель для хранения доп.данных о пользователе (профайл)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="пользователь")
    full_name = models.CharField(max_length=150, verbose_name="ФИО")
    phone = models.CharField(unique=True, max_length=10, null=True, verbose_name="телефон")
    deleted = models.BooleanField(choices=STATUS_CHOICES, default=False, verbose_name="Статус")  # Мягкое удаление

    class Meta:
        db_table = "profile"
        verbose_name = "профиль"
        verbose_name_plural = "учетные записи"

    def __str__(self):
        return self.full_name


# FIXME Не дублировать модели с картинками 3 раза!!!
class ImageForAvatar(models.Model):
    """
    Модель для хранения данных об аватарах пользователей
    """
    path = models.ImageField(upload_to=save_avatar, verbose_name="изображение")
    alt = models.CharField(max_length=250, verbose_name="alt")
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, verbose_name="профиль", related_name="avatar")

    class Meta:
        db_table = "images_for_avatars"
        verbose_name = "аватар"
        verbose_name_plural = "аватары"

    @property
    def src(self) -> str:
        """
        Переопределяем path для подстановки в frontend и корректного отображения картинки
        """
        return f"/{self.path}"

    def __str__(self) -> str:
        return str(self.path)
