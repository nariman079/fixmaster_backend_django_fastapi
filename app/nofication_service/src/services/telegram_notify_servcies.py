from nofication_service.src.models import (
    Booking,
    Client,
    Organization,
    Moderator,
    Master,
)
from nofication_service.src.messages.telegram import (
    MasterMessages,
    ModeratorMessages,
    OrganizationMessages,
    ClientMessages,
)

from nofication_service.src.interfaces import BotRepository


class NewBookingNotifyService:
    def __init__(self, bot: BotRepository, booking: Booking):
        self.bot_repo = bot
        self.master_id = booking.master.telegram_id
        self.client_name = booking.client.name
        self.client_phone = booking.client.phone_number
        self.services = booking.services
        self.time = booking.time
        self.date = booking.date

    def _parse_services(self) -> None:
        self.services = "\n".join([service.title for service in self.services])

    def execute(self) -> None:
        self._parse_services()

        message_text = MasterMessages.NEW_BOOKING.format(
            client_name=self.client_name,
            client_phone=self.client_phone,
            date=self.date,
            time=self.time,
            service=self.services,
        )

        self.bot_repo.send(chat_id=self.master_id, text=message_text)
