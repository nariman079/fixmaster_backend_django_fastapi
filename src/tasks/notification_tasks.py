from celery import shared_task

from bot.config import master_bot
from src.models import Master


@shared_task
def send_message_telegram_on_master(
        master_id: int,
        client_phone_number: str,
        booking_date: str,
        booking_time: str,
):
    """
    Отправка сообщения Мастеру о бронировании
    """
    master = Master.objects.get(id=master_id)

    text = (f"У вас новая бронь\n"
            f"Клиент: {client_phone_number}\n"
            f"Дата: {booking_date}\n"
            f"Время: {booking_time}")

    master_bot.send_message(
        chat_id=master.telegram_id,
        text=text
    )
