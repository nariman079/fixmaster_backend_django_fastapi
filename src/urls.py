from django.urls import path
from src.views.order_views import OrderCreateView, FreeBookingView

urlpatterns = [
   path('order/create/', OrderCreateView.as_view()),
   path('booking/get-free-times/', FreeBookingView.as_view())
]
