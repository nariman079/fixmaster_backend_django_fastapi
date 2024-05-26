from django.conf import settings
from telebot import TeleBot


client_bot = TeleBot(
    settings.FIXMASTER_CLIENT_BOT_TOKEN
)
master_bot = TeleBot(
    settings.FIXMASTER_MASTER_BOT_TOKEN
)
organization_bot = TeleBot(
    ''
)