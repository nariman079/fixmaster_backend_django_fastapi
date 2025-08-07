from typing import ClassVar
from dataclasses import dataclass


@dataclass(frozen=True)
class MasterMessages:
    """Сообщения для мастеров"""

    NEW_BOOKING: ClassVar[str] = (
        "🆕 Новая запись!\n"
        "Клиент: {client_name}\n"
        "Телефон: {client_phone}\n"
        "Дата: {date}\n"
        "Время: {time}\n"
        "Услуга: {service}"
    )

    SCHEDULE_CHANGE: ClassVar[str] = (
        "⚠️ Изменение расписания!\n"
        "Новое время работы: {schedule} \n"
        "Обновите свои доступные слоты"
    )
