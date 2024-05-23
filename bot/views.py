from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from bot.permissions import api_key_permission
from bot.services import GetProfile


class BotMyProfileView(APIView):
    @extend_schema(
        description='Search organization',
        methods=["GET",],
        parameters=[
            OpenApiParameter(
                name='Api-Key',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.HEADER,
                description='Api key for telegram'
            ),
            OpenApiParameter(
                name='phone_number',
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name='telegram_id',
                type=OpenApiTypes.STR
            ),
            OpenApiParameter(
                name='username',
                type=OpenApiTypes.STR
            ),
            OpenApiParameter(
                name='user_keyword',
                type=OpenApiTypes.STR
            )
        ])
    def get(self, *args, **kwargs) -> Response:
        """ Получение профиля клиента """
        if api_key_permission(request=self.request):
            user_params = self.request.query_params

            get_profile = GetProfile(
                data=user_params
            )
            return get_profile.execute()

        return Response(
            {
                'message': "Неизвествная ошибка\nОбратитесь к администратору @nariman079i",
                'success': False,
                'data': []
            }, status=422
        )