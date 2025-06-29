from celery import shared_task

from src.models import Order


@shared_task
def change_status_order(order_id: int, new_status: str):
    """Изменение статуса заказа или брони"""
    order = Order.objects.get(id=order_id)
    order.status = new_status
    order.save()
