import logging
import time
from typing import Dict

from celery import shared_task

from src.api_shop.models.order import Order


logger = logging.getLogger(__name__)


@shared_task()
def payment(order_id: int, data: Dict) -> bool:
    """
    Оплата заказа
    """
    order = Order.objects.filter(id=order_id).first()

    if order:
        number = data["number"]

        logger.info(
            f"Оплата заказа: №{order_id}, карта №{number}, сумма к оплате - {order.total_cost}"
        )

        order.status = 4  # Смена статуса заказа на "Подтверждение оплаты"
        order.save()

        # Имитация ожидания оплаты заказа
        time.sleep(10)

        if int(number) % 2 == 0 and int(number) % 10 != 0:
            order.status = 5  # Смена статуса заказа на "Оплачен"
            order.save()
            logger.info(f"Заказ #{order_id} успешно оплачен")

            return True

        else:
            order.status = 3  # Смена статуса заказа на "Не оплачен"
            order.save()

            logger.error(f"Заказ #{order_id} не оплачен")
            return False

    else:
        logger.error(f"Заказ №{order_id} не найден!")
        return False
