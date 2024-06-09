from datetime import datetime

from django.db.models import F
from django.db.transaction import atomic
from config.settings import dict_get, dict_set, cache
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from src.serializers.organization_serializers import OrganizationDetailSerializer
from src.models import Customer, Organization, Master, Moderator, Service, Image
from src.tasks import (send_message_on_moderator_about_organization,
                       send_message_about_verify_master,
                       send_is_verified_organization,
                       send_message_about_verify_customer)


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


def next_session(start_date, start_time):
    start_date_time_str = f"{start_date} {start_time}"
    start_date_time = datetime.strptime(start_date_time_str, "%Y-%m-%d %H:%M:%S")

    current_date_time = datetime.now()

    result_text = "Следующая процедура через\n"

    time_difference = start_date_time - current_date_time

    total_seconds = int(time_difference.total_seconds())
    days, seconds = divmod(total_seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes = seconds // 60

    months = days // 30
    days = days % 30

    if months > 0:
        result_text += f' {months} месяцев,'
    if days > 0:
        result_text += f' {days} дней,'
    if hours > 0:
        result_text += f' {hours} часов,'

    output = f"{result_text} {minutes} минут."

    return output


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
            self.gallery = self.organization.pop('gallery')
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

    def _create_gallery(self):

        if self.gallery:
            for image_url in self.gallery:
                Image.objects.create(
                    organization=self.organization_obj,
                    image_url=image_url
                )

    def _send_notification(self):
        send_message_on_moderator_about_organization.delay(self.organization_obj.pk)

    @atomic()
    def execute(self):
        self._create_organization()
        self._send_notification()
        self._create_gallery()
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
        print(dict_get(self.telegram_id), 'TEST')

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


class BotGetOrganizationDataByTelegramId:
    def __init__(self, organization_data: dict):
        self.telegram_id = organization_data['telegram_id']

    def get_organization(self):
        self.organization = Organization.objects.filter(telegram_id=self.telegram_id).first()

    def execute(self):
        self.get_organization()

        return Response({
            'message': "Данные успешно получены",
            'success': True,
            'data': OrganizationDetailSerializer(instance=self.organization).data
        }, status=200)


class MasterDeleteSrv:
    def __init__(self, master_id: int):
        self.master_id = master_id

    def get_master(self):
        self.master = Master.objects.filter(pk=self.master_id)

    def delete_master(self):
        if self.master:
            cache.delete(str(self.master.first().organization.telegram_id))
            self.master.delete()

    def execute(self):
        self.get_master()
        self.delete_master()
        return Response(status=204)


class MasterCreateSrv:
    def __init__(self, master_data: dict):
        self.master_data = master_data

    def create_master(self):
        try:
            self.master = Master.objects.create(**self.master_data)
        except:
            raise ValidationError(
                {
                    'message': "Не удалось создать мастера",
                    'code': 422,
                    'success': False,
                    'data': []
                }
            )

    def execute(self):
        self.create_master()

        return Response({
            'message': "Мастер успешно создан",
            'success': True,
            'data': self.master.code
        }, status=201)


class MasterEditSrv:
    def __init__(self, master_id: int, master_data: dict):
        self.master_data = master_data
        self.master_id = master_id

    def get_master(self):
        self.master = Master.objects.filter(pk=self.master_id)

    def update_master(self):
        if self.master:
            self.master.update(**self.master_data)

    def execute(self):
        self.get_master()
        self.update_master()
        return Response(
            {
                'message': 'Мастер изменен',
                'success': True,
                'data': []
            }, status=200
        )


class MasterServiceListSrv:
    def __init__(self, *args, **kwargs):
        self.master_id = kwargs.get('master_id')

    def get_master_services(self):
        self.master = Master.objects.filter(pk=self.master_id).first()
        self.master_services = self.master.service_set.values(
            'id',
            'title',
            'short_description',
            'price',
            'min_time',
            'master_id'
        )

    def execute(self):
        self.get_master_services()
        return Response({
            'message': "Запрос прошел успешно",
            'success': True,
            'data': self.master_services
        }, status=200)


class MasterServiceCreateSrv:
    def __init__(self, *args, **kwargs):
        self.master_id = kwargs.get('master_id')
        self.service_data = kwargs.get('service_data')

    def get_master(self):
        self.master = Master.objects.filter(pk=self.master_id).first()
        if not self.master:
            raise ValidationError(
                {
                    'message': 'Нет такого мастера',
                    'success': False,
                    'data': []
                }
            )

    def create_service(self):
        self.master.service_set.create(**self.service_data)

    def execute(self):
        self.get_master()
        self.create_service()
        return Response({
            'message': "Запрос прошел успешно",
            'success': True,
            'data': {}
        }, status=201
        )


class MasterServiceEditSrv:
    def __init__(self, *args, **kwargs):
        self.service_id = kwargs.get('service_id')
        self.service_data = kwargs.get('service_data')

    def get_and_update_service(self):
        self.service = Service.objects.filter(pk=self.service_id)
        self.service.update(**self.service_data)

    def execute(self):
        self.get_and_update_service()
        return Response({
            'message': "Запрос прошел успешно",
            'success': True,
            'data': {}
        }, 200)


class MasterServiceDeleteSrv:
    def __init__(self, *args, **kwargs):
        self.service_id = kwargs.get('service_id')

    def get_and_delete_service(self):
        self.service = Service.objects.filter(pk=self.service_id)
        self.service.delete()

    def execute(self):
        self.get_and_delete_service()
        return Response({
            'message': "Запрос прошел успешно",
            'success': True,
            'data': {}
        }, status=204)


class MasterServiceDetailSrv:
    def __init__(self, *args, **kwargs):
        self.service_id = kwargs.get('service_id')

    def get_master_service_detail(self):
        self.services = Service.objects.filter(pk=self.service_id)
        if not self.services:
            raise ValidationError(
                {
                    'message': 'Такой услуги нет в системе',
                    'success': False,
                    'data': {}
                }
            )
        self.service = self.services.values(
            'id',
            'title',
            'short_description',
            'price',
            'min_time',
            'master_id'
        ).first()

    def execute(self):
        self.get_master_service_detail()
        return Response({
            'message': "Запрос прошел успешно",
            'success': True,
            'data': self.service
        })


class CustomerListSrv:
    def __init__(self, organization_telegram_id: int):
        self.organization_telegram_id = organization_telegram_id

    def get_organization_customers(self):
        self.customers = Customer.objects.filter(
            organizatoin__telegram_id=self.organization_telegram_id
        )

    def execute(self):
        self.get_organization_customers()
        return Response(
            {
                'message': 'Запрос прощел успешно'
            }
        )


class MasterVerifySrv:
    def __init__(self, code: str, telegram_id: str):
        self.code = code
        self.telegram_id = telegram_id

    def get_master_by_code(self):
        self.master = Master.objects.filter(
            code=self.code
        ).first()
        print(self.master)

    def check_master(self):
        if self.master:
            if self.master.is_verified:
                raise ValidationError({
                    'message': 'Такой пользователь уже есть в системе',
                    'data': [],
                    'success': True
                })
            self.master.telegram_id = self.telegram_id
            self.master.is_verified = True
            self.master.save()
        else:
            raise ValidationError({
                'message': 'Такого пользователя нет в системе\nПопробуйте еще раз',
                'data': [],
                'success': True
            })

    def send_notification(self):
        if self.master:
            send_message_about_verify_master.delay(self.master.id)

    def execute(self):
        self.get_master_by_code()
        self.check_master()
        self.send_notification()
        return Response(
            {
                'message': 'Вы авторизованы',
                'success': True,
                'data': []
            }, status=200
        )


class MasterCustomers:
    def __init__(
            self,
            serializer_data: dict
    ):
        self.telegram_id = serializer_data.get('telegram_id')

    def get_master(self):
        self.master = Master.objects.filter(telegram_id=self.telegram_id).first()
        print(self.master)
        if not self.master:
            raise ValidationError(
                {
                    'message': "Такого мастера нет в системе",
                    'success': False,
                    'data': []
                }
            )

    def get_master_clients(self):
        self.customers = self.master.customer_set.all().values(
            'id',
            'username'
        )
        print(self.customers)

    def execute(self):
        self.get_master()
        self.get_master_clients()
        return Response(
            {
                'message': 'Список клиентов получен',
                'success': True,
                'data': self.customers
            }
        )


class MasterNextSessionSrv:
    def __init__(
            self,
            serializer_data: dict
    ):
        self.telegram_id = serializer_data.get('telegram_id')

    def get_master(self):
        self.master = Master.objects.filter(telegram_id=self.telegram_id).first()

        if not self.master:
            raise ValidationError(
                {
                    'message': "Такого мастера нет в системе",
                    'success': False,
                    'data': []
                }
            )

    def get_master_bookings(self):
        self.booking = (
            self.master.booking_set.filter(
                booking_date__gte=datetime.now().date(),
                booking_time__gte=datetime.now().time())
            .order_by('booking_date')
            .order_by('booking_time')
        ).annotate(
            start_time=F('booking_time'),
            start_date=F('booking_date')
        ).values('start_time', 'start_date').first()

    def complete_time(self):
        self.next_time = next_session(**self.booking)

    def execute(self):
        self.get_master()
        self.get_master_bookings()
        if not self.booking:
            return Response(
                {
                    'message': 'У вас нет броней',
                    'success': True,
                    'data': []
                }
            )

        self.complete_time()

        return Response(
            {
                'message': self.next_time,
                'success': True,
                'data': []
            }
        )


class CustomerNextSessionSrv:
    def __init__(
            self,
            serializer_data: dict
    ):
        self.telegram_id = serializer_data.get('telegram_id')

    def get_client(self):
        self.customer = Customer.objects.filter(telegram_id=self.telegram_id).first()

        if not self.customer:
            raise ValidationError(
                {
                    'message': "Такого клиента нет в системе",
                    'success': False,
                    'data': []
                }
            )

    def get_customer_bookings(self):
        self.booking = (
            self.customer.master.booking_set.filter(
                booking_date__gte=datetime.now().date(),
                booking_time__gte=datetime.now().time())
            .order_by('booking_date')
            .order_by('booking_time')
        ).annotate(
            start_time=F('booking_time'),
            start_date=F('booking_date')
        ).values('start_time', 'start_date').first()

    def complete_time(self):
        self.next_time = next_session(**self.booking)

    def execute(self):
        self.get_client()
        self.get_customer_bookings()
        if not self.booking:
            return Response(
                {
                    'message': 'У вас нет броней',
                    'success': True,
                    'data': []
                }
            )

        self.complete_time()

        return Response(
            {
                'message': self.next_time,
                'success': True,
                'data': []
            }
        )


class CustomerVerifySrv:
    def __init__(self, serializer_data: dict):
        self.code = serializer_data.get("code")
        self.telegram_id = serializer_data.get("telegram_id")

    def get_customer_by_code(self):
        self.customer = Customer.objects.filter(
            code=self.code
        ).first()

    def verify_customer(self):
        if self.customer:
            if self.customer.is_verified:
                raise ValidationError({
                    'message': 'Такой пользователь уже есть в системе',
                    'data': [],
                    'success': True
                })
            self.customer.telegram_id = self.telegram_id
            self.customer.is_verified = True
            self.customer.save()
        else:
            raise ValidationError({
                'message': 'Такого пользователя нет в системе\nПопробуйте еще раз',
                'data': [],
                'success': True
            })

    def send_notification(self):
        if self.customer:
            send_message_about_verify_customer.delay(self.customer.master.telegram_id, self.telegram_id)

    def execute(self):
        self.get_customer_by_code()
        self.verify_customer()
        self.send_notification()
        return Response(
            {
                'message': 'Вы авторизованы',
                'success': True,
                'data': []
            }, status=200
        )