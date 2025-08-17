from prometheus_client import metrics

APP_BOOKINGS_TOTAL = metrics.Gauge(
    "bookings_total", "Сколько бронирований сейчас в базе данных (состояние)"
)
APP_BOOKINGS_CREATED = metrics.Counter(
    "bookings_created_total", "Общее количество бронирований"
)
APP_BOOKING_DURATION = metrics.Histogram(
    "booking_creation_duration_seconds", "Время создания бронирования"
)
APP_ORDERS_TOTAL_COUNTER = metrics.Counter(
    "app_orders_total", "Total number of orders created (increases monotonically)"
)
# 2. Gauge: количество заказов по статусам (может меняться)
APP_ORDER_STATUS_GAUGE = metrics.Gauge(
    "app_order_status_count", "Number of orders by status", labelnames=["status"]
)
# 3. Histogram: длительность процедуры (если нужно)
APP_ORDER_LENGTH_HISTOGRAM = metrics.Histogram(
    "app_order_length_minutes",
    "Length of order in minutes",
    buckets=(15, 30, 60, 90, 120, 180),  # настрой под свои услуги
)
# 4. Gauge: новых заказов за день (если хочешь "сегодня")
APP_ORDERS_NEW_TODAY = metrics.Gauge(
    "app_orders_new_today", "Number of new orders created today (resets at 00:00)"
)
APP_ORGANIZATION_GAUGE = metrics.Gauge(
    "organization_counter", "Количество салонов", labelnames=["organization_type"]
)
APP_MASTER_TOTAL_GAUGE = metrics.Gauge("app_master_total", "Общее количество мастеров")
APP_CUSTOMER_COUNT = metrics.Counter(
    "app_customer_total", "сколько всего клиентов создано"
)
APP_CUSTOMER_GAUGE = metrics.Gauge("app_customer_gauge", "текущее количество клиентов")
APP_CUSTOMER_TODAY_GAUGE = metrics.Gauge(
    "app_customers_new_today", "текущее количество клиентов"
)
APP_CUSTOMER_NEW_COUNTER = metrics.Counter(
    "app_customers_new_total", "Total number of new customers (first order)"
)

APP_CUSTOMER_RETURNING_COUNTER = metrics.Counter(
    "app_customers_returning_total",
    "Total number of returning customers (repeat orders)",
)
APP_AVG_PROCEDURE_TIME_GAUGE = metrics.Gauge(
    "app_avg_procedure_time", "Средняя длительность процедур"
)
APP_AVG_ORDER_PRICE_GAUGE = metrics.Gauge(
    "app_avg_order_price", "Средняя длительность процедур"
)
APP_REQUEST_DURATION = metrics.Histogram(
    "app_request_duration",
    "Request duration (latency)",
    buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0),  # настрой под себя
    labelnames=["method", "view", "status"],
)
APP_SERVICE_SOLD_COUNTER = metrics.Counter(
    "app_service_sold_total",
    "Total number of times a service was ordered",
    labelnames=["service_id", "service_name", "service_price"],
)

APP_DAU_GAUGE = metrics.Gauge("app_dau_count", "DAU")
APP_MAU_GAUGE = metrics.Gauge("app_mau_count", "MAU")
APP_SERVICE_REVENUE_GAUGE = metrics.Gauge(
    "app_service_revenue", "Service reneuew", labelnames=["title"]
)

HTTP_500_ERRORS_COUNTER = metrics.Counter(
    'http_500_errors_total',
    'Total number of HTTP 500 errors'
)

# Счётчик по путям (опционально)
HTTP_500_ERRORS_BY_PATH = metrics.Counter(
    'http_500_errors_by_path',
    'HTTP 500 errors by path',
    labelnames=['path']
)