from dataclasses import dataclass

from datetime import datetime


@dataclass
class BaseUser:
    telegram_id: int

@dataclass
class Service:
    title: str

@dataclass 
class Client(BaseUser):
    name: str
    phone_number: str

@dataclass
class Master(BaseUser):
    name: str
    specialization: str
    access_code: str

@dataclass
class Organization(BaseUser):
    name: str
    phone_number: str
    url: str

@dataclass
class Moderator(BaseUser):
    pass

@dataclass
class Booking:
    client: Client
    master: Master
    services: list[Service]
    address: str
    date: datetime.date
    time: datetime.time

