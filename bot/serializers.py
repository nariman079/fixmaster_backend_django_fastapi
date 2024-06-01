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


class BotModeratorGetProfileSerializer(serializers.Serializer):
    telegram_id = serializers.CharField()
    login = serializers.CharField()
    code = serializers.CharField()