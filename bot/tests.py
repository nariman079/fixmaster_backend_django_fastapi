from django.urls import reverse
from rest_framework.test import APITestCase


class BotTestCase(APITestCase):

    def test_get_my_profile_api_key_error(self):
        headers = {
            "Api-Key": "test"
        }
        params = {
            'phone_number': '',
            'telegram_id': '',
            'user_keyword': '',
            'username': ''
        }
        response = self.client.get(
            reverse('get-profile'),
            headers=headers,
            params=params
        )
        print(response.data)
        self.assertEqual(response.status_code, 401)

    def test_get_profile_api_key_ok(self):
        headers = {
            "Api-Key": "X20HHA"
        }
        params = {
            'phone_number': '',
            'telegram_id': '',
            'user_keyword': '',
            'username': ''
        }
        response = self.client.get(
            reverse('get-profile'),
            headers=headers,
            params=params
        )
        self.assertEqual(response.status_code, 200 )
