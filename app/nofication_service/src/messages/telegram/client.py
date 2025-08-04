from typing import ClassVar
from dataclasses import dataclass



@dataclass(frozen=True)
class ClientMessages:
    """Сообщения для клиентов"""
    
    BOOKING_CONFIRMED: ClassVar[str] = (
        "✅ Ваша запись подтверждена!\n"
        "Мастер: {master_name}\n"
        "Дата: {date}\n"
        "Время: {time}\n"
        "Адрес: {address}"
    )
    
    PAYMENT_SUCCESS: ClassVar[str] = (
        "Оплата прошла успешно! 💰\n"
        "Сумма: {amount} ₽\n"
        "Ссылка на чек: {receipt_url}"
    )

    REMINDER_24H: ClassVar[str] = (
        "⏰ Напоминание: через 24 часа у вас запись\n"
        "Мастер: {master_name}\n"
        "Время: {time}"
    )





# Пример использования
