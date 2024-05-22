from django.urls import path
from bot.views import BotMyProfileView

urlpatterns = [
    path('get-my-profile/', BotMyProfileView.as_view(), name='get-profile')
]