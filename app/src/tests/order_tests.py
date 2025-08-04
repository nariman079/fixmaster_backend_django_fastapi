from datetime import datetime, time
from collections import OrderedDict
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APITestCase

from src.services.order_services import OrderCreateSrv, FreeBookingSrv
from src.models import Master, Service, Organization, OrganizationType


def generate_image():
    return SimpleUploadedFile(
        name="image.png",
        content=open("image.png", "rb").read(),
        content_type="image/png",
    )


class OrderTestCase(APITestCase):
    """
    Order test case
    """

    def setUp(self):
        self.organization_type = OrganizationType.objects.create(
            title="orgnization_type"
        )
        self.organization = Organization.objects.create(
            title="title",
            main_image=generate_image(),
            is_verified=True,
            address="address",
            contact_phone="9999",
            time_begin=datetime.now().time(),
            time_end=datetime.now().time(),
            work_schedule="5/2",
            organization_type_id=self.organization_type.id,
        )
        self.master = Master.objects.create(
            name="test",
            surname="test",
            image=generate_image(),
            organization=self.organization,
        )
        self.service = Service.objects.create(
            master=self.master, title="title", price=10, min_time=30
        )
        self.booking_test_date = datetime(day=10, year=2023, month=12)

    def test_create_order(self):
        data = OrderedDict(
            master_id=self.master.id,
            service_ids=[
                1,
            ],
            begin_date=datetime(day=10, year=2023, month=12),
            begin_time=time(hour=10, minute=30),
            customer_phone="89",
            customer_name="name",
            customer_notice="notice",
        )
        order_create_srv = OrderCreateSrv(
            serialzier_data=data, serializer_validate_data=data
        )
        response = order_create_srv.execute()

        self.master.refresh_from_db()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.master.booking_set.all().count(), 1)

    def test_getting_bookings(self):
        data = OrderedDict(master_id=self.master.id, date=self.booking_test_date)
        booking_times = FreeBookingSrv(data)
        response = booking_times.execute()
        self.assertEqual(response.status_code, 200)

    def test_getting_bookings_ok(self):
        service = self.service = Service.objects.create(
            master=self.master, title="title", price=10, min_time=90
        )
        data = OrderedDict(
            master_id=self.master.id,
            service_ids=[
                service.pk,
            ],
            begin_date=self.booking_test_date,
            begin_time=time(hour=10, minute=30),
            customer_phone="89",
            customer_name="name",
            customer_notice="notice",
        )
        order_create_srv = OrderCreateSrv(
            serialzier_data=data, serializer_validate_data=data
        )
        order_create_srv.execute()

        booking_data = OrderedDict(
            master_id=self.master.id, date=datetime(day=11, year=2023, month=12)
        )
        booking_times = FreeBookingSrv(booking_data)
        response = booking_times.execute()
        self.assertEqual(response.status_code, 200)

        # todo Дописать тесты
