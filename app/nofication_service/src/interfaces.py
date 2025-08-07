from abc import abstractmethod, ABC


class BotRepository(ABC):
    @abstractmethod
    async def send(self, chat_id: int, text: str, reply_markup=None) -> None:
        pass
