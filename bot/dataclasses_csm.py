from dataclasses import  dataclass


@dataclass
class OrganizationData:
    """
    Огранизации
    """

    telegram_id: str
    title: str
    main_image: bytes
    address: str
    contact_phone: str
    time_begin: str
    time_end: str
    work_schedule: str
    organization_type_id: int
