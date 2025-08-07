import pytest

import datetime
from nofication_service.src.interfaces import BotRepository
from nofication_service.src.services.telegram_notify_servcies import (
    NewBookingNotifyService,
)
from nofication_service.src.models import Booking, Client, Master, Service


class TestBot(BotRepository):
    def send(self, chat_id, text, reply_markup=None):
        return text


@pytest.mark.asyncio
async def test_new_booking_notify_service():
    bot = TestBot()

    booking = Booking(
        client=Client(1, "nariman", "89232"),
        master=Master(2, "name", "se", "23d"),
        services=[Service("test")],
        address="Test",
        date=datetime.datetime(year=2025, day=21, month=1),
        time=datetime.datetime(year=2025, day=21, month=1),
    )
    new_booking = NewBookingNotifyService(bot, booking)
    new_booking.execute()
