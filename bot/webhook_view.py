from django.http.request import HttpRequest
from django.http.response import HttpResponse
import telebot


from bot.config import client_bot


def webhook_organization(request: HttpRequest):
    json_string = request.POST
    update = telebot.types.Update.de_json(json_string)
    client_bot.process_new_updates([update])
    return HttpResponse(status=200)
