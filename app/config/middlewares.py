import time
import uuid

from rest_framework.request import Request

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
