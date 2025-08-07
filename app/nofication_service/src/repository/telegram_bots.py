from aiogram import types as aiotypes
from telebot import types as teletypes


from telebot import TeleBot
from aiogram import Bot

from nofication_service.src.interfaces import BotRepository


class TeleBotRepository(BotRepository):
    def __init__(self, token: str):
        self.token = token
        self.bot = TeleBot(self.token)

    async def send(
        self,
        chat_id: int,
        text: str,
        reply_murkup: teletypes.ReplyKeyboardMarkup
        | teletypes.InlineKeyboardButton
        | None = None,
    ) -> None:
        """Отравка сообщения к tguser через telebot"""
        self.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_murkup)


class AiogramBotRepository(BotRepository):
    def __init__(self, token: str):
        self.token = token
        self.bot = Bot(token=self.token)

    async def send(
        self,
        chat_id: int,
        text: str,
        reply_markup: aiotypes.ReplyKeyboardMarkup
        | aiotypes.InlineKeyboardMarkup
        | None = None,
    ) -> None:
        """Отравка сообщения к tguser через aiogram"""
        await self.bot.send_message(
            chat_id=chat_id, text=text, reply_markup=reply_markup
        )
