import datetime

from rest_framework import serializers

from src.models import Organization, Master, Service
from src.serializers.image_serializers import ImageSerializer
from src.services.image_services import get_full_url


class MasterServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("id", "title")


class OrganizationServiceSerializer(serializers.ModelSerializer):
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
    services = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Master
        fields = ("id", "image", "name", "surname", "services")

    def get_services(self, master: Master):
        return MasterServiceSerializer(
            instance=master.service_set.all(), many=True
        ).data[:3]

    def get_image(self, obj):
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
        now_time = datetime.datetime.now().time()
        return organization.time_begin < now_time < organization.time_end

    def get_main_image(self, organization: Organization):
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
        gallery_serializer = ImageSerializer(
            instance=organization.image_set.all(), many=True, context=self.context
        )
        return gallery_serializer.data

    def get_masters(self, organization: Organization):
        master_serializer = MasterSerializer(
            instance=organization.master_set.all(), many=True, context=self.context
        )
        return master_serializer.data

    def get_services(self, organization: Organization):
        services = OrganizationServiceSerializer(
            instance=Service.objects.filter(master__organization=organization),
            many=True,
        )
        return services.data
