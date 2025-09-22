import time
import uuid
from collections import defaultdict, deque
from threading import Lock

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseServerError
from django.db import connection
from django.db import DatabaseError, OperationalError, InterfaceError

from rest_framework.request import Request

import logging

from config import csm_metrics
from src.utils.logger import RequestLogger


class RequestTimingMiddleware:
    """
    Обработчик для подсчета времени выполнения запроса
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time

        view_name = getattr(request.resolver_match, "url_name", "unknown")
        method = request.method
        status = response.status_code

        csm_metrics.APP_REQUEST_DURATION.labels(
            method=method, view=view_name, status=status
        ).observe(duration)

        return response


class RequestIDMiddleware:
    """
    Обработчик для создания RequestID
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Request):
        if request.path == "/metrics":
            return self.get_response(request)

        request_id = request.META.get("HTTP_X_REQUEST_ID") or str(uuid.uuid4())
        logger = RequestLogger(request_id=request_id)

        setattr(request, "request_id", request_id)
        setattr(request, "logger", logger)

        logger.info(
            "Начало HTTP-запроса",
            extra={
                "method": request.method,
                "path": request.path,
            },
        )
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        if duration > 1.0:
            logger.warning(
                "Медленный HTTP-запрос",
                extra={
                    "request_id": getattr(request, "request_id", "unknown"),
                    "path": request.path,
                    "method": request.method,
                    "duration": round(duration, 3),
                    "status_code": response.status_code,
                    "user_id": getattr(request.user, "id", None),
                    "event": "http.slow.request",
                },
            )

        logger.info(
            "Завершение HTTP-запроса", extra={"status_code": response.status_code}
        )

        return response


logger = logging.getLogger("src.errors")


class ErrorHandlingMiddleware(MiddlewareMixin):
    """
    Обработчик 500-х ошибок
    """

    def process_exception(self, request, exception):
        logger.error(
            "500 Internal Server Error",
            extra={
                "request_id": getattr(request, "request_id", "unknown"),
                "path": request.path,
                "method": request.method,
                "user_id": getattr(request.user, "id", None),
                "exception": str(exception),
                "exception_type": type(exception).__name__,
                "event": "http.500.error",
            },
        )

        csm_metrics.HTTP_500_ERRORS_COUNTER.inc()
        csm_metrics.HTTP_500_ERRORS_BY_PATH.labels(path=request.path).inc()

        return HttpResponseServerError("Internal Server Error")


class UncaughtExceptionMiddleware:
    """
    Обработчик необработанных исключений
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, (DatabaseError, OperationalError, InterfaceError)):
            logger.error(
                "Ошибка БД в запросе",
                extra={
                    "trace_id": getattr(request, "trace_id", "unknown"),
                    "path": request.path,
                    "method": request.method,
                    "error_type": type(exception).__name__,
                    "error_message": str(exception),
                    "event": "db.connection.error"
                    if "connection" in str(exception).lower()
                    else "db.timeout.error"
                    if "timeout" in str(exception).lower()
                    else "db.error",
                },
            )
            return
        logger.critical(
            "Необработанное исключение в Django",
            extra={
                "request_id": getattr(request, "request_id", "unknown"),
                "path": request.path,
                "method": request.method,
                "user_id": getattr(request.user, "id", None),
                "exception_type": type(exception).__name__,
                "exception_message": str(exception),
                "event": "django.uncaught.exception",
            },
        )


class SlowQueryMiddleware:
    """
    Обработчик медленных запросов
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        connection.queries_log.clear()

        start_time = time.time()
        response = self.get_response(request)
        _ = time.time() - start_time

        for query in connection.queries:
            query_time = float(query["time"])
            if query_time > 1.0:  # больше 1 секунды
                logger.warning(
                    "Медленный SQL-запрос",
                    extra={
                        "request_id": getattr(request, "request_id", "unknown"),
                        "sql": query["sql"][:1000],  # ограничиваем длину
                        "duration": query_time,
                        "path": request.path,
                        "method": request.method,
                        "event": "db.slow.query",
                    },
                )

        return response


ip_requests = defaultdict(lambda: defaultdict(deque))
ip_lock = Lock()


class SecurityIPRateLimitMiddleware:
    def __init__(self, get_response, threshold=100) -> None:
        self.get_response = get_response
        self.threshold = threshold

    def __call__(self, request):
        if request.path == "/metrics":
            return self.get_response(request)

        ip = self.get_client_ip(request)
        logger = getattr(request, "logger")

        endpoint = f"{request.method} {request.path}"
        now = time.time()

        with ip_lock:
            while ip_requests[ip][endpoint] and ip_requests[ip][endpoint][0] < now - 60:
                ip_requests[ip][endpoint].popleft()

            ip_requests[ip][endpoint].append(now)

            if len(ip_requests[ip][endpoint]) > self.threshold:
                logger.warning(
                    "Подозрительная активность: частые запросы к эндпоинту",
                    extra={
                        "ip": ip,
                        "endpoint": endpoint,
                        "requests_count": len(ip_requests[ip][endpoint]),
                        "user_agent": request.META.get("HTTP_USER_AGENT", "")[:200],
                        "event": "security.endpoint.rate_limit.exceeded",
                    },
                )

        response = self.get_response(request)

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
