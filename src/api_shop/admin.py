from django.contrib import admin, messages
from django.db.models import QuerySet
from mptt.admin import DraggableMPTTAdmin

from src.api_shop.models.order import Order, PurchasedProduct
from src.api_shop.models.product import Product
from src.api_shop.models.category import Category
from src.api_shop.models.image import ImageForCategory, ImageForProduct
from src.api_shop.models.review import Review
from src.api_shop.models.specification import Specification
from src.api_shop.models.tag import Tag
from src.api_shop.models.sales import SaleItem
from src.api_shop.models.basket import Basket
from src.api_shop.utils.admin.soft_remove import soft_remove_child_records


# FIXME Раскидать по разным файлам!!!
@admin.action(description="Мягкое удаление всех записей (включая дочерние)")
def deleted_all_records(adminmodel, request, queryset):
    """
    Мягкое удаление всех записей, включая дочерние
    """
    soft_remove_child_records(queryset)  # Мягкое удаление всех дочерних записей
    queryset.update(deleted=True)  # Мягкое удаление родительской записи


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


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Админ-панель для товарных тегов
    """
    list_display = ['id', 'name', 'deleted']
    list_display_links = ("name",)
    list_editable = ("deleted",)

    # Мягкое удаление/восстановление записей
    actions = (
        deleted_records,
        restore_records,
    )

    fieldsets = (("Основное", {"fields": ("name", "deleted")}),)


class ChoiceImagesForCategory(admin.TabularInline):
    """
    Вывод изображений на странице категории
    """

    model = ImageForCategory
    extra = 1


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """
    Админ-панель для категорий товаров
    """

    list_display = (
        "tree_actions",
        "indented_title",
        "id",
        "deleted",
    )
    list_display_links = ("indented_title",)
    list_filter = ("deleted",)
    list_editable = ("deleted",)
    search_fields = ("title",)

    inlines = (ChoiceImagesForCategory,)

    # Мягкое удаление/восстановление записей
    actions = (deleted_all_records, restore_records)

    fieldsets = (
        ("Основное", {"fields": ("title", "parent")}),
        # ("Файлы", {"fields": ("image",)}),
        ("Статусы", {"fields": ("deleted",)}),
    )

    def save_model(self, request, obj, form, change):
        """
        Проверяем уровень вложенности категории перед сохранением
        """
        if obj.parent:
            max_indent = 2
            lvl = obj.parent.level + 1

            if lvl < max_indent:
                super(CategoryAdmin, self).save_model(request, obj, form, change)
            else:
                # Меняем уровень сообщения на ERROR
                messages.set_level(
                    request, messages.ERROR
                )
                # Чтобы избежать вывода одновременно 2 сообщений: успешного и в случае ошибки
                messages.add_message(
                    request,
                    level=messages.ERROR,
                    message=f"Превышена максимальная вложенность категорий в {max_indent} уровня! "
                    f"Текущая вложенность: {lvl + 1}",
                )
        else:
            super(CategoryAdmin, self).save_model(request, obj, form, change)


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    """
    Админ-панель для комментариев к товарам
    """

    list_display = ("product", "author", "short_review", "date", "deleted")
    # list_display_links = ("product_title",)
    list_filter = ("deleted",)
    search_fields = ("product", "short_review")
    list_editable = ("deleted",)

    # Мягкое удаление/восстановление записей
    actions = (
        deleted_records,
        restore_records,
    )

    def short_review(self, obj):
        """
        Возврат короткого отзыва (не более 250 символов)
        """
        if len(obj.text) > 250:
            return f"{obj.text[0:250]}..."
        return obj.text

    short_review.short_description = "Отзыв"

    def product_name(self, obj):
        """
        Возврат короткого названия товара (не более 100 символов)
        """
        if len(obj.product.name) > 50:
            return f"{obj.product.name[0:50]}..."
        return obj.product.name

    product_name.short_description = "Товар"


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    """
    Админ-панель для характеристик товара
    """
    list_display = ['id', 'name', 'value']
    list_display_links = ("name",)


class ChoiceSpecifications(admin.TabularInline):
    """
    Вывод характеристик на странице товара
    """

    model = Specification
    extra = 1


class ChoiceReviews(admin.TabularInline):
    """
    Вывод комментариев на странице товара
    """

    model = Review
    extra = 0


class ChoiceImages(admin.TabularInline):
    """
    Вывод изображений на странице товара
    """

    model = ImageForProduct
    extra = 0


class ChoiceSales(admin.TabularInline):
    """
    Вывод записей о распродаже товара
    """

    model = SaleItem
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Админ-панель для товаров
    """

    list_display = (
        "id",
        "short_name",
        "category",
        "price",
        "count",
        "date",
        "deleted",
    )
    list_display_links = ("short_name",)
    list_filter = ("category", "tags")
    search_fields = ("title",)
    list_editable = ("deleted",)

    # FIXME Добавлять при помощи миксина
    # Мягкое удаление/восстановление записей
    actions = (
        deleted_records,
        restore_records,
    )

    inlines = (ChoiceSales, ChoiceReviews, ChoiceSpecifications, ChoiceImages)

    fieldsets = (
        (
            "Основное",
            {
                "fields": ("title", "short_description", "description"),
                "description": "Название и описание товара",
            },
        ),
        ("Категория и теги", {"fields": ("category", "tags")}),
        ("Стоимость", {"fields": ("price",)}),
        # ("Изображения", {"fields": ("images",)}),
        (
            "Кол-во товара",
            {
                "fields": ("count",),
                "description": "Оставшееся кол-во товара на складе",
            },
        ),
        (
            "Статус",
            {
                "fields": ("deleted",),
                "description": "Статус товара: активен или удален из БД",
                "classes": ("collapse",),
            },
        ),
    )

    def short_name(self, obj):
        """
        Возврат короткого названия товара (не более 150 символов)
        """
        if len(obj.title) > 150:
            return f"{obj.title[0:150]}..."

        return obj.title

    short_name.short_description = "Название товара"


