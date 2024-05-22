from rest_framework.response import Response
from rest_framework.views import APIView

from bot.permissions import api_key_permission
from bot.services import GetProfile


class BotMyProfileView(APIView):


    def get(self, *args, **kwargs) -> Response:
        api_key_permission(request=self.request)
        user_data = self.request.data
        if (user_data.phone_number and
                user_data.username and
                user_data.telegram_id and
                user_data.user_keyword):
            get_profile = GetProfile(
                **user_data
            )
            return get_profile.execute()
        return Response(
            {
                'message': "Неизвествная ошибка\nОбратитесь к администратору @nariman079i"
            }
        )
