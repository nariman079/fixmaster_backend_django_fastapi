from django.db.transaction import atomic
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from src.models import Customer, Organization, Master, Moderator
from src.tasks import (send_message_telegram_on_master,
                       send_message_on_moderator_about_organization,
                       send_is_verified_organization)


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
            self.organization_obj: Organization = Organization.objects.create(**self.organization)

        except Exception as error:

            raise ValidationError(
                {
                    'message': "Неизвестная ошибка\nОбратитесь к администратору @nariman079i\n",
                    'status': False,
                    'data': error.args
                }, code=422
            )

    def _send_notification(self):
        send_message_on_moderator_about_organization.delay(self.organization_obj.pk)

    @atomic()
    def execute(self):
        self._create_organization()
        self._send_notification()
        return Response(
            {
                'message': "Вы успешно авторизовались\nВы будете получать уведомления о брони",
                'success': True,
                'data': self.organization
            }, status=201
        )


class BotMasterGetProfile:
    """ Создание организации """

    def __init__(
            self,
            master_data: dict
    ):
        try:
            self.telegram_id = master_data['telegram_id']
            self.code = master_data['code']
            self.name = master_data['name']

        except Exception as error:
            raise ValidationError(
                {
                    'message': "Неизвествная ошибка\nОбратитесь к администратору @nariman079i\n",
                    'success': False,
                    'data': {}
                }, code=422
            )

    def _get_master(self):
        try:
            master = Master.objects.filter(name=self.name).first()
            if not (master and master.code == self.code):
                raise ValidationError()
            master.telegram_id = self.telegram_id

        except Exception as error:

            raise ValidationError(
                {
                    'message': "Неизвестная ошибка\nОбратитесь к администратору @nariman079i\n",
                    'status': False,
                    'data': error.args
                }, code=422
            )

    def execute(self):
        self._get_master()
        # self._send_notification()
        return Response(
            {
                'message': "Вы успешно авторизовались\nВы будете получать уведомления о брони",
                'success': True,
                'data': self.organization
            }, status=201
        )


class BotModeratorGetProfile:
    """ Создание организации """

    def __init__(
            self,
            moderator_data: dict
    ):
        try:
            self.telegram_id = moderator_data['telegram_id']
            self.code = moderator_data['code']
            self.login = moderator_data['login']

        except Exception as error:
            raise ValidationError(
                {
                    'message': "Неизвествная ошибка\nОбратитесь к администратору @nariman079i\n",
                    'success': False,
                    'code': 422,
                    'data': {}
                }
            )

    def _get_moderator(self):
        moderator = Moderator.objects.filter(login=self.login).first()
        if moderator.telegram_id == self.telegram_id:
            raise ValidationError(
                {
                    'message': "Вы уже зарегистрированы в системе",
                    'success': True,
                    'code': 440,
                    'data': []
                }
            )
        if not moderator:
            raise ValidationError(
                {
                    'message': 'Модератор с таком логином не зарегистрирован',
                    'success': False,
                    'code': 404,
                    'data': []
                }
            )
        if not (moderator and str(moderator.code).strip() == str(self.code).strip()):
            raise ValidationError(
                {
                    'message': "Вы неправильно ввели код\nПопробуйте еще раз",
                    'status': False,
                    'code': 400,
                    'data': []
                }
            )

        moderator.telegram_id = self.telegram_id
        moderator.save()

    def execute(self):
        self._get_moderator()

        return Response(
            {
                'message': "Вы успешно авторизовались\nВы будете получать заявки на верификацию организаций",
                'success': True,
                'code': 201,
                'data': []
            }, status=201
        )


class BotVerifyOrganization:
    def __init__(self, verify_organization_data: dict):
        self.organization_id = verify_organization_data['organization_id']
        self.is_verify = verify_organization_data['is_verify']

    def get_organization(self):
        self.organization = Organization.objects.filter(pk=self.organization_id).first()

    def check_verify(self):
        self.organization.is_verified = self.is_verify
        self.organization.save()

    def send_notification(self):
        send_is_verified_organization.delay(self.organization.id, self.is_verify)

    def execute(self):
        self.get_organization()
        self.check_verify()
        self.send_notification()
        return Response({
            'message': ""
        })


class BotGetOrganizationByTelegramId:
    def __init__(self, organization_data: dict):
        self.telegram_id = organization_data['telegram_id']

    def get_organization(self):
        self.organization = Organization.objects.filter(telegram_id=self.telegram_id).first()

    def check_organization(self):
        if self.organization:
            raise ValidationError(
                {
                    'message': "Вы уже есть в системе",
                    'success': False,
                    'data': [],
                    'code': 400
                }
            )

    def execute(self):
        self.get_organization()
        self.check_organization()
        return Response({
            'message': "Такого аккаунта нет в системе",
            'success': True,
            'data': []
        }, status=200)
