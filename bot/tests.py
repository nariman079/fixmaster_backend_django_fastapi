from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase

from bot.services import BotOrganizationCreate
from src.models import OrganizationType


class BotTestCase(APITestCase):
    def setUp(self):
        self.organization_type = OrganizationType.objects.create(title="title")

    def test_get_my_profile_api_key_error(self):
        headers = {"Api-Key": "test"}
        params = {
            "phone_number": "",
            "telegram_id": "",
            "user_keyword": "",
            "username": "",
        }
        response = self.client.get(
            reverse("get-profile"), headers=headers, params=params
        )
        self.assertEqual(response.status_code, 400)

    def test_get_profile_api_key_ok(self):
        headers = {"Api-Key": "X20HHA"}
        params = {
            "phone_number": "",
            "telegram_id": "",
            "user_keyword": "",
            "username": "",
        }
        response = self.client.get(
            reverse("get-profile"), headers=headers, params=params
        )
        self.assertEqual(response.status_code, 422)

    def test_create_organization_from_bot(self):
        headers = {"Api-Key": "test"}
        data = {
            "telegram_id": "11111",
            "title": "title",
            "main_image": SimpleUploadedFile(
                name="test.png",
                content=open("image.png", "rb").read(),
                content_type="image/png",
            ),
            "address": "address",
            "contact_phone": "contact_phone",
            "time_begin": "10:00",
            "time_end": "19:00",
            "work_schedule": "work_schedule",
            "organization_type_id": self.organization_type.id,
        }
        response = BotOrganizationCreate(organization_data=data).execute()

        self.assertEqual(response.status_code, 201)
