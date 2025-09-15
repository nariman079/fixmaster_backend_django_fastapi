from django.http import HttpResponse
from prometheus_client import generate_latest

from config import csm_metrics
from config.settings import dict_get


def metrics_view(request):
    try:
        order_status_count = dict_get("order_status_count")
        organization_type_count = dict_get("organization_type_count")

        for status, count in order_status_count.items():
            csm_metrics.APP_ORDER_STATUS_GAUGE.labels(status=status).set(count)

        for organization_type, count in organization_type_count.items():
            csm_metrics.APP_ORGANIZATION_GAUGE.labels(
                organization_type=organization_type
            ).set(count)

        for title, total_income in dict_get("income_by_services").items():
            csm_metrics.APP_SERVICE_REVENUE_GAUGE.labels(title=title).set(total_income)

        counts = dict_get("counts")
        master_count = counts.get("masters")
        customers_today_count = counts.get("customers_today")

        avg_times = dict_get("avg_data")
        point_data = dict_get("point_data")

        procedure_time = avg_times.get("procedure_time")
        order_price = avg_times.get("order_price")

        dau = point_data.get("dau")
        mau = point_data.get("mau")

        if master_count:
            csm_metrics.APP_MASTER_TOTAL_GAUGE.set(master_count)
        if customers_today_count:
            csm_metrics.APP_CUSTOMER_TODAY_GAUGE.set(customers_today_count)
        if procedure_time:
            csm_metrics.APP_AVG_PROCEDURE_TIME_GAUGE.set(procedure_time)
        if order_price:
            csm_metrics.APP_AVG_ORDER_PRICE_GAUGE.set(order_price)
        if dau:
            csm_metrics.APP_DAU_GAUGE.set(dau)
        if mau:
            csm_metrics.APP_MAU_GAUGE.set(mau)

    except Exception as e:
        print(f"❌ Не удалось обновить метрику из БД: {e}")

    return HttpResponse(generate_latest(), content_type="text/plain")
