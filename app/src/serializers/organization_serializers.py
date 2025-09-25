# pylint: disable=too-few-public-methods,missing-class-docstring,no-member,abstract-method
"""
Сериализаторы для приложения Организации
"""

import datetime

from rest_framework import serializers

from src.models import Organization, Master, Service
from src.serializers.image_serializers import ImageSerializer
from src.services.image_services import get_full_url


class MasterServiceSerializer(serializers.ModelSerializer):
    """Сериализатор услуг мастера"""

    class Meta:
        model = Service
        fields = ("id", "title")


class OrganizationServiceSerializer(serializers.ModelSerializer):
    """Сериализатор организаций"""

    class Meta:
        model = Service
        fields = (
            "id",
            "title",
            "short_description",
            "price",
            "min_time",
        )


class MasterSerializer(serializers.ModelSerializer):
    """Сериализатор мастеров"""

    services = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Master
        fields = ("id", "image", "name", "surname", "services")

    def get_services(self, master: Master):
        """Получение услуг мастера"""
        return MasterServiceSerializer(
            instance=master.service_set.all(), many=True
        ).data[:3]

    def get_image(self, obj):
        """Получение изображения"""
        return get_full_url(self, obj, "image")


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for the organization's list page"""

    main_image = serializers.SerializerMethodField()
    time_begin = serializers.TimeField(format="%H:%M")
    time_end = serializers.TimeField(format="%H:%M")
    is_open = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = (
            "id",
            "title",
            "main_image",
            "time_begin",
            "time_end",
            "address",
            "work_schedule",
            "is_open",
        )

    def get_is_open(self, organization: Organization):
        """Получение поля IsOpen"""
        now_time = datetime.datetime.now().time()
        return organization.time_begin < now_time < organization.time_end

    def get_main_image(self, organization: Organization):
        """Получение главного изображение организаций"""
        return get_full_url(self, organization, "main_image")


class OrganizationDetailSerializer(OrganizationSerializer):
    """Serializer for the detailed organization page"""

    gallery = serializers.SerializerMethodField()
    masters = serializers.SerializerMethodField()
    services = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = "__all__"

    def get_gallery(self, organization: Organization):
        """Получение фотографий организации"""
        gallery_serializer = ImageSerializer(
            instance=organization.image_set.all(), many=True, context=self.context
        )
        return gallery_serializer.data

    def get_masters(self, organization: Organization):
        """Получение мастеров организации"""
        master_serializer = MasterSerializer(
            instance=organization.master_set.all(), many=True, context=self.context
        )
        return master_serializer.data

    def get_services(self, organization: Organization):
        """Получение услуг организации"""
        services = OrganizationServiceSerializer(
            instance=Service.objects.filter(master__organization=organization),
            many=True,
        )
        return services.data
