import time
import uuid

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseServerError

from rest_framework.request import Request

import logging

from config import csm_metrics
from src.utils.logger import RequestLogger


class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time

        # Определяем view (если возможно)
        view_name = getattr(request.resolver_match, "url_name", "unknown")
        method = request.method
        status = response.status_code

        csm_metrics.APP_REQUEST_DURATION.labels(
            method=method, view=view_name, status=status
        ).observe(duration)

        return response


class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Request):
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

        response = self.get_response(request)

        logger.info(
            "Завершение HTTP-запроса", extra={"status_code": response.status_code}
        )

        return response

logger = logging.getLogger('src.errors')

class ErrorHandlingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        
        logger.error(
            "500 Internal Server Error",
            extra={
                'request_id': getattr(request, 'request_id', 'unknown'),
                'path': request.path,
                'method': request.method,
                'user_id': getattr(request.user, 'id', None),
                'exception': str(exception),
                'exception_type': type(exception).__name__,
                'event': 'http.500.error'
            }
        )
        
        csm_metrics.HTTP_500_ERRORS_COUNTER.inc()
        csm_metrics.HTTP_500_ERRORS_BY_PATH.labels(path=request.path).inc()
        
        return HttpResponseServerError("Internal Server Error")


class UncaughtExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        
        if isinstance(exception, (DatabaseError, OperationalError, InterfaceError)):
            logger.error(
                "Ошибка БД в запросе",
                extra={
                    'trace_id': getattr(request, 'trace_id', 'unknown'),
                    'path': request.path,
                    'method': request.method,
                    'error_type': type(exception).__name__,
                    'error_message': str(exception),
                    'event': 'db.connection.error' if 'connection' in str(exception).lower() 
                             else 'db.timeout.error' if 'timeout' in str(exception).lower()
                             else 'db.error'
                }
            )
            return
        logger.critical(
            "Необработанное исключение в Django",
            extra={
                'request_id': getattr(request, 'request_id', 'unknown'),
                'path': request.path,
                'method': request.method,
                'user_id': getattr(request.user, 'id', None),
                'exception_type': type(exception).__name__,
                'exception_message': str(exception),
                'event': 'django.uncaught.exception'
            }
        )