@admin.register(SaleItem)
class SaleAdmin(admin.ModelAdmin):
    """
    Админ-панель для записей о распродажах товаров
    """
    list_display = (
        "id",
        "product_name",
        "sale_price",
        "discount",
        "date_from",
        "date_to",
        "deleted",
    )
    list_display_links = ("product_name",)
    search_fields = ("product_name",)
    list_editable = ("deleted",)

    # FIXME Добавлять при помощи миксина
    # Мягкое удаление/восстановление записей
    actions = (
        deleted_records,
        restore_records,
    )

    def product_name(self, obj):
        """
        Возврат названия товара
        """
        return obj.product.title[:150]

    product_name.short_description = "Товар"

    def discount(self, obj):
        """
        Вывод скидки
        """
        return obj.discount

    discount.short_description = " Скидка"

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    """
    Админ-панель для корзин с товарами пользователей
    """

    list_display = ("id", "user", "product", "count", "price")


class ProductsInOrder(admin.TabularInline):
    """
    Вывод товаров в текущем заказе
    """

    model = PurchasedProduct
    can_delete = False
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        """
        Запрещаем редактировать поля заказа
        """
        if obj:
            return ["order", "product", "count", "price"]

        return self.readonly_fields

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Админ-панель для вывода заказов
    """

    list_display = ("id", "full_name", "delivery", "payment", "city", "data", "status")
    list_display_links = ("id",)
    search_fields = ("id", "user__profile__full_name", "city", "address")
    list_filter = ("delivery", "payment", "status")
    inlines = (ProductsInOrder,)

    def data(self, obj):
        """
        Изменяем формат вывода даты и времени
        """
        return obj.data_created.strftime(f"%d.%m.%Y %H:%M:%S")

    data.short_description = "дата оформления"

    def full_name(self, obj):
        """
        Полное имя покупателя
        """
        return obj.user.profile.full_name

    full_name.short_description = "Покупатель"

    def get_queryset(self, request) -> QuerySet:
        return Order.objects.select_related("user__profile")

    fieldsets = (
        (
            "Данные о заказе",
            {
                "fields": ("payment", "status"),
                "description": "Номер заказа, тип оплаты и статус заказа",
            },
        ),
        (
            "Данные о покупателе и доставке",
            {
                "fields": ("full_name", "city", "address", "delivery"),
                "description": "ФИО покупателя, город, адрес и тип доставки",
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        """
        Запрещаем редактировать поля заказа
        """
        if obj:
            return [
                "id",
                "full_name",
                "data_created",
                "city",
                "address",
                "delivery",
                "payment",
                "status",
            ]
            # Снимаем запрет на изменение статуса оплаты (для тестирования)
            # return ['id', 'full_name', 'data_created', 'city', 'address', 'delivery', 'payment']

        return self.readonly_fields
