from datetime import timedelta
from collections import defaultdict

from celery import shared_task
from django.utils import timezone
from django.db.models import Avg, Count, F, Q

from config.settings import dict_set

from src.models import Order, Master
from src.models import (
    OrganizationType,
    Organization,
    Customer,
    Service,
)
from src.enums.statuses import CHOICES_STATUS


@shared_task
def update_metrics():
    try:
        order_status_count = {}
        for status, _ in CHOICES_STATUS:
            count = Order.objects.filter(status=status).count()
            order_status_count[status] = count

        dict_set("order_status_count", order_status_count)

        organization_type_count = {}
        for organization_type in OrganizationType.objects.all():
            organizations_count = Organization.objects.filter(
                organization_type=organization_type
            ).count()
            organization_type_count[organization_type.title] = organizations_count

        dict_set("organization_type_count", organization_type_count)

        master_count = Master.objects.count()
        today = timezone.now().date()
        month_ago = today - timedelta(days=30)

        customers_new_today_count = Customer.objects.filter(
            create_at__date=today
        ).count()
        dict_set(
            "counts",
            {"masters": master_count, "customers_today": customers_new_today_count},
        )

        avg_procedure_time = Order.objects.filter(status="done").aggregate(
            avg_procedure_time=Avg("length_time")
        )["avg_procedure_time"]
        avg_order_price = Order.objects.filter(status="done").aggregate(
            avg_order_price=Avg("services__price")
        )["avg_order_price"]

        dict_set(
            "avg_data",
            {"procedure_time": avg_procedure_time, "order_price": avg_order_price},
        )

        dau = (
            Order.objects.filter(begin_date=today)
            .values("customer_id")
            .distinct()
            .count()
        )

        mau = (
            Order.objects.filter(begin_date__gte=month_ago)
            .values("customer_id")
            .distinct()
            .count()
        )

        dict_set("point_data", {"dau": dau, "mau": mau})
        completed_orders = Order.objects.filter(status="done").prefetch_related('services')
        income_by_service = defaultdict(int)
        for order in completed_orders:
            for service in order.services.all():
                income_by_service[service.title] += service.price
     
        income_by_services = {title: income for title, income in income_by_service.items() if income > 0}

        dict_set("income_by_services", income_by_services)

    except Exception as e:
        print(f"❌ Не удалось обновить метрику из БД: {e}")
