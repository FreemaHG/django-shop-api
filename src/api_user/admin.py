from django.contrib import admin

from src.api_user.models import Profile, ImageForAvatar


# FIXME Убрать (не дублировать)
@admin.action(description="Мягкое удаление")
def deleted_records(adminmodel, request, queryset):
    """
    Мягкое удаление записей (смена статуса)
    """
    queryset.update(deleted=True)


@admin.action(description="Восстановить записи")
def restore_records(adminmodel, request, queryset):
    """
    Восстановить записи, отключенные ч/з мягкое удаление (смена статуса)
    """
    queryset.update(deleted=False)


class ChoiceAvatar(admin.TabularInline):
    """
    Вывод аватара пользователя
    """

    model = ImageForAvatar
    extra = 1


@admin.register(Profile)
class TagAdmin(admin.ModelAdmin):
    """
    Админ-панель для профайлов пользователей
    """
    list_display = ['id', 'username', 'full_name', 'email', 'phone', 'deleted']
    list_display_links = ("full_name",)
    list_editable = ("deleted",)
    inlines = (ChoiceAvatar,)

    # Мягкое удаление/восстановление записей
    actions = (
        deleted_records,
        restore_records,
    )

    fieldsets = (("Основное", {"fields": ("full_name", "phone", "deleted")}),)

    def username(self, object):
        return object.user.username

    username.short_description = "Username"

    def email(self, object):
        return object.user.email

    email.short_description = "Email"
