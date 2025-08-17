from celery import shared_task

from src.models import Order
from src.utils.logger import RequestLogger

@shared_task
def change_status_order(
    order_id: int, 
    new_status: str,
    request_id: str
):
    """Изменение статуса заказа или брони"""
    logger = RequestLogger(request_id=request_id)
    order = Order.objects.get(id=order_id)
    order.status = new_status
    order.save()
    logger.debug(
        "Изменение статуса процедуры",
        extra={
            'new_status': new_status
        }
    )

    
