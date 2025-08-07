from celery import shared_task
from django.utils import timezone
from django.db.models import Avg

from config.settings import dict_set
from config import csm_metrics

from src.models import Order, GaugeValue, Master
from src.models import GaugeValue, Order, OrganizationType, Organization, Master, Customer
from src.enums.statuses import CHOICES_STATUS


@shared_task
def update_metrics():
    try:
        order_status_count = {}
        for status, _ in CHOICES_STATUS:
            count = Order.objects.filter(status=status).count()
            order_status_count[status] = count

        dict_set('order_status_count', order_status_count)

        organization_type_count = {}
        for organization_type in OrganizationType.objects.all():
            organizations_count = Organization.objects.filter(organization_type=organization_type).count()
            organization_type_count[organization_type.title] =  organizations_count
        
        dict_set('organization_type_count', organization_type_count)
        
        master_count = Master.objects.count()
        today = timezone.now().date()
        customers_new_today_count = Customer.objects.filter(create_at__date=today).count()
        dict_set('counts', {
            'masters': master_count,
            'customers_today': customers_new_today_count
        })
        
        avg_procedure_time = Order.objects.filter(status='done').aggregate(
            avg_procedure_time=Avg('length_time')
        )['avg_procedure_time']
        avg_order_price = Order.objects.filter(
            status='done'
        ).aggregate(
            avg_order_price=Avg("services__price")
        )['avg_order_price']

        dict_set('avg_data', 
        {
            'procedure_time': avg_procedure_time,
            'order_price': avg_order_price
        }
        
        )
    


        
        
    except Exception as e:
        print(f"❌ Не удалось обновить метрику из БД: {e}")
