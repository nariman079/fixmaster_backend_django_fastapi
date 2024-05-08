from datetime import datetime, timedelta

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import organization_models


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = organization_models.Business
        fields = '__all__'


class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = organization_models.Master
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = organization_models.Service
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = organization_models.Order
        fields = '__all__'

    def validate(self, data):
        master, begin_date, begin_time = data.get('master'), data.get('begin_date'), data.get('begin_time')
        business = master.business
        existing_booking = organization_models.Booking.objects.filter(
            master=master,
            booking_date=begin_date,
            booking_time=begin_time
        ).first()

        if existing_booking:
            raise ValidationError({"error": "Бронь уже существует"})
        if begin_time >= (
                datetime.strptime(str(business.time_end), '%H:%M:%S') - timedelta(hours=1)).time():
            raise ValidationError({"order.begin_time": "За час до закрытия заявки не принимаются"})
        if begin_time < business.time_begin:
            raise ValidationError({"order.begin_time": "Салон еще не открыт"})

        return data


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = organization_models.Customer
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = organization_models.Booking
        fields = '__all__'
