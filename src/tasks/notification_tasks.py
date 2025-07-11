from celery import shared_task
from telebot import types

from bot.config import master_bot, moderator_bot, organization_bot
from src.models import Master, Organization, Moderator, Customer


def callback_verify_true_organization(organization_id: int) -> str:
    return f"organization_verify_true_{organization_id}"


def callback_verify_false_organization(organization_id: int) -> str:
    return f"organization_verify_false_{organization_id}"


def callback_verify_organization(organization_id: int, is_verify: bool) -> str:
    return f"organization_verify_{'true' if is_verify else 'false'}_{organization_id}"


def get_moderator_for_send_message() -> Moderator:
    return Moderator.objects.first()


@shared_task
def send_message_telegram_on_master(
    master_id: int,
    client_phone_number: str,
    booking_date: str,
    booking_time: str,
):
    """
    Отправка сообщения Мастеру о бронировании
    """
    master = Master.objects.get(id=master_id)

    text = (
        f"У вас новая бронь\n"
        f"Клиент: {client_phone_number}\n"
        f"Дата: {booking_date}\n"
        f"Время: {booking_time}"
    )

    master_bot.send_message(chat_id=master.telegram_id, text=text)


@shared_task
def send_message_about_verify_master(
    master_id: int,
):
    """
    Отправка сообщения Мастеру о бронировании
    """
    master = Master.objects.get(id=master_id)
    text = f"✅ Мастер {master.name} {master.surname} зарегистрировался в системе \n"
    organization_bot.send_message(chat_id=master.organization.telegram_id, text=text)


@shared_task
def send_message_about_verify_customer(master_id: int, customer_id: int):
    """
    Отправка сообщения Мастеру о бронировании
    """
    customer = Customer.objects.get(telegram_id=customer_id)
    text = (
        f"✅ Клиент {customer.username} {customer.name} зарегистрировался в системе \n"
    )
    master_bot.send_message(chat_id=master_id, text=text)


@shared_task
def send_message_on_moderator_about_organization(organization_id: int):
    """Отправка сообщения модератору о регистрации новой организации"""
    organization = Organization.objects.get(pk=organization_id)
    moderator = get_moderator_for_send_message()

    message = f"""Новая заявка на верификацию!🟩🟩🟩
Название: {organization.title}
Адрес: {organization.address}
Номер телефона: {organization.contact_phone}
Тип огранизации: {organization.organization_type.title}
Начало рабочего дня: {organization.time_begin}
Конец рабочего дня: {organization.time_end}\n
Ссылка на галерею: https://booking.fix-mst.ru/admin/src/image/?organization__id__exact={organization.pk}"""

    moderator_inline_markup = types.InlineKeyboardMarkup()
    verify_true_button = types.InlineKeyboardButton(
        "✅ Верифицировать",
        callback_data=callback_verify_organization(organization_id, True),
    )
    verify_false_button = types.InlineKeyboardButton(
        "❌ Не верифицировать",
        callback_data=callback_verify_organization(organization_id, False),
    )
    moderator_inline_markup.add(verify_true_button)
    moderator_inline_markup.add(verify_false_button)
    moderator_bot.send_message(
        chat_id=moderator.telegram_id,
        text=message,
        reply_markup=moderator_inline_markup,
    )


@shared_task()
def send_is_verified_organization(
    organization_id: int,
    is_verify: bool,
):
    """Отправка сообщения о регистрации новой организации"""
    organization = Organization.objects.get(pk=organization_id)
    if is_verify:
        message = """Хорошая новость! ❇️❇️❇️
Ваша организация была верифицировна.
Теперь вы можете добавлять мастеров и услуг.
        """
        organization_menu_markup = types.ReplyKeyboardMarkup()

        master_list = types.KeyboardButton("📃 Список мастеров")
        client_list = types.KeyboardButton("👥 Список клиентов")
        add_master = types.KeyboardButton("➕ Добавить мастера")

        organization_menu_markup.add(master_list)
        organization_menu_markup.add(client_list)
        organization_menu_markup.add(add_master)

        organization_bot.send_message(
            chat_id=organization.telegram_id,
            text=message,
            reply_markup=organization_menu_markup,
        )
    else:
        message = (
            "Ваша организация не прошла верификацию!‼️\n"
            "Заполните данные еще раз - /start"
        )
        organization_bot.send_message(
            chat_id=organization.telegram_id,
            text=message,
        )
