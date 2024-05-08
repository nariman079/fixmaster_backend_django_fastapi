from datetime import date

from django.db.models.signals import post_save
from rest_framework import generics

from .models import organization_models

from .serializers import serializers
from .signals.signals import create_booking


class OrderCreateAPIView(generics.CreateAPIView):
    queryset = organization_models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        post_save.connect(create_booking, sender=organization_models.Order, dispatch_uid='create_booking')
        return response


class BookingListApiView(generics.ListAPIView):
    queryset = organization_models.Booking.objects.all()
    serializer_class = serializers.BookingSerializer
    lookup_field = 'master'

    def get_queryset(self):
        master_id = self.kwargs['master']
        today = date.today()
        queryset = super().get_queryset()
        queryset = queryset.filter(master=master_id, booking_date=today)
        return queryset
