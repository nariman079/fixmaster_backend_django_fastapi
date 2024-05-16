
from datetime import  datetime, timedelta
from typing import Any, OrderedDict, List


from django.db.models.query import QuerySet
from django.db.models import Sum

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from src.models import Order, Booking, Service

def parse_ids(list_as_str: str) -> List[int]:
    """ Parse ids from ids list """
    ids = map(lambda x: int(x), list_as_str.split(','))
    return list(ids)

def complete_totals(serivices: QuerySet['Service']) -> Any:
    """ Complete full time length """
    return serivices.aggregate(
        total_time_length=Sum('min_time'),
        total_price=Sum('price'))

class OrderCreateSrc:
    """
    Create order service
    """

    def __init__(self, serializer_data: OrderedDict):
        self.master_id = serializer_data.get('master_id')
        self.service_ids = parse_ids(serializer_data.get('service_ids')) # type: ignore
        self.begin_date = serializer_data.get('begin_date')
        self.begin_time = serializer_data.get('begin_time')
        self.customer_phone = serializer_data.get('customer_phone')

        if not self.service_ids:
            raise ValidationError()

    def _validate_booking_master(self) -> None:
        bookings = Booking.objects.filter(
            master_id=self.master_id,
            booking_date=self.begin_date, 
            booking_time=self.begin_time
            )
        if bookings:
            raise ValidationError({
                'success':False,
                'message':'Время уже забронировано другим пользователем',
                'data':{}
            }, code=400)

    def _get_all_services(self) -> None:
        self.serivces = Service.objects.filter(id__in=self.service_ids)
        if not self.serivces:
            raise ValidationError(code=422)
  
    def _complete_full_time_length(self) -> None:
        sum_total_data = complete_totals(serivices=self.serivces)
        self.summed_num = sum_total_data['total_time_length']
        self.summed_time = (datetime.combine(self.begin_date, self.begin_time
        ) + timedelta(minutes=sum_total_data['total_time_length'])).time()
        self.total_price = sum_total_data['total_price']

        if not self.summed_time or not self.total_price:
            raise ValidationError(code=422)
        
    def _create_order(self) -> None:
        
        self.order = Order.objects.create(
            begin_date=self.begin_date,
            begin_time=self.begin_time,
            length_time=self.summed_num,
            customer_phone=self.customer_phone,

        )
        for i in self.service_ids: # type: ignore
            self.order.services.add(i)
        self.order.save()

    def _create_booking(self):
        self.booking = Booking.objects.create(
            booking_date=self.order.begin_date,
            booking_time=self.begin_time,
            booking_end_time=self.summed_time,
            master_id=self.master_id
        )
    
    def execute(self):

        self._validate_booking_master()
        self._get_all_services()
        self._complete_full_time_length()
        self._create_order()
        self._create_booking()

        return Response({
            'message':"Success",
            'success':True,
            'data':{}
        }, status=201)