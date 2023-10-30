import datetime

from django.core.exceptions import ValidationError


def validate_sale_price(obj):
    """
    Валидатор, проверяющий, что цена товара со скидкой не больше цены без скидки,
    а также, что скидка на товар составляет от 10 до 90 %.
    """
    price = obj.product.price
    sale_price = obj.sale_price

    if sale_price >= price:
        raise ValidationError(
            f'Цена товара со скидкой ({sale_price}) не может быть больше или равно цене товара без скидки ({price}).'
        )

    discount = 100 - ((sale_price / price) * 100)

    if not 5 <= discount <= 90:
        raise ValidationError(
            f'Скидка на товар должна быть в пределах 5-90%. Текущая скидка - {int(discount)}%'
        )


def validate_date_to(obj):
    """
    Валидатор проверяет, что дата окончания распродажи товара позже даты начала распродажи,
    а также что дата не является текущей или ранее текущей.
    """
    # current_date = datetime.datetime.now()
    date_from = obj.date_from.replace(tzinfo=None)
    date_to = obj.date_to.replace(tzinfo=None)

    if date_to <= date_from:
        raise ValidationError('Дата окончания распродажи не может быть раньше или равна даты начала распродажи')

    # elif date_to <= current_date:
    #     raise ValidationError('Дата окончания распродажи не может быть раньше или равна текущей дате')
