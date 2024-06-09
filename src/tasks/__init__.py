from src.tasks.notification_tasks import (send_message_telegram_on_master,
                                          send_message_on_moderator_about_organization,
                                          send_is_verified_organization,
                                          send_message_about_verify_master,
                                          send_message_about_verify_customer)
from src.tasks.order_tasks import change_status_order

__all__ = (
    'send_message_telegram_on_master',
    'change_status_order',
    'send_message_on_moderator_about_organization',
    'send_message_about_verify_master',
    'send_message_about_verify_customer',
    'send_is_verified_organization'
)