from datetime import time
from typing import OrderedDict
from pprint import pprint

from rest_framework.response import Response

from src.models import Booking


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


class FreeBookingSrc:
    """
    Free booking dates and times
    """

    times = [f'{i}:00' for i in range(4, 20)]

    def __init__(self, serializer_data: OrderedDict) -> None:
        self.date = serializer_data.get('date')
        self.master_id = serializer_data.get('master_id')

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
        pprint(self.free_times)

    def execute(self):
        self._get_master_bookings()
        self._get_master_available_time()
        self._generate_all_times()
        return Response({
            'message': "All times has been received",
            'success': True,
            'data': self.free_times
        }, status=200)