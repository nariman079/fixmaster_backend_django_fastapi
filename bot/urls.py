from django.urls import path
from bot.views import (BotMyProfileView,
                       BotOrganizationCreateView,
                       BotModeratorGetProfileView,
                       BotVerifyOrganizationView,
                       BotGetOrganizationByTelegramIdView)


urlpatterns = [
    path('get-my-profile/', BotMyProfileView.as_view(), name='get-profile'),
    path('organization/create/', BotOrganizationCreateView.as_view(), name='bot-create-organization'),
    path('organization/verify/<int:organization_id>/', BotVerifyOrganizationView.as_view(), name='bot-organization-verify'),
    path('organization/get-by-telegram_id/<str:telegram_id>',BotGetOrganizationByTelegramIdView.as_view(), name='bot-organization-get-by-telegram_id' ),
    path('moderator/', BotModeratorGetProfileView.as_view(), name="get-moderator-profile"),
]