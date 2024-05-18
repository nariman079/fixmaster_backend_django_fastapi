from typing import List
import dataclasses
from pprint import pprint


def create_datas():
   from datetime import datetime, time, date
   from typing import OrderedDict
   from django.core.files.uploadedfile import SimpleUploadedFile
   from rest_framework.test import APITestCase

   from src.models import Master, Service, Organization, OrganizationType
   def generate_image():
    return SimpleUploadedFile(
            name='image.png',
            content=open('image.png', 'rb').read(),
            content_type='image/png'
        )

   organization_type = OrganizationType.objects.create(
      title="orgnization_type"
   )
   organization = Organization.objects.create(
      title='title',
      main_image=generate_image(),
      is_verified=True,
      address="address",
      contact_phone="9999",
      time_begin=datetime.now().time(), 
      time_end=datetime.now().time(),
      work_schedule="5/2",
      organization_type_id=organization_type.id,
   )
   master = Master.objects.create(
      name="test",
      surname="test",
      image=generate_image(),
      organization=organization
   )
   service = Service.objects.create(
      master=master,
      title="title",
      price=10,
      min_time=30
   )



@dataclasses.dataclass
class Booking:
   end_time: str
   start_time: str


def get_master_available_time(bookigns: list[Booking]):
   available_times = set()
   for booking in bookigns:
      start = int(booking.start_time.split(':')[0])
      end = int(booking.end_time.split(':')[0])
      for i in range(start, end+1):
         available_times.add(f'{i}:00')
   return sorted(available_times)

available_times = get_master_available_time(
   [
      Booking(start_time='12:20', end_time='15:10')
   ]
)
times = [f'{i}:00' for i in range(4,20)]


def is_free_time(time:str):
   hour = time.split(':')[0]
   all_times = map(lambda x: x.split(':')[0], available_times)

   return   {
      'time':time,
      'is_free': hour not in all_times
   }

free_times = [is_free_time(i) for i in times]


