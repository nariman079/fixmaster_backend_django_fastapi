from typing import ClassVar
from dataclasses import dataclass


@dataclass(frozen=True)
class ModeratorMessages:
    """Сообщения для модераторов"""

    NEW_VERIFICATION_REQUEST: ClassVar[str] = (
        "🔔 Новая заявка на верификацию\n"
        "Организация: {org_name}\n"
        "Телефон: {phone}\n"
        "Просмотреть: {admin_link}"
    )

    REPORT_READY: ClassVar[str] = (
        "📊 Отчет за неделю готов\n"
        "Новых организаций: {new_orgs}\n"
        "Жалоб: {complaints}\n"
        "Проблемных броней: {issues}"
    )
