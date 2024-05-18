from django.urls import path
from src.views.order_views import OrderCreateView

urlpatterns = [
   path('order/create/', OrderCreateView.as_view())
]
