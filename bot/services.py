import dataclasses

from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from bot.dataclasses_csm import OrganizationData
from src.models import Customer, Organization


def check_organization_exist(contact_phone) -> Response:
    """ Проверка существования организации в БД """
    organization = Organization.objects.filter(contact_phone=contact_phone).first()
    if organization:
        raise ValidationError(
            {
                'message': "Такая организация уже есть в системе",
                'success': False,
                'data': []
            }, code=400
        )
    return Response(
        {
            'message': 'Такой организации нет в системе',
            'success': True,
            'data': []
        },
        status=200
    )


class GetProfile:
    def __init__(
            self,
            data: dict
    ):
        try:
            self.phone_number = data['phone_number']
            self.username = data['username']
            self.telegram_id = data['telegram_id']
            self.user_keyword = data['user_keyword']
        except Exception as error:
            raise ValidationError(
                {
                    'message': "Неизвествная ошибка\nОбратитесь к администратору @nariman079i",
                    'success': False,
                    'data': '\n'.join(error.args)
                }, code=422
            )

    def _get_customer_from_db(self) -> None:
        """
        Получение клиента из базы данных
        """
        self.customer = Customer.objects.filter(phone=self.phone_number).first()
        if not self.customer:
            raise ValidationError({
                "message": "Такого клиента нет в системе"
            })

    def _check_user_keyword(self):
        """ Проверка ключегово слова """
        if self.customer.user_keyword != self.user_keyword:
            raise ValidationError(
                {
                    'message': "Вы неправильно указали слово пароля",
                    'success': False,
                    'data': []
                }, code=400
            )

    def _fill_telegram_user_data(self) -> None:
        """
        Заполнение данных
        """
        self.customer.username = self.username
        self.customer.telegram_id = self.telegram_id
        self.customer.save()

    def execute(self):
        self._get_customer_from_db()
        self._check_user_keyword()
        self._fill_telegram_user_data()

        return Response(
            {
                'message': "Вы успешно авторизовались\nВы будете получать уведомления о брони",
                'success': True,
            }
        )


class BotOrganizationCreate:
    """ Создание организации """
    def __init__(
            self,
            organization_data: dict
    ):
        try:
            self.organization = organization_data
        except Exception as error:
            raise ValidationError(
                {
                    'message': "Неизвествная ошибка\nОбратитесь к администратору @nariman079i\n",
                    'success': False,
                    'data': {}
                }, code=422
            )

    def _create_organization(self):
        try:
            Organization.objects.create(**self.organization)

        except Exception as error:

            raise ValidationError(
                {
                    'message': "Неизвестная ошибка\nОбратитесь к администратору @nariman079i\n" ,
                    'status': False,
                    'data': error.args
                }, code=422
            )

    def execute(self):
        self._create_organization()
        return Response(
            {
                'message': "Вы успешно авторизовались\nВы будете получать уведомления о брони",
                'success': True,
                'data': self.organization
            },status=201
        )
