from datetime import time
from datetime import datetime, timedelta
from typing import Any, OrderedDict

from django.db import transaction
from django.db.models.query import QuerySet
from django.db.models import Sum

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from src.tasks import send_message_telegram_on_master, change_status_order
from src.models import Order, Booking, Service, Customer


def complete_totals(serivices: QuerySet['Service']) -> Any:
    """ Complete full time length """
    return serivices.aggregate(
        total_time_length=Sum('min_time'),
        total_price=Sum('price'))


def time_to_int(time: time) -> int:
    """ Time to int """
    return int(time.strftime('%H:%M').split(':')[0])


def is_free_time(time: str, available_times: list[str]):
    hour = time.split(':')[0]
    all_times = map(lambda x: x.split(':')[0], available_times)

    return {
        'time': time,
        'is_free': hour not in all_times
    }


class OrderCreateSrc:
    """
    Create order service
    """

    def __init__(
            self,
            serializer_validate_data: OrderedDict,
            serialzier_data: OrderedDict
    ):
        self.serializer_data = serialzier_data
        self.master_id = serializer_validate_data.get('master_id')
        self.service_ids = serializer_validate_data.get('service_ids')  # type: ignore
        self.begin_date = serializer_validate_data.get('begin_date')
        self.begin_time = serializer_validate_data.get('begin_time')
        self.customer_phone = serializer_validate_data.get('customer_phone')
        self.customer_name = serializer_validate_data.get('customer_name')
        self.customer_notice = serializer_validate_data.get('customer_notice')

    def _validate_booking_master(self) -> None:
        bookings = Booking.objects.filter(
            master_id=self.master_id,
            booking_date=self.begin_date,
            booking_time=self.begin_time
        )
        if bookings:
            raise ValidationError({
                'success': False,
                'message': 'Время уже забронировано другим пользователем',
                'data': {}
            }, code=400)

    def _get_all_services(self) -> None:
        self.serivces = Service.objects.filter(id__in=self.service_ids)
        if not self.serivces:
            raise ValidationError({
                'message': "Services not found",
                'success': False,
                'data': []
            },
                code=422)

    def _complete_full_time_length(self) -> None:
        """ Complete full time length """
        sum_total_data = complete_totals(serivices=self.serivces)
        self.summed_num = sum_total_data['total_time_length']
        self.summed_time = (datetime.combine(self.begin_date, self.begin_time
                                             ) + timedelta(minutes=sum_total_data['total_time_length'])).time()
        self.total_price = sum_total_data['total_price']

        if not self.summed_time or not self.total_price:
            raise ValidationError(code=422)

    def _create_order(self) -> None:
        """ Create order """
        self.order = Order.objects.create(
            begin_date=self.begin_date,
            begin_time=self.begin_time,
            length_time=self.summed_num,
            customer_phone=self.customer_phone,
            customer_name=self.customer_name,
            customer_notice=self.customer_notice
        )
        for i in self.service_ids:  # type: ignore
            self.order.services.add(i)
        self.order.save()

    def _create_booking(self):
        """ Create booking """
        self.booking = Booking.objects.create(
            booking_date=self.order.begin_date,
            booking_time=self.begin_time,
            booking_end_time=self.summed_time,
            master_id=self.master_id
        )

    def _create_customer(self):
        """ Создание клиента в БД"""
        self.customer = Customer.objects.create(
            phone=self.customer_phone,
            user_keyword=self.customer_name
        )

    def _send_notification_on_master(self):
        """ Отправка сообщания мастеру о брони """
        send_message_telegram_on_master.delay(
            self.master_id, self.customer_phone,
            self.begin_date, self.begin_time
        )

    def _send_order_status_check(self):
        """ Смена статуса брони или заказа """
        change_in_progress_time = (datetime.combine(
            self.begin_date, self.begin_time
        ) - datetime.now()).total_seconds()

        change_done_time = (datetime.combine(
            self.begin_date, self.begin_time
        ) + datetime.timedelta(minutes=30) - datetime.now()
                            ).total_seconds()

        change_status_order.apply_async(
            (self.order.pk, 'in-progress'),
            countdown=change_in_progress_time
        )
        change_status_order.apply_async(
            (self.order.pk, 'done'),
            countdown=(change_done_time)
        )

    @transaction.atomic
    def execute(self):
        """ Run commands """
        self._validate_booking_master()
        self._get_all_services()
        self._complete_full_time_length()

        self._create_order()
        self._create_booking()
        self._send_notification_on_master()
        self._send_order_status_check()

        return Response({
            'message': "Заказ успешно создан",
            'success': True,
            'data': self.serializer_data
        }, status=201)


class FreeBookingSrc:
    """
    Free booking dates and times
    """

    times = [f'{i}:00' for i in range(4, 20)]

    def __init__(self, serializer_validated_data: OrderedDict) -> None:
        self.date = serializer_validated_data.get('date')
        self.master_id = serializer_validated_data.get('master_id')

    def _get_master_bookings(self) -> None:
        """
        Get all booking on current date
        """
        self.bookings = Booking.objects.filter(
            master_id=self.master_id,
            booking_date=self.date
        )

    def _get_master_available_time(self):
        """
        Get master available time
        """
        self.available_times = set()
        for booking in self.bookings:
            start = time_to_int(booking.booking_time)
            end = time_to_int(booking.booking_end_time)
            for i in range(start, end + 1):
                self.available_times.add(f'{i}:00')

    def _generate_all_times(self):
        """
        Generate all times for response
        """
        self.free_times = [is_free_time(i, sorted(self.available_times)) for i in self.times]

    @transaction.atomic
    def execute(self):
        """
        Run commands
        """
        self._get_master_bookings()
        self._get_master_available_time()
        self._generate_all_times()
        return Response({
            'message': "All times has been received",
            'success': True,
            'data': self.free_times
        }, status=200)
