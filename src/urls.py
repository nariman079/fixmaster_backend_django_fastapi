from django.urls import path
from src.views.order_views import OrderCreateView, FreeBookingView
from src.views.organization_views import OrganizationListView, OrganizationDetailView

urlpatterns = [
   path('order/create/', OrderCreateView.as_view()),
   path('booking/get-free-times/', FreeBookingView.as_view()),
   path('organizations/', OrganizationListView.as_view()),
   path('organizations/<int:organization_id>/', OrganizationDetailView.as_view())
]
