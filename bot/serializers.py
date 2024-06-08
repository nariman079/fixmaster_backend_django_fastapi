from rest_framework import serializers


class BotOrganizationCreateSerializer(serializers.Serializer):
    telegram_id = serializers.CharField()
    title = serializers.CharField()
    main_image_url = serializers.CharField()
    address = serializers.CharField()
    contact_phone = serializers.CharField()
    time_begin = serializers.CharField()
    time_end = serializers.CharField()
    work_schedule = serializers.CharField()
    organization_type_id = serializers.IntegerField()
    gallery = serializers.ListField(child=serializers.CharField())

class BotModeratorGetProfileSerializer(serializers.Serializer):
    telegram_id = serializers.CharField()
    login = serializers.CharField()
    code = serializers.CharField()


class MasterCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    surname = serializers.CharField()
    image_url = serializers.CharField()
    organization_id = serializers.IntegerField()


class MasterEditSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    surname = serializers.CharField(required=False)
    image_url = serializers.CharField(required=False)
    organization_id = serializers.IntegerField()


class MasterServiceCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    short_description = serializers.CharField()
    price = serializers.CharField()
    min_time = serializers.CharField()


class MasterServiceEditSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    short_description = serializers.CharField(required=False)
    price = serializers.IntegerField(required=False)
    min_time = serializers.CharField(required=False)


class MasterVerifySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=200)
    telegram_id = serializers.CharField(max_length=100)
