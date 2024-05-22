from django.urls import reverse
from rest_framework.test import APITestCase


class BotTestCase(APITestCase):

    def test_get_my_profile_api_key_error(self):
        headers = {
            "Api-Key":"test"
        }
        response = self.client.get(
            reverse('get-profile'),
            headers=headers
        )

