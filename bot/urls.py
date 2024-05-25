from django.urls import path
from bot.views import BotMyProfileView, BotOrganizationCreateView

urlpatterns = [
    path('get-my-profile/', BotMyProfileView.as_view(), name='get-profile'),
    path('organization/create/', BotOrganizationCreateView.as_view(), name='bot-create-organization')
]