
from datetime import datetime, time, date
from typing import OrderedDict
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from src.services.order_services import OrderCreateSrc
from src.models import Master, Service, Organization, OrganizationType

def generate_image():
    return SimpleUploadedFile(
            name='image.png',
            content=open('image.png', 'rb').read(),
            content_type='image/png'
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
            title='title',
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
            organization=self.organization
        )
        self.service = Service.objects.create(
            master=self.master,
            title="title",
            price=10,
            min_time=30
        )
    def test_create_order(self):
        data = OrderedDict(
            master_id=self.master.id,
            service_ids='1,1',
            begin_date=date(day=10,year=2023, month=12),
            begin_time=time(hour=10, minute=30),
            customer_phone="89"
        )
        order_create_srv = OrderCreateSrc(
            data
        )
        order_create_srv.execute()

        self.master.refresh_from_db()
        self.assertEqual(self.master.booking_set.all().count(), 1)
        