from typing import ClassVar
from dataclasses import dataclass

@dataclass(frozen=True)
class OrganizationMessages:
    """Сообщения для организаций"""
    
    VERIFICATION_SUCCESS: ClassVar[str] = (
        "🎉 Ваша организация верифицирована!\n"
        "Теперь вы можете:\n"
        "- Добавлять мастеров\n"
        "- Настраивать услуги\n"
        "- Принимать записи"
    )
    
    NEW_MASTER_JOINED: ClassVar[str] = (
        "👋 Новый мастер в команде!\n"
        "Имя: {master_name}\n"
        "Специализация: {specialization}\n"
        "Код для мастера: {access_code}"
    )
    
