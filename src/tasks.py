import os

from celery import shared_task
from telebot import TeleBot
from django.utils import timezone

from src.models import Order

telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
bot = TeleBot(telegram_bot_token)


@shared_task
def send_message_on_telegram(chat_id, message):
    """ Async sending message on telegram chat """
    bot.send_message(chat_id=chat_id, text=message)


@shared_task(bind=True, default_retry_delay=60, max_retries=None)
def auto_checking_order(self, order_id: int):
    """ Checking order on end time """
    now_date, now_time = timezone.now().date(), timezone.now().time()
    order: Order = Order.objects.get(id=order_id)

    if order.begin_date > now_date:
        end_time = (order.begin_time.min - now_time.min).total_seconds()
        if end_time <= 60:
            # Send message, 1 hour before the start
            send_message_on_telegram(chat_id=order.customer.telegram_id, message=f'Message {end_time}')
            self.retry(countdown=30*60)
        elif end_time <= 30:
            # Send message, half an hour before the start
            send_message_on_telegram(chat_id=order.customer.telegram_id, message=f"Message {end_time}")
            self.retry(countdown=15*60)
        elif end_time <= 15:
            # Send message, 15 min before the start
            send_message_on_telegram(chat_id=order.customer.telegram_id, message=f"Message {end_time}")
            self.retry(countdown=3*60)
        elif end_time <= 3:
            send_message_on_telegram(chat_id=order.customer.telegram_id, message=f"Message {end_time}")



