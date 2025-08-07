# views.py
from django.http import HttpResponse
from prometheus_client import generate_latest
from config import csm_metrics

from src.models import GaugeValue, Order, OrganizationType, Organization, Master
from src.enums.statuses import CHOICES_STATUS
from config.settings import dict_get

def metrics_view(request):
    try:
        order_status_count = dict_get('order_status_count')

        for status, count in order_status_count.items():
            csm_metrics.APP_ORDER_STATUS_GAUGE.labels(status=status).set(count)
        
        organization_type_count = dict_get("organization_type_count")

        for organization_type, count in organization_type_count.items():
            csm_metrics.APP_ORGANIZATION_GAUGE.labels(
                organization_type=organization_type
            ).set(count)
        
        counts = dict_get('counts')
        master_count = counts.get('masters')
        customers_today_count = counts.get("customers_today")

        if master_count:
            csm_metrics.APP_MASTER_TOTAL_GAUGE.set(master_count)
        if customers_today_count:
            csm_metrics.APP_CUSTOMER_TODAY_GAUGE.set(customers_today_count)
        
        avg_times = dict_get('avg_data')
        procedure_time = avg_times.get('procedure_time')
        order_price = avg_times.get('order_price')

        if procedure_time:
            csm_metrics.APP_AVG_PROCEDURE_TIME_GAUGE.set(procedure_time)
        if order_price:
            csm_metrics.APP_AVG_ORDER_PRICE_GAUGE.set(order_price)
            
    except Exception as e:
        print(f"❌ Не удалось обновить метрику из БД: {e}")

    return HttpResponse(generate_latest(), content_type="text/plain")
