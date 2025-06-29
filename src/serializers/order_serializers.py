"""
Order serializers
"""

from rest_framework import serializers


class OrderSerializer(serializers.Serializer):
    """Order create serializer"""

    master_id = serializers.IntegerField()
    service_ids = serializers.ListField(child=serializers.IntegerField())
    begin_date = serializers.DateField()
    begin_time = serializers.TimeField()
    customer_phone = serializers.CharField(max_length=30)
    customer_name = serializers.CharField(
        max_length=60,
    )
    customer_notice = serializers.CharField(
        max_length=120, allow_null=True, required=False, allow_blank=True
    )


class BookingSerializer(serializers.Serializer):
    date = serializers.DateField()
    master_id = serializers.IntegerField()
