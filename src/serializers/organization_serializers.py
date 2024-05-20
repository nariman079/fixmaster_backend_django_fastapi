from rest_framework import serializers

from src.models import Organization, Master, Service
from src.serializers.image_serializers import ImageSerializer
from src.services.image_services import get_full_url


class MasterServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            'id',
            'title'
        )

class OrganizationServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ()

class MasterSerializer(serializers.ModelSerializer):
    services = serializers.SerializerMethodField()

    class Meta:
        model = Master
        fields = (
            'id',
            'image',
            'name',
            'surname',
            'services'
        )

    def get_services(self, master: Master):
        return ServiceSerializer(
            instance=master.service_set.all(),
            many=True).data[:3]


class OrganizationSerializer(serializers.ModelSerializer):
    """ Serializer for the organization's list page """
    main_image = serializers.SerializerMethodField()
    time_begin = serializers.TimeField(format="%H:%M")
    time_end = serializers.TimeField(format="%H:%M")

    class Meta:
        model = Organization
        fields = (
            'id',
            'title',
            'main_image',
            'time_begin',
            'time_end',
            'address',
            'work_schedule'
        )

    def get_main_image(self, organization: Organization):
        return get_full_url(self, organization, 'main_image')


class OrganizationDetailSerializer(OrganizationSerializer):
    """ Serializer for the detailed organization page """

    gallery = serializers.SerializerMethodField()
    masters = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = '__all__'

    def get_gallery(self, organization: Organization):
        gallery_serializer = ImageSerializer(
            instance=organization.image_set.all(),
            many=True,
            context=self.context)
        return gallery_serializer.data

    def get_masters(self, organization: Organization):
        master_serializer = MasterSerializer(
            instance=organization.master_set.all(),
            many=True,
            context=self.context)
        return master_serializer.data
