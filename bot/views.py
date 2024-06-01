from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from bot.permissions import api_key_permission
from bot.services import GetProfile, BotOrganizationCreate, BotModeratorGetProfile, BotVerifyOrganization, \
    BotGetOrganizationByTelegramId
from bot.serializers import BotOrganizationCreateSerializer, BotModeratorGetProfileSerializer


class BotMyProfileView(APIView):
    @extend_schema(
        description='Search organization',
        methods=["GET", ],
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


class BotOrganizationCreateView(APIView):
    @extend_schema(
        description='Search organization',
        methods=["POST", ],
        parameters=[
            OpenApiParameter(
                name='Api-Key',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.HEADER,
                description='Api key for telegram'
            ),
            OpenApiParameter(
                name='title',
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name='telegram_id',
                type=OpenApiTypes.STR
            ),
            OpenApiParameter(
                name='main_image',
                type=OpenApiTypes.BINARY
            ),
            OpenApiParameter(
                name='time_begin',
                type=OpenApiTypes.TIME
            ),
            OpenApiParameter(
                name='time_end',
                type=OpenApiTypes.TIME
            ),
            OpenApiParameter(
                name='address',
                type=OpenApiTypes.STR
            ),
            OpenApiParameter(
                name='work_schedule',
                type=OpenApiTypes.STR
            ),
            OpenApiParameter(
                name='organization_type',
                type=OpenApiTypes.STR
            ),
            OpenApiParameter(
                name='contact_phone',
                type=OpenApiTypes.STR
            )
        ])
    def post(self, request, *args, **kwargs) -> Response:
        """ Создание организации """
        if api_key_permission(request=self.request):
            organization_data = BotOrganizationCreateSerializer(data=self.request.data)
            organization_data.is_valid(raise_exception=True)
            create_organization = BotOrganizationCreate(
                organization_data=organization_data.validated_data
            )
            return create_organization.execute()

        return Response(
            {
                'message': "Неизвествная ошибка\nОбратитесь к администратору @nariman079i",
                'success': False,
                'data': [
                    'Неверный API-KEY'
                ]
            }, status=422
        )


class BotModeratorGetProfileView(APIView):
    def post(self, request, *args, **kwargs) -> Response:
        """ Создание организации """
        if api_key_permission(request=self.request):
            moderator_data = BotModeratorGetProfileSerializer(data=self.request.data)
            moderator_data.is_valid(raise_exception=True)
            moderator_get_profile = BotModeratorGetProfile(
                moderator_data=moderator_data.validated_data
            )
            return moderator_get_profile.execute()

        return Response(
            {
                'message': "Неизвествная ошибка\nОбратитесь к администратору @nariman079i",
                'success': False,
                'data': [
                    'Неверный API-KEY'
                ]
            }, status=422
        )


class BotVerifyOrganizationView(APIView):
    def post(self, request, *args, **kwargs):
        if api_key_permission(request=self.request):
            verify_organization_data = dict(
                organization_id=kwargs.get('organization_id'),
                is_verify=self.request.data.get('is_verify')
            )
            verify_organization = BotVerifyOrganization(
                verify_organization_data=verify_organization_data
            )
            return verify_organization.execute()

        return Response(
            {
                'message': "Неизвествная ошибка\nОбратитесь к администратору @nariman079i",
                'success': False,
                'data': [
                    'Неверный API-KEY'
                ]
            }, status=422
        )


class BotGetOrganizationByTelegramIdView(APIView):
    def get(self, *args, **kwargs):
        if api_key_permission(request=self.request):
            organization_data = dict(
                telegram_id=kwargs.get('telegram_id')
            )

            get_organization_by_telegram_id = BotGetOrganizationByTelegramId(
                organization_data=organization_data
            )
            return get_organization_by_telegram_id.execute()

        return Response(
            {
                'message': "Неизвествная ошибка\nОбратитесь к администратору @nariman079i",
                'success': False,
                'data': [
                    'Неверный API-KEY'
                ]
            }, status=422
        )