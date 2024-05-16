"""
Order serializers
"""
from rest_framework import serializers


class OrderSerializer(serializers.Serializer):
    """ Order create serializer """
    master_id = serializers.IntegerField()
    service_ids  = serializers.CharField(
        max_length=255
    )
    begin_date = serializers.DateField()
    begin_time = serializers.TimeField()
    customer_phone = serializers.CharField(
        max_length=30
    )